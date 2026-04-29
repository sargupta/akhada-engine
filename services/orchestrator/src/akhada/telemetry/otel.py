"""Telemetry initialiser.

V0: structured logging via stdlib only.
V1: hook OTEL OTLP exporter to Cloud Trace / Cloud Logging via the
`OTEL_EXPORTER_OTLP_ENDPOINT` env var (defaults to telemetry.googleapis.com).
"""
from __future__ import annotations

import logging
import sys

from akhada.config import settings


def init_logging() -> logging.Logger:
    logging.basicConfig(
        level=settings.akhada_log_level,
        stream=sys.stdout,
        format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
    )
    return logging.getLogger("akhada")
