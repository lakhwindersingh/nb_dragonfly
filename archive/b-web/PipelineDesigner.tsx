import React, { useState, useCallback, useEffect } from 'react';
import {
  Box,
  Paper,
  Toolbar,
  IconButton,
  Typography,
  Button,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import {
  Save as SaveIcon,
  PlayArrow as PlayIcon,
  Add as AddIcon,
  Delete as DeleteIcon,
  Settings as SettingsIcon,
  Visibility as PreviewIcon,
} from '@mui/icons-material';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState,
  Connection,
  Edge,
  Node,
  ReactFlowProvider,
} from 'react-flow-renderer';
import { useParams, useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../hooks/redux';
import { PipelineDefinition, StageDefinition, StageType } from '../../types/pipeline';
import { StageNode } from './StageNode';
import { StageConfigPanel } from './StageConfigPanel';
import { PipelineConfigPanel } from './PipelineConfigPanel';
import { createPipeline, updatePipeline, fetchPipeline } from '../../store/slices/pipelinesSlice';

const nodeTypes = {
  stageNode: StageNode,
};

const DRAWER_WIDTH = 280;

const stageTemplates = [
  { type: StageType.PLANNING, name: 'Planning', icon: '📋', color: '#2196F3' },
  { type: StageType.REQUIREMENTS, name: 'Requirements', icon: '📝', color: '#4CAF50' },
  { type: StageType.DESIGN, name: 'Design', icon: '🎨', color: '#9C27B0' },
  { type: StageType.IMPLEMENTATION, name: 'Implementation', icon: '⚡', color: '#FF9800' },
  { type: StageType.TESTING, name: 'Testing', icon: '🧪', color: '#F44336' },
  { type: StageType.DEPLOYMENT, name: 'Deployment', icon: '🚀', color: '#00BCD4' },
  { type: StageType.MAINTENANCE, name: 'Maintenance', icon: '🔧', color: '#795548' },
];

export const PipelineDesigner: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  
  const { currentPipeline, creating, loading } = useAppSelector(state => state.pipelines);
  
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedStage, setSelectedStage] = useState<StageDefinition | null>(null);
  const [showPipelineConfig, setShowPipelineConfig] = useState(false);
  const [saveDialogOpen, setSaveDialogOpen] = useState(false);
  const [pipelineName, setPipelineName] = useState('');
  const [pipelineDescription, setPipelineDescription] = useState('');

  // Load pipeline if editing
  useEffect(() => {
    if (id && id !== 'new') {
      dispatch(fetchPipeline(id));
    }
  }, [id, dispatch]);

  // Convert pipeline to nodes/edges
  useEffect(() => {
    if (currentPipeline) {
      setPipelineName(currentPipeline.name);
      setPipelineDescription(currentPipeline.description);
      
      const pipelineNodes: Node[] = currentPipeline.stages.map((stage, index) => {
        const template = stageTemplates.find(t => t.type === stage.type);
        return {
          id: stage.id,
          type: 'stageNode',
          position: { x: (index % 3) * 300, y: Math.floor(index / 3) * 200 },
          data: {
            stage,
            template,
            onSelect: () => setSelectedStage(stage),
          },
        };
      });

      const pipelineEdges: Edge[] = [];
      currentPipeline.stages.forEach(stage => {
        stage.dependencies.forEach(depId => {
          pipelineEdges.push({
            id: `${depId}-${stage.id}`,
            source: depId,
            target: stage.id,
            type: 'smoothstep',
          });
        });
      });

      setNodes(pipelineNodes);
      setEdges(pipelineEdges);
    }
  }, [currentPipeline, setNodes, setEdges]);

  const onConnect = useCallback(
    (params: Connection | Edge) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const addStageToCanvas = (template: typeof stageTemplates[0]) => {
    const newStageId = `stage-${Date.now()}`;
    const newStage: StageDefinition = {
      id: newStageId,
      type: template.type,
      name: `${template.name} Stage`,
      description: `${template.name} stage description`,
      dependencies: [],
      ai_config: {
        model: 'gpt-4',
        temperature: 0.3,
        max_tokens: 4000,
      },
      prompt_template: '',
      validation_rules: [],
      repositories: [],
      timeout_minutes: 30,
      approval_required: false,
      reviewers: [],
    };

    const newNode: Node = {
      id: newStageId,
      type: 'stageNode',
      position: { x: Math.random() * 500, y: Math.random() * 300 },
      data: {
        stage: newStage,
        template,
        onSelect: () => setSelectedStage(newStage),
      },
    };

    setNodes((nds) => [...nds, newNode]);
  };

  const updateStage = (updatedStage: StageDefinition) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === updatedStage.id) {
          return {
            ...node,
            data: {
              ...node.data,
              stage: updatedStage,
            },
          };
        }
        return node;
      })
    );
    setSelectedStage(updatedStage);
  };

  const deleteStage = (stageId: string) => {
    setNodes((nds) => nds.filter((node) => node.id !== stageId));
    setEdges((eds) => eds.filter((edge) => edge.source !== stageId && edge.target !== stageId));
    setSelectedStage(null);
  };

  const savePipeline = async () => {
    if (!pipelineName.trim()) {
      setSaveDialogOpen(true);
      return;
    }

    const stages: StageDefinition[] = nodes.map((node) => {
      const stage = node.data.stage;
      const dependencies = edges
        .filter((edge) => edge.target === node.id)
        .map((edge) => edge.source);
      
      return {
        ...stage,
        dependencies,
      };
    });

    const pipelineData: PipelineDefinition = {
      id: id !== 'new' ? id : undefined,
      name: pipelineName,
      description: pipelineDescription,
      version: currentPipeline?.version || '1.0',
      stages,
      global_config: currentPipeline?.global_config || {
        retry_policy: { max_retries: 3 },
        notification_config: {
          email_notifications: true,
          slack_notifications: false,
          webhook_notifications: false,
        },
        artifact_retention: {
          days: 365,
          backup_strategy: 'cloud_storage',
        },
        security_config: {
          encrypt_artifacts: true,
          access_logging: true,
          compliance_validation: true,
        },
      },
    };

    try {
      if (id && id !== 'new') {
        await dispatch(updatePipeline({ pipelineId: id, pipeline: pipelineData }));
      } else {
        const action = await dispatch(createPipeline(pipelineData));
        if (createPipeline.fulfilled.match(action)) {
          navigate(`/pipelines/${action.payload.id}/edit`);
        }
      }
    } catch (error) {
      console.error('Failed to save pipeline:', error);
    }
  };

  const executePipeline = () => {
    if (currentPipeline?.id) {
      navigate(`/pipelines/${currentPipeline.id}/execute`);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Typography>Loading pipeline...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      {/* Stage Templates Drawer */}
      <Drawer
        variant="permanent"
        sx={{
          width: DRAWER_WIDTH,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: DRAWER_WIDTH,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <Typography variant="h6" sx={{ p: 2 }}>
            Stage Templates
          </Typography>
          <List>
            {stageTemplates.map((template) => (
              <ListItem key={template.type} disablePadding>
                <ListItemButton onClick={() => addStageToCanvas(template)}>
                  <ListItemIcon>
                    <Box
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: 32,
                        height: 32,
                        borderRadius: 1,
                        backgroundColor: template.color,
                        color: 'white',
                        fontSize: '16px',
                      }}
                    >
                      {template.icon}
                    </Box>
                  </ListItemIcon>
                  <ListItemText primary={template.name} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      {/* Main Content */}
      <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Toolbar */}
        <Paper elevation={1} sx={{ zIndex: 1000 }}>
          <Toolbar>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              {id === 'new' ? 'Create New Pipeline' : `Edit: ${currentPipeline?.name || 'Pipeline'}`}
            </Typography>
            <IconButton onClick={() => setShowPipelineConfig(true)}>
              <SettingsIcon />
            </IconButton>
            <IconButton>
              <PreviewIcon />
            </IconButton>
            <Button
              variant="contained"
              startIcon={<SaveIcon />}
              onClick={savePipeline}
              disabled={creating}
              sx={{ mr: 1 }}
            >
              Save
            </Button>
            {currentPipeline && (
              <Button
                variant="outlined"
                startIcon={<PlayIcon />}
                onClick={executePipeline}
              >
                Execute
              </Button>
            )}
          </Toolbar>
        </Paper>

        {/* Flow Canvas */}
        <Box sx={{ flexGrow: 1, position: 'relative' }}>
          <ReactFlowProvider>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              nodeTypes={nodeTypes}
              fitView
            >
              <Background />
              <Controls />
              <MiniMap />
            </ReactFlow>
          </ReactFlowProvider>
        </Box>
      </Box>

      {/* Stage Configuration Panel */}
      {selectedStage && (
        <StageConfigPanel
          stage={selectedStage}
          onUpdate={updateStage}
          onDelete={() => deleteStage(selectedStage.id)}
          onClose={() => setSelectedStage(null)}
        />
      )}

      {/* Pipeline Configuration Dialog */}
      {showPipelineConfig && currentPipeline && (
        <PipelineConfigPanel
          pipeline={currentPipeline}
          open={showPipelineConfig}
          onClose={() => setShowPipelineConfig(false)}
          onSave={(updatedPipeline) => {
            // Handle pipeline config update
            setShowPipelineConfig(false);
          }}
        />
      )}

      {/* Save Dialog */}
      <Dialog open={saveDialogOpen} onClose={() => setSaveDialogOpen(false)}>
        <DialogTitle>Save Pipeline</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Pipeline Name"
            type="text"
            fullWidth
            variant="outlined"
            value={pipelineName}
            onChange={(e) => setPipelineName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Description"
            type="text"
            fullWidth
            multiline
            rows={3}
            variant="outlined"
            value={pipelineDescription}
            onChange={(e) => setPipelineDescription(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSaveDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={() => {
              setSaveDialogOpen(false);
              savePipeline();
            }}
            variant="contained"
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PipelineDesigner;
