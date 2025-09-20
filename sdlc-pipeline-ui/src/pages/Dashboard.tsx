import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  LinearProgress,
  IconButton,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Add as AddIcon,
  PlayArrow as PlayIcon,
  MoreVert as MoreVertIcon,
  TrendingUp as TrendingUpIcon,
  Assignment as AssignmentIcon,
  Speed as SpeedIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../hooks/redux';
import { fetchPipelines } from '../../store/slices/pipelinesSlice';
import { fetchExecutions } from '../../store/slices/executionsSlice';
import { PipelineDefinition, PipelineExecution, ExecutionStatus } from '../../types/pipeline';
import { MetricsCard } from './MetricsCard';
import { RecentExecutions } from './RecentExecutions';
import { QuickActions } from './QuickActions';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  
  const { pipelines, loading: pipelinesLoading } = useAppSelector(state => state.pipelines);
  const { executions, loading: executionsLoading } = useAppSelector(state => state.executions);
  
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedPipeline, setSelectedPipeline] = useState<PipelineDefinition | null>(null);

  useEffect(() => {
    dispatch(fetchPipelines());
    dispatch(fetchExecutions());
  }, [dispatch]);

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>, pipeline: PipelineDefinition) => {
    event.stopPropagation();
    setAnchorEl(event.currentTarget);
    setSelectedPipeline(pipeline);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedPipeline(null);
  };

  const handleExecutePipeline = (pipeline: PipelineDefinition) => {
    navigate(`/pipelines/${pipeline.id}/execute`);
    handleMenuClose();
  };

  const handleEditPipeline = (pipeline: PipelineDefinition) => {
    navigate(`/pipelines/${pipeline.id}/edit`);
    handleMenuClose();
  };

  const getStatusColor = (status: ExecutionStatus) => {
    switch (status) {
      case ExecutionStatus.COMPLETED:
        return 'success';
      case ExecutionStatus.RUNNING:
        return 'primary';
      case ExecutionStatus.FAILED:
        return 'error';
      case ExecutionStatus.PAUSED:
        return 'warning';
      default:
        return 'default';
    }
  };

  const getMetrics = () => {
    const totalExecutions = executions.length;
    const completedExecutions = executions.filter(e => e.status === ExecutionStatus.COMPLETED).length;
    const failedExecutions = executions.filter(e => e.status === ExecutionStatus.FAILED).length;
    const runningExecutions = executions.filter(e => e.status === ExecutionStatus.RUNNING).length;
    
    const successRate = totalExecutions > 0 ? (completedExecutions / totalExecutions) * 100 : 0;
    const avgExecutionTime = completedExecutions > 0 
      ? executions
          .filter(e => e.status === ExecutionStatus.COMPLETED && e.end_time)
          .reduce((sum, e) => {
            const startTime = new Date(e.start_time).getTime();
            const endTime = new Date(e.end_time!).getTime();
            return sum + (endTime - startTime);
          }, 0) / completedExecutions / 1000 / 60 // Convert to minutes
      : 0;

    return {
      totalExecutions,
      completedExecutions,
      failedExecutions,
      runningExecutions,
      successRate,
      avgExecutionTime,
    };
  };

  const metrics = getMetrics();

  return (
    <Box>
      <Grid container spacing={3}>
        {/* Metrics Cards */}
        <Grid item xs={12} md={3}>
          <MetricsCard
            title="Total Executions"
            value={String(metrics.totalExecutions)}
            icon={<PlayArrow />}
            color="#1976d2"
            subtitle="All-time"
            trend={{ value: 12, direction: 'up' }}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <MetricsCard
            title="Completed"
            value={String(metrics.completedExecutions)}
            icon={<CheckCircleIcon />}
            color="#2e7d32"
            subtitle={`Success Rate: ${metrics.successRate.toFixed(1)}%`}
            trend={{ value: 5, direction: 'up' }}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <MetricsCard
            title="Failed"
            value={String(metrics.failedExecutions)}
            icon={<AssignmentIcon />}
            color="#c62828"
            subtitle="Last 30 days"
            trend={{ value: 3, direction: 'down' }}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <MetricsCard
            title="Avg Execution Time"
            value={`${metrics.avgExecutionTime.toFixed(1)}m`}
            icon={<SpeedIcon />}
            color="#6a1b9a"
            subtitle="Completed runs"
          />
        </Grid>

        {/* Recent Executions */}
        <Grid item xs={12} md={8}>
          <RecentExecutions executions={executions as PipelineExecution[]} />
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={4}>
          <QuickActions />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
