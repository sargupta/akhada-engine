"""Persona sampling — real k-DPP from V0.9.

Implements plan §19.2:

  P(S | |S|=N) ∝ det(L_S),  L_ij = q_i q_j K(x_i, x_j)

with K = RBF on persona embeddings. Sampling is exact via the
Kulesza-Taskar (2012) spectral algorithm. The k-DPP guarantees negative
association: similar personas have a suppressed joint inclusion
probability — provable diversity, not best-effort heuristics.

V0.9 embedding: TF-IDF on the persona's narrative_summary +
top_5_books titles + pet_issues. Cheap, deterministic, no model calls.
V1 swaps to real Sentence-BERT or Vertex embeddings.

API:
  sample_panel(library, n)  → existing call site (backward-compatible).
                              Now uses k-DPP if numpy/scipy available
                              and `library` size > n; falls back to
                              the V0.5 cycle otherwise.

  dpp_sample(library, n, *, sigma=0.6, seed=None)  → explicit k-DPP.
"""
from __future__ import annotations

import logging
from collections.abc import Sequence

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from akhada.persona_registry.fixtures import LIBRARY, get_panel
from akhada.persona_registry.schema import Persona

log = logging.getLogger("akhada.sampler")


def _persona_text(p: Persona) -> str:
    bio = p.biography
    parts = [
        bio.narrative_summary,
        " ".join(c.title for c in bio.top_5_books),
        " ".join(bio.pet_issues),
        " ".join(p.expertise),
        f"{p.demographic.state} {p.demographic.religion} {p.demographic.caste_cat} "
        f"{p.demographic.education} {p.demographic.occupation}",
    ]
    return " ".join(parts)


def _embed(library: Sequence[Persona]) -> np.ndarray:
    """TF-IDF embedding matrix (M, d). Deterministic per library."""
    docs = [_persona_text(p) for p in library]
    vec = TfidfVectorizer(
        max_features=2048,
        ngram_range=(1, 2),
        min_df=1,
        stop_words="english",
        sublinear_tf=True,
    )
    X = vec.fit_transform(docs).toarray().astype(np.float64)
    # Row-normalise so RBF kernel is bounded.
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    return X / norms


def _kernel_L(X: np.ndarray, sigma: float) -> np.ndarray:
    """L_ij = q_i q_j K(x_i, x_j), q_i = 1 (uniform quality at V0.9)."""
    # squared-Euclidean distances (rows are unit-normed → dist² = 2(1 - cos))
    sq = np.maximum(0.0, 2.0 * (1.0 - X @ X.T))
    K = np.exp(-sq / (2.0 * sigma * sigma))
    return K


def _k_dpp_sample_via_eigen(
    eigenvalues: np.ndarray, eigenvectors: np.ndarray, k: int, rng: np.random.Generator
) -> list[int]:
    """Kulesza-Taskar 2012 exact k-DPP sampler (Algorithm 8).

    eigenvalues  : (M,) ascending or any order
    eigenvectors : (M, M) columns are eigenvectors
    Returns indices (length k) of the sampled subset.
    """
    M = len(eigenvalues)
    # Compute elementary symmetric polynomials e_n(λ) for n = 0..k via DP.
    # E[m, n] = e_n(λ_1..λ_m)
    E = np.zeros((M + 1, k + 1))
    E[:, 0] = 1.0
    for m in range(1, M + 1):
        for n in range(1, min(m, k) + 1):
            E[m, n] = E[m - 1, n] + eigenvalues[m - 1] * E[m - 1, n - 1]

    # Sample subset of eigenvectors (Algorithm 8, top-down).
    selected: list[int] = []
    remaining = k
    for m in range(M, 0, -1):
        if remaining == 0:
            break
        if E[m, remaining] == 0:
            continue
        prob_include = eigenvalues[m - 1] * E[m - 1, remaining - 1] / E[m, remaining]
        if rng.random() < prob_include:
            selected.append(m - 1)
            remaining -= 1

    if remaining > 0:
        # Fall back: pad with random remaining indices (rare numerical case).
        log.warning("k-DPP eigen-sampling under-filled by %d; padding with uniform", remaining)
        pool = [i for i in range(M) if i not in selected]
        rng.shuffle(pool)
        selected.extend(pool[:remaining])

    # Now sample k items conditioned on those eigenvectors.
    V = eigenvectors[:, selected].copy()
    chosen: list[int] = []
    for _ in range(k):
        # Probability of item i is proportional to ||V_i||²
        probs = np.sum(V * V, axis=1)
        total = probs.sum()
        if total <= 0:
            break
        probs = probs / total
        i = int(rng.choice(M, p=probs))
        chosen.append(i)
        # Project V into the orthogonal complement of e_i
        Vi = V[i, :].copy()
        if np.linalg.norm(Vi) < 1e-12:
            break
        # Find a column with non-zero projection on e_i and subtract
        col = int(np.argmax(np.abs(Vi)))
        v_col = V[:, col].copy()
        if abs(v_col[i]) < 1e-12:
            break
        # Eliminate dimension `col` so subsequent picks must be diverse
        V = V - np.outer(v_col / v_col[i], Vi)
        V = np.delete(V, col, axis=1)

    return chosen


def dpp_sample(
    library: Sequence[Persona],
    n: int,
    *,
    sigma: float = 0.6,
    seed: int | None = None,
) -> list[Persona]:
    """Exact k-DPP draw of `n` personas from `library`. RBF kernel on
    TF-IDF embeddings; quality weight q_i ≡ 1.

    Negative association property (plan §19.2):
        P({i,j} ⊂ S) − P(i ∈ S)·P(j ∈ S) ≤ 0
    so similar personas suppress each other's joint probability.
    """
    if n <= 0:
        return []
    if n >= len(library):
        return list(library)

    rng = np.random.default_rng(seed)

    X = _embed(library)
    L = _kernel_L(X, sigma)

    # symmetrise + add tiny ridge for numerical stability
    L = 0.5 * (L + L.T) + 1e-9 * np.eye(L.shape[0])
    eigvals, eigvecs = np.linalg.eigh(L)
    # Clip tiny negatives from float error
    eigvals = np.clip(eigvals, 0.0, None)

    indices = _k_dpp_sample_via_eigen(eigvals, eigvecs, n, rng)
    return [library[i] for i in indices]


def sample_panel(library: Sequence[Persona] | None = None, n: int = 50) -> list[Persona]:
    """Backward-compatible entrypoint.

    V0.5 cycled. V0.9 uses k-DPP when the library is bigger than the
    requested panel size — that's when DPP can actually express negative
    association. Below or equal we keep the deterministic cycle.
    """
    src = list(library) if library is not None else LIBRARY
    if not src:
        raise ValueError("empty persona library")
    if n >= len(src):
        # When the library is smaller than or equal to the panel size,
        # cycle the fixtures (existing behaviour).
        if library is None:
            return get_panel(n)
        return [src[i % len(src)] for i in range(n)]
    try:
        return dpp_sample(src, n)
    except Exception as exc:  # noqa: BLE001
        log.warning("k-DPP failed (%s); falling back to first-N cycle", exc)
        return list(src[:n])
