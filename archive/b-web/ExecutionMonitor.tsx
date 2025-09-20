import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  Grid,
  Button,
  IconButton,
  Collapse,
  List,
  ListItem,
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
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Schedule as ScheduleIcon,
  CloudDownload as DownloadIcon,
} from '@mui/icons-material';
import { useParams } from 'react-router-dom';
import { format } from 'date-fns';
import { useAppDispatch, useAppSelector } from '../../hooks/redux';
import { fetchExecution, pauseExecution, resumeExecution, cancelExecution } from '../../store/slices/executionsSlice';
import { PipelineExecution, ExecutionStatus, StageOutput } from '../../types/pipeline';
import websocketService from '../../services/websocket';
import { StageExecutionCard } from './StageExecutionCard';
import { ExecutionLogs } from './ExecutionLogs';
import { ArtifactViewer } from './ArtifactViewer';

export const ExecutionMonitor: React.FC = () => {
  const { executionId } = useParams<{ executionId: string }>();
  const dispatch = useAppDispatch();
  
  const { currentExecution, loading } = useAppSelector(state => state.executions);
  
  const [expandedStage, setExpandedStage] = useState<string | null>(null);
  const [showLogs, setShowLogs] = useState(false);
  const [showArtifacts, setShowArtifacts] = useState(false);
  const [approvalDialogOpen, setApprovalDialogOpen] = useState(false);
  const [approvalComments, setApprovalComments] = useState('');

  useEffect(() => {
    if (executionId) {
      dispatch(fetchExecution(executionId));
      
      // Subscribe to real-time updates
      websocketService.connect();
      websocketService.subscribeToExecution(executionId);
      
      const handleExecutionUpdate = (execution: PipelineExecution) => {
        if (execution.execution_id === executionId) {
          // Update Redux state with new execution data
        }
      };
      
      websocketService.on('executionUpdate', handleExecutionUpdate);
      
      return () => {
        websocketService.off('executionUpdate', handleExecutionUpdate);
        websocketService.unsubscribeFromExecution(executionId);
      };
    }
  }, [executionId, dispatch]);

  const handlePause = () => {
    if (executionId) {
      dispatch(pauseExecution(executionId));
    }
  };

  const handleResume = () => {
    if (executionId) {
      dispatch(resumeExecution(executionId));
    }
  };

  const handleCancel = () => {
    if (executionId) {
      dispatch(cancelExecution(executionId));
    }
  };

  const handleRefresh = () => {
    if (executionId) {
      dispatch(fetchExecution(executionId));
    }
  };

  const getStatusColor = (status: ExecutionStatus): "success" | "error" | "primary" | "warning" | "default" => {
    switch (status) {
      case ExecutionStatus.COMPLETED:
        return 'success';
      case ExecutionStatus.FAILED:
        return 'error';
      case ExecutionStatus.RUNNING:
        return 'primary';
      case ExecutionStatus.PAUSED:
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: ExecutionStatus) => {
    switch (status) {
      case ExecutionStatus.COMPLETED:
        return <CheckCircleIcon />;
      case ExecutionStatus.FAILED:
        return <ErrorIcon />;
      case ExecutionStatus.RUNNING:
        return <PlayIcon />;
      case ExecutionStatus.PAUSED:
        return <PauseIcon />;
      default:
        return <ScheduleIcon />;
    }
  };

  if (loading || !currentExecution) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography>Loading execution details...</Typography>
      </Box>
    );
  }

  const canPause = currentExecution.status === ExecutionStatus.RUNNING;
  const canResume = currentExecution.status === ExecutionStatus.PAUSED;
  const canCancel = [ExecutionStatus.RUNNING, ExecutionStatus.PAUSED, ExecutionStatus.PENDING].includes(currentExecution.status);

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" component="h1">
            Execution Monitor
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            {currentExecution.execution_id}
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <IconButton onClick={handleRefresh}>
            <RefreshIcon />
          </IconButton>
          {canPause && (
            <Button variant="outlined" startIcon={<PauseIcon />} onClick={handlePause}>
              Pause
            </Button>
          )}
          {canResume && (
            <Button variant="contained" startIcon={<PlayIcon />} onClick={handleResume}>
              Resume
            </Button>
          )}
          {canCancel && (
            <Button variant="outlined" color="error" startIcon={<StopIcon />} onClick={handleCancel}>
              Cancel
            </Button>
          )}
          <Button variant="outlined" onClick={() => setShowLogs(true)}>
            View Logs
          </Button>
          <Button variant="outlined" onClick={() => setShowArtifacts(true)} startIcon={<DownloadIcon />}>
            Artifacts
          </Button>
        </Box>
      </Box>

      {/* Status Overview */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                {getStatusIcon(currentExecution.status)}
                <Typography variant="h6" sx={{ ml: 1 }}>
                  Status: 
                </Typography>
                <Chip
                  label={currentExecution.status}
                  color={getStatusColor(currentExecution.status)}
                  sx={{ ml: 1 }}
                />
              </Box>
              
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                Progress: {currentExecution.progress.toFixed(1)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={currentExecution.progress}
                sx={{ mb: 2 }}
              />
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="caption" color="text.secondary">
                    Started
                  </Typography>
                  <Typography variant="body2">
                    {format(new Date(currentExecution.start_time), 'PPpp')}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  {currentExecution.end_time && (
                    <>
                      <Typography variant="caption" color="text.secondary">
                        Completed
                      </Typography>
                      <Typography variant="body2">
                        {format(new Date(currentExecution.end_time), 'PPpp')}
                      </Typography>
                    </>
                  )}
                  {currentExecution.current_stage && (
                    <>
                      <Typography variant="caption" color="text.secondary">
                        Current Stage
                      </Typography>
                      <Typography variant="body2">
                        {currentExecution.current_stage}
                      </Typography>
                    </>
                  )}
                </Grid>
              </Grid>
              
              {currentExecution.error_message && (
                <Box sx={{ mt: 2, p: 2, bgcolor: 'error.light', borderRadius: 1 }}>
                  <Typography variant="body2" color="error.contrastText">
                    Error: {currentExecution.error_message}
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Stage Summary
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Completed: {currentExecution.completed_stages.length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total: {Object.keys(currentExecution.stage_outputs).length || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Stage Details */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Stage Execution Details
          </Typography>
          
          <List>
            {Object.entries(currentExecution.stage_outputs).map(([stageId, output], index) => (
              <React.Fragment key={stageId}>
                <ListItem
                  sx={{ cursor: 'pointer' }}
                  onClick={() => setExpandedStage(expandedStage === stageId ? null : stageId)}
                >
                  <ListItemIcon>
                    {output.status === 'completed' ? <CheckCircleIcon color="success" /> : 
                     output.status === 'failed' ? <ErrorIcon color="error" /> : 
                     <ScheduleIcon color="primary" />}
                  </ListItemIcon>
                  <ListItemText
                    primary={stageId}
                    secondary={`Status: ${output.status} • Duration: ${output.execution_time.toFixed(2)}s`}
                  />
                  <IconButton>
                    {expandedStage === stageId ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                  </IconButton>
                </ListItem>
                
                <Collapse in={expandedStage === stageId} timeout="auto" unmountOnExit>
                  <StageExecutionCard stageId={stageId} output={output} />
                </Collapse>
                
                {index < Object.entries(currentExecution.stage_outputs).length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </CardContent>
      </Card>

      {/* Logs Dialog */}
      <Dialog
        open={showLogs}
        onClose={() => setShowLogs(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>Execution Logs</DialogTitle>
        <DialogContent>
          <ExecutionLogs executionId={currentExecution.execution_id} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowLogs(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Artifacts Dialog */}
      <Dialog
        open={showArtifacts}
        onClose={() => setShowArtifacts(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>Generated Artifacts</DialogTitle>
        <DialogContent>
          <ArtifactViewer executionId={currentExecution.execution_id} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowArtifacts(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Approval Dialog */}
      <Dialog open={approvalDialogOpen} onClose={() => setApprovalDialogOpen(false)}>
        <DialogTitle>Approval Required</DialogTitle>
        <DialogContent>
          <Typography sx={{ mb: 2 }}>
            This stage requires approval before proceeding.
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Comments (optional)"
            value={approvalComments}
            onChange={(e) => setApprovalComments(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setApprovalDialogOpen(false)}>Cancel</Button>
          <Button color="error" variant="outlined">
            Reject
          </Button>
          <Button color="primary" variant="contained">
            Approve
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ExecutionMonitor;
