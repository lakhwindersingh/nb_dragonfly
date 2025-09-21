# Adapter module to expose WorkflowEngine under package namespace
import os
import sys

# Ensure engine root (where workflow_engine.py resides) is importable
ENGINE_ROOT = os.path.dirname(os.path.dirname(__file__))
if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

from workflow_engine import WorkflowEngine  # noqa: E402

__all__ = ["WorkflowEngine"]
