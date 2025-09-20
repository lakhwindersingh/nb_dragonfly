"""
Workflow Engine
Manages workflow execution, dependencies, and state transitions
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import json

class WorkflowState(Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"

@dataclass
class WorkflowNode:
    id: str
    name: str
    dependencies: List[str]
    state: WorkflowState
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 1800  # 30 minutes default
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class WorkflowExecution:
    id: str
    workflow_id: str
    state: WorkflowState
    nodes: Dict[str, WorkflowNode]
    start_time: datetime
    end_time: Optional[datetime] = None
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}

class WorkflowEngine:
    """Engine for managing workflow execution with dependency resolution"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Active workflow executions
        self.active_executions: Dict[str, WorkflowExecution] = {}
        
        # Node execution handlers
        self.node_handlers: Dict[str, Callable] = {}
        
        # Event listeners
        self.event_listeners: Dict[str, List[Callable]] = {}
        
        # Configuration
        self.max_concurrent_nodes = config.get('max_concurrent_nodes', 10)
        self.default_timeout = config.get('default_timeout_seconds', 1800)
        self.cleanup_interval = config.get('cleanup_interval_hours', 24)
        
        # Start cleanup task
        asyncio.create_task(self._cleanup_completed_executions())
    
    def register_node_handler(self, node_type: str, handler: Callable):
        """Register a handler for a specific node type"""
        self.node_handlers[node_type] = handler
        self.logger.info(f"Registered handler for node type: {node_type}")
    
    def add_event_listener(self, event_type: str, listener: Callable):
        """Add event listener for workflow events"""
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(listener)
    
    async def _emit_event(self, event_type: str, data: Any):
        """Emit workflow event to listeners"""
        if event_type in self.event_listeners:
            for listener in self.event_listeners[event_type]:
                try:
                    if asyncio.iscoroutinefunction(listener):
                        await listener(data)
                    else:
                        listener(data)
                except Exception as e:
                    self.logger.error(f"Error in event listener {event_type}: {str(e)}")
    
    async def create_workflow_execution(
        self,
        workflow_id: str,
        nodes: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new workflow execution"""
        
        execution_id = f"{workflow_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Build workflow nodes
        workflow_nodes = {}
        for node_data in nodes:
            node = WorkflowNode(
                id=node_data['id'],
                name=node_data.get('name', node_data['id']),
                dependencies=node_data.get('dependencies', []),
                state=WorkflowState.PENDING,
                max_retries=node_data.get('max_retries', 3),
                timeout_seconds=node_data.get('timeout_seconds', self.default_timeout),
                metadata=node_data.get('metadata', {})
            )
            workflow_nodes[node.id] = node
        
        # Validate dependencies
        self._validate_dependencies(workflow_nodes)
        
        # Create execution
        execution = WorkflowExecution(
            id=execution_id,
            workflow_id=workflow_id,
            state=WorkflowState.PENDING,
            nodes=workflow_nodes,
            start_time=datetime.utcnow(),
            context=context or {}
        )
        
        self.active_executions[execution_id] = execution
        
        await self._emit_event('workflow_created', {
            'execution_id': execution_id,
            'workflow_id': workflow_id,
            'node_count': len(workflow_nodes)
        })
        
        self.logger.info(f"Created workflow execution: {execution_id}")
        return execution_id
    
    def _validate_dependencies(self, nodes: Dict[str, WorkflowNode]):
        """Validate workflow dependencies for cycles and invalid references"""
        
        # Check for invalid dependencies
        for node_id, node in nodes.items():
            for dep in node.dependencies:
                if dep not in nodes:
                    raise ValueError(f"Node {node_id} has invalid dependency: {dep}")
        
        # Check for cycles using DFS
        def has_cycle(node_id: str, visited: Set[str], rec_stack: Set[str]) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)
            
            for dep in nodes[node_id].dependencies:
                if dep not in visited:
                    if has_cycle(dep, visited, rec_stack):
                        return True
                elif dep in rec_stack:
                    return True
            
            rec_stack.remove(node_id)
            return False
        
        visited = set()
        for node_id in nodes:
            if node_id not in visited:
                if has_cycle(node_id, visited, set()):
                    raise ValueError(f"Circular dependency detected involving node: {node_id}")
    
    async def start_execution(self, execution_id: str) -> bool:
        """Start workflow execution"""
        
        if execution_id not in self.active_executions:
            return False
        
        execution = self.active_executions[execution_id]
        
        if execution.state != WorkflowState.PENDING:
            return False
        
        execution.state = WorkflowState.RUNNING
        
        await self._emit_event('workflow_started', {
            'execution_id': execution_id,
            'start_time': execution.start_time.isoformat()
        })
        
        # Start execution loop
        asyncio.create_task(self._execute_workflow(execution_id))
        
        self.logger.info(f"Started workflow execution: {execution_id}")
        return True
    
    async def _execute_workflow(self, execution_id: str):
        """Main workflow execution loop"""
        
        execution = self.active_executions[execution_id]
        
        try:
            while execution.state == WorkflowState.RUNNING:
                # Find ready nodes
                ready_nodes = self._get_ready_nodes(execution)
                
                if not ready_nodes:
                    # Check if workflow is complete
                    if self._is_workflow_complete(execution):
                        execution.state = WorkflowState.COMPLETED
                        execution.end_time = datetime.utcnow()
                        break
                    else:
                        # Wait for running nodes to complete
                        await asyncio.sleep(1)
                        continue
                
                # Execute ready nodes (up to max concurrent)
                tasks = []
                for node in ready_nodes[:self.max_concurrent_nodes]:
                    if len([n for n in execution.nodes.values() if n.state == WorkflowState.RUNNING]) < self.max_concurrent_nodes:
                        task = asyncio.create_task(self._execute_node(execution_id, node.id))
                        tasks.append(task)
                
                # Wait a bit before checking again
                if tasks:
                    await asyncio.sleep(0.1)
                else:
                    await asyncio.sleep(1)
            
            # Emit completion event
            if execution.state == WorkflowState.COMPLETED:
                await self._emit_event('workflow_completed', {
                    'execution_id': execution_id,
                    'end_time': execution.end_time.isoformat(),
                    'duration': (execution.end_time - execution.start_time).total_seconds()
                })
            
        except Exception as e:
            self.logger.error(f"Workflow execution failed {execution_id}: {str(e)}")
            execution.state = WorkflowState.FAILED
            execution.end_time = datetime.utcnow()
            
            await self._emit_event('workflow_failed', {
                'execution_id': execution_id,
                'error': str(e),
                'end_time': execution.end_time.isoformat()
            })
    
    def _get_ready_nodes(self, execution: WorkflowExecution) -> List[WorkflowNode]:
        """Get nodes that are ready to execute"""
        
        ready_nodes = []
        
        for node in execution.nodes.values():
            if node.state != WorkflowState.PENDING:
                continue
            
            # Check if all dependencies are completed
            deps_completed = True
            for dep_id in node.dependencies:
                dep_node = execution.nodes[dep_id]
                if dep_node.state != WorkflowState.COMPLETED:
                    deps_completed = False
                    break
            
            if deps_completed:
                ready_nodes.append(node)
        
        return ready_nodes
    
    def _is_workflow_complete(self, execution: WorkflowExecution) -> bool:
        """Check if workflow execution is complete"""
        
        for node in execution.nodes.values():
            if node.state in [WorkflowState.PENDING, WorkflowState.RUNNING]:
                return False
        
        return True
    
    async def _execute_node(self, execution_id: str, node_id: str):
        """Execute a single workflow node"""
        
        execution = self.active_executions[execution_id]
        node = execution.nodes[node_id]
        
        # Set node to running
        node.state = WorkflowState.RUNNING
        node.start_time = datetime.utcnow()
        
        await self._emit_event('node_started', {
            'execution_id': execution_id,
            'node_id': node_id,
            'start_time': node.start_time.isoformat()
        })
        
        try:
            # Execute node with timeout
            await asyncio.wait_for(
                self._run_node_handler(execution_id, node_id),
                timeout=node.timeout_seconds
            )
            
            # Mark as completed
            node.state = WorkflowState.COMPLETED
            node.end_time = datetime.utcnow()
            
            await self._emit_event('node_completed', {
                'execution_id': execution_id,
                'node_id': node_id,
                'end_time': node.end_time.isoformat(),
                'duration': (node.end_time - node.start_time).total_seconds()
            })
            
            self.logger.info(f"Node completed: {node_id} in {execution_id}")
            
        except asyncio.TimeoutError:
            node.state = WorkflowState.FAILED
            node.end_time = datetime.utcnow()
            node.error_message = f"Node execution timed out after {node.timeout_seconds} seconds"
            
            await self._emit_event('node_failed', {
                'execution_id': execution_id,
                'node_id': node_id,
                'error': node.error_message,
                'end_time': node.end_time.isoformat()
            })
            
            self.logger.error(f"Node timed out: {node_id} in {execution_id}")
            
        except Exception as e:
            node.retry_count += 1
            
            if node.retry_count <= node.max_retries:
                # Retry node
                self
