# Adapter module to expose WorkflowEngine under package namespace
import os
import sys

# Ensure parent directory (where WorkflowExecutionEngine.py resides) is importable
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from WorkflowExecutionEngine import WorkflowEngine  # noqa: E402

__all__ = ["WorkflowEngine"]
