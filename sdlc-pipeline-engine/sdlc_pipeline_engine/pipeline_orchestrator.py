# Adapter module so consumers can import from sdlc_pipeline_engine.SDLCPipelineOrchestrator
import os
import sys

# Ensure engine root (where sdlc_orchestrator.py resides) is importable
ENGINE_ROOT = os.path.dirname(os.path.dirname(__file__))
if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

# Import the orchestrator class from the top-level engine module
from sdlc_orchestrator import SDLCPipelineOrchestrator  # noqa: E402

__all__ = ["SDLCPipelineOrchestrator"]
