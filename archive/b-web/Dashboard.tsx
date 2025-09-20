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

  if (pipelinesLoading || executionsLoading) {
    return (
      <Box sx={{ width: '100%', mt: 2 }}>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" fontWeight="bold">
          SDLC Pipeline Dashboard
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/pipelines/new')}
        >
          Create Pipeline
        </Button>
      </Box>

      {/* Metrics Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricsCard
            title="Total Pipelines"
            value={pipelines.length.toString()}
            icon={<AssignmentIcon />}
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricsCard
            title="Success Rate"
            value={`${metrics.successRate.toFixed(1)}%`}
            icon={<CheckCircleIcon />}
            color="#4caf50"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricsCard
            title="Running Executions"
            value={metrics.runningExecutions.toString()}
            icon={<SpeedIcon />}
            color="#ff9800"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricsCard
            title="Avg Execution Time"
            value={`${metrics.avgExecutionTime.toFixed(0)}min`}
            icon={<TrendingUpIcon />}
            color="#9c27b0"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Pipelines Overview */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="h2">
                  My Pipelines
                </Typography>
                <Button 
                  size="small" 
                  onClick={() => navigate('/pipelines')}
                >
                  View All
                </Button>
              </Box>
              
              {pipelines.length === 0 ? (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                    No pipelines created yet
                  </Typography>
                  <Button
                    variant="outlined"
                    startIcon={<AddIcon />}
                    onClick={() => navigate('/pipelines/new')}
                  >
                    Create Your First Pipeline
                  </Button>
                </Box>
              ) : (
                <Grid container spacing={2}>
                  {pipelines.slice(0, 6).map((pipeline) => (
                    <Grid item xs={12} sm={6} md={4} key={pipeline.id}>
                      <Card 
                        variant="outlined" 
                        sx={{ 
                          cursor: 'pointer',
                          '&:hover': { boxShadow: 2 }
                        }}
                        onClick={() => navigate(`/pipelines/${pipeline.id}`)}
                      >
                        <CardContent>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                            <Typography variant="h6" component="h3" noWrap>
                              {pipeline.name}
                            </Typography>
                            <IconButton
                              size="small"
                              onClick={(e) => handleMenuClick(e, pipeline)}
                            >
                              <MoreVertIcon />
                            </IconButton>
                          </Box>
                          
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            {pipeline.description}
                          </Typography>
                          
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <Chip 
                              label={`${pipeline.stages.length} stages`} 
                              size="small" 
                              variant="outlined" 
                            />
                            <Typography variant="caption" color="text.secondary">
                              v{pipeline.version}
                            </Typography>
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions & Recent Activity */}
        <Grid item xs={12} lg={4}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <QuickActions />
            </Grid>
            <Grid item xs={12}>
              <RecentExecutions executions={executions.slice(0, 5)} />
            </Grid>
          </Grid>
        </Grid>
      </Grid>

      {/* Pipeline Actions Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={() => selectedPipeline && handleExecutePipeline(selectedPipeline)}>
          <PlayIcon sx={{ mr: 1 }} />
          Execute
        </MenuItem>
        <MenuItem onClick={() => selectedPipeline && handleEditPipeline(selectedPipeline)}>
          Edit
        </MenuItem>
        <MenuItem onClick={() => selectedPipeline && navigate(`/pipelines/${selectedPipeline.id}`)}>
          View Details
        </MenuItem>
        <MenuItem onClick={() => selectedPipeline && navigate(`/executions?pipeline=${selectedPipeline.id}`)}>
          View Executions
        </MenuItem>
      </Menu>
    </Box>
  );
};

export default Dashboard;
