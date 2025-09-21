# Adapter module to expose ArtifactManager under package namespace
import os
import sys

# Ensure engine root (where artifact_manager.py resides) is importable
ENGINE_ROOT = os.path.dirname(os.path.dirname(__file__))
if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

from artifact_manager import ArtifactManager  # noqa: E402

__all__ = ["ArtifactManager"]
