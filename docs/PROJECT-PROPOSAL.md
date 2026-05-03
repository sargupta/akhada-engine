# Akhada — Project Proposal

> **An open civic-deliberation engine for India: stress-testing public deliberation, before public deliberation stress-tests you.**
>
> *A SARGVISION Intelligence proposal. Companion to `README.md`, `RELATED-WORK.md`, and `BUSINESS-PROPOSAL.md`.*

| | |
|---|---|
| Document version | 1.0 (May 2026) |
| Format | Research-and-implementation proposal, suitable for grant boards, foundation programme officers, multilateral country offices, and academic-partnership review |
| Built artefact pinned | [Akhada v0.10.0](https://github.com/sargupta/akhada-engine/releases/tag/v0.10.0) |
| Programme duration sought | 18 months (V0.11 → V2 ministry pilot) |
| Indicative budget | ₹3.0 cr — ₹4.5 cr (USD 360K — 540K) for the 18-month programme |

---

## Abstract

Akhada is a working open-source software engine, currently at v0.10.0, that runs a panel of biographically-grounded AI personas — anchored to the Indian Census 2011, NFHS-5, CSDS-Lokniti, and World Values Survey distributions — through a structured multi-agent debate on a policy topic, and produces a sourced editorial article + Bradley-Terry-quality-weighted conclusive remark + cryptographic, hash-chained audit trail. End-to-end latency is 70–90 seconds; cost is ₹2–5 per debate; the V0.10 library covers 27 Indian states + Union Territories, every major religion, the full caste spectrum, and the literacy spectrum from oral-only to doctorate.

This proposal seeks support for an 18-month programme — V0.11 hardening through V2 ministry pilot — that delivers (a) a 500-persona V1 library with provable representativeness, (b) a published evaluation benchmark (`AkhadaBench` v1) calibrated against CSDS poll baselines, (c) a co-authored peer-reviewed methodology paper, (d) one signed multilateral pilot with an India programme office, (e) one signed Indian-state-government pilot, and (f) the V2 Data Protection Impact Assessment + EU AI Act Annex IV technical-documentation pack required for production deployment in regulated contexts.

The proposal is structured as a research-and-implementation hybrid. The primary research contributions are: (i) the *first* India-grounded synthetic-persona civic-deliberation engine; (ii) provable-diversity persona sampling via exact k-DPP (Kulesza-Taskar 2012) on biographically-rich embeddings; (iii) Bradley-Terry quality-weighted synthesis with calibration on a held-out 50-debate × 3-rater set; (iv) a hash-chained per-debate audit trail with executable tamper detection. The primary implementation contributions are the open-source AGPL-3.0 release, the `AkhadaBench` v1 public scoreboard, the methodology paper, and two operational pilots.

---

## 1. Introduction and motivation

### 1.1 The problem

Multilateral programme offices (World Bank India, BMGF India, UNDP India, ADB India, Omidyar Network India, Tata Trusts) and Indian policy bodies (NITI Aayog, central ministries, state governments) routinely commit programme spend in India before they fully understand how that spend will be received across the country's heterogeneous population. The current toolkit for closing that gap — qualitative fieldwork via FGDs, IDIs, KIIs, and PRA — is genuinely useful but bound by four constraints visible in any practitioner's published methodology:

1. **Iteration speed.** A typical TOR allows one round of fieldwork. Re-fielding to test a revised hypothesis is a budget conversation, not a methodological adjustment.
2. **Coverage.** Six districts is a sample. India has 28 states + 8 UTs and ~ 700 districts; six is a defensible cluster sample for a single research question, not for the multi-question hypothesis-iteration that programme design actually requires.
3. **Defensibility.** A typical deliverable is a slide deck. The path from a transcript line in Bhojpuri to a claim on slide 17 is rarely auditable, and the deck does not survive a CAG / IG / Standing Committee challenge back to underlying transcripts.
4. **Languages.** A debate happening in Bhojpuri at an FGD in Saran is reported in English at a Washington-DC programme review; voice quality compresses by an order of magnitude across that translation.

These are standard limitations of qualitative fieldwork at multilateral budget scales (₹15–40 lakh per engagement, 4–8 weeks). The Indian qualitative-research market itself is **₹29,008 crore (USD 3.5 B), 10.9 % YoY growth as of FY25** (Market Research Society of India, January 2026); the multilateral and foundation slice — work commissioned for programme design — is the high-defensibility component of that market and is the target for this proposal.

### 1.2 The research question

> *Can a software system that runs a panel of biographically-grounded synthetic Indian personas through a structured debate, with provable-diversity sampling and a cryptographic audit trail, produce stakeholder-analysis output that is defensible enough to be cited as evidence in a multilateral programme report or a peer-reviewed academic paper, at one-hundredth the cost and one-thousandth the elapsed time of equivalent qualitative fieldwork?*

The thesis defended in this proposal — and partly demonstrated by the v0.10.0 release — is that the answer is *yes*, conditional on three constraints being met simultaneously: (i) the persona library must be calibrated against external Indian poll baselines (CSDS, Pew India) and must pass a quarterly bias audit; (ii) the synthesis must explicitly mark unverified claims and cite evidence; (iii) every debate must be persisted with a tamper-evident audit log auditable by a third party.

The 18-month programme described here delivers, tests, and publishes against all three constraints.

### 1.3 Position in the literature

A full survey is in [`docs/RELATED-WORK.md`](RELATED-WORK.md). Headlines:

- The *closest academic neighbour* is DeepMind's Habermas Machine (Science 2024) — AI-mediated deliberation that synthesises group statements while preserving minority perspectives, tested on 5,000+ UK participants. Habermas Machine works on real human input; Akhada works on synthetic personas. The two complement: Akhada for hypothesis-iteration, Habermas Machine for post-hoc synthesis of real-citizen output.
- The *closest civic-tech neighbour* is Pol.is (used in Taiwan vTaiwan, UK Cabinet Office, and Anthropic's Collective Constitutional AI). Pol.is requires real human respondents and clusters their stated opinions; Akhada simulates the panel.
- The *closest persona-simulation neighbour* is Stanford's 1,052-persona work (Park et al. 2024, [arXiv:2411.10109](https://arxiv.org/abs/2411.10109)), which achieved 85 % accuracy in matching individual human responses across Big Five, GSS, and economic-game items. Akhada applies a population-aligned variant of that methodology to the Indian context.
- The *closest open-source civic-platform neighbours* — Decidim, Loomio, Consul Project — are mature AGPL-3.0 platforms for human deliberation; none has an AI deliberation layer.

No surveyed system covers the **intersection** of (i) Indian demographic grounding, (ii) provable-diversity sampling, (iii) hash-chained audit, (iv) Bradley-Terry quality-weighted synthesis. The eight-point gap analysis in `docs/RELATED-WORK.md` §8 documents this in detail. This proposal funds the work to maintain that intersection through V1 and V2.

---

## 2. Methodology and system design

The system architecture is documented at engineering depth in [`README.md`](../README.md) §3–§9. This section summarises the methodology at proposal depth.

### 2.1 Persona library — distribution-anchored, biographically rich

Each persona in the Akhada library is a Pydantic record (`akhada/persona_registry/schema.py`) with two layers:

- **Demographic / ideological / psychometric layer** — anchored to Census 2011 (state · district type · age band · gender · religion · caste category · MPCE quintile · education · occupation · urban / rural), NFHS-5 (household composition supplement), CSDS-Lokniti (Lokniti scales: lokniti_econ, lokniti_social), WVS w7 (Inglehart values: traditional/secular, survival/self-expression), and a Big-Five + MBTI psychometric profile.
- **Biographical layer** — a 200-word first-person narrative, 3–5 life eras anchored to district + cohort, 3–5 formative experiences, 8–15 cultural influences, exactly 5 `top_5_books` (with a `kind` discriminator that gracefully degrades from books-for-the-literate to TV-serials-and-kirtan-and-radio-programmes for the oral-tradition cohort), 1–3 mentors, 4–10 historical events lived through, 0–3 documented worldview shifts, plus pet issues, vocabulary quirks, aspirations, fears.

V0.10 ships a 50-persona library (5 hand-curated + 45 generated by Pro-tier biography generation, validated against Open Library). V1 expands to 500 personas via stratified Census 2011 sampling; V2 expands to 50,000 with district-level anchoring.

### 2.2 Sampling — provable-diversity via k-DPP

When the requested panel size is smaller than the library, Akhada samples via an *exact* k-Determinantal Point Process implemented in `akhada/persona_registry/sampler.py` (Kulesza-Taskar 2012 spectral algorithm). The kernel is `L_ij = q_i q_j K(x_i, x_j)` with `K(x,y) = exp(-||x-y||² / 2σ²)` on TF-IDF embeddings (V1: Sentence-BERT) of `narrative_summary + top_5_books_titles + pet_issues + expertise + demographic line`. The k-DPP guarantees the negative-association property:

```
P({i, j} ⊂ S)  −  P(i ∈ S) · P(j ∈ S)  ≤  0
```

i.e. the joint probability that two similar personas are both selected is suppressed below the product of the marginals. **This is provable diversity, not heuristic stratification.** No reviewed comparable surfaces this guarantee.

V0.10 verification: a 30-persona DPP draw from the 50-library spans 22 distinct Indian states; deterministic under seed; no duplicates.

### 2.3 Debate runtime — single-round V0.10, hierarchical V1

V0.10 ships a single-round runtime (`akhada/runtime/online.py`):

- **R1 openings** — N parallel Gemini 2.5 Flash calls (`asyncio.Semaphore(10)` for Vertex regional RPM safety), each producing an 80–150-word first-person opening conditioned on the persona prompt.
- **Synthesis** — one Gemini 2.5 Pro call composing a 7-section editorial article: *Context & Framing · Perspectives by Cluster · Points of Agreement · Points of Contention · Evidence Map · Recommendations · Minority Voices Appendix.*
- **Conclusion** — one Pro call writing the Bradley-Terry-leaning conclusive remark, instructed to cite the strongest *argument*, not the most popular *side*.

V1 (plan §6) replaces this with a Google ADK SequentialAgent + ParallelAgent hierarchical fan-out: `5 × ParallelAgent(100) → 25 cluster reps → 5 super-cluster aggregators → 1 final synthesiser`, with sparse-communication between cluster boundaries (S²-MAD-inspired, NAACL 2025) to control token cost at 500-persona scale.

### 2.4 Synthesis quality — Bradley-Terry calibration

The conclusive remark in V0.10 is generated by a prompted instruction to cite the strongest argument. V1 replaces this with an explicit Bradley-Terry quality formula:

```
q_j = β₁ · groundedness + β₂ · coherence + β₃ · cross_cluster_reach
    + β₄ · red_team_survival − β₅ · conformity_inflation
```

with weights β fit by maximum likelihood on a held-out **50-debate × 3-rater calibration set**, version-pinned (e.g. `weights:v1.0.0`), shipped as part of the open-core release, and re-calibrated quarterly. The MLE calibration is the V1 research deliverable; the calibration corpus is the V1 dataset deliverable.

### 2.5 Audit trail — hash-chained per-event

Every debate persists 4 events to `debate_events`: `topic_received → openings_complete → synthesis_complete → conclusive_complete`. Each event's `payload_hash = SHA-256(canonical_json(payload) + "|" + prev_hash)` — linking inside the digest, not just sequence order. Tampering with any payload invalidates every downstream hash. An executable test (`test_tampering_breaks_the_chain`) mutates a stored payload directly in SQLite and asserts that `verify_chain` returns `False`.

V1 commits a daily Merkle root of the day's events to a GCS WORM bucket with retention-lock — tamper-evident even against database operators (per plan §20.10). V2 extends this to an external auditor who can run `akhada audit verify <debate_id>` independently of the system operator.

### 2.6 Evaluation — `AkhadaBench` v1

The V1 evaluation deliverable (`benchmarks/akhada-bench/`) is a public scoreboard with the following components:

- **20-topic India-policy gold set** — ground-truth consensus answers on settled policy questions (e.g. "is the earth round?", "did India liberalise its economy in 1991?") plus contestable consensus topics (MSP, UBI, NRC).
- **4 metrics, M3MAD-Bench-compatible** — accuracy on factual subset, conformity (does dissent survive?), faithfulness (does NLI judge the synthesis to be supported by the openings?), cost.
- **Reproducibility scoreboard** — same topic + same seed + same persona-library version → same conclusive remark with ROUGE ≥ 0.9.
- **Bias audit** — KS-test against CSDS poll-data baselines; quarterly publication.

The first published results land at the end of Programme Month 4.

---

## 3. Programme structure

The 18-month programme is divided into four phases. Each phase ships a specific artefact and a specific deliverable to the funding partner.

| Phase | Months | Artefact | Deliverable |
|---|---|---|---|
| **Phase A — Hardening** | 0–3 | V0.11–V0.12 | Multi-tenant isolation, ToS, DPDP DPIA v0, persona library expansion to 200, Wikidata SPARQL fallback, `AkhadaBench` v0 with 20-topic factual gold, SSE streaming + Studio live cluster view, bias-audit v0 against CSDS, methodology paper draft (6 pages) |
| **Phase B — V1 MVP** | 3–8 | V1 | Real Google ADK SequentialAgent + ParallelAgent fan-out (5 × 100 → 25 → 5 → 1), 500-persona V1 library (Census + Lokniti stratified sampler), EN + HI via Sarvam, Bradley-Terry weights MLE-fit on calibration set, multi-tenant CMEK, peer-review-ready methodology paper submitted, **first multilateral pilot signed (₹4 lakh, 4 weeks)** |
| **Phase C — Government pilot** | 8–14 | V2 | 22 Indian languages, 50,000-persona district-anchored V2 library, **first state-government pilot signed and delivered**, DPDP DPIA finalised, EU AI Act Annex IV technical-doc pack, on-prem deploy kit (Anthos / Confidential GKE), `AkhadaBench` v1 published with V1 results |
| **Phase D — Platform** | 14–18 | V3 | Public API (`POST /v1/debates`), pluggable model adapters via LiteLLM, white-label Studio, V3 release, methodology paper accepted (target venue: *ACM CHI* or *CSCW* or *AAAI*), $50K MRR sustained, AkhadaBench cited in ≥ 2 external papers |

### 3.1 Specific gating milestones

| Month | Milestone | Counted as success if |
|---|---|---|
| 3 | DPDP DPIA v0 + ToS + multi-tenant isolation shipped | external lawyer signs off; multi-tenant test suite passes |
| 4 | `AkhadaBench` v0 + bias-audit v0 + methodology-paper draft circulated | KS-test passes (`max_k D_KS ≤ 0.15`); two external academic readers acknowledge draft |
| 6 | First multilateral pilot signed | ₹4 lakh contract executed with one of [World Bank India, BMGF India, UNDP India, ADB India, Omidyar Network India, Tata Trusts] |
| 8 | V1 release + 500-persona library + Bradley-Terry weights `weights:v1.0.0` | calibration validated; library bias audit passes |
| 10 | Methodology paper submitted to peer-reviewed venue | submission acknowledged |
| 12 | First state-government pilot signed | engagement letter executed |
| 14 | V2 release + DPDP DPIA + EU AI Act pack | independent CERT-In-empanelled audit pass |
| 18 | V3 release + AkhadaBench v1 published + paper accepted | DOI assigned; 2 external citations |

Failure to hit a gating milestone triggers a written progress-and-revision note to the funding partner before continuing into the next phase.

---

## 4. Indicative budget

The programme is delivered by a small core team (1.5 senior engineers + 0.5 research lead + 0.25 advisory legal counsel) supplemented by per-phase externals (auditor, calibration raters, paper co-authors). All figures in INR ex-GST.

| Line item | 18-month total | Notes |
|---|---|---|
| Engineering — 1.5 FTE senior | ₹1.50 cr | Akhada V0.11 → V3 ship; SARGVISION Intelligence team |
| Research lead — 0.5 FTE | ₹0.45 cr | persona library, calibration set, methodology paper, AkhadaBench |
| Legal / compliance — advisory retainer | ₹0.20 cr | DPDP DPIA, EU AI Act Annex IV, ECI advisory note, ToS / commercial-license drafting |
| Cloud + LLM — 18 months | ₹0.30 cr | persona library generation (one-time ~₹2 L), real-debate Gemini calls during pilots, V1 / V2 production infra ramp |
| Calibration set — 50 debates × 3 raters | ₹0.20 cr | external academic / civil-servant / journalist raters, ₹13 K each engaged at 2-day rate |
| External audits — pen-test + bias audit + DR drill | ₹0.30 cr | CERT-In-empanelled auditor, quarterly bias-audit verification, annual DR exercise |
| Methodology paper — co-author engagement + venue | ₹0.05 cr | one academic co-author honorarium, submission fees |
| Pilot delivery costs (incl. travel, working sessions) | ₹0.20 cr | covers 2 multilateral + 1 state pilot |
| Contingency (10 %) | ₹0.30 cr | scope variability, exchange-rate movement |
| **Total — 18-month indicative budget** | **₹3.50 cr** | (USD ~ 420K @ ₹84 / USD) |

### 4.1 Funding flexibility

The programme is structured so each phase is independently fundable. A funder can support Phase A alone (₹0.6 cr, 3 months — DPDP DPIA + AkhadaBench v0 + methodology paper draft), Phase A + B (₹1.6 cr, 8 months — through V1 MVP and first multilateral pilot), or the full 18 months. Multi-funder splits are accepted; each funder receives a phase-specific MoU referencing this proposal as the technical foundation.

### 4.2 Cost economics for the funder

A single ₹4 lakh Akhada pilot delivers the equivalent of a ₹15–40 lakh traditional fieldwork engagement (Dalberg India, Sambodhi, Athena Infonomics, Outline India typical scales). The programme's break-even on funded subsidy is ~ 8 pilots — well within the year-2 ARR target documented in `BUSINESS-PROPOSAL.md` §7.3 (₹1.8 cr Year-1 ARR).

---

## 5. Expected outputs

### 5.1 Software outputs

- Akhada V1 (500-persona library, hierarchical ADK debate, EN + HI)
- Akhada V2 (50,000-persona district-anchored library, 22 Indian languages, DPDP / EU-AI-Act pack)
- Akhada V3 (public API, pluggable adapters, white-label Studio)
- `AkhadaBench` v1 — 20-topic India-policy public scoreboard
- Persona library v1 (`personas:2026.Q3.0`) — 500 personas, AGPL-3.0
- Persona library v2 (`personas:2027.Q1.0`) — 50,000 personas, district-anchored, commercial-licensed for the gov tier

### 5.2 Research outputs

- A peer-reviewed methodology paper (target venue: ACM CHI or CSCW or AAAI; alternates: *Journal of Deliberative Democracy*, *Politics and the Life Sciences*, *Indian Journal of Public Administration*).
- Quarterly bias-audit reports (4 reports across the 18 months).
- An open-source `LICENSE`-vendored reference implementation in TypeScript (Studio) and Python (orchestrator), AGPL-3.0.
- A short technical note co-authored with an Indian academic co-author, on persona-attribution accuracy + KS-test bias-audit results, suitable for *AI & Society* or similar.

### 5.3 Operational outputs

- Two signed multilateral pilots (₹4 lakh each, target buyers in `BUSINESS-PROPOSAL.md` §4.1).
- One signed state-government pilot (₹40 lakh, departmental contract).
- One signed think-tank Pro subscription (₹3 lakh / yr; ORF / CPR / Vidhi / IDFC Institute / CEEW are the candidate buyers).
- A published case study of one signed pilot, redacted as needed for buyer confidentiality.

### 5.4 Distribution outputs

- The GitHub repository at https://github.com/sargupta/akhada-engine remains the canonical artefact. v0.10.0, v1.0.0, v2.0.0, v3.0.0 are all tagged releases.
- `README.md`, `RELATED-WORK.md`, `BUSINESS-PROPOSAL.md`, `PROJECT-PROPOSAL.md` are versioned alongside the code.
- A maintained changelog in the GitHub Releases section so a programme officer's IT due-diligence can resolve any cited version to a fixed snapshot.

---

## 6. Risk register

A condensed version of `BUSINESS-PROPOSAL.md` §8, oriented toward funding-board review.

| Risk | Likelihood | Mitigation |
|---|---|---|
| **Anthropic + Pol.is or DeepMind ship a competing India-grounded product** | Medium | Move quickly on India-specific moat (Census + NFHS-5 + Lokniti + Sarvam languages + DPDP DPIA pack); plant `AkhadaBench` flag in literature; close one ministry pilot reference in V2 to create an 18-month lead; the open-source AGPL release with the commercial-tier carve-out reduces forking risk |
| **Multilateral procurement is slower than 6–12 weeks** | Medium-High | Pilot offer is sized for *discretionary* programme-officer budget (₹4 lakh), not annual procurement; three pro-bono Indian think-tank pilots in Phase A produce reference cases independent of multilateral cycle |
| **Persona-library bias audit fails CSDS-baseline KS-test** | Medium | Quarterly mandatory pass; failure halts new gov-pilot conversations until rebalanced; published per persona-library version |
| **Hallucination at scale; "the AI made it up"** | Medium | `[unverified]` markers mandatory in synthesis Evidence Map; Open Library + V1 Wikidata book-authenticity validators; V1 NLI citation verifier strips claims that don't dereference; output framed as "deliberation simulation" with mandatory human-in-loop notice |
| **DPDP / IT Rules / EU AI Act compliance becomes a blocker** | Medium-High | DPIA + Annex IV are gating Phase-C milestones; budgeted at ₹50 lakh + 6 months in Phase C; treated as investment, not afterthought |
| **ECI Model Code of Conduct misclassifies output as paid news / synthetic content** | Medium | Hard ToS ban on candidate / party-targeted use; rate-limit on political topics during ECI Model-Code period; lookup-table-driven `mode: publication` block (already in V0.10); ECI advisory in V2 |
| **Sarvam single-vendor for 22-language layer fails or pivots** | Low-Medium | V2 fallback to Google Translate + Gemini multilingual; data-portability clause in any commercial agreement |
| **Public backlash: "AI is writing our policy"** | Medium-High | Branding: "deliberation simulator", never "policy decider"; mandatory human-in-loop disclaimer; press strategy at V2 launch led by an Indian academic co-author |
| **Funding partner exits mid-programme** | Medium | Don't bet the year on a single partner; aim for 2 multilateral + 1 think-tank + 1 state pilot in parallel; phase-independent fundability per §4.1 |
| **Open-core fork erodes the commercial tier** | Medium | AGPL-3.0 (not MIT) prevents closed forks; commercial features (50K library v2, DigiLocker, on-prem kit, WORM provisioning, multi-tenant CMEK) remain commercially licensed by SARGVISION Intelligence; entitlement check via signed JWT licence |

---

## 7. Why us, why now

### 7.1 Why us

- **Built artefact, not promise.** Akhada v0.10.0 is a tagged GitHub release, AGPL-3.0-licensed by GitHub's own license detector, with 31 / 31 tests passing in 0.80 s, a 50-persona Indian library on disk, three real persisted Gemini-powered debates with verifiable hash chains, and an editorial-grade Studio. The full system architecture is documented at engineering depth in `README.md` and at academic depth in `RELATED-WORK.md`. The funding partner is not investing in a hypothesis.
- **India-rooted methodology.** The persona library cites Daya Pawar's *Baluta*, Maulana Azad's *Ghubar-e-Khatir*, James Dokhuma's *Thla Hleinga Zan*, Rabon Singh Kharsuka's *Ka Jingsneng Tymmen*, and Jagannatha Dasa's Odia Bhāgabata. These are real, verifiable, region-specific texts and traditions. The design choice was made before the GitHub repo opened, not after first contact with a buyer.
- **Audit by default.** Every Akhada output ships with a hash-chained provenance log that an external auditor can verify independently. This is what programme officers worried about *"how would I defend this to my IG?"* need to see in the first demo, not the third meeting.
- **Open-core licensing alignment.** AGPL-3.0 lets the funding partner's technical team inspect the engine; the commercial tier covers the gov-tier features the partner's beneficiaries actually need (50K-persona library v2, on-prem deploy, DPDP DPIA pack). No "trust us" gap.

### 7.2 Why now

- **Generative AI is institutionally legible.** Programme officers in 2024 had to defend *"we used AI"*; in 2026 they have to defend *"we did not use AI to test this."*
- **DPDP Act phasing creates a window.** Phase III (full substantive compliance) lands May 2027; tools that ship a DPDP-ready posture *today* have an 18-month adoption window before compliance becomes table stakes.
- **Anthropic × Pol.is and DeepMind Habermas Machine** have legitimised the *AI-mediated deliberation* category for the exact buyer set we target — but neither has been deployed in an Indian context.
- **Indian-language LLM quality** (Gemini 2.5, Sarvam, AI4Bharat IndicTrans, BharatGen) crossed a usability threshold in 2025–26 that makes the V2 22-language synthesis genuinely possible.

The window for an India-rooted, audit-defensible, multilateral-aimed engine is approximately 18–24 months before incumbents (Dalberg with internal AI, McKinsey with QuantumBlack, the multilaterals' own platforms, Anthropic / Google enterprise products) close it. The 18-month programme described in this document is sized to that window.

---

## 8. Acknowledgements

This proposal builds on the methodological work surveyed in [`docs/RELATED-WORK.md`](RELATED-WORK.md) — most directly on Du et al. (ICML 2024), Park et al. (Stanford 2023, 2024), DeepMind's Habermas Machine (Science 2024), Pol.is (Computational Democracy Project), and the Kulesza-Taskar 2012 k-DPP foundation. It uses datasets from the Government of India (Census 2011, NFHS-5), CSDS-Lokniti, World Values Survey, AI4Bharat (IndicVoices, IndicAlign, IndicCorp), Open Library, Wikidata, PRS Legislative Research, and Pratham StoryWeaver — full attribution in `NOTICE`.

The proposal is authored on behalf of **SARGVISION Intelligence**.

---

## 9. The single contact ask

If you are a programme officer at a multilateral, foundation, think tank, academic centre, or large newsroom evaluating this proposal:

> **One 30-minute working session with one of your live programme questions.** SARGVISION Intelligence will run it through Akhada in front of you and you will see the article + the conclusive remark + the audit chain. If it does not earn the next conversation, both sides stop. If it does, the funding conversation begins on Phase A (₹0.6 cr, 3 months).

Repository: https://github.com/sargupta/akhada-engine
Pinned release: [v0.10.0](https://github.com/sargupta/akhada-engine/releases/tag/v0.10.0)
Companion documents: [`README.md`](../README.md), [`RELATED-WORK.md`](RELATED-WORK.md), [`BUSINESS-PROPOSAL.md`](BUSINESS-PROPOSAL.md)

---

*Akhada is a product of SARGVISION Intelligence.*
