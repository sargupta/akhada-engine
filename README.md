# Akhada — Open Debate Engine

> **Stress-test public deliberation, before public deliberation stress-tests you.**
>
> *A SARGVISION Intelligence product.*

Akhada is an open civic-deliberation engine that runs a panel of biographically-grounded AI personas — drawn from real Indian demographic distributions — through a structured debate on any policy topic, then synthesises a sourced article and a Bradley-Terry-quality-weighted conclusive remark. Every debate is persisted with a cryptographic, hash-chained audit trail.

It is built for serious institutional users — multilateral programme offices, policy think tanks, ministries, journalism desks, academic research groups — who currently rely on weeks of multi-state qualitative fieldwork to understand how a policy proposal would land across India.

| | |
|---|---|
| **Version** | V0.10 (May 2026) |
| **License** | AGPL-3.0-or-later (open core) + commercial license for gov-tier features |
| **Tests** | 31 / 31 passing in 0.80 s |
| **Repo** | `~/code/akhada-engine` (private until V3 open-core release) |
| **Stack** | Python 3.11 (FastAPI + Pydantic v2 + google-genai) · TypeScript (Next.js 14 + Tailwind) · SQLite (V0) → BigQuery + GCS WORM (V1) · Google Gemini 2.5 (Flash + Pro) |

---

## 1. What it does, in one round trip

```
POST /v1/debates
{
  "topic": "Should India introduce a Universal Basic Income for households below the third MPCE quintile?",
  "n_agents": 12,
  "rounds": 1
}
        ↓
  ▸ k-DPP-sample 12 personas from the 50-persona library
  ▸ R1 fan-out: 12 Flash calls in parallel (asyncio.gather, sem=10)
  ▸ Synthesis: 1 Pro call → 7-section editorial article
  ▸ Conclusion: 1 Pro call → quality-weighted conclusive remark
  ▸ Persist debate + 4 hash-chained audit events to SQLite
        ↓
  HTTP 200 in ~80 s, ~$0.02 cost
  GET /v1/debates/{id}/audit  → chain_valid: true, 4 events
```

Live demo, persisted from V0.10 verification:

```
http://localhost:3000/audit/9dfc21cc-97f8-457f-a8a4-60d22b44fe95
http://localhost:3000/audit/72e211cc-d64c-4361-8f6f-6e336ed96d39
```

---

## 2. Quickstart

### 2.1 Prerequisites

- macOS or Linux
- Python 3.11+ (we test against 3.13)
- Node 20+
- Poetry 2.x (`pip install --user poetry`)
- *Optional, for online mode:* a Gemini API key from <https://aistudio.google.com/apikey>

### 2.2 Offline mode (deterministic stub, no network, no key)

```bash
git clone <repo> ~/code/akhada-engine
cd ~/code/akhada-engine

# orchestrator
cd services/orchestrator
poetry install
poetry run pytest -q             # 31 passed in 0.80 s
poetry run uvicorn akhada.api.main:app --reload --port 8080

# studio (in another terminal)
cd services/studio-web
npm install
npm run dev                       # http://localhost:3000
```

`POST /v1/debates` returns the deterministic stub. Useful for CI, schema work, and Studio UI iteration.

### 2.3 Online mode (real Gemini)

```bash
cp .env.example services/orchestrator/.env
# edit:
#   AKHADA_OFFLINE=false
#   GOOGLE_API_KEY=AIza...
#   AKHADA_PERSONAS_FILE=data/personas/personas-2026.Q2.1.jsonl
# restart uvicorn

curl http://127.0.0.1:8080/v1/runtime
# {"online_ready": true, "reason": null}
```

Now `POST /v1/debates` runs real Flash openings (one per persona, async-fanned) → Pro synthesis → Pro conclusion. Cost ≈ $0.02 per 12-persona debate; ~$0.05 per 50-persona debate.

---

## 3. Architecture

