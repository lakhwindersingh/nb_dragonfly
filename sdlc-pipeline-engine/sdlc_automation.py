"""
SDLC Pipeline Engine
A comprehensive automation engine for Software Development Life Cycle processes
"""

__version__ = "1.0.0"
__author__ = "SDLC Pipeline Team"

from .pipeline_orchestrator import SDLCPipelineOrchestrator
from .ai_processor import AIPromptProcessor
from .artifact_manager import ArtifactManager
from .repository_connectors import RepositoryConnectorFactory
from .workflow_engine import WorkflowEngine
from .validation_engine import ValidationEngine

__all__ = [
    'sdlc_orchestrator.py',
    'AIPromptProcessor',
    'artifact_manager.py',
    'RepositoryConnectorFactory',
    'WorkflowEngine',
    'validation_engine.py'
]
