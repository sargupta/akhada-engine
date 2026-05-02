"""Persistence layer.

V0.10: SQLite-backed debate store with hash-chained audit events
(plan §20.10). V1 swaps the backend to BigQuery + GCS WORM bucket
for tamper-evident retention.
"""