```
                     Studio (Next.js 14)
                     ├── /                — debate launcher + result render
                     ├── /audit/[id]      — hash-chain visualisation
                     └── /debate/[id]     — V1 SSE live cluster view (stub)
                                  │
                                  │  HTTP / SSE
                                  ▼
                     Orchestrator (FastAPI / asyncio)
                     ├── POST /v1/debates           — run + persist + audit
                     ├── GET  /v1/debates           — list (recent first)
                     ├── GET  /v1/debates/{id}      — full record
                     ├── GET  /v1/debates/{id}/audit— chain + chain_valid
                     ├── GET  /v1/runtime           — online_ready status
                     └── GET  /health
                                  │
              ┌───────────────────┼─────────────────────────┐
              ▼                   ▼                         ▼
      Persona registry      Runtime backend          Persistence
      ──────────────       ─────────────────       ─────────────
      • 5 hand-curated  +  • offline (stub)        • SQLite (V0)
        45 generated         deterministic          ├── debates
      • k-DPP sampler       no network              └── debate_events
      • Open Library       • online (Gemini)          (hash-chained)
        validator           Flash R1 + Pro
      • TF-IDF embed.       synthesis +
                            conclusion
```

V1 swaps SQLite → BigQuery + GCS WORM bucket and the runtime → real Google ADK SequentialAgent + ParallelAgent fan-out (plan §6, §20).

---

## 4. Persona library

### 4.1 Sources (V0.10)

The library is composed of two layers:

**Hand-curated (`fixtures.py`):** 5 personas covering core archetypes — Karnataka teacher, Bihar farmer, Mumbai founder, Kerala nurse, Punjab veteran — each with a hand-written full Biography. These ship in-tree as the always-available baseline.

**Generated (`data/personas/personas-2026.Q2.1.jsonl`):** 45 personas produced by the Pro-tier biography generator from a fixed seed list. Combined library spans **27 states + UTs**, every major religion, the full caste spectrum, and the literacy spectrum from oral-only to doctorate.

Demographic seeds are anchored to:

| Source | License | Used for |
|---|---|---|
| Census of India 2011 | Govt open | state, district type, age band, gender, religion, caste category, education, occupation, urban/rural |
| NFHS-5 (2019–21) | DHS Program (free, registration) | household composition supplement |
| CSDS-Lokniti National Election Studies | Academic | ideological vectors (Lokniti scales) |
| World Values Survey wave 7 | CC-BY/proprietary | Inglehart values (traditional/secular, survival/self-expression) |
| AI4Bharat IndicVoices | CC-BY 4.0 | district + language-cohort plausibility |

V1 expands the seed sampler to a stratified Census 2011 → 5,000-persona library, then 50,000 at V2 (district-anchored). See plan §5 for the full data catalog.

### 4.2 Schema

Defined in `akhada/persona_registry/schema.py` (Pydantic v2, immutable).

```python
class Persona:
  id: "akh-p-fixture-001" | "akh-p-gen-001"
  version: "personas:2026.Q2.1"
  source_anchor: { dataset, row_hash, weight }
  demographic:   { state, district_type, age_band, gender,
                   religion, caste_cat, mpce_quintile,
                   education, occupation, urban_rural }
  ideological:   { lokniti_econ, lokniti_social,
                   wvs_traditional_secular,
                   wvs_survival_self_expression }     ∈ [-1, 1]
  psych:         { big5: { openness, conscientiousness, extraversion,
                           agreeableness, neuroticism },
                   mbti }
  expertise: list[str]
  language:      { primary (BCP-47), literacy, scripts_known, code_mix }
  comm_style:    { formality, verbosity, rhetoric }
  knowledge_cutoff: date
  embedding: list[float] | None  (1536-d, populated at V1)
  biography: Biography
```

`Biography` is the high-signal layer:

```python
class Biography:
  narrative_summary:    str (200-word first-person bio)
  eras:                 list[LifeEra]                  (3-5)
  formative_experiences: list[FormativeExperience]      (3-5)
  cultural_influences:  list[CulturalInfluence]         (8-15)
  top_5_books:          list[CulturalInfluence]         (exactly 5)
  mentors:              list[Mentor]                    (1-3)
  historical_events_lived: list[str]                    (4-10)
  worldview_shifts:     list[WorldviewShift]            (0-3)
  pet_issues, vocabulary_quirks, aspirations, fears
```

`top_5_books` is a `list[CulturalInfluence]` (not a list of strings) so it gracefully handles non-literate personas via the `kind` discriminator: a marginal Bihar farmer's top-5 contains the Ramayan TV serial, JP Narayan speeches, Sharda Sinha lokgeet, and AIR Krishi Darshan — not invented books. An Odisha fisherman's top-5 cites Jagannatha Dasa's Odia Bhāgabata + local Pala/Daskathia oral traditions.

