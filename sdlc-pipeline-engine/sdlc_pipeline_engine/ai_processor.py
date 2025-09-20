# Adapter module to expose AIPromptProcessor under package namespace
import os
import sys
from typing import Any

# Ensure parent directory (where AIPromptProcessingManager.py resides) is importable
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from AIPromptProcessingManager import AIPromptProcessor  # noqa: E402

__all__ = ["AIPromptProcessor"]
