# Adapter module to expose AIPromptProcessor under package namespace
import os
import sys
from typing import Any

# Ensure engine root (where ai_prompt_processors.py resides) is importable
ENGINE_ROOT = os.path.dirname(os.path.dirname(__file__))
if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

from ai_prompt_processors import AIPromptProcessor  # noqa: E402

__all__ = ["AIPromptProcessor"]