### 4.3 Generator (V0.8+)

```bash
poetry run akhada library generate \
    --start 0 --end 45 \
    --append \
    --output data/personas/personas-2026.Q2.1.jsonl
```

For each demographic seed, the generator calls Gemini 2.5 Pro with a structured-JSON prompt (`response_mime_type=application/json`, temperature 0.9, semaphore-bounded concurrency = 4), parses the response, and validates against the Pydantic schema. One retry on parse / validation failure with the error fed back into the prompt.

Validated run on the V0.10 library:

```
generation complete: 45/45 ok
appended; 5 existing + 45 new = 50 total → data/personas/personas-2026.Q2.1.jsonl
elapsed: 182 s   cost: ~$1.05   retries triggered: 0
```

### 4.4 Validator (V0.9+)

```bash
poetry run akhada library validate data/personas/personas-2026.Q2.1.jsonl
```

For every `kind == "book"` cultural influence, looks up Open Library by title + author with token-overlap fuzzy match (≥ 0.6) and an allow-list for known Indian sacred / classical texts that Open Library's coverage misses. Honest output:

```
=== Book authenticity report ===
  personas         : 45
  total books      : 22  (subset of 273 cultural influences)
  Open-Library hit : 12
  Indian sacred    : 0   (allow-listed; OL coverage gap)
  unverified       : 10  ← all manually confirmed real (e.g. Daya Pawar's
                          *Baluta*, Benyamin's *Aadujeevitham*, Maulana
                          Azad's *Ghubar-e-Khatir*) — Open Library has
                          weak Indic-language coverage. V1 wires Wikidata
                          SPARQL fallback per plan §5.4.
  verified fraction: 54.55 %
```

The `--fail-threshold` flag turns the validator into a CI gate. V1 publishes a quarterly bias-audit report (plan §5.7).

---

## 5. Sampling — k-DPP (plan §19.2)

When `n_agents < |library|`, the sampler is an exact k-Determinantal Point Process implemented in `akhada/persona_registry/sampler.py`.

**Kernel:** `L_ij = q_i · q_j · K(x_i, x_j)` with `K(x, y) = exp(−‖x − y‖² / 2σ²)`, `σ = 0.6`, `q_i ≡ 1` at V0.9 (uniform quality; V1 introduces topic-conditional quality weighting).

**Embedding:** TF-IDF (sklearn, max-features 2048, ngram (1, 2), sublinear-tf) over a concatenation of `narrative_summary`, `top_5_books` titles, `pet_issues`, `expertise`, and the demographic line — row-normalised so the kernel is bounded. V1 swaps to Sentence-BERT or Vertex embeddings.

**Sampling:** Kulesza-Taskar (2012) exact spectral algorithm. Eigendecompose `L`, sample a subset of eigenvectors via dynamic programming over the elementary symmetric polynomials of the eigenvalues, then sequentially pick items with probability ∝ ‖V_i‖² in the chosen eigenspace, projecting orthogonally after each pick.

**Negative-association property** (plan §19.2):
```
P({i, j} ⊂ S) − P(i ∈ S) · P(j ∈ S) ≤ 0
```
which is what k-DPP buys us over heuristic "stratified sampling" — provable suppression of similar-persona joint inclusion.

**Verified:**
- 30-persona DPP draw from the 50-library spans 22 distinct states (V0.9 commit message; reproducible)
- Deterministic under `seed`
- No duplicates
- Falls back to fixture-cycle when `n ≥ |library|`

Tests in `tests/test_sampler.py`.

---

## 6. Debate flow

Implementation: `akhada/runtime/online.py`.

| Stage | Calls | Model | Purpose |
|---|---|---|---|
| R1 openings | N (panel size) | Gemini 2.5 Flash | each persona's 80–150-word first-person opening, persona-prompt-conditioned via `prompt_renderer.render_summary` |
| Synthesis | 1 | Gemini 2.5 Pro | composes the 7-section article |
| Conclusion | 1 | Gemini 2.5 Pro | writes the Bradley-Terry-leaning conclusive remark |

