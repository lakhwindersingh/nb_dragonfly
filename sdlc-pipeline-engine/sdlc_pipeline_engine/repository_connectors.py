# Adapter module to expose RepositoryConnectorFactory under package namespace
import os
import sys

# Ensure parent directory (where repository_connectors.py resides) is importable
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from RepositoryConnectorsImplementation import RepositoryConnectorFactory  # noqa: E402

__all__ = ["RepositoryConnectorFactory"]
