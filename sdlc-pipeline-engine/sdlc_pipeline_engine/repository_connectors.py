# Adapter module to expose RepositoryConnectorFactory under package namespace
import os
import sys

# Ensure engine root (where repository_connectors.py resides) is importable
ENGINE_ROOT = os.path.dirname(os.path.dirname(__file__))
if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

from repository_connectors import RepositoryConnectorFactory  # noqa: E402

__all__ = ["RepositoryConnectorFactory"]