Concurrency for R1 openings is bounded by `asyncio.Semaphore(10)` (Vertex regional RPM-safe). Per-leaf failure falls back to a demographic-only placeholder and is tagged so the synthesis layer still runs and the count is reported back as `openings_failed`.

V1 (plan §6) rebuilds this as

```python
SequentialAgent(
    sub_agents=[
        framer,                              # R0
        ParallelAgent(persona_leaf x 500),   # R1 openings (5 nested ParallelAgent(100))
        ParallelAgent(cluster x 25),         # R1' cluster debate
        ParallelAgent(super_cluster x 5),    # R2
        LoopAgent(final, max_iters=2),       # R3 with conformity-check loop
    ]
)
```

via the real Google ADK orchestration primitives.

### 6.1 Synthesis prompt (plan §7)

The Pro synthesis instruction enforces seven exact sections:

1. **Context & Framing**
2. **Perspectives by Cluster** (one paragraph per cluster, named by core stance, persona ids cited inline)
3. **Points of Agreement** (claims with low contention)
4. **Points of Contention** (steelmanned both sides)
5. **Evidence Map** (claims marked `[unverified]` where the panel asserts without grounding)
6. **Recommendations / Decision Tree**
7. **Minority Voices Appendix** (3 most distinctive minority statements verbatim)

### 6.2 Conclusive remark — argument-quality, not majority

The conclusive-remark prompt explicitly instructs the Pro model to cite the strongest *argument*, not the most popular *side*. In the V0.10-verified MSP debate, the synthesis backed the institutional-skeptic position (one persona — `akh-p-fixture-003`) over the four-persona moral-imperative cluster, because the argument cleared the §6 quality bar.

V1 replaces this with the explicit Bradley-Terry quality formula

```
q_j = β₁ · groundedness + β₂ · coherence + β₃ · cross_cluster_reach
    + β₄ · red_team_survival − β₅ · conformity_inflation
```

with weights `β` MLE-fit on a held-out 50-debate × 3-rater calibration set, version-pinned (`weights:vX.Y.Z`) and shipped as part of the open-core release. See plan §6, §19.6.

---

## 7. Audit trail (plan §20.10)

Every debate writes 4 events to `debate_events` keyed by `(debate_id, seq)`:

| seq | type | payload |
|---|---|---|
| 0 | `topic_received` | topic, n_personas, library_version, weights_version, mode, panel_persona_ids |
| 1 | `openings_complete` | count, failed, backend |
| 2 | `synthesis_complete` | article_chars, h2_count |
| 3 | `conclusive_complete` | remark_chars |

**Hash chain.** Each event's `payload_hash` is `SHA-256(canonical_json(payload) + "|" + prev_hash)`. Linking inside the digest (not just sequence order) is what binds the chain — any payload mutation invalidates every downstream hash. The chain root has `prev_hash = 64 × "0"`.

`canonical_payload_json` uses `json.dumps(..., sort_keys=True, separators=(",", ":"))` so reproducibility is independent of dict ordering or whitespace.

**Verification.** `akhada.persistence.audit.verify_chain(events)` walks events in seq order, recomputes each hash, returns `(valid, error)`. The `GET /v1/debates/{id}/audit` endpoint runs this verify on every read and returns `chain_valid` + `chain_error`.

**Tamper detection — verified by test.** `tests/test_persistence.py::test_tampering_breaks_the_chain` mutates a stored `payload_json` field directly in SQLite and asserts that `verify_chain` returns `False` with `"payload_hash mismatch"`. Without this test the chain claim would be vapor.

V1 commits a daily Merkle root over each day's events to a GCS WORM bucket with retention-lock so the chain is tamper-evident even against database operators (plan §20.10).

The Studio `/audit/[id]` page renders the verified chain as an editorial document with prev → hash linkage in saffron, JSON payload preview, and a saffron `HASH CHAIN · VERIFIED` pill (or red `TAMPERED` with the chain_error reason).

---

## 8. API reference

All endpoints return JSON. CORS is permissive on localhost in dev; locked to specific origins at V1.

### `GET /health`
```json
{ "status": "ok", "version": "0.0.1" }
```

