
"""
SDLC Pipeline Orchestrator
Manages the execution of automated SDLC workflows with AI prompt chaining
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import uuid
from pathlib import Path
import os

from sdlc_pipeline_engine.ai_processor import AIPromptProcessor
from sdlc_pipeline_engine.artifact_manager import ArtifactManager
from sdlc_pipeline_engine.repository_connectors import RepositoryConnectorFactory
from sdlc_pipeline_engine.validation_engine import ValidationEngine

class StageType(Enum):
    PLANNING = "planning"
    REQUIREMENTS = "requirements"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"

class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

@dataclass
class PipelineContext:
    """Shared context passed between pipeline stages"""
    project_id: str
    execution_id: str
    stage_outputs: Dict[str, Any]
    metadata: Dict[str, Any]
    user_inputs: Dict[str, Any]
    
class StageDefinition:
    """Defines a single stage in the SDLC pipeline"""
    
    def __init__(self, stage_config: Dict[str, Any]):
        self.stage_id = stage_config["id"]
        self.stage_type = StageType(stage_config["type"])
        self.name = stage_config["name"]
        self.description = stage_config.get("description", "")
        
        # AI Configuration
        self.ai_config = stage_config.get("ai_config", {})
        self.prompt_template = stage_config.get("prompt_template", "")
        self.model_settings = stage_config.get("model_settings", {})
        
        # Validation Configuration
        self.validation_rules = stage_config.get("validation_rules", [])
        self.quality_gates = stage_config.get("quality_gates", [])
        
        # Repository Configuration
        self.repository_configs = stage_config.get("repositories", [])
        
        # Workflow Configuration
        self.dependencies = stage_config.get("dependencies", [])
        self.parallel_execution = stage_config.get("parallel_execution", False)
        self.timeout_minutes = stage_config.get("timeout_minutes", 30)
        self.retry_policy = stage_config.get("retry_policy", {"max_retries": 3})
        
        # Human-in-the-loop Configuration
        self.approval_required = stage_config.get("approval_required", False)
        self.reviewers = stage_config.get("reviewers", [])

class SDLCPipelineOrchestrator:
    """Main orchestrator for SDLC pipeline execution"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.ai_processor = AIPromptProcessor(config.get("ai_config", {}))
        self.artifact_manager = ArtifactManager(config.get("artifact_config", {}))
        self.validation_engine = ValidationEngine(config.get("validation_config", {}))
        self.repository_factory = RepositoryConnectorFactory(config.get("repository_config", {}))
        
        # Pipeline state
        self.active_executions: Dict[str, Dict] = {}
        
    async def create_pipeline(self, pipeline_definition: Dict[str, Any]) -> str:
        """Create a new pipeline from definition"""
        pipeline_id = str(uuid.uuid4())
        
        # Validate pipeline definition
        await self._validate_pipeline_definition(pipeline_definition)
        
        # Store pipeline definition
        await self.artifact_manager.store_pipeline_definition(
            pipeline_id, pipeline_definition
        )
        
        self.logger.info(f"Created pipeline {pipeline_id}")
        return pipeline_id
    
    async def execute_pipeline(
        self, 
        pipeline_id: str, 
        user_inputs: Dict[str, Any],
        execution_options: Optional[Dict[str, Any]] = None
    ) -> str:
        """Execute a pipeline with given inputs"""
        execution_id = str(uuid.uuid4())
        
        try:
            # Load pipeline definition
            pipeline_def = await self.artifact_manager.load_pipeline_definition(pipeline_id)
            
            # Initialize execution context
            context = PipelineContext(
                project_id=pipeline_id,
                execution_id=execution_id,
                stage_outputs={},
                metadata={
                    "start_time": datetime.utcnow().isoformat(),
                    "pipeline_version": pipeline_def.get("version", "1.0"),
                    "execution_options": execution_options or {}
                },
                user_inputs=user_inputs
            )
            
            # Store execution state
            self.active_executions[execution_id] = {
                "status": ExecutionStatus.PENDING,
                "context": context,
                "pipeline_def": pipeline_def,
                "current_stage": None
            }
            
            # Start pipeline execution
            asyncio.create_task(self._execute_pipeline_async(execution_id))
            
            self.logger.info(f"Started pipeline execution {execution_id}")
            return execution_id
            
        except Exception as e:
            self.logger.error(f"Failed to start pipeline execution: {str(e)}")
            raise
    
    async def _execute_pipeline_async(self, execution_id: str):
        """Async pipeline execution logic"""
        execution_state = self.active_executions[execution_id]
        context = execution_state["context"]
        pipeline_def = execution_state["pipeline_def"]
        
        try:
            execution_state["status"] = ExecutionStatus.RUNNING
            
            # Build execution graph
            stages = [StageDefinition(stage_config) for stage_config in pipeline_def["stages"]]
            execution_graph = self._build_execution_graph(stages)
            
            # Execute stages according to dependency graph
            for stage_batch in execution_graph:
                if execution_state["status"] != ExecutionStatus.RUNNING:
                    break
                
                # Execute stages in parallel if possible
                if len(stage_batch) > 1:
                    tasks = [self._execute_stage(stage, context) for stage in stage_batch]
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    # Check for failures
                    for i, result in enumerate(results):
                        if isinstance(result, Exception):
                            stage_id = stage_batch[i].stage_id
                            self.logger.error(f"Stage {stage_id} failed: {str(result)}")
                            execution_state["status"] = ExecutionStatus.FAILED
                            return
                else:
                    # Single stage execution
                    stage = stage_batch[0]
                    try:
                        await self._execute_stage(stage, context)
                    except Exception as e:
                        self.logger.error(f"Stage {stage.stage_id} failed: {str(e)}")
                        execution_state["status"] = ExecutionStatus.FAILED
                        return
            
            # Mark execution as completed
            execution_state["status"] = ExecutionStatus.COMPLETED
            context.metadata["end_time"] = datetime.utcnow().isoformat()
            
            self.logger.info(f"Pipeline execution {execution_id} completed successfully")
            
        except Exception as e:
            self.logger.error(f"Pipeline execution {execution_id} failed: {str(e)}")
            execution_state["status"] = ExecutionStatus.FAILED
        
        finally:
            # Store final execution state
            await self.artifact_manager.store_execution_result(execution_id, execution_state)
    
    async def _execute_stage(self, stage: StageDefinition, context: PipelineContext):
        """Execute a single pipeline stage"""
        stage_start_time = datetime.utcnow()
        
        try:
            self.logger.info(f"Starting stage {stage.stage_id}: {stage.name}")
            
            # Update context with current stage
            self.active_executions[context.execution_id]["current_stage"] = stage.stage_id
            
            # Prepare stage inputs
            stage_inputs = await self._prepare_stage_inputs(stage, context)
            
            # Execute AI processing
            ai_outputs = await self._execute_ai_processing(stage, stage_inputs, context)
            
            # Validate outputs
            validation_results = await self._validate_stage_outputs(stage, ai_outputs)
            if not validation_results["passed"]:
                raise ValueError(f"Stage validation failed: {validation_results['errors']}")
            
            # Handle approval gates
            if stage.approval_required:
                approval_result = await self._handle_approval_gate(stage, ai_outputs, context)
                if not approval_result["approved"]:
                    raise ValueError(f"Stage approval rejected: {approval_result['reason']}")
            
            # Store artifacts in external repositories
            repository_results = await self._store_stage_artifacts(stage, ai_outputs, context)
            
            # Update context with stage outputs
            context.stage_outputs[stage.stage_id] = {
                "outputs": ai_outputs,
                "validation": validation_results,
                "repositories": repository_results,
                "execution_time": (datetime.utcnow() - stage_start_time).total_seconds(),
                "status": "completed"
            }
            
            self.logger.info(f"Completed stage {stage.stage_id}")
            
        except Exception as e:
            # Store error information
            context.stage_outputs[stage.stage_id] = {
                "status": "failed",
                "error": str(e),
                "execution_time": (datetime.utcnow() - stage_start_time).total_seconds()
            }
            raise
    
    async def _prepare_stage_inputs(
        self, 
        stage: StageDefinition, 
        context: PipelineContext
    ) -> Dict[str, Any]:
        """Prepare inputs for a stage from context and dependencies"""
        stage_inputs = {
            "stage_type": stage.stage_type.value,
            "user_inputs": context.user_inputs,
            "project_metadata": context.metadata
        }
        
        # Add outputs from dependent stages
        for dependency in stage.dependencies:
            if dependency in context.stage_outputs:
                dep_output = context.stage_outputs[dependency]
                stage_inputs[f"{dependency}_output"] = dep_output["outputs"]
            else:
                self.logger.warning(f"Missing dependency {dependency} for stage {stage.stage_id}")
        
        # Add stage-specific configurations
        stage_inputs.update(stage.ai_config.get("additional_inputs", {}))
        
        return stage_inputs
    
    async def _execute_ai_processing(
        self, 
        stage: StageDefinition, 
        inputs: Dict[str, Any], 
        context: PipelineContext
    ) -> Dict[str, Any]:
        """Execute AI processing for a stage"""
        
        # Prepare prompt with inputs
        prompt = await self._build_stage_prompt(stage, inputs)
        
        # Execute AI processing
        ai_result = await self.ai_processor.process_prompt(
            prompt=prompt,
            model_config=stage.model_settings,
            context=context
        )
        
        return ai_result
    
    async def _build_stage_prompt(
        self, 
        stage: StageDefinition, 
        inputs: Dict[str, Any]
    ) -> str:
        """Build the prompt for AI processing.
        Supports externalized prompt files in sdlc-pipeline repository via:
        - Absolute or relative file paths ending with .md/.txt/.yaml
        - Strings starting with "file:" prefix
        - Logical keys like "analyze-resources" resolved under stage directory
        - Fully qualified keys like "1-planning/prompts/analyze-resources.md"
        Falls back to treating stage.prompt_template as inline Jinja template.
        """
        
        prompt_spec = stage.prompt_template or ""
        base_dir = self.config.get('prompts_base_dir')
        try:
            content = self._resolve_prompt_content(prompt_spec, stage, base_dir)
        except Exception as e:
            self.logger.warning(f"Prompt resolution failed for stage {stage.stage_id}: {e}. Using inline content if provided.")
            content = prompt_spec
        
        # Replace placeholders with actual values
        import jinja2
        template = jinja2.Template(content)
        rendered_prompt = template.render(**inputs)
        
        return rendered_prompt

    def _resolve_prompt_content(self, prompt_spec: str, stage: StageDefinition, base_dir: Optional[str]) -> str:
        """Resolve prompt content from file system if prompt_spec indicates a file or key.
        If resolution fails or no spec, raises Exception.
        """
        # If no spec, raise
        if not prompt_spec:
            raise ValueError("Empty prompt_spec")
        
        # Normalize
        spec = prompt_spec.strip()
        # If starts with file: prefix
        if spec.lower().startswith("file:"):
            spec = spec[5:].strip()
        
        # Determine candidate paths
        candidates: List[Path] = []
        # Absolute path
        p = Path(spec)
        if p.is_absolute():
            candidates.append(p)
        
        # If looks like relative file path (has extension)
        if p.suffix.lower() in {'.md', '.txt', '.yaml', '.yml'}:
            if not p.is_absolute():
                if base_dir:
                    candidates.append(Path(base_dir) / p)
                candidates.append((Path(__file__).resolve().parent / p).resolve())
        else:
            # Treat as logical key, possibly including stage folder
            # Map StageType to directory prefix
            stage_dir_map = {
                'planning': '1-planning',
                'requirements': '2-requirements',
                'design': '3-design',
                'implementation': '4-implementation',
                'testing': '5-testing',
                'deployment': '6-deployment',
                'maintenance': '7-maintenance',
            }
            stage_dir = stage_dir_map.get(stage.stage_type.value, stage.stage_type.value)
            # If the spec already includes a slash, try as-is under prompts_base_dir
            if '/' in spec or '\\' in spec:
                if base_dir:
                    candidates.append(Path(base_dir) / spec)
            else:
                # Build common paths under sdlc-pipeline
                for ext in ['.md', '.txt']:
                    if base_dir:
                        candidates.append(Path(base_dir) / stage_dir / 'prompts' / f"{spec}{ext}")
                        candidates.append(Path(base_dir) / stage_dir / 'prompts' / spec)
        
        # Also try full qualified under base_dir if provided
        if base_dir:
            candidates.append(Path(base_dir) / spec)
        
        # Filter unique and existing
        tried = []
        for c in candidates:
            c = c.resolve()
            if c in tried:
                continue
            tried.append(c)
            if c.exists() and c.is_file():
                try:
                    return c.read_text(encoding='utf-8')
                except Exception as e:
                    # Try without encoding fallback
                    return c.read_text()
        
        # If nothing matched, raise
        raise FileNotFoundError(f"No prompt file found for spec '{prompt_spec}'. Tried: {', '.join(str(t) for t in tried)}")
    
    async def _validate_stage_outputs(
        self, 
        stage: StageDefinition, 
        outputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate stage outputs against defined rules"""
        
        validation_result = await self.validation_engine.validate(
            outputs=outputs,
            rules=stage.validation_rules,
            quality_gates=stage.quality_gates
        )
        
        return validation_result
    
    async def _handle_approval_gate(
        self, 
        stage: StageDefinition, 
        outputs: Dict[str, Any], 
        context: PipelineContext
    ) -> Dict[str, Any]:
        """Handle human approval gates"""
        
        # Create approval request
        approval_request = {
            "stage_id": stage.stage_id,
            "stage_name": stage.name,
            "outputs": outputs,
            "reviewers": stage.reviewers,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Store approval request
        approval_id = await self.artifact_manager.store_approval_request(
            context.execution_id, approval_request
        )
        
        # For now, simulate approval (in real implementation, this would wait for human input)
        # This could integrate with Slack, email, or web UI for approvals
        approval_result = {
            "approved": True,  # This would come from actual approval system
            "approver": "system",
            "approved_at": datetime.utcnow().isoformat(),
            "comments": "Auto-approved for demo"
        }
        
        return approval_result
    
    async def _store_stage_artifacts(
        self, 
        stage: StageDefinition, 
        outputs: Dict[str, Any], 
        context: PipelineContext
    ) -> Dict[str, Any]:
        """Store stage artifacts in external repositories"""
        
        repository_results = {}
        
        for repo_config in stage.repository_configs:
            try:
                # Get repository connector
                connector = self.repository_factory.get_connector(repo_config["type"])
                
                # Prepare artifacts for storage
                artifacts = await self._prepare_artifacts_for_storage(
                    outputs, repo_config, context
                )
                
                # Store artifacts
                storage_result = await connector.store_artifacts(
                    artifacts=artifacts,
                    config=repo_config,
                    context=context
                )
                
                repository_results[repo_config["name"]] = storage_result
                
                self.logger.info(
                    f"Stored artifacts in {repo_config['type']}: {repo_config['name']}"
                )
                
            except Exception as e:
                self.logger.error(
                    f"Failed to store artifacts in {repo_config['name']}: {str(e)}"
                )
                repository_results[repo_config["name"]] = {"error": str(e)}
        
        return repository_results
    
    async def _prepare_artifacts_for_storage(
        self, 
        outputs: Dict[str, Any], 
        repo_config: Dict[str, Any], 
        context: PipelineContext
    ) -> List[Dict[str, Any]]:
        """Prepare artifacts for storage based on repository configuration"""
        
        artifacts = []
        
        # Extract relevant outputs based on repository mapping
        for mapping in repo_config.get("artifact_mappings", []):
            output_key = mapping["output_key"]
            if output_key in outputs:
                artifact = {
                    "name": mapping["artifact_name"],
                    "content": outputs[output_key],
                    "type": mapping["artifact_type"],
                    "metadata": {
                        "stage_id": context.execution_id,
                        "created_at": datetime.utcnow().isoformat(),
                        "project_id": context.project_id
                    }
                }
                
                # Apply any transformation scripts
                if "transformation_script" in mapping:
                    artifact = await self._apply_transformation_script(
                        artifact, mapping["transformation_script"]
                    )
                
                artifacts.append(artifact)
        
        return artifacts
    
    async def _apply_transformation_script(
        self, 
        artifact: Dict[str, Any], 
        script_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply transformation script to artifact before storage"""
        
        # This could execute Python scripts, shell commands, or custom transformations
        # For now, implement basic transformations
        
        script_type = script_config.get("type", "python")
        script_content = script_config.get("script", "")
        
        if script_type == "python":
            # Execute Python transformation
            try:
                # Create safe execution environment
                exec_globals = {
                    "artifact": artifact,
                    "json": json,
                    "datetime": datetime
                }
                
                exec(script_content, exec_globals)
                return exec_globals["artifact"]
                
            except Exception as e:
                self.logger.error(f"Transformation script failed: {str(e)}")
                return artifact
        
        return artifact
    
    def _build_execution_graph(self, stages: List[StageDefinition]) -> List[List[StageDefinition]]:
        """Build execution graph based on dependencies"""
        
        # Simple topological sort implementation
        # In production, use more sophisticated dependency resolution
        
        executed = set()
        execution_order = []
        
        while len(executed) < len(stages):
            ready_stages = []
            
            for stage in stages:
                if stage.stage_id not in executed:
                    # Check if all dependencies are satisfied
                    deps_satisfied = all(dep in executed for dep in stage.dependencies)
                    if deps_satisfied:
                        ready_stages.append(stage)
            
            if not ready_stages:
                raise ValueError("Circular dependency detected in pipeline stages")
            
            execution_order.append(ready_stages)
            executed.update(stage.stage_id for stage in ready_stages)
        
        return execution_order
    
    async def _validate_pipeline_definition(self, pipeline_def: Dict[str, Any]):
        """Validate pipeline definition structure and dependencies"""
        
        required_fields = ["name", "version", "stages"]
        for field in required_fields:
            if field not in pipeline_def:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate stages
        stage_ids = set()
        for stage_config in pipeline_def["stages"]:
            stage_id = stage_config.get("id")
            if not stage_id:
                raise ValueError("Stage missing required 'id' field")
            
            if stage_id in stage_ids:
                raise ValueError(f"Duplicate stage ID: {stage_id}")
            
            stage_ids.add(stage_id)
        
        # Validate dependencies
        for stage_config in pipeline_def["stages"]:
            for dep in stage_config.get("dependencies", []):
                if dep not in stage_ids:
                    raise ValueError(f"Invalid dependency: {dep}")
    
    async def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Get current status of pipeline execution"""
        
        if execution_id not in self.active_executions:
            # Try to load from persistent storage
            return await self.artifact_manager.load_execution_result(execution_id)
        
        execution_state = self.active_executions[execution_id]
        
        return {
            "execution_id": execution_id,
            "status": execution_state["status"].value,
            "current_stage": execution_state.get("current_stage"),
            "completed_stages": list(execution_state["context"].stage_outputs.keys()),
            "start_time": execution_state["context"].metadata.get("start_time"),
            "progress": self._calculate_progress(execution_state)
        }
    
    def _calculate_progress(self, execution_state: Dict[str, Any]) -> float:
        """Calculate execution progress percentage"""
        total_stages = len(execution_state["pipeline_def"]["stages"])
        completed_stages = len(execution_state["context"].stage_outputs)
        
        return (completed_stages / total_stages) * 100 if total_stages > 0 else 0
    
    async def pause_execution(self, execution_id: str):
        """Pause pipeline execution"""
        if execution_id in self.active_executions:
            self.active_executions[execution_id]["status"] = ExecutionStatus.PAUSED
            self.logger.info(f"Paused execution {execution_id}")
    
    async def resume_execution(self, execution_id: str):
        """Resume paused pipeline execution"""
        if execution_id in self.active_executions:
            execution_state = self.active_executions[execution_id]
            if execution_state["status"] == ExecutionStatus.PAUSED:
                execution_state["status"] = ExecutionStatus.RUNNING
                self.logger.info(f"Resumed execution {execution_id}")
    
    async def cancel_execution(self, execution_id: str):
        """Cancel pipeline execution"""
        if execution_id in self.active_executions:
            self.active_executions[execution_id]["status"] = ExecutionStatus.CANCELLED
            self.logger.info(f"Cancelled execution {execution_id}")

# Example usage
if __name__ == "__main__":
    import yaml
    
    async def main():
        # Load configuration
        config = {
            "ai_config": {"default_model": "gpt-4"},
            "artifact_config": {"storage_path": "./artifacts"},
            "repository_config": {"connectors_path": "./connectors"}
        }
        
        # Create orchestrator
        orchestrator = SDLCPipelineOrchestrator(config)
        
        # Load pipeline definition
        with open("pipeline/definitions/full-sdlc-pipeline.yaml", "r") as f:
            pipeline_def = yaml.safe_load(f)
        
        # Create and execute pipeline
        pipeline_id = await orchestrator.create_pipeline(pipeline_def)
        
        user_inputs = {
            "project_name": "E-commerce Platform",
            "business_domain": "Online Retail",
            "target_users": "Small business owners and customers",
            "technology_preferences": "React, Spring Boot, PostgreSQL",
            "timeline_months": 6,
            "budget_range": "$150K-$200K"
        }
        
        execution_id = await orchestrator.execute_pipeline(pipeline_id, user_inputs)
        
        print(f"Started pipeline execution: {execution_id}")
        
        # Monitor execution
        while True:
            status = await orchestrator.get_execution_status(execution_id)
            print(f"Status: {status['status']}, Progress: {status['progress']}%")
            
            if status['status'] in ['completed', 'failed', 'cancelled']:
                break
            
            await asyncio.sleep(5)
    
    asyncio.run(main())
