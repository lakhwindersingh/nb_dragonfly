"""
Artifact Manager
Handles storage, retrieval, and versioning of pipeline artifacts
"""

import asyncio
import json
import os
import shutil
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import aiofiles
import yaml
from dataclasses import dataclass, asdict

@dataclass
class Artifact:
    id: str
    name: str
    type: str
    content: str
    metadata: Dict[str, Any]
    created_at: str
    size: int
    checksum: str
    execution_id: str
    stage_id: str
    version: str = "1.0"

@dataclass
class ArtifactIndex:
    artifacts: List[Artifact]
    total_count: int
    total_size: int
    last_updated: str

class ArtifactManager:
    """Manages pipeline artifacts with versioning and metadata"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Storage configuration
        self.storage_path = Path(config.get('storage_path', './artifacts'))
        self.max_storage_size = config.get('max_storage_size', 10 * 1024 * 1024 * 1024)  # 10GB
        self.retention_days = config.get('retention_days', 365)
        self.compression_enabled = config.get('compression_enabled', True)
        
        # Initialize storage structure
        self._initialize_storage()
        
        # In-memory index for performance
        self.artifact_index: Dict[str, Artifact] = {}
        # Load index asynchronously
        asyncio.create_task(self._load_index())
    
    def _initialize_storage(self):
        """Initialize storage directory structure"""
        
        directories = [
            self.storage_path,
            self.storage_path / 'executions',
            self.storage_path / 'pipelines',
            self.storage_path / 'templates',
            self.storage_path / 'metadata',
            self.storage_path / 'backups'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Initialized artifact storage at {self.storage_path}")
    
    async def _load_index(self):
        """Load artifact index from storage"""
        
        index_file = self.storage_path / 'metadata' / 'artifact_index.json'
        
        if index_file.exists():
            try:
                async with aiofiles.open(index_file, 'r') as f:
                    content = await f.read()
                    index_data = json.loads(content)
                    
                    for artifact_data in index_data.get('artifacts', []):
                        artifact = Artifact(**artifact_data)
                        self.artifact_index[artifact.id] = artifact
                
                self.logger.info(f"Loaded {len(self.artifact_index)} artifacts from index")
                
            except Exception as e:
                self.logger.error(f"Failed to load artifact index: {str(e)}")
    
    async def _save_index(self):
        """Save artifact index to storage"""
        
        index_file = self.storage_path / 'metadata' / 'artifact_index.json'
        
        try:
            artifacts_data = [asdict(artifact) for artifact in self.artifact_index.values()]
            
            index_data = ArtifactIndex(
                artifacts=artifacts_data,
                total_count=len(artifacts_data),
                total_size=sum(artifact.size for artifact in self.artifact_index.values()),
                last_updated=datetime.utcnow().isoformat()
            )
            
            async with aiofiles.open(index_file, 'w') as f:
                await f.write(json.dumps(asdict(index_data), indent=2))
                
        except Exception as e:
            self.logger.error(f"Failed to save artifact index: {str(e)}")
    
    async def store_artifact(
        self,
        name: str,
        content: str,
        artifact_type: str,
        execution_id: str,
        stage_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Store an artifact and return its ID"""
        
        # Generate artifact ID
        artifact_id = self._generate_artifact_id(name, execution_id, stage_id)
        
        # Calculate checksum
        checksum = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # Create artifact object
        artifact = Artifact(
            id=artifact_id,
            name=name,
            type=artifact_type,
            content=content,
            metadata=metadata or {},
            created_at=datetime.utcnow().isoformat(),
            size=len(content.encode('utf-8')),
            checksum=checksum,
            execution_id=execution_id,
            stage_id=stage_id
        )
        
        # Store artifact file
        artifact_path = await self._store_artifact_file(artifact)
        
        # Update index
        self.artifact_index[artifact_id] = artifact
        await self._save_index()
        
        self.logger.info(f"Stored artifact {artifact_id}: {name} ({artifact.size} bytes)")
        
        return artifact_id
    
    async def _store_artifact_file(self, artifact: Artifact) -> Path:
        """Store artifact content to file"""
        
        # Create directory structure: executions/{execution_id}/{stage_id}/
        artifact_dir = self.storage_path / 'executions' / artifact.execution_id / artifact.stage_id
        artifact_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine file extension based on artifact type
        file_extension = self._get_file_extension(artifact.type)
        file_path = artifact_dir / f"{artifact.name}{file_extension}"
        
        # Store content
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(artifact.content)
        
        # Store metadata
        metadata_path = artifact_dir / f"{artifact.name}.metadata.json"
        async with aiofiles.open(metadata_path, 'w') as f:
            metadata = {
                'artifact': asdict(artifact),
                'stored_at': datetime.utcnow().isoformat(),
                'file_path': str(file_path)
            }
            await f.write(json.dumps(metadata, indent=2))
        
        return file_path
    
    def _get_file_extension(self, artifact_type: str) -> str:
        """Get appropriate file extension for artifact type"""
        
        extensions = {
            'source_code': '.java',
            'test_code': '.java',
            'documentation': '.md',
            'configuration': '.yml',
            'script': '.sh',
            'docker': '.dockerfile',
            'kubernetes': '.yaml',
            'pipeline': '.yml',
            'json': '.json',
            'sql': '.sql',
            'requirements': '.md',
            'design': '.md',
            'test_plan': '.md',
            'runbook': '.md'
        }
        
        return extensions.get(artifact_type, '.txt')
    
    def _generate_artifact_id(self, name: str, execution_id: str, stage_id: str) -> str:
        """Generate unique artifact ID"""
        
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        unique_string = f"{execution_id}_{stage_id}_{name}_{timestamp}"
        
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    async def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """Retrieve artifact by ID"""
        
        if artifact_id in self.artifact_index:
            return self.artifact_index[artifact_id]
        
        return None
    
    async def get_artifact_content(self, artifact_id: str) -> Optional[str]:
        """Get artifact content by ID"""
        
        artifact = await self.get_artifact(artifact_id)
        if not artifact:
            return None
        
        try:
            # Reconstruct file path
            file_extension = self._get_file_extension(artifact.type)
            file_path = (self.storage_path / 'executions' / 
                        artifact.execution_id / artifact.stage_id / 
                        f"{artifact.name}{file_extension}")
            
            if file_path.exists():
                async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                    return await f.read()
            else:
                # Fallback to in-memory content
                return artifact.content
                
        except Exception as e:
            self.logger.error(f"Failed to read artifact content {artifact_id}: {str(e)}")
            return None
    
    async def list_artifacts(
        self,
        execution_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        artifact_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Artifact]:
        """List artifacts with optional filters"""
        
        artifacts = list(self.artifact_index.values())
        
        # Apply filters
        if execution_id:
            artifacts = [a for a in artifacts if a.execution_id == execution_id]
        
        if stage_id:
            artifacts = [a for a in artifacts if a.stage_id == stage_id]
        
        if artifact_type:
            artifacts = [a for a in artifacts if a.type == artifact_type]
        
        # Sort by creation time (newest first)
        artifacts.sort(key=lambda x: x.created_at, reverse=True)
        
        # Apply limit
        if limit:
            artifacts = artifacts[:limit]
        
        return artifacts
    
    async def delete_artifact(self, artifact_id: str) -> bool:
        """Delete artifact by ID"""
        
        artifact = await self.get_artifact(artifact_id)
        if not artifact:
            return False
        
        try:
            # Delete file
            file_extension = self._get_file_extension(artifact.type)
            file_path = (self.storage_path / 'executions' / 
                        artifact.execution_id / artifact.stage_id / 
                        f"{artifact.name}{file_extension}")
            
            if file_path.exists():
                file_path.unlink()
            
            # Delete metadata file
            metadata_path = file_path.parent / f"{artifact.name}.metadata.json"
            if metadata_path.exists():
                metadata_path.unlink()
            
            # Remove from index
            del self.artifact_index[artifact_id]
            await self._save_index()
            
            self.logger.info(f"Deleted artifact {artifact_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete artifact {artifact_id}: {str(e)}")
            return False
    
    async def store_pipeline_definition(self, pipeline_id: str, definition: Dict[str, Any]) -> bool:
        """Store pipeline definition"""
        
        try:
            pipeline_path = self.storage_path / 'pipelines' / f"{pipeline_id}.yaml"
            
            # Add metadata
            definition['stored_at'] = datetime.utcnow().isoformat()
            definition['id'] = pipeline_id
            
            async with aiofiles.open(pipeline_path, 'w') as f:
                await f.write(yaml.dump(definition, default_flow_style=False, indent=2))
            
            self.logger.info(f"Stored pipeline definition: {pipeline_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store pipeline definition {pipeline_id}: {str(e)}")
            return False
    
    async def load_pipeline_definition(self, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """Load pipeline definition"""
        
        try:
            pipeline_path = self.storage_path / 'pipelines' / f"{pipeline_id}.yaml"
            
            if not pipeline_path.exists():
                return None
            
            async with aiofiles.open(pipeline_path, 'r') as f:
                content = await f.read()
                return yaml.safe_load(content)
                
        except Exception as e:
            self.logger.error(f"Failed to load pipeline definition {pipeline_id}: {str(e)}")
            return None
    
    async def store_execution_result(self, execution_id: str, execution_state: Dict[str, Any]) -> bool:
        """Store execution result"""
        
        try:
            execution_path = self.storage_path / 'executions' / f"{execution_id}_result.json"
            
            # Add metadata
            result = {
                'execution_id': execution_id,
                'stored_at': datetime.utcnow().isoformat(),
                'execution_state': execution_state
            }
            
            async with aiofiles.open(execution_path, 'w') as f:
                await f.write(json.dumps(result, indent=2, default=str))
            
            self.logger.info(f"Stored execution result: {execution_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store execution result {execution_id}: {str(e)}")
            return False
    
    async def load_execution_result(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Load execution result"""
        
        try:
            execution_path = self.storage_path / 'executions' / f"{execution_id}_result.json"
            
            if not execution_path.exists():
                return None
            
            async with aiofiles.open(execution_path, 'r') as f:
                content = await f.read()
                return json.loads(content)
                
        except Exception as e:
            self.logger.error(f"Failed to load execution result {execution_id}: {str(e)}")
            return None
    
    async def store_approval_request(self, execution_id: str, approval_request: Dict[str, Any]) -> str:
        """Store approval request"""
        
        approval_id = self._generate_artifact_id(
            'approval_request', 
            execution_id, 
            approval_request.get('stage_id', 'unknown')
        )
        
        try:
            approval_path = self.storage_path / 'metadata' / f"approval_{approval_id}.json"
            
            request = {
                'approval_id': approval_id,
                'execution_id': execution_id,
                'stored_at': datetime.utcnow().isoformat(),
                **approval_request
            }
            
            async with aiofiles.open(approval_path, 'w') as f:
                await f.write(json.dumps(request, indent=2, default=str))
            
            self.logger.info(f"Stored approval request: {approval_id}")
            return approval_id
            
        except Exception as e:
            self.logger.error(f"Failed to store approval request: {str(e)}")
            raise
    
    async def cleanup_old_artifacts(self, days: int = None) -> Dict[str, Any]:
        """Clean up old artifacts based on retention policy"""
        
        days = days or self.retention_days
        cutoff_date = datetime.utcnow().timestamp() - (days * 24 * 3600)
        
        cleanup_stats = {
            'artifacts_deleted': 0,
            'bytes_freed': 0,
            'errors': []
        }
        
        artifacts_to_delete = []
        
        for artifact in self.artifact_index.values():
            artifact_date = datetime.fromisoformat(artifact.created_at).timestamp()
            if artifact_date < cutoff_date:
                artifacts_to_delete.append(artifact.id)
        
        for artifact_id in artifacts_to_delete:
            try:
                artifact = self.artifact_index[artifact_id]
                if await self.delete_artifact(artifact_id):
                    cleanup_stats['artifacts_deleted'] += 1
                    cleanup_stats['bytes_freed'] += artifact.size
            except Exception as e:
                cleanup_stats['errors'].append(f"Failed to delete {artifact_id}: {str(e)}")
        
        self.logger.info(f"Cleanup completed: {cleanup_stats['artifacts_deleted']} artifacts deleted, "
                        f"{cleanup_stats['bytes_freed']} bytes freed")
        
        return cleanup_stats
    
    async def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        
        total_artifacts = len(self.artifact_index)
        total_size = sum(artifact.size for artifact in self.artifact_index.values())
        
        # Group by type
        type_stats = {}
        for artifact in self.artifact_index.values():
            if artifact.type not in type_stats:
                type_stats[artifact.type] = {'count': 0, 'size': 0}
            type_stats[artifact.type]['count'] += 1
            type_stats[artifact.type]['size'] += artifact.size
        
        # Group by execution
        execution_stats = {}
        for artifact in self.artifact_index.values():
            if artifact.execution_id not in execution_stats:
                execution_stats[artifact.execution_id] = {'count': 0, 'size': 0}
            execution_stats[artifact.execution_id]['count'] += 1
            execution_stats[artifact.execution_id]['size'] += artifact.size

        return {
            'total_artifacts': total_artifacts,
            'total_size': total_size,
            'by_type': type_stats,
            'by_execution': execution_stats,
        }
