# Adapter module to expose ValidationEngine under package namespace
import os
import sys

# Ensure engine root (where validation_engine.py resides) is importable
ENGINE_ROOT = os.path.dirname(os.path.dirname(__file__))
if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

from validation_engine import ValidationEngine  # noqa: E402

__all__ = ["ValidationEngine"]
