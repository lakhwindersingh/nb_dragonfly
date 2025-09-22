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

  if (!currentExecution) {
    return (
      <Box sx={{ p: 2 }}>
        <Typography>Loading execution details...</Typography>
        <LinearProgress sx={{ mt: 2 }} />
      </Box>
    );
  }

  return (
    <Box>
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h6">Execution Details</Typography>
              <Typography variant="body2" color="text.secondary">
                ID: {currentExecution.execution_id}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Started: {format(new Date(currentExecution.start_time), 'PPpp')}
              </Typography>
              {currentExecution.end_time && (
                <Typography variant="body2" color="text.secondary">
                  Ended: {format(new Date(currentExecution.end_time), 'PPpp')}
                </Typography>
              )}
            </Grid>
            <Grid item xs={12} md={6}>
              <Grid container spacing={1} justifyContent="flex-end">
                <Grid item>
                  <Chip label={currentExecution.status} color={getStatusColor(currentExecution.status)} />
                </Grid>
                <Grid item>
                  <IconButton onClick={handleRefresh}><RefreshIcon /></IconButton>
                </Grid>
                <Grid item>
                  {currentExecution.status === ExecutionStatus.RUNNING ? (
                    <IconButton onClick={handlePause}><PauseIcon /></IconButton>
                  ) : (
                    <IconButton onClick={handleResume}><PlayIcon /></IconButton>
                  )}
                </Grid>
                <Grid item>
                  <IconButton color="error" onClick={handleCancel}><StopIcon /></IconButton>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Placeholder for stage execution details, logs, and artifacts */}
      <Typography variant="body2" color="text.secondary">
        Stage and log details components would be rendered here.
      </Typography>
    </Box>
  );
};

export default ExecutionMonitor;