### `GET /v1/runtime`
Reports backend readiness without making a model call.
```json
{ "online_ready": true, "reason": null }
// or
{ "online_ready": false, "reason": "AKHADA_OFFLINE=true (default V0 stub)" }
```

### `POST /v1/debates`

Request:
```json
{
  "topic": "Should the central government extend MSP guarantees…",
  "n_agents": 12,            // 5–2000
  "cluster_size": 12,        // 2–100
  "rounds": 1,               // 1–5
  "mode": "research",        // "research" | "publication"
  "persona_library_version": "personas:2026.Q2.1",
  "weights_version": "weights:v0.0.0"
}
```

Response (truncated):
```json
{
  "debate_id": "9dfc21cc-…",
  "topic": "…",
  "article": "# … (markdown)",
  "conclusive_remark": "…",
  "n_personas": 12,
  "panel_archetypes": [ { "persona_id": "…", "label": "…", "count": 1, … } ],
  "backend": "online-gemini",
  "openings_failed": 0,
  "persona_library_version": "personas:2026.Q2.1",
  "weights_version": "weights:v0.0.0"
}
```

`mode: "publication"` returns 400 — gov-tier attestation required (plan §20.15 ECI guard).

### `GET /v1/debates?limit=50`
```json
[ { "debate_id": "…", "topic": "…", "backend": "online-gemini",
    "n_personas": 50, "created_at": 1777714660.756663 }, … ]
```

### `GET /v1/debates/{id}`
Full persisted record.

### `GET /v1/debates/{id}/audit`
```json
{
  "debate_id": "…",
  "topic": "…",
  "chain_valid": true,
  "chain_error": null,
  "events": [
    { "seq": 0, "event_type": "topic_received",
      "prev_hash": "00000000…", "payload_hash": "e5b2a77c…",
      "payload": { … }, "ts": 1777714208.0 },
    …
  ]
}
```

---

## 9. Configuration (`.env`)

| Variable | Default | Purpose |
|---|---|---|
| `AKHADA_OFFLINE` | `true` | When `true`, debates use the deterministic stub. Set `false` for real Gemini. |
| `GOOGLE_API_KEY` | `""` | Gemini API key from <https://aistudio.google.com/apikey>. Required for online mode. |
| `GOOGLE_GENAI_USE_VERTEXAI` | `false` | V1 switch to Vertex AI auth (workload identity). |
| `GEMINI_MODEL_FLASH` | `gemini-2.5-flash` | R1 opening model. |
| `GEMINI_MODEL_PRO` | `gemini-2.5-pro` | Synthesis + conclusion + library generation. |
| `AKHADA_PERSONAS_FILE` | `""` | Path to a JSONL persona library to merge with the 5 hand-curated fixtures. |
| `AKHADA_DB_PATH` | `data/akhada.db` | SQLite path for the debate store + audit log. |
| `AKHADA_API_HOST` / `AKHADA_API_PORT` | `127.0.0.1` / `8080` | API bind. |
| `AKHADA_LOG_LEVEL` | `INFO` | stdlib logging level. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `""` | V1 OTEL → Cloud Trace. |
| `SARVAM_API_KEY` / `ANTHROPIC_API_KEY` | `""` | V1+ adapters. |

---

## 10. CLI

```bash
poetry run akhada debate run --topic "…" --agents 12 --rounds 1 --language en-IN
poetry run akhada library generate --start 0 --end 45 --append --output data/personas/personas-2026.Q2.1.jsonl
poetry run akhada library validate data/personas/personas-2026.Q2.1.jsonl --fail-threshold 0.5
poetry run akhada library show data/personas/personas-2026.Q2.1.jsonl
poetry run akhada eval bench:diversity   # V1 stub
```

---

## 11. Tests

```
poetry run pytest -q
............................... [100%]
31 passed in 0.80s
```

