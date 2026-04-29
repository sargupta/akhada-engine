# akhada-studio-web

Next.js 14 Studio for Akhada. V0 has a single-page form that POSTs to the
local orchestrator at `http://127.0.0.1:8080` and renders the stub debate
output. V1 adds a live SSE cluster-stream view at `/debate/[id]`.

```bash
npm install
npm run dev   # http://localhost:3000
```

Set `NEXT_PUBLIC_API_BASE` in `.env.local` to point at a non-default API host.
