# Akhada infra (Terraform)

V1+ only. Local-only V0 needs no infra.

V1 modules ship:
- `vpc.tf` — VPC SC perimeter `akhada-perimeter`, Private Service Connect
- `firestore.tf` — single-region `asia-south1` (data residency for India)
- `bigquery.tf` — `akhada_audit` dataset with hash-chained `debate_events`, CMEK
- `gcs.tf` — `akhada-audit-worm` bucket with Bucket Lock retention 7yr
- `vertex.tf` — Agent Engine + Vector Search 2.0 + model endpoints
- `memorystore.tf` — Redis 7 HA for hot persona-library cache
- `kms.tf` — Cloud HSM (FIPS 140-2 L3) for gov tier
- `iam.tf` — service accounts: orchestrator / api / worker / synth (least privilege)
- `cloud_run.tf` — Studio + API backend (Cloud Run 2nd gen)
- `cloudbuild.tf` — CI pipeline with SLSA L3 attestations + Binary Authorization
- `monitoring.tf` — SLO definitions per §20.11

See plan §20 for the full architecture map.