| Suite | Count | What it verifies |
|---|---|---|
| `test_smoke.py` | 4 | health, debate stub round-trip, runtime status, online-mode-key-required |
| `test_schema.py` | 5 | Persona / Biography Pydantic invariants (top_5_books exactly 5; MBTI regex; persona-id pattern; immutable persona; age-range validation) |
| `test_fixtures.py` | 8 | hand-curated diversity (state spread, religion + econ-axis spread, literacy spectrum, cultural-input kind variety, cycle behaviour, age-vs-events consistency) |
| `test_sampler.py` | 4 | k-DPP returns requested size, no dups, deterministic under seed, falls back to cycle when `n ≥ |library|` |
| `test_persistence.py` | 7 | save→get round-trip, chain valid by construction, prev_hash linkage, **tamper detection** (mutates SQLite directly), recency ordering, end-to-end POST→audit, 404 |
| `tests/conftest.py` | autouse | clears `AKHADA_OFFLINE`, `GOOGLE_API_KEY`, `AKHADA_PERSONAS_FILE`, `AKHADA_DB_PATH` at top-level so tests are hermetic regardless of `.env` |

---

## 12. Performance & cost (measured V0.10)

All numbers are from real runs against `gemini-2.5-flash` + `gemini-2.5-pro` over the public Generative Language API.

| Workload | Latency | Cost | Failures |
|---|---|---|---|
| 5-persona online debate (MSP) | ~70 s | ~$0.005 | 0 |
| 12-persona DPP debate (UBI) | ~80 s | ~$0.012 | 0 |
| 30-persona DPP debate (MSP, 22 states) | ~80 s | ~$0.04 | 0 |
| 50-persona online debate (MSP) | ~90 s | ~$0.05 | 0 |
| Library generation: 35 personas | ~6 min | ~$1.05 | 0 (no retries) |
| Open Library validation: 22 books | ~3 s | $0 | n/a |
| `pytest` (offline, 31 tests) | 0.80 s | $0 | 0 |
| Studio prod build | ~12 s | $0 | 0 |
| Studio bundle: `/` First Load JS | 135 kB | — | — |
| Studio bundle: `/audit/[id]` First Load JS | 95 kB | — | — |

Throughput is dominated by the synthesis call (one Pro call), so latency is approximately constant beyond ~5 personas; the linear cost component is openings-on-Flash. This is the right shape for the V1 hierarchical 25 × 20 → 5 → 1 fan-out.

---

## 13. Project layout

```
akhada-engine/
├── README.md                  ← this file
├── LICENSE                    ← AGPL-3.0-or-later + commercial note
├── NOTICE                     ← dataset attribution
├── .env.example               ← all env vars documented
├── docs/
│   ├── BUSINESS-PROPOSAL.md   ← strategic deck for multilateral wedge
│   ├── compliance/            ← DPDP / IT Rules / EU AI Act packs (V2)
│   └── persona-library/       ← bias-audit reports
├── services/
│   ├── orchestrator/          ← Python; ADK + FastAPI; the engine
│   │   ├── pyproject.toml
│   │   ├── data/
│   │   │   ├── personas/personas-2026.Q2.1.jsonl   ← 45 generated
│   │   │   └── akhada.db (gitignored)              ← SQLite store
│   │   ├── src/akhada/
│   │   │   ├── api/           ← FastAPI app + routes + schemas
│   │   │   ├── flows/         ← debate dispatcher (offline ↔ online)
│   │   │   ├── runtime/       ← online (real Gemini) backend + prompts
│   │   │   ├── persona_registry/
│   │   │   │   ├── schema.py          ← Pydantic models
│   │   │   │   ├── fixtures.py        ← 5 hand-curated baseline
│   │   │   │   ├── sampler.py         ← k-DPP
│   │   │   │   ├── prompt_renderer.py ← persona prompts
│   │   │   │   ├── biography/         ← Pro-tier generator + seeds
│   │   │   │   └── validation/        ← Open Library validator
│   │   │   ├── persistence/   ← SQLite + hash-chained audit
│   │   │   ├── synthesis/     ← extract / compose / conclude / verify
│   │   │   ├── conformity/    ← deterministic dissent appendix (V1)
│   │   │   ├── eval/          ← diversity / conformity / bias-audit (V1)
│   │   │   ├── agents/        ← V1 ADK LlmAgent templates
│   │   │   ├── telemetry/     ← OTEL → Cloud Trace (V1)
│   │   │   ├── cli.py         ← `akhada` CLI
│   │   │   └── config.py      ← pydantic-settings
│   │   └── tests/             ← 31 tests, hermetic
│   └── studio-web/            ← Next.js 14 + Tailwind + Source Serif 4
│       ├── app/
│       │   ├── page.tsx                ← debate launcher + result
│       │   ├── audit/[id]/page.tsx     ← hash-chain visualisation
│       │   └── debate/[id]/page.tsx    ← V1 SSE live cluster view
│       ├── components/        ← editorial component library
│       ├── lib/cn.ts, format.ts
│       └── tailwind.config.ts ← warm cream + ink + saffron palette
├── packages/
│   └── shared-types/          ← TS types (V1 codegen from Pydantic)
├── benchmarks/akhada-bench/   ← gold sets, eval harness (V1 — `AkhadaBench`)
├── infra/                     ← Terraform; V1 lands Vertex / Firestore / KMS
└── .github/workflows/ci.yml   ← ruff + mypy --strict + pytest + Studio build
```

