# Akhada — Open Debate Engine

A 500+ AI-agent debate engine grounded in real Indian demographic data. Topics in, structured article + quality-weighted conclusive remark + audit trail out. Built on Google ADK + Gemini.

**Status:** V0 scaffold (April 2026). See [the plan](https://) — copy at `/Users/sargupta/.claude/plans/i-want-to-build-atomic-liskov.md`.

## Layout

```
services/
  orchestrator/         # Python, ADK + FastAPI
  studio-web/           # Next.js 14, live debate stream UI
packages/
  shared-types/         # TS types generated from Pydantic
infra/                  # Terraform — V1+
benchmarks/
  akhada-bench/         # Eval harness, gold sets, results
docs/
  compliance/           # DPDP, IT Rules, EU AI Act
  persona-library/      # Bias-audit reports
```

## Local dev (V0)

```bash
# Python orchestrator
cd services/orchestrator
~/Library/Python/3.13/bin/poetry install
~/Library/Python/3.13/bin/poetry run uvicorn akhada.api.main:app --reload --port 8080
# in another shell
~/Library/Python/3.13/bin/poetry run adk web

# Studio
cd services/studio-web
npm install
npm run dev
```

V0 runs entirely local (no GCP required). Vertex/Firestore wiring lands at V1.

## Offline vs online (V0.7)

The orchestrator has two backends. Default is **offline** — a deterministic
stub used by tests + CI.

To run **online** with real Gemini:

```bash
# 1. Get a free Gemini API key from https://aistudio.google.com/apikey
# 2. cp .env.example .env  (at repo root)
# 3. Edit .env:
#       AKHADA_OFFLINE=false
#       GOOGLE_API_KEY=<paste key>
# 4. Restart uvicorn
```

Verify:

```bash
curl http://127.0.0.1:8080/v1/runtime
# {"online_ready":true,"reason":null}
```

Now `POST /v1/debates` runs real Flash openings (one per persona, async-fanned)
+ Pro synthesis + Pro conclusion. Cost ≈ $0.01 per 50-persona debate.

## License

AGPL-3.0 (engine + persona library v1). See `LICENSE`.

Commercial license (gov tier features: 50K-persona library v2, DigiLocker e-KYC, on-prem deploy kit, Opus synthesis tier, white-label) available — contact maintainers.

## Roadmap

- **V0 (4w):** 50 agents flat, English, hand-curated personas, naive round-robin. ← *we are here*
- **V1 (10w):** 500 agents hierarchical, EN+HI, Census-anchored library, audit trail, Studio live view.
- **V2 (20w):** 22 Indian languages, district-anchored 50K library, first ministry pilot, DPDP/EU AI Act compliance pack.
- **V3 (24w):** Public API, pluggable models (LiteLLM), white-label, AkhadaBench published, global persona modules.
