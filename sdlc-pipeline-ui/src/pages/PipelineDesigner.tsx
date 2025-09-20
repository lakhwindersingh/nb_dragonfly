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

  const onConnect = useCallback((params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  const handleAddStage = (template: any) => {
    // Implementation for adding a new stage based on template
  };

  const handleSave = () => {
    setSaveDialogOpen(true);
  };

  const handleExecute = () => {
    if (id) {
      navigate(`/pipelines/${id}/execute`);
    }
  };

  const handleSaveConfirm = () => {
    // Save pipeline changes
    setSaveDialogOpen(false);
  };

  return (
    <ReactFlowProvider>
      <Box sx={{ display: 'flex', height: 'calc(100vh - 112px)' }}>
        <Drawer
          variant="permanent"
          anchor="left"
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
            <List>
              {stageTemplates.map((template) => (
                <ListItem key={template.type} disablePadding>
                  <ListItemButton onClick={() => handleAddStage(template)}>
                    <ListItemIcon>{template.icon}</ListItemIcon>
                    <ListItemText primary={template.name} />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </Box>
        </Drawer>

        <Box component="main" sx={{ flexGrow: 1 }}>
          <Toolbar />
          <Paper sx={{ height: '100%', position: 'relative' }}>
            <Toolbar sx={{ gap: 1 }}>
              <IconButton color="primary" onClick={handleSave}>
                <SaveIcon />
              </IconButton>
              <IconButton color="primary" onClick={handleExecute}>
                <PlayIcon />
              </IconButton>
              <IconButton>
                <PreviewIcon />
              </IconButton>
              <IconButton>
                <SettingsIcon />
              </IconButton>
            </Toolbar>

            <Box sx={{ height: 'calc(100% - 64px)' }}>
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                nodeTypes={nodeTypes}
                fitView
              >
                <MiniMap />
                <Controls />
                <Background />
              </ReactFlow>
            </Box>
          </Paper>
        </Box>

        <Drawer
          variant="permanent"
          anchor="right"
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
          <Box sx={{ p: 2 }}>
            {/* Configuration panels would go here */}
            <Typography variant="h6">Configuration</Typography>
          </Box>
        </Drawer>

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
            />
            <TextField
              margin="dense"
              label="Description"
              type="text"
              fullWidth
              variant="outlined"
              multiline
              rows={3}
              value={pipelineDescription}
              onChange={(e) => setPipelineDescription(e.target.value)}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSaveDialogOpen(false)}>Cancel</Button>
            <Button onClick={handleSaveConfirm} variant="contained">Save</Button>
          </DialogActions>
        </Dialog>
      </Box>
    </ReactFlowProvider>
  );
};

export default PipelineDesigner;