---

## 14. Roadmap

| Phase | Duration | Scope | Gating milestone |
|---|---|---|---|
| **V0–V0.10** | shipped | scaffold; 5 fixtures → 50-persona library; real Gemini debates; k-DPP; Open Library validator; SQLite + hash-chained audit; editorial Studio + audit page | 31 tests; 8 commits; live demo of MSP + UBI + plastics-ban debates with verified audit chains |
| **V1 — MVP** | 10 weeks | Real ADK SequentialAgent + ParallelAgent fan-out (25 × 20 → 5 → 1). 500-persona library v1 (Census + Lokniti stratified sampler). EN + HI via Sarvam. SSE live cluster stream. Bradley-Terry weights calibrated. `AkhadaBench` v0 published. Multi-tenant CMEK. | First external beta with 5 think-tank partners; CSDS bias-audit pass. |
| **V2 — Government pilot** | 20 weeks | 22 Indian languages. 50,000-persona district-anchored library. First ministry pilot (e.g. farm-bill simulation re-run). DPDP DPIA + EU AI Act Annex IV docs shipped. On-prem deploy kit (Anthos / Confidential GKE). | One signed ministry MoU; DPDP compliance attested; EU AI Act readiness verified externally. |
| **V3 — Platform** | 24 weeks | Public API. Pluggable model adapters (LiteLLM for Claude / OpenAI / open-weights). White-label (UPSC coaching, election research). `AkhadaBench` cited externally. Vertex batch + spot GPUs for open-weight tier. Global persona modules (WVS / Pew / Eurobarometer). | $50K MRR; AkhadaBench cited by ≥ 2 external papers. |

---

## 15. License

**Open core: AGPL-3.0-or-later.** The engine, the persona schema, the k-DPP sampler, the offline runtime, the audit trail, the Open Library validator, the Studio, and the eval harness are all AGPL-3.0. See `LICENSE`.

**Commercial license** issued by **SARGVISION Intelligence** for gov-tier features: 50,000-persona district-anchored library v2, DigiLocker e-KYC integration, Opus synthesis tier, on-prem deploy kit (Anthos + Confidential GKE), audit-immutability WORM provisioning, multi-tenant CMEK provisioning, white-label Studio, observability + SLO dashboard pack. Contact via this repository's issues or the maintainers' email.

Dataset attribution in `NOTICE`.

---

Akhada is a product of **SARGVISION Intelligence**.

---

## 16. Acknowledgements

Built on the shoulders of:

- **Google Agent Development Kit** (Apache-2.0) — V1 multi-agent orchestration primitives
- **google-genai** — Gemini 2.5 Flash + Pro inference
- **AI4Bharat** (CC-BY 4.0) — IndicVoices, IndicAlign, IndicCorp
- **Open Library** (CC0 + ODbL) — book metadata
- **Wikidata** (CC0) — V1 fallback for Indic-language coverage gaps
- **PRS Legislative Research** (CC-BY 4.0) — bills, votes, MP profiles
- **Pratham StoryWeaver** (CC-BY 4.0) — multilingual literacy content
- **CSDS-Lokniti National Election Studies** — ideological scales (academic license)
- **Du et al., ICML 2024** ("Improving Factuality and Reasoning in Language Models through Multiagent Debate") — methodological foundation
- **Stanford generative-agents work (Park et al. 2023)** — persona-attribution framing
- **S²-MAD (NAACL 2025)** — sparse-communication motif for V1 cluster debate
- **Kulesza & Taskar 2012** — exact k-DPP sampling
