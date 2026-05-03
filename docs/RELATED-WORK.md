# Akhada — Related Work

> **Literature review and competitive landscape, paper-style.**
>
> *A SARGVISION Intelligence document. Companion to `README.md` and `BUSINESS-PROPOSAL.md`.*

| | |
|---|---|
| Document version | 1.0 (May 2026) |
| Akhada release pinned | [v0.10.0](https://github.com/sargupta/akhada-engine/releases/tag/v0.10.0) |
| Method | GitHub repository search (`gh search`) + targeted academic / commercial web research, May 2026 |
| Coverage threshold | Open-source projects with ≥ 50 stars or institutional backing (DeepMind, Anthropic, Stanford, MIT, Tsinghua, etc.); academic systems with peer review or preprint citations |

---

## 0. Abstract

This document is the *Related Work* section of the Akhada project: a structured survey of the open-source repositories, academic systems, and commercial products that operate in the same vector space — multi-agent LLM debate, generative-agent / synthetic-persona simulation, AI-mediated civic deliberation, and human-only deliberation platforms. We map each line of work, identify what Akhada inherits from it, and articulate the **defensible gap** that justifies a new system. The headline finding is that **no public system, open-source or commercial, simultaneously combines: (i) biographically-grounded personas anchored to the Indian Census + NFHS-5 + CSDS-Lokniti; (ii) provable-diversity sampling via k-DPP; (iii) Bradley-Terry quality-weighted synthesis with sourced reasoning; (iv) hash-chained audit trail by default; and (v) editorial-grade output suitable for institutional consumption.** Habermas Machine (DeepMind 2024) is the nearest academic neighbour, Pol.is + Anthropic CCAI the nearest civic-tech neighbour, and DeepMind Concordia + Stanford Generative Agents the nearest persona-simulation neighbours; Akhada sits in the union of these and ships under AGPL-3.0.

---

## 1. Multi-agent LLM debate

### 1.1 Methodological foundations

| Paper | Year | Venue | Contribution |
|---|---|---|---|
| Du, Li, Tenenbaum, Mordatch — "Improving Factuality and Reasoning in Language Models through Multiagent Debate" | 2023 / 2024 | ICML 2024 ([arXiv:2305.14325](https://arxiv.org/abs/2305.14325)) | Foundational result: multi-round debate between independent LLM instances improves factuality + reasoning on math / strategy / fact-completion tasks; effect size depends on round count and topology |
| Liang, Wang, Ge et al. — "Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate" | 2023 | EMNLP 2023 | Diversity-aware debate for translation + reasoning |
| Khan, Hughes, Valentine et al. — "Debating with More Persuasive LLMs Leads to More Truthful Answers" | 2024 | NAACL 2024 | Adversarial debate as alignment + truth surrogate |
| Diverse Multi-Agent Debate (DMAD) | 2025 | ICLR 2025 | Diversity-aware agent routing breaks "mental set" / cascade-conformity |
| M3MAD-Bench | 2026 | preprint ([arXiv:2601.02854](https://arxiv.org/pdf/2601.02854)) | Multi-domain, multi-modal, multi-dimensional benchmark for multi-agent debate; 13 datasets × 9 base models; reports accuracy + cost trade-offs |
| S²-MAD (Sparse-Sampling MAD) | 2025 | NAACL 2025 | Token-cost reduction via sparse communication topologies |
| GroupDebate | 2024 | preprint | Hierarchical group-of-groups debate scaling |

These papers establish the technical viability of structured multi-LLM debate for reasoning tasks. **What they leave out:** a *deliberative* framing — i.e. who is debating, why, with what stake, and how their reasoning binds to a population. Akhada reuses Du et al.'s round-based debate scaffold but *grounds the agents in demographically-anchored biographies*, replacing "agent_1 / agent_2 / …" with `akh-p-fixture-002 (55-64 male marginal farmer, rural Bihar)`.

### 1.2 Open-source debate frameworks

| Repository | Org / Author | Approx. stars | License | What it ships |
|---|---|---|---|---|
| `Skytliang/Multi-Agents-Debate` | independent | ~250 | MIT (?) | First systematic OSS implementation of Du-et-al-style multi-agent debate; consensus mechanisms; clean Python API |
| `thunlp/ChatEval` | Tsinghua NLP | ~180 | MIT | Multi-agent debate framework for LLM-based *evaluation* (judge quality) |
| `MraDonkey/DMAD` | independent | ~65 | unspecified | Reference implementation of the ICLR 2025 DMAD paper |
| `SU-JIAYUAN/M-MAD` | independent | ~55 | unspecified | Multi-dimensional debate for MT evaluation (ACL 2025) |

**Akhada's relationship.** Akhada's V0.10 runtime ships a single-round persona-conditioned opening + Pro synthesis. V1 plans a real multi-round hierarchical debate (`5 × ParallelAgent(100) → 25 cluster reps → 5 super-clusters → 1 final synthesis`) — this is structurally Du et al. extended with sparse communication (S²-MAD-inspired) at the cluster boundary. Reuses the **method**, replaces the **framing**.

---

## 2. Generative agents and synthetic-persona simulation

### 2.1 Foundational systems

| System | Authors / Org | Year | Public artefact |
|---|---|---|---|
| **Smallville (Generative Agents)** | Park, O'Brien, Cai, Morris, Liang, Bernstein (Stanford) | 2023 | [Paper](https://dl.acm.org/doi/10.1145/3586183.3606763) · [`joonspk-research/generative_agents`](https://github.com/joonspk-research/generative_agents) (~12K ⭐, MIT) — 25 LLM agents living in a virtual town with memory, reflection, planning |
| **AI Town** | a16z infra | 2024 | [`a16z-infra/ai-town`](https://github.com/a16z-infra/ai-town) (~8K ⭐, MIT) — browser-based real-time gen-agent town built on Convex |
| **Concordia** | Google DeepMind / Cooperative AI Foundation | 2023–24 | [`google-deepmind/concordia`](https://github.com/google-deepmind/concordia) (Apache-2.0) — game-master-mediated social simulation; supports negotiation, reciprocity, promise-keeping; 2024 contest with $10K prizes |
| **Habermas Machine** | DeepMind | 2024 | [Science paper](https://www.science.org/doi/10.1126/science.adq2852) — AI-mediated *deliberation*: iteratively synthesises group statements that maximise approval while preserving minority perspectives; tested on 5,000+ UK participants on Brexit / immigration / minimum wage / climate; outperforms human mediators on clarity + inclusivity. **No public OSS implementation as of writing.** |

### 2.2 Population-aligned persona research

| System | Authors / Org | Year | Reference |
|---|---|---|---|
| **1,052-persona simulation** | Park, Bernstein et al. (Stanford) | 2024 | [arXiv:2411.10109](https://arxiv.org/abs/2411.10109) — interview + survey-grounded LLM personas; agents match human responses with 85 % accuracy on Big Five, GSS items, economic-game behaviour |
| **SYNTHIA** | multi-institutional | 2025 | [arXiv:2507.14922](https://arxiv.org/abs/2507.14922) — 30,000 personas grounded in real BlueSky social-media posts; population-aligned generation with temporal dimensionality + fairness audit |
| **AgentSociety / AgentVerse / ChatDev society modes** | Tsinghua / multi | 2024–25 | various preprints; OSS implementations sparse |

**Akhada's relationship.** Smallville and the 1,052-persona work are the methodological ancestors. Akhada's V0.10 schema (`Persona.biography` with `eras / formative_experiences / cultural_influences / top_5_books / mentors / worldview_shifts`) is a direct extension of Park et al.'s memory-stream pattern, calibrated to the *Indian* demographic context (Census 2011 + NFHS-5 + CSDS-Lokniti + WVS w7) and validated against external authorities (Open Library for books; V1 Wikidata for films / serials / events). SYNTHIA's *temporal-dimensionality + fairness audit* idea informs Akhada's quarterly bias-audit gating (V1 KS-test against CSDS poll baselines). What is novel in Akhada relative to all four:

- **Cross-literacy biographical depth.** Akhada's `top_5_books` field uses a `kind` discriminator that gracefully degrades from books-for-the-literate to TV-serials-and-kirtan-and-radio-programmes-for-the-oral-tradition — a marginal Bihar farmer's entries are the 1987 Ramayan TV serial, JP Narayan's Total Revolution speeches, Sharda Sinha's Bhojpuri lokgeet, AIR Krishi Darshan, and Tulsidas's Ramcharitmanas. Smallville and the 1,052-persona work are largely literate-Western; SYNTHIA is BlueSky-resident.
- **External authority validation.** Akhada validates `top_5_books` against Open Library's API by title + author; failures are reported, not hidden. Spot-check on the V0.10 library: 12 / 22 verified, 10 flagged as "no-match" — manual inspection confirms all 10 are real Indic-language works (Daya Pawar's *Baluta*, Maulana Azad's *Ghubar-e-Khatir*, James Dokhuma's *Thla Hleinga Zan*) that Open Library's coverage misses. V1 wires Wikidata SPARQL for fallback.

---

## 3. Civic deliberation platforms (human-only)

These are the operational reference points: tools that real citizens have actually used to deliberate at scale.

| Platform | Year | Org | Repo | License | What it does | Where it has run |
|---|---|---|---|---|---|---|
| **Pol.is** | 2012– | Computational Democracy Project (Megill et al.) | [`compdemocracy/polis`](https://github.com/compdemocracy/polis) (AGPL-3.0) | Wiki-survey + consensus clustering + divisiveness detection | Taiwan vTaiwan (28 issues, 80 % enacted), UK Cabinet Office, Anthropic CCAI |
| **Decidim** | 2016– | Ajuntament de Barcelona + global community | [`decidim/decidim`](https://github.com/decidim/decidim) (AGPL-3.0, ~3.8K ⭐) | Participatory democracy framework — proposals, debates, voting, budgeting | Barcelona, Helsinki, Mexico City, French National Assembly; 300+ instances in 18 countries |
| **Loomio** | 2012– | Loomio Cooperative (NZ) | [`loomio/loomio`](https://github.com/loomio/loomio) (AGPL-3.0, ~1.2K ⭐) | Group decision-making — threads, proposals, consent / majority / advice models | 15+ year track record; cooperatives + civic groups |
| **Consul Project** | 2015– | Madrid City Council | [`consul/consul`](https://github.com/consul/consul) (AGPL-3.0) | Citizen-engagement platform — proposals, debates, participatory budgeting | Madrid; ~135 instances in 33 countries |

**What they share.** All four are AGPL-3.0 open-source civic platforms, mature, multi-jurisdictional. They are built on the assumption that *real humans* are the deliberating parties; AI is at most an analysis layer atop the human deliberation transcript.

**What they leave out.** None has an AI-mediated deliberation layer that can either (i) synthesise the deliberation transcript at editorial quality or (ii) simulate stakeholder reaction in advance of running the platform. This gap is what Habermas Machine starts to fill on the synthesis side, and what Akhada fills on the simulation side.

---

## 4. AI-mediated civic deliberation — the closest commercial / institutional comparables

| System | Year | Org | Funding / status | Closest to Akhada in… |
|---|---|---|---|---|
| **Pol.is + Anthropic Collective Constitutional AI (CCAI)** | 2023 | Anthropic + Collective Intelligence Project | Anthropic-internal research; published method | use of public-deliberation input as *training data* for a normative system |
| **Habermas Machine** | 2024 | Google DeepMind | Science 2024; no commercial offering | AI-mediated synthesis of group deliberation; minority-preservation by design |
| **Remesh** | 2016– | independent (NY); $35M+ raised | UN (Yemen, Libya), governments, brand research | rapid-round AI-assisted synthesis at scale; pair-voting + agreement mechanisms |
| **Convocation AI** | 2024 | independent | early-stage | civic-tech AI mediation |
| **CivicSignal** | research | Compute Foundation | research-only | meta-analytic layer atop Pol.is |

**Akhada vs Habermas Machine** — the most informative comparison. Habermas Machine takes a *real* group of citizens (e.g. 5,000 UK participants on Brexit) and uses an LLM to draft synthesis statements that maximise approval while preserving minority views; the contribution is in the *aggregation* of human-authored input. Akhada inverts the data direction: the citizens are *simulated* (50-persona Indian library), and the deliberation transcript itself is the artefact, with synthesis as a downstream step. The two tools complement: a programme office wanting to validate a policy idea before convening real citizens runs Akhada first; the same office, after running real citizens, runs Habermas Machine on the transcript to produce the report.

**Akhada vs Remesh.** Remesh requires real human respondents and excels at compressing months of deliberation into two weeks. Akhada requires no human respondents and produces an article in ~80 seconds. They sit at opposite ends of the speed / authority axis: Remesh's output cites real human voices verbatim; Akhada's output cites synthetic personas with full audit-trail provenance. A real-world programme would use Akhada for hypothesis-iteration and Remesh for the final round of empirical validation.

---

## 5. Agent-orchestration frameworks (the substrate Akhada sits on)

These are general-purpose multi-agent frameworks; Akhada uses them as building blocks rather than competing with them.

| Framework | Org | Stars | License | Position relative to Akhada |
|---|---|---|---|---|
| **Microsoft AutoGen / AG2** | Microsoft AI | ~28K | Apache-2.0 | Production-grade general-purpose multi-agent framework. Akhada considered AutoGen for V1 but chose ADK for tighter Gemini integration + Vertex deployment |
| **Google ADK (Agent Development Kit)** | Google | active | Apache-2.0 | V1 target. Native ParallelAgent / SequentialAgent / LoopAgent primitives map cleanly to the Akhada hierarchical-debate topology (plan §6) |
| **CrewAI** | CrewAIInc | ~18K | MIT | Role-based agent collaboration. Akhada's persona model is structurally compatible — each Akhada `Persona` could become a CrewAI Role — but Akhada layers demographic grounding + audit on top |
| **LangGraph** | LangChain | ~9K | MIT | Graph-based stateful agent orchestration. Considered for V1 audit-state; ADK chosen for first-party Gemini support |
| **MetaGPT, ChatDev, CAMEL, AgentVerse, Agno/Phidata** | various | 5K–20K each | Apache-2.0 / MIT | Adjacent frameworks; not direct competitors |

**Implication for Akhada.** Akhada is *vertical* (civic deliberation) on top of a *horizontal* substrate (agent frameworks). The substrate is a commodity: multiple credible options exist. The vertical is the moat.

---

## 6. The Indian context — what is and isn't there

Three distinct gaps separate Akhada from anything currently shipping in India.

### 6.1 No India-grounded synthetic-persona civic-deliberation tool exists

A targeted search across (a) GitHub repos with "india" + "deliberation" / "civic" / "policy" / "personas", (b) MyGov-platform-adjacent OSS, (c) Indian civic-tech orgs (Janaagraha, Civic Tech India, eGov Foundation, SAMAGRA, Ekstep), (d) Indian AI startups (Sarvam, Krutrim, BharatGen) returns **zero direct competitors**. The closest is BharatGen (IIT Bombay + Govt, June 2025) — a multimodal LLM in 22 Indian languages, but a **model**, not a deliberation product. Sarvam ($53.8M raised, 120B-parameter government-tier model) is similarly a foundation-model / API play.

### 6.2 The Indian qualitative-research market is an order of magnitude larger than initially estimated

Research correction: the Market Research Society of India (Jan 2026) reports the Indian qualitative-research industry at **₹29,008 crore (USD 3.5 B), 10.9 % YoY growth**. Earlier internal estimates of ₹1,500–3,000 crore reflected only a slice of the market (the Tier-1 players); the broader spend including bespoke field-research firms (Ipsos India, Kantar India, Sambodhi, Athena Infonomics, Outline India, Dalberg India, McKinsey Health Institute India) is materially larger.

### 6.3 Multilateral programme spend in India is concrete and addressable

| Buyer | Programme scale (2025–26) | Discretionary procurement size |
|---|---|---|
| **World Bank India** | CPF FY26–31: USD 8–10 B / yr financing; 32 active advisory studies (Aug 2025) | USD 200K – $1 M per advisory |
| **BMGF India** | "AI Fellows 2026" 12-month fellowship; health + agriculture focus; estimated annual India spend USD 50–150 M | USD 100K – $500K per RFP |
| **UNDP India** | Country Programme 2023–27 — SDG localisation, U-WIN digital health, eVIN, climate adaptation | USD 150K – $750K per programme |
| **ADB India** | USD 59.5 B committed since 2001; USD 16.5 B active portfolio; USD 10 B urban-transformation initiative announced 2026 | USD 200K+ per advisory |
| **Omidyar Network India** | 119 portfolio companies (Dec 2024); Citizen Innovation Lab (CivicTech / PropTech / LegalTech) with CIIE.CO | USD 200K – $2 M per grant |
| **Tata Trusts** | STRIVE FY25: 450K+ youth, 1,950+ entrepreneurs; estimated ₹200–300 cr / yr programme spend | varies |
| **Ford / Hewlett / Rockefeller / Open Society India** | Public-interest tech pillar; civic-tech grants | USD 100K – $1 M per grant |

This buyer-set is the wedge defended in `BUSINESS-PROPOSAL.md` §4.

### 6.4 Regulatory context (mid-2026)

- **DPDP Act 2023** — Phase I (Data Protection Board, Nov 2025) live; Phase II (Consent Manager registration, Nov 2026); Phase III (full substantive compliance, May 2027). *Implication:* any Aadhaar-anchored persona work (Akhada gov tier) requires DPIA + Consent Manager integration before May 2027.
- **IT Rules 2026 amendment** — defines Synthetically Generated Information (SGI); mandatory visible labelling + metadata provenance on AI-generated content; 3-hour takedown for unlawful synthetic content. *Implication:* every Akhada output ships with `synthetic_persona_simulation` provenance metadata + a visible "AI deliberation simulation" banner.
- **ECI directives (Oct 2025 + Apr 2026)** — election-period synthetic-content rules; 10 % visible-label coverage on AI video. *Implication:* Akhada V0.10's `mode: publication` ECI guard already aligns; expand to a maintained election-calendar lookup table (V0.11).
- **EU AI Act** — Akhada's civic-deliberation use case is likely *high-risk* under Annex III §8; conformity assessment + Annex IV technical doc required for EU sales (V2 work).

---

## 7. Comparison matrix

The single page summary. Tick = present and shipped; partial = present in research but not productised; blank = absent.

| Capability | Smallville | AI Town | Concordia | Habermas Machine | SYNTHIA | Pol.is | Decidim | Remesh | Anthropic CCAI | **Akhada V0.10** |
|---|---|---|---|---|---|---|---|---|---|---|
| Multi-agent LLM debate | partial | partial | ✓ | – | – | – | – | – | – | ✓ |
| Biographically-rich personas | ✓ | partial | partial | – | partial | – | – | – | – | ✓ |
| **Indian** demographic grounding | – | – | – | – | – | – | – | – | – | **✓** |
| Population-aligned distribution | partial | – | – | partial | ✓ | partial (real users) | partial (real users) | partial (real users) | partial (real users) | ✓ |
| Provable-diversity sampling (k-DPP) | – | – | – | – | – | – | – | – | – | **✓** |
| Bradley-Terry quality-weighted synthesis | – | – | – | partial | – | – | – | – | – | **✓** |
| Sourced reasoning (`[unverified]` flags) | – | – | – | partial | – | – | – | partial | partial | ✓ |
| Hash-chained audit trail | – | – | – | – | – | – | partial | – | – | **✓** |
| Editorial-grade output for institutional use | – | – | – | partial | – | – | partial | ✓ | partial | ✓ |
| Multi-tenant + commercial-license-ready | – | – | – | – | – | partial | ✓ | ✓ | – | partial (V0.11) |
| Open-source AGPL-3.0 | ✓ MIT | ✓ MIT | ✓ Apache | – | – | ✓ AGPL | ✓ AGPL | – | partial (research) | ✓ |
| Productionised for civic deliberation in production | – | – | – | – | – | ✓ | ✓ | ✓ | – | (pilot stage) |

**Three columns where Akhada is the only ✓:** Indian demographic grounding, provable-diversity sampling, hash-chained audit trail. These three are the moat.

---

## 8. Defensible gap analysis — Akhada's eight specific positions

Synthesised from the matrix above and from the three research passes underlying this document. Each numbered point is a capability that no surveyed system fully covers and that Akhada V0.10 either ships or has on a near-term roadmap.

1. **India-grounded biographical personas at scale.** No reviewed tool combines Census 2011 + NFHS-5 + CSDS-Lokniti + WVS w7 with LLM-generated biography depth. Akhada V0.10 ships 50; V1 plans 500; V2 plans 50,000 (district-anchored). Persona-attribution accuracy benchmark — Stanford 1,052-persona work hit 85 %; Akhada's quarterly KS-test against CSDS baselines (V1) is the equivalent representativeness gate.
2. **Provable-diversity persona sampling.** k-DPP (Kulesza-Taskar 2012 exact spectral algorithm) is implemented in V0.10 (`akhada/persona_registry/sampler.py`) with the negative-association property formalised in `README.md` §6 — zero reviewed comparable surfaces this guarantee.
3. **Hash-chained audit trail by default.** Pol.is, Decidim, Loomio, Consul, Remesh, Anthropic CCAI — none ship cryptographic per-event audit. Akhada V0.10 ships SQLite-backed SHA-256 chain with an executable tamper-detection test. V1 commits a daily Merkle root to a GCS WORM bucket with retention-lock.
4. **Bradley-Terry quality-weighted synthesis with sourced reasoning.** The conclusive remark is instructed to cite the strongest *argument*, not the most popular *side*; V1 calibrates weights via MLE on a held-out 50-debate × 3-rater set. The §7 article structure mandates `[unverified]` flags in the Evidence Map section. Verified in production V0.10: in the May 2026 MSP debate, the synthesis backed a single retired-IAS persona's institutional critique over a four-persona moral-imperative cluster.
5. **Deliberation as evidence-grounded reasoning, not opinion aggregation.** Pol.is, Decidim, vTaiwan are *voting / consensus* tools. Habermas Machine, Remesh, Anthropic CCAI are *aggregation* tools. Akhada is a *reasoning + evidence* tool — personas justify positions; synthesis cites them.
6. **Multi-literate persona depth.** The `top_5_books` field's `kind` discriminator handles oral-tradition personas (TV serials, kirtan, kavi sammelan, AIR programmes, sermon series, mass speeches) with the same first-class status as books. No reviewed tool acknowledges literacy stratification at the persona level.
7. **Auditable methodology citable in a peer-reviewed paper.** v0.10.0 is a tagged GitHub release with a published `LICENSE`, `NOTICE`, `BUSINESS-PROPOSAL.md`, and this `RELATED-WORK.md`. The boilerplate citation is *"Akhada Open Debate Engine, v0.10.0 (May 2026). SARGVISION Intelligence. https://github.com/sargupta/akhada-engine/releases/tag/v0.10.0"*. Of the surveyed comparables, only Smallville and Decidim provide an equivalent.
8. **Multilateral / foundation pricing parity.** Pol.is, vTaiwan, Decidim, Loomio are free OSS but require self-hosting and lack delivery / SLAs that a programme officer can sign against. Remesh's enterprise pricing is opaque. Akhada's `BUSINESS-PROPOSAL.md` §7 ships transparent tier pricing (Free / Pro ₹3L / yr / Multilateral ₹40L / yr / Government ₹1 cr+ / Enterprise API metered).

---

## 9. Concrete learnings for the V0.11 → V1 roadmap

Each numbered learning is traceable to a specific finding in §1–§6 and is reflected in the updated `README.md` §14.

| # | Learning | Source | V0.11 / V1 action |
|---|---|---|---|
| 1 | Habermas Machine demonstrates that AI-mediated synthesis with explicit minority-preservation is institutionally credible (Science 2024). | §4 | Akhada V1 conformity guard (`dissent_appendix`) ships with a *Minority-Voice Fraction* metric in every audit JSON — target ≥ 30 % across 100-debate window |
| 2 | Stanford 1,052-persona work proves 85 %-accuracy persona attribution from biographical depth. | §2.2 | Akhada V1 publishes a persona-attribution benchmark on `AkhadaBench` v1 — blind classifier predicts persona from transcript at ≥ 70 % (V1) → ≥ 80 % (V2) |
| 3 | SYNTHIA's fairness-audit-across-demographics is the right shape for a *live* representativeness check. | §2.2 | V1 ships quarterly KS-test bias audit against CSDS poll baselines — published per persona-library version |
| 4 | M3MAD-Bench (2026) standardises multi-agent debate evaluation. | §1.1 | V1 publishes `AkhadaBench` v1 with M3MAD-compatible metrics (accuracy, cost, conformity) on a 20-topic India-policy gold set |
| 5 | Open Library has weak Indic-language coverage (V0.9 validation: 10 / 22 Indian books not matched, all confirmed real). | §6.1 | V1 wires Wikidata SPARQL fallback for film / TV / song / historical-event validation; published quarterly book-authenticity report |
| 6 | Pol.is's *divisiveness detection* is a useful primitive for civic deliberation. | §3 | V1.1 adds an analogous `contention_score` column to the `Claim` schema — surfaced in the Studio article view |
| 7 | Anthropic CCAI uses Pol.is to source norms; the inverse direction (synthesise stakeholder reactions to a *proposed* norm) is unoccupied. | §4 | V1 ships an *inverse-CCAI* mode — submit a proposed AI policy, get back simulated Indian-stakeholder reaction across 50 personas |
| 8 | DPDP Phase III deadline May 2027; IT Rules 2026 SGI labelling is in force now. | §6.4 | V0.11 ships DPIA draft + every Akhada output emits `synthetic_persona_simulation` provenance metadata + visible "AI deliberation simulation" banner |
| 9 | ECI 3-hour takedown rule for synthetic content during elections. | §6.4 | V0.11 expands `mode: publication` ECI guard from a single-flag block to a maintained election-calendar lookup table covering all 28 state assemblies + national elections |
| 10 | None of the surveyed civic platforms (Pol.is, Decidim, Loomio, Consul) have an editorial-quality output layer. | §3 | V0.6's institutional-editorial Studio is the right design choice — preserve and extend (V0.12 adds SSE live cluster stream, V1 adds the audit-page methodology export) |

---

## 10. Summary

Akhada sits at the union of three surveyed lines of work — **multi-agent LLM debate** (§1), **generative-agent persona simulation** (§2), and **AI-mediated civic deliberation** (§4) — and adds three capabilities that none of them currently combines: **Indian demographic grounding** (§6.1), **provable-diversity persona sampling** (§7), and **hash-chained audit trail** (§7). The closest single comparable is DeepMind's Habermas Machine (Science 2024) on the synthesis side, and Anthropic × Pol.is CCAI on the civic-tech side; both are research projects without commercial deployment in India, and neither addresses the demographic-grounding or audit gaps. The case for Akhada — open-core AGPL-3.0 with a commercial license — is therefore that it occupies a defensible intersection that neither a horizontal agent framework (AutoGen, ADK, CrewAI), a Western civic-tech platform (Pol.is, Decidim), nor a research artefact (Habermas, Smallville, SYNTHIA) can reach without years of additional investment.

The eight defensible-gap items in §8 are the version of this case that survives a literature-aware reviewer.

---

## References

### Academic

1. Du, Y., Li, S., Tenenbaum, J., Mordatch, I. *Improving Factuality and Reasoning in Language Models through Multiagent Debate.* ICML 2024. [arXiv:2305.14325](https://arxiv.org/abs/2305.14325)
2. Park, J. S., O'Brien, J., Cai, C. J., Morris, M. R., Liang, P., Bernstein, M. S. *Generative Agents: Interactive Simulacra of Human Behavior.* UIST 2023. [DOI:10.1145/3586183.3606763](https://dl.acm.org/doi/10.1145/3586183.3606763)
3. Park et al. *Generative Agent Simulations of 1,000 People.* 2024. [arXiv:2411.10109](https://arxiv.org/abs/2411.10109)
4. SYNTHIA: *30,000-persona BlueSky-grounded simulation.* 2025. [arXiv:2507.14922](https://arxiv.org/abs/2507.14922)
5. M3MAD-Bench: *Multi-domain, multi-modal, multi-dimensional benchmark for multi-agent debate.* 2026. [arXiv:2601.02854](https://arxiv.org/pdf/2601.02854)
6. *Habermas Machine.* DeepMind, Science 2024. [DOI:10.1126/science.adq2852](https://www.science.org/doi/10.1126/science.adq2852)
7. Anthropic. *Collective Constitutional AI: Aligning a Language Model with Public Input.* 2023. [link](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input)
8. Kulesza, A., Taskar, B. *Determinantal Point Processes for Machine Learning.* Foundations and Trends in Machine Learning 2012. (k-DPP exact sampling foundation)
9. Bradley, R. A., Terry, M. E. *Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons.* Biometrika 1952. (BT model foundation)

### Open-source projects (selected)

10. `joonspk-research/generative_agents` — Park et al. 2023 reference implementation
11. `a16z-infra/ai-town` — browser-based gen-agent simulation
12. `google-deepmind/concordia` — DeepMind social simulation framework
13. `compdemocracy/polis` — Pol.is civic-tech wiki-survey platform
14. `decidim/decidim` — Barcelona-led participatory democracy framework
15. `loomio/loomio` — cooperative deliberation platform
16. `ag2ai/ag2` — Microsoft AutoGen / AG2
17. `crewAIInc/crewAI` — role-based agent collaboration
18. `langchain-ai/langgraph` — graph-based agent orchestration
19. `google/adk-python` — Google Agent Development Kit
20. `OpenBMB/ChatDev`, `FoundationAgents/MetaGPT`, `camel-ai/camel`, `agno-agi/agno` — adjacent agent frameworks

### Commercial / institutional

21. Pol.is in Taiwan — [vTaiwan case study](https://www.peoplepowered.org/news-content/digital-participation-case-study-taiwan)
22. Remesh — [Knight Columbia coverage of UN deployments](https://knightcolumbia.org/content/can-ai-mediation-improve-democratic-deliberation)
23. Anthropic CCAI — [Anthropic research blog](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input)
24. World Bank India CPF FY26–31 — [press release Jan 2026](https://www.worldbank.org/en/news/press-release/2026/01/30/india-country-partnership-framework-cpf-fy26-31)
25. India IT Rules 2026 (SGI definition) — [Outlook coverage](https://www.outlookbusiness.com/news/it-rules-amendment-2026-3-hour-takedown-rule-synthetic-content-defined-new-compliance-norms)
26. ECI Apr 2026 directive on AI in elections — [MediaNama coverage](https://www.medianama.com/2026/04/223-eci-orders-3-hour-takedown-rule-ai-fake-content-elections/)

### Indian context

27. Census of India 2011 — [censusindia.gov.in](https://censusindia.gov.in/)
28. Lokniti-CSDS National Election Studies — [lokniti.org](https://www.lokniti.org/state-election-studies)
29. AI4Bharat IndicVoices, IndicAlign, IndicCorp — [ai4bharat.iitm.ac.in](https://ai4bharat.iitm.ac.in/)
30. PRS Legislative Research — [prsindia.org](https://prsindia.org/)
31. Sarvam AI — sovereign LLM for India — [sarvam.ai](https://www.sarvam.ai/)
32. BharatGen (IIT Bombay + GoI) — multimodal LLM in 22 Indian languages — [PIB Jun 2025](https://www.pib.gov.in/PressNoteDetails.aspx?id=156786)
33. Market Research Society of India — Indian qualitative-research market sizing — [Jan 2026](https://startupnews.fyi/2026/01/05/indian-research-and-insights-industry/)

---

*This document is the academic-style related-work survey for Akhada. Its claims are calibrated against the V0.10 release; any later release should add an erratum + updated comparison rows rather than retroactively edit. Suggestions, corrections, and additions are welcome via repository issues.*
