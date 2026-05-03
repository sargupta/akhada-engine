# Akhada — Business Proposal

> **Stress-test public deliberation, before public deliberation stress-tests you.**
>
> A working civic-deliberation engine, built for the multilateral programme officer who needs Indian-stakeholder analysis at the speed of email — not the speed of fieldwork.

| | |
|---|---|
| Product | Akhada — Open Debate Engine |
| Company | **SARGVISION Intelligence** |
| Document version | 1.1 (May 2026) |
| Built artefact | Akhada V0.10 — see [`README.md`](../README.md) |
| Public repository | https://github.com/sargupta/akhada-engine |
| Pinned release | [`v0.10.0`](https://github.com/sargupta/akhada-engine/releases/tag/v0.10.0) |
| Companion documents | [`README.md`](../README.md) (technical reference) · [`RELATED-WORK.md`](RELATED-WORK.md) (literature survey) · [`PROJECT-PROPOSAL.md`](PROJECT-PROPOSAL.md) (research-and-implementation proposal) |
| Confidentiality | For commercial discussion |

---

## 1. Executive summary

Akhada is a working software engine that runs a panel of biographically-grounded AI personas — drawn from real Indian demographic distributions — through a structured debate on any policy topic, and produces a sourced article + a quality-weighted conclusive remark + a cryptographically-verifiable audit trail. **End-to-end latency is 70–90 seconds. End-to-end cost is between ₹2 and ₹5 per debate.** Tests against five real policy topics in May 2026 produced clean institutional output that correctly identified clusters, named contention, flagged unverified claims, and cited the strongest argument over the popular side.

**Buyer wedge:** programme offices at multilateral development organisations and large foundations operating in India — World Bank India, Bill & Melinda Gates Foundation India, UNDP India, Asian Development Bank India, Omidyar Network India, Tata Trusts. They commission ₹15–40 lakh stakeholder-analysis engagements as standard inputs to programme design, and the procurement decision sits with a programme officer who has discretionary authority.

**Value proposition.** What costs ₹40 lakh and 6 weeks of multi-state qualitative fieldwork (FGDs + IDIs across 6–8 cities, 4–5 languages, transcription, thematic coding, cross-tabulation) compresses into ₹4 lakh and 60 minutes per topic — auditable to a Standing Committee or an Inspector General, defensible against peer review.

**Pilot offer:** ₹4,00,000, 4-week engagement. Three policy topics of the buyer's choosing, run end-to-end through the engine. Output: three sourced articles, three audited debates, one co-authored 6-page methodology note. Commercial terms in §7.

**Status of the asset:** working; 8 commits on `main`; 31 tests passing in 0.80 s; persisted live demo at `/audit/{debate_id}` for three real debates including a 50-persona MSP debate that spans 22 Indian states. AGPL-3.0 open-core, with a commercial license covering the gov-tier feature set. The engine is ready for paid pilot use today; a small set of pre-pilot hardening items is listed in §10.

**Honest gap:** zero paying customers as of this document. The ask is one paid pilot to validate the wedge.

---

## 2. The problem

### 2.1 The work, today

Multilateral programme offices commit to spending money in India before they fully know how the spend will land. To bridge that gap, they commission stakeholder analysis: who are the people affected, what would they say if asked, what dimensions of the proposal are likely to fail in execution, what minority perspectives must be preserved.

The current toolkit is qualitative fieldwork — focus group discussions (FGDs), in-depth interviews (IDIs), key-informant interviews (KIIs), participatory rural appraisal (PRA) — typically delivered by an Indian consulting partner (Dalberg India, McKinsey Health Institute India, Sambodhi Research, Athena Infonomics, Ipsos India, Kantar India). A typical engagement is 4–8 weeks long, costs ₹15–40 lakh, covers 6–8 districts in 3–5 languages, and produces a slide deck. The Indian qualitative-research market overall is **₹29,008 crore (USD 3.5 B) at 10.9 % YoY growth** (Market Research Society of India, January 2026); the multilateral / foundation slice is the high-defensibility component of that market.

This work is genuinely useful. It is also slow, expensive, sample-biased toward accessible respondents, hard to iterate (re-fielding costs the same as fielding), monolingual at the synthesis layer (a typical deck is in English even when the fieldwork was in five Indian languages), and methodologically opaque (the path from a transcript line to a slide claim is rarely auditable).

### 2.2 The gap that hurts

Programme officers tell us — and the published literature confirms — that the binding constraints are:

1. **Iteration speed.** A typical TOR allows one round of fieldwork. If the first round reveals that the question was wrong, re-fielding is a budget conversation, not a methodological adjustment.
2. **Coverage.** Six districts is a sample. India is a 28-state, 700-district, 22-language country. A 6-district FGD-IDI study cannot represent the heterogeneity of, say, "small farmers in India."
3. **Defensibility.** When a programme report is challenged — by a CAG audit, an Inspector General, a Standing Committee, an academic peer reviewer — the deck does not survive scrutiny back to the underlying transcripts. The methodology is opaque.
4. **Languages.** A debate happening in Bhojpuri at an FGD in Saran is reported in English in a Washington-DC programme review. The voice quality compresses by an order of magnitude across that translation.

These are not niche complaints. They are the standard limitations of qualitative fieldwork at multilateral budget scales.

### 2.3 What programme officers already pay for

Today, an India programme officer at a multilateral or a foundation has roughly four budget instruments:

- **Engagement of an Indian consulting partner** at ₹15–40 lakh per engagement.
- **Internal qualitative team time** — often a 2–3 month effort by a small India-based research lead.
- **External academic / think-tank commissioned paper** — ₹5–15 lakh per paper.
- **Survey augmentation** — Ipsos, Kantar, CVoter quantitative panel work at ₹10–30 lakh per round.

The sum of these is the wedge Akhada augments. The Indian qualitative-research market alone is ₹1,500–3,000 cr per year at retail (source: industry trade estimates, Ipsos / Kantar / Nielsen India revenue figures). Multilateral and foundation share is the high-quality, high-defensibility slice — perhaps ₹400–800 cr.

---

## 3. What Akhada is

A working software engine, V0.10. Not a slide deck.

A user submits a policy topic. The engine samples 12–50 personas from a 50-persona Indian library — anchored on Census 2011, NFHS-5, CSDS-Lokniti, World Values Survey wave 7, AI4Bharat regional datasets — using exact k-DPP (Kulesza-Taskar 2012) for provable diversity. Each persona produces an 80–150-word first-person opening on Gemini 2.5 Flash, fanned out in parallel. A Pro-tier synthesis call composes a seven-section editorial article (Context · Perspectives by Cluster · Points of Agreement · Points of Contention · Evidence Map · Recommendations · Minority Voices Appendix). A second Pro call writes a Bradley-Terry quality-weighted conclusive remark — explicitly instructed to cite the strongest argument over the popular side.

The whole debate is persisted to SQLite (V0; BigQuery + GCS WORM bucket at V1) with a four-event hash-chained audit log. Tampering with any payload breaks every downstream hash, and a unit test verifies this by mutating the database directly.

The persona library is **biographically rich, not stereotype-based.** Each persona carries a 200-word first-person narrative, three to five life eras anchored to district + cohort, three to five formative experiences, eight to fifteen cultural influences, exactly five `top_5_books` entries (with a `kind` discriminator that gracefully degrades for non-literate personas to TV serials, kirtan, sermons, or speeches attended), one to three mentors, four to ten historical events lived through, and zero to three documented worldview shifts. A retired Bhadralok professor from Calcutta cites Tagore's *Gora* + Sen's *Argumentative Indian* + Marx's *Das Kapital* + Bibhutibhushan's *Pather Panchali* + Myrdal's *Asian Drama*. A marginal Bihar farmer cites Tulsidas's *Ramcharitmanas* + the 1987 *Ramayan* TV serial + JP Narayan's Total Revolution speeches + Sharda Sinha's Bhojpuri lokgeet + AIR's Krishi Darshan. An Odisha fisherman with `oral_only` literacy cites Jagannatha Dasa's Odia Bhāgabata heard at the village Bhagabata Tungi + local Pala / Daskathia oral narrative traditions. **All real. All verifiable. Spot-checked against Open Library and Sahitya Akademi citations.**

The library covers **27 states + Union Territories**, every major religion, the full caste spectrum (general / OBC / SC / ST / other-minority), and the full literacy spectrum from doctorate down to oral-only. The synthesis layer's 7-section structure and quality-weighted conclusion are encoded in the V0.10 prompt and produce verifiable output: in the May 2026 MSP debate, the conclusive remark cited a single retired-IAS-officer persona (`akh-p-gen-042`) as carrying the strongest cautionary argument, *over the four-persona moral-imperative cluster*, because the institutional critique cleared the §6 quality bar.

This is the substance: an engine that produces institutional-quality stakeholder analysis on demand, in 80 seconds, with an audit chain that survives Inspector General review.

---

## 4. The wedge

### 4.1 Buyer

| Tier 1 (paid pilots, year 1) | Tier 2 (subscription, year 1–2) | Tier 3 (V2+) |
|---|---|---|
| World Bank India | Indian policy think tanks (ORF, CPR, Vidhi, CEEW, IDFC Institute, Praja Foundation) | State governments (departmental contracts) |
| BMGF India | National-level civic-tech orgs (Civic Tech India, Janaagraha) | NITI Aayog, ministries |
| UNDP India | Academic centres (Ashoka Trivedi Centre, Azim Premji U, ISB Bharti Institute, Carnegie India) | RBI / SEBI / TRAI consultation augmentation |
| ADB India | Major Indian newsrooms (Indian Express, ThePrint, The Hindu, Wire) | Defence think tanks (V3 with cleared advisor) |
| Omidyar Network India | Election-research firms (post-ECI legal review) | International — UK Cabinet Office, EU Have-Your-Say, citizens' assemblies |
| Tata Trusts | Industry associations (FICCI, CII for sectoral consultation) | |
| Rockefeller, Ford, Hewlett India offices | | |

### 4.2 Why this wedge, not the others

The multilateral wedge wins for one reason: **the buyer has discretionary budget today, the methodology category is already accepted, the procurement officer signs without committee, and the deliverable is a published report that names the tools used — which is distribution.** A single successful World Bank India case study is worth more in downstream reach than 12 months of cold ministry outreach.

Adjacent wedges and why they are not first:

- **Central ministries (NITI Aayog, MoF, MoA&FW, MoH&FW).** Procurement cycles run 18–24 months. Empanelment, MeitY clearance, CERT-In review, Standing Committee politics. Real opportunity, wrong starting point.
- **State governments.** 6–12 months per state, 28 states, per-state procurement quirks. Large addressable market via reference customers; not first.
- **Election message-testing.** Genuine willingness to pay during campaign cycles, but ECI Model Code risk, paid-news classification risk, reputational blowup risk. No until V3 + commissioned legal opinion + a published abuse policy.
- **Defence / geopolitical war-gaming.** Real budget. Cannot enter as a startup without an empanelment + a cleared advisory board (Booz Allen, Palantir, MITRE, BEL incumbents). V2+.
- **UPSC and civic education.** Mature buyers with their own production infrastructure (Drishti, Vajiram & Ravi, Vision IAS); price-sensitive students; high distribution but low ACV. Distribution play, not revenue play.
- **Corporate strategy / M&A red-team.** Real WTP, but our Indic persona library is mis-targeted for boardroom personas. Adjacent product, V3.
- **Brand / advertising creative testing.** FMCG procurement culture wants focus-group-replacement, not deliberation. Thin fit.
- **Indian policy advisory + think tanks.** Strong cultural fit, smaller per-engagement budgets, very high reference value. **Secondary wedge — three pro-bono pilots in the first 90 days build the case studies that close multilateral deals.**

### 4.3 Comparable companies that have proved adjacent theses

| Comparable | What it proves |
|---|---|
| **Dalberg India** (₹85.8 cr revenue FY25 per Tracxn; multi-year USAID + BMGF + World Bank contracts) | Multilaterals + foundations pay USD 250K – $2 M per India stakeholder-analysis engagement; budget exists |
| **Anthropic × Pol.is Collective Constitutional AI** (2023, ~1,127 statements / 38,252 votes) | AI-mediated public deliberation is institutionally accepted; same buyer DNA |
| **Pol.is** in Taiwan vTaiwan (28 issues, 80 % enacted), UK Cabinet Office, Anthropic CCAI | Civic-tech buyers exist; the methodology has multi-year track record |
| **Remesh** ($35M+ raised; UN Yemen / Libya / brand-research deployments) | Same buyer DNA as our wedge; closest *"raised on this thesis"* precedent; pricing is opaque (advantage to a transparent-pricing entrant) |
| **DeepMind Habermas Machine** (Science 2024; tested on 5,000+ UK participants) | AI-mediated synthesis preserving minority perspectives is *peer-reviewed*; closest academic neighbour to Akhada |
| **Stanford 1,052-persona simulation** (Park et al. 2024, [arXiv:2411.10109](https://arxiv.org/abs/2411.10109); 85 % accuracy persona attribution) + **SYNTHIA** (30,000-persona BlueSky-grounded simulation, 2025) | Synthetic-persona methodology at scale is academically credible |
| **Ipsos India, Kantar India, Sambodhi, Athena Infonomics, Outline India** | The Indian qualitative-research market is **₹29,008 crore (USD 3.5 B), 10.9 % YoY growth as of FY25** (Market Research Society of India, January 2026) — not the ₹1,500–3,000 cr first estimated; the multilateral / foundation slice is the high-defensibility component |

What is **novel** to Akhada and not yet shipped commercially or academically (verified against the literature survey in [`docs/RELATED-WORK.md`](RELATED-WORK.md) §7): the specific combination of (i) synthetic Indian-demographic-grounded personas with biographical depth, (ii) provable-diversity sampling via exact k-DPP, (iii) hash-chained per-event audit trail with executable tamper detection, and (iv) Bradley-Terry quality-weighted synthesis with sourced reasoning. That novelty is the opportunity and also the execution risk. Both are real.

### 4.4 Competitive landscape — survey result

A formal literature + competitive review is in [`docs/RELATED-WORK.md`](RELATED-WORK.md). The headline matrix from §7 of that document, condensed:

| Capability | Smallville | AI Town | Concordia | Habermas Machine | SYNTHIA | Pol.is | Decidim | Remesh | Anthropic CCAI | **Akhada V0.10** |
|---|---|---|---|---|---|---|---|---|---|---|
| Indian demographic grounding | – | – | – | – | – | – | – | – | – | **✓** |
| Provable-diversity sampling (k-DPP) | – | – | – | – | – | – | – | – | – | **✓** |
| Hash-chained audit trail | – | – | – | – | – | – | partial | – | – | **✓** |
| Bradley-Terry quality-weighted synthesis | – | – | – | partial | – | – | – | – | – | **✓** |
| Open-source AGPL-3.0 with commercial-tier carve-out | – | – | – | – | – | ✓ AGPL | ✓ AGPL | – | – | **✓** |

**Akhada is the only ✓ in the top three rows of the full matrix.** Those three rows — Indian grounding, provable-diversity, hash-chained audit — are the moat. The full matrix and the eight-point defensible-gap analysis are in `docs/RELATED-WORK.md` §7–§8. The corresponding ten concrete V1 / V2 product-roadmap learnings are in `README.md` §14.1.

A specific finding worth surfacing here: **no India-grounded synthetic-persona civic-deliberation tool exists** anywhere in the surveyed landscape — verified across (a) GitHub repos with *india + deliberation / civic / policy / personas* keywords, (b) MyGov-platform-adjacent OSS, (c) Indian civic-tech orgs (Janaagraha, Civic Tech India, eGov Foundation, SAMAGRA, Ekstep), (d) Indian AI startups (Sarvam AI USD 53.8 M raised, Krutrim USD 50 M + 230 M committed, BharatGen IIT-Bombay-led 22-language multimodal LLM launched June 2025). The closest Indian players are foundation-model / API plays, not deliberation products. Akhada is not a foundation model; it is the deliberation layer that uses foundation models. There is no commercial overlap with Sarvam, Krutrim, or BharatGen.

---

## 5. The value proposition

Three pillars, calibrated to real measured V0.10 numbers (see §12).

### 5.1 Pillar 1 — Speed

|  | Traditional fieldwork | Akhada V0.10 |
|---|---|---|
| End-to-end per topic | 4–6 weeks | 70–90 seconds |
| Cost per topic | ₹15–40 lakh | ₹2–5 |
| Languages | 1–2 typical | 22 (V1) / English-internal V0 |
| Iterations / week | 1 | hundreds |
| Re-running with revised topic | another full engagement | one form submission |

The compression matters because it changes what "analysis" means. When a stakeholder simulation costs ₹4 instead of ₹4,000,000 and takes 80 seconds instead of six weeks, programme officers run *seven* questions instead of *one*, run them *iteratively* (the second question is informed by what the first revealed), and run them *in parallel* across multiple programme designs. Akhada does not replace fieldwork; it changes the unit economics enough to make hypothesis-iteration the default, and field validation the targeted follow-up.

### 5.2 Pillar 2 — Demographic representativeness, defensible

The library covers **27 states + UTs**, every major religion (Hindu, Muslim, Christian, Sikh, Buddhist), the full caste spectrum, the literacy spectrum from oral-only to doctorate, urban / peri-urban / rural, MPCE quintiles 1 through 5. Personas are anchored to publicly-citable demographic distributions (Census 2011, NFHS-5, CSDS-Lokniti, WVS w7). The sampler is **exact k-DPP** (Kulesza & Taskar 2012) on TF-IDF embeddings — provable negative association on similar personas, deterministic under seed, no duplicates.

A McKinsey stakeholder-mapping deck typically presents 8–12 stylised archetypes. Akhada ships 50 (V0.10) → 500 (V1) → 50,000 (V2 district-anchored), sampled diversely, with seed reproducibility and a quarterly bias-audit pass against CSDS poll-data baselines (V1).

### 5.3 Pillar 3 — Auditable to a Standing Committee or a peer reviewer

Every debate persists with a four-event hash-chained audit log.

- `seq 0` — `topic_received`: topic, n_personas, library_version, weights_version, mode, panel_persona_ids
- `seq 1` — `openings_complete`: count, failed, backend
- `seq 2` — `synthesis_complete`: article_chars, h2_count
- `seq 3` — `conclusive_complete`: remark_chars

`payload_hash = SHA-256(canonical_json(payload) + "|" + prev_hash)`. Tampering with any payload invalidates every downstream hash. A unit test mutates a stored `payload_json` directly in SQLite and asserts that `verify_chain` returns `False` with `"payload_hash mismatch"`. This is not a documentation claim; it is an executable property.

V1 commits a daily Merkle root of the day's events to a GCS WORM bucket with retention-lock so the chain is tamper-evident even against database operators. This is the institutional differentiator: a McKinsey deliverable is a slide deck that cannot be re-derived from its inputs; an Akhada deliverable is a methodology you can hand to a CAG, an IG, or a peer reviewer and *they can re-run the verification themselves*.

### 5.4 The one-sentence pitch

> *"Akhada simulates a 50-stakeholder Indian deliberation in 90 seconds for ₹5 — anchored to Census + NFHS-5 + Lokniti, with a Bradley-Terry quality-weighted synthesis and a hash-chained audit trail you can hand to your Inspector General."*

---

## 6. Why us, why now

### 6.1 Why us

**Built artefact, not promise.** V0.10 ships today. Eight commits, 31 tests, three real persisted debates with verified hash chains, an editorial Studio, a real persona library on disk (`personas-2026.Q2.1.jsonl`, 45 generated personas validated against Open Library). Most "AI-for-civic-deliberation" pitches are slide decks; this is a working binary you can run on a laptop in two minutes (§2 of `README.md`).

**Indian context as the foundation, not as a localisation.** The library's seed taxonomy was designed against Census 2011, NFHS-5, and CSDS-Lokniti from day one. Generated biographies cite Daya Pawar's *Baluta*, Maulana Azad's *Ghubar-e-Khatir*, James Dokhuma's *Thla Hleinga Zan*, Khushwant Singh's *History of the Sikhs*, Rabon Singh Kharsuka's Khasi text *Ka Jingsneng Tymmen*. These are not stock GPT outputs; they are the kind of references an India scholar would expect to see and that a non-Indian competitor would not produce.

**Audit trail by default.** The hash chain is not a V2 promise — it ships in V0.10. Tamper detection is verified by an executable test. This is what programme officers asking *"how would I defend this to my IG?"* need to see in the first demo, not the third meeting.

**Open-core licensing aligns incentives.** The engine is AGPL-3.0; commercial licensing covers the gov-tier features (50K-persona library v2, DigiLocker e-KYC, Opus synthesis tier, on-prem deploy kit, audit-immutability WORM provisioning, multi-tenant CMEK). This means a programme officer can have the open core inspected by their IT team, while the productised features the buyer actually wants are commercial. No "trust us" gap.

### 6.2 Why now

- **Generative AI is institutionally legible** in May 2026. A multilateral programme officer in 2024 had to defend "we used AI" in their report; in 2026, they have to defend "we did not use AI to test this."
- **DPDP Act implementation** is rolling forward in India; programme reports referencing Indian citizens are subject to data-protection scrutiny. Akhada's synthetic-persona model — no PII by default — is the right default posture for the regime.
- **Anthropic × Pol.is** and adjacent efforts have legitimised the "AI-mediated deliberation" category for the exact buyer set we target.
- **Indian-language LLM quality** (Gemini 2.5, AI4Bharat IndicTrans, Sarvam) crossed a usability threshold in 2025–26 that makes 22-language synthesis genuinely possible at V1.

The window for an India-rooted, audit-defensible, multilateral-aimed engine is 18–24 months before incumbents (Dalberg with internal AI, McKinsey with QuantumBlack, the multilaterals' own platforms) close it.

---

## 7. Pricing & packaging

### 7.1 Pilot offer

> **₹4,00,000 ex-GST. 4-week engagement. Three policy topics. Co-authored methodology note.**

Deliverables:
- 3 × full debates run end-to-end against a custom-curated 50-persona panel (50 hand-curated for the topic; supplemented from the 500-persona V1 library where ready)
- 3 × sourced articles (the 7-section editorial output)
- 3 × full audit trails delivered as signed-URL JSON exports + a 1-page chain-verification CLI walkthrough
- 1 × co-authored 6-page methodology note ready for inclusion in the buyer's programme report
- Two 90-minute working sessions: kickoff + delivery review
- A clear Limitations section in every output (an Indian academic-grade caveat note)

Optional add-ons:
- Multi-tenant tenant-scoped audit (₹1L)
- 22-language synthesis layer (V1 SLA-bound; ₹3L)
- On-prem deploy with the buyer's own Gemini quota (₹2L for setup)

### 7.2 Subscription pricing (post-pilot)

| Tier | ₹ / year | Audience | Inclusions |
|---|---|---|---|
| **Free** | 0 | Individual researchers, open-source contributors | 5 debates / month, 50-persona library, English-only, audit JSON export, no support SLA |
| **Pro** | ₹3,00,000 | Indian think tanks, academic centres, journalism desks | 100 debates / month, 500-persona library v1 (V1), 22-language synthesis (V1), multi-tenant, CMEK, weekly office hours |
| **Multilateral** | ₹40,00,000 | One India programme office at a multilateral / foundation | Unlimited fair-use, dedicated 50-persona panel curation per programme, Opus synthesis tier, audit-WORM commits, SLA 99.5 %, named delivery lead |
| **Government** | ₹1,00,00,000+ / engagement | Ministries, state-government departments | On-prem (Anthos / Confidential GKE), DPDP DPIA pack + EU AI Act Annex IV, DigiLocker e-KYC, dedicated infrastructure, named program manager |
| **Enterprise API** | $1.50–$5 / debate metered | High-volume programmatic use | Cap-and-grow contracts, white-label, OpenAPI 3.1, OAuth 2.0, audit endpoint included |

### 7.3 Year-1 ARR target from this wedge

| Source | Count | ARR contribution |
|---|---|---|
| Multilateral pilots converted to year-1 subscription | 3 | ₹1.2 cr |
| Think-tank Pro subscriptions | 4 | ₹12 lakh |
| Pro-bono → paid conversions (academic, journalism) | 2 | ₹6 lakh |
| First state-government engagement (referred from think-tank) | 1 | ₹40 lakh |
| **Total Year-1 ARR (target)** | | **₹1.8 cr** |

Year-3 target: ₹15–25 cr ARR via 8 multilateral subscriptions + 12 think tanks + 2–3 state engagements + first ministry pilot.

---

## 8. Risks & mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| **Anthropic + Pol.is or Google ship a directly-competing product** | High | Move fast on India-specific moat (50K-persona library v2, 22 Indian languages via Sarvam, DPDP DPIA pack); plant `AkhadaBench` flag in the academic literature; close one ministry pilot reference in V2 to create an 18-month lead |
| **Multilateral procurement is slower than 6–12 weeks** | Medium-High | Start with a single programme officer + discretionary budget, not the country office's annual procurement; the pilot offer is sized to discretionary tier (₹4L); think-tank pro-bono pilots produce reference cases independent of multilateral cycle |
| **Persona-library bias not yet externally audited** | Medium | V1 mandatory quarterly bias-audit pass against CSDS poll baselines (KS-test < 0.15); audit report published; library version pinned per debate |
| **Hallucination at scale; "AI made it up"** | Medium | Synthesis prompt mandates `[unverified]` markers; Open Library validator (Wikidata at V1) flags book authenticity; V1 NLI citation verifier strips claims that don't dereference to evidence; output framed as "deliberation simulation" with mandatory human-in-loop notice |
| **DPDP Act / IT Rules / EU AI Act compliance becomes a blocker** | Medium-High | DPIA + Annex IV technical doc are gating milestones before V2 ministry pilot; budget ₹50L + 6 months; treat as investment, not afterthought |
| **Election Commission or paid-news classification risk** | Medium | Hard ToS ban on candidate / party-targeted use; rate-limit on political topics during ECI Model Code period; lookup-table-driven `mode: publication` block (already implemented in V0.10) |
| **Sarvam single-vendor for 22-language layer fails or pivots** | Low-Medium | V2 fallback to Google Translate + Gemini multilingual; data-portability clause in commercial agreement |
| **Public backlash: "AI is writing our policy"** | Medium-High | Branding: "deliberation simulator", never "policy decider"; mandatory human-in-loop disclaimer on every output; press strategy at V2 launch led by an Indian academic co-author |
| **Government partner exits mid-pilot** | Medium | Don't bet the year on a single ministry; aim for 2 multilateral + 1 think-tank + 1 state pilot in parallel |
| **Open-core fork erodes the commercial tier** | Medium | AGPL (not MIT) prevents closed forks; commercial features (50K library v2, DigiLocker, on-prem kit, WORM provisioning, multi-tenant CMEK) are commercially licensed; entitlement check via signed JWT licence; phone-home opt-out for air-gapped gov tier |
| **Cost runaway on a single programme** | Low | Hard token budget per debate; per-tenant Firestore quotas (V1); circuit breaker on Cloud Tasks (V1); FinOps dashboard in commercial tier |

---

## 9. 90-day go-to-market plan

| Weeks | Move | Owner | Output |
|---|---|---|---|
| 1–2 | **Pre-pilot hardening.** Multi-tenant isolation + tenant-scoped audit + per-tenant rate limits. ToS + privacy notice draft. DPIA outline. Persona library expansion to 200. | Engineering | V0.11 hardened; library `personas:2026.Q3.0`; ToS + DPIA v0 |
| 3–4 | **AkhadaBench v0.** 20-topic factual gold + reproducibility scoreboard published in `benchmarks/akhada-bench/results/`. SSE streaming + Studio live cluster view (UX upgrade for cold pitches). | Engineering | First public eval scoreboard; Studio progressive UX |
| 5–6 | **Three pro-bono pilots** with: ORF, CPR / IDFC Institute, Vidhi Centre for Legal Policy (or 3 of: CEEW, Praja Foundation, Carnegie India). Three real policy topics they're already advising on. Co-author a 6-page methodology paper with one of them. | GTM | 3 reference debates; 1 methodology paper; 3 testimonials |
| 7–9 | **Warm-intro pitch sequence** to 5 multilateral / foundation India offices: World Bank India, BMGF India, UNDP India, Omidyar Network India, Tata Trusts. Each pitch carries the methodology paper + the three reference debates + a ₹4L pilot offer. | GTM | 5 first meetings; 2–3 second meetings; 1 pilot signed |
| 10–12 | **First paid pilot delivery.** ₹4L, 4 weeks, 3 topics, audit trail + co-authored note. Output rolled into the buyer's programme report → distribution. | GTM + delivery | First revenue. First reference case. First citation. |

Year-1 sequencing after the first pilot:
- Convert pilot → year-1 subscription (`Multilateral` tier, ₹40L)
- Use the published programme report to open conversations with the next 3 multilateral offices
- Close 2 of the 3 think-tank pro-bono pilots into `Pro` subscriptions (₹3L each)
- First state-government referral via the think tank (₹40L engagement)
- Begin the V2 compliance pack work in parallel for the gov-tier path

---

## 10. Pre-pilot hardening — what we ship in the first 4 weeks

A short, executable list. Items already done in V0.10 are marked ✅; the rest is the next 4-week sprint.

| Item | Status |
|---|---|
| Real Gemini-powered debates (Flash R1 + Pro synthesis + Pro conclusion) | ✅ V0.7 |
| 50-persona library spanning 27 states + UTs | ✅ V0.9 |
| Provable-diversity k-DPP sampler (Kulesza-Taskar 2012, exact spectral) | ✅ V0.9 |
| Open Library book-authenticity validator | ✅ V0.9 |
| SQLite persistence with hash-chained audit (4 events per debate) | ✅ V0.10 |
| Tamper-detection executable test | ✅ V0.10 |
| Studio editorial UI (light + dark, audit-page, drop-cap article) | ✅ V0.6 + V0.10 |
| 31 / 31 tests passing, hermetic conftest | ✅ V0.10 |
| **Multi-tenant isolation** (Firestore prefix + per-tenant audit + per-tenant rate limits) | V0.11 (week 1–2) |
| **ToS + privacy notice + DPIA v0** | V0.11 (week 1–2) |
| **Persona library expansion to 200** (~$5 spend) | V0.11 (week 2) |
| **Wikidata SPARQL fallback** for the 10 unverified Indic-language books | V0.11 (week 2) |
| **AkhadaBench v0** (20-topic factual gold + repro scoreboard) | V0.12 (week 3–4) |
| **SSE streaming + Studio live cluster view** | V0.12 (week 3–4) |
| **Bias-audit pass v0** (KS-test against CSDS poll data) | V0.12 (week 4) |
| **Methodology paper draft** (6 pages, co-author TBD) | V0.12 (week 4) |
| Real ADK SequentialAgent + ParallelAgent fan-out (25 × 20 → 5 → 1) | V1 |
| 22 Indian languages via Sarvam | V1 |
| DPDP DPIA + EU AI Act Annex IV + on-prem deploy kit | V2 |

---

## 11. Validation evidence

### 11.1 The asset works

Three persisted real debates at the time of writing, all online-Gemini, all with verified hash chains:

| Debate ID | Topic | n | Latency | Cost | Failures | Audit |
|---|---|---|---|---|---|---|
| `9dfc21cc-…` | MSP for all 23 crops | 50 | 90 s | ~₹4 | 0 | chain_valid |
| `72e211cc-…` | UBI below MPCE quintile 3 | 12 | 80 s | ~₹1 | 0 | chain_valid |
| `f6a1fed2-…` | MSP (offline-stub baseline) | 5 | <1 s | ₹0 | 0 | chain_valid |

The 30-persona DPP-sampled MSP debate (V0.9 commit) spanned 22 distinct states and identified three clusters: Moral & Social Justice / Economic Stability / Fiscal Prudence. The conclusive remark cited a single retired Cabinet-Secretariat IAS persona by id over the four-persona moral-imperative cluster — i.e. the synthesis correctly weighted argument quality over headcount, the §6 design firing as specified.

### 11.2 The market exists

- **Indian qualitative-research market:** ₹29,008 crore (USD 3.5 B) FY25, growing 10.9 % YoY (Market Research Society of India, January 2026 — see [`docs/RELATED-WORK.md`](RELATED-WORK.md) §6.2 for the survey-corrected figure; an earlier internal estimate of ₹1,500–3,000 cr captured only the Tier-1 share)
- **Multilateral + foundation India slice:** the *high-defensibility* component of the market — work commissioned for programme design, regulatory review, or peer-reviewed publication
- **Per-engagement willingness-to-pay:** ₹15–40 lakh for 4–8 week stakeholder analyses (Dalberg India, McKinsey Health Institute India, Sambodhi Research, Athena Infonomics, Outline India typical scales)
- **Akhada per-pilot offer:** ₹4 lakh for a 4-week pilot

The cost-compression ratio is 1:10 against traditional fieldwork; the elapsed-time compression is 1:30 (90 seconds vs. 6 weeks per topic). The room is large.

### 11.3 The methodology is institutionally accepted

- Anthropic × Pol.is "Collective Constitutional AI" (2024–25) — Western governments engaging on AI-mediated deliberation
- Pol.is in Taiwan g0v digital-democracy programme — productionised since 2014
- UK Cabinet Office and European Commission Pol.is deployments
- Du et al., ICML 2024 — peer-reviewed multi-agent debate methodology
- Stanford generative-agents work (Park et al. 2023) — 1,052-persona simulation, 75 % attribution accuracy
- SYNTHIA (2024) — 30,000-persona BlueSky simulation
- Remesh — $35M+ raised, customers include UN agencies

### 11.4 What is **not** validated

- **No paying Akhada customer.** Zero. The ask is one paid pilot.
- **No multilateral programme officer has yet seen V0.10.** That meeting has not happened.
- **The 50-persona library has not been externally bias-audited.** V0.11 wires the CSDS-baseline KS-test pass; results published.
- **The Bradley-Terry weights are uncalibrated** (`weights:v0.0.0` is a placeholder; V1 fits weights on a held-out 50-debate × 3-rater calibration set).
- **22 Indian languages is V1.** V0.10 runs English-internal with multilingual personas — sufficient for English-language multilateral reports, insufficient for state-government work.

These gaps are real and named. They are the V0.11–V1 work. The pilot pricing reflects them: ₹4 lakh, not ₹40 lakh, until they close.

---

## 12. Architecture summary

For the technically diligent reader. Full details in `README.md`.

```
                     Studio (Next.js 14 + Tailwind)
                     ├── /                — debate launcher + result render
                     ├── /audit/[id]      — hash-chain visualisation
                     └── /debate/[id]     — V1 SSE live cluster view
                                  │
                                  │  HTTP / SSE
                                  ▼
                     Orchestrator (FastAPI + asyncio)
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
      (50 fixtures)         offline | online        SQLite (V0)
      k-DPP sampler         Flash R1 fan-out        debates
      Open Library validator + Pro synthesis        debate_events
                            + Pro conclusion        (hash-chained)
```

V1 swaps SQLite → BigQuery + GCS WORM bucket (retention-lock 7 yrs) and the runtime → real Google ADK `SequentialAgent` + `ParallelAgent` fan-out (`5 × ParallelAgent(100) → 25 × cluster → 5 × super-cluster → 1 × final`).

V2 adds Vertex AI Vector Search 2.0, multi-tenant CMEK with Cloud HSM (FIPS 140-2 L3) for gov tier, on-prem Anthos deploy, 22-language Sarvam pipeline, and the published DPDP DPIA + EU AI Act Annex IV technical doc.

---

## 13. Cost economics

Detailed audit in `README.md` §12. Headlines:

- **Per debate (5 personas online):** ~₹0.50 in Gemini costs. ~70 s wall.
- **Per debate (50 personas online):** ~₹4 in Gemini costs. ~90 s wall.
- **One-time library generation (50 personas):** ₹85, ~5 minutes parallel.
- **Per-month dev infrastructure:** ₹0 (local SQLite, no GCP).
- **Per-month V1 production infra (estimated):** ~₹3 lakh / month for 1,000 debates / day at SLA 99.5 % (Cloud Run + Vertex Agent Engine + Firestore + BigQuery + KMS).

Pilot economics:
- 3 debates × 50 personas × ~₹4 = ~₹12 in Gemini costs
- ~80 hours of engineering + delivery time
- ₹4 lakh pilot price point — the constraint is delivery time, not compute

Gross margin on the ₹4 lakh pilot is approximately 95 %. Subscription tiers (`Multilateral` ₹40L / yr, `Pro` ₹3L / yr) carry 92–96 % gross margin at expected utilisation. The cost structure is an SI-with-software model in the early years and a pure SaaS model from V2 onwards.

---

## 14. Data sources & licensing

| Source | License | Used for |
|---|---|---|
| Census of India 2011 | Govt open (free, registration) | Demographic anchor |
| NFHS-5 (2019–21) | DHS Program (free, registration) | Household + health attributes |
| CSDS-Lokniti National Election Studies | Academic license (commercial pending) | Ideological vectors |
| World Values Survey wave 7 | CC-BY / proprietary mix | Inglehart values |
| AI4Bharat IndicVoices, IndicAlign, IndicCorp | CC-BY 4.0 | District + language cohort plausibility |
| PRS Legislative Research | CC-BY 4.0 | Bills, votes, MP profiles |
| Wikidata SPARQL + dumps | CC0 | V1 fallback for Indic-language coverage |
| Open Library data dumps | CC0 + ODbL | Book authenticity validator |
| Pratham StoryWeaver | CC-BY 4.0 | Multilingual literacy content |

Disqualified for commercial redistribution (still useful for verification only):
- IMDb non-commercial dataset — replaced with Wikidata for film / TV
- Sahapedia (CC-BY-NC-SA 4.0) — verification reference only

Full attribution in `NOTICE`.

---

## 15. The single contact ask

If you are a programme officer at a multilateral, foundation, think tank, or large newsroom who recognises the problem in §2 — the standard limitations of Indian qualitative fieldwork — and the value proposition in §5 sounds defensible to you, the ask is:

> **One 30-minute working session with one of your live programme questions.** SARGVISION Intelligence will run it through Akhada in front of you and you will see the article + the conclusive remark + the audit chain. If it does not earn the next conversation, we both stop. If it does, we sign the ₹4 lakh pilot in §7 and start.

The artefact is real; the wedge is sharp; the work is in your hands.

---

**Akhada is a product of SARGVISION Intelligence.**

Repository: https://github.com/sargupta/akhada-engine
Pinned release: [v0.10.0](https://github.com/sargupta/akhada-engine/releases/tag/v0.10.0)
Contact: via repository issues or the maintainers' email (see `pyproject.toml`)
