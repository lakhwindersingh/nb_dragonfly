# Adapter module so consumers can import from sdlc_pipeline_engine.SDLCPipelineOrchestrator
import os
import sys

# Ensure parent directory (where SDLCPipelineOrchestrator.py resides) is importable
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

# Import the orchestrator class
from SDLCPipelineOrchestrator import SDLCPipelineOrchestrator  # noqa: E402

__all__ = ["SDLCPipelineOrchestrator"]
