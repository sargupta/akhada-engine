"""Runtime backends for the debate flow.

`online` makes real Gemini calls via google-genai. `offline` (default,
stub) is implemented inline in `flows.debate.run_debate` and runs without
any network or model dependency — used for tests and CI.
"""
