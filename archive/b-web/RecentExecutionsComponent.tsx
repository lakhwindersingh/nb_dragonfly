import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Box
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Pause as PauseIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { PipelineExecution, ExecutionStatus } from '../../types/pipeline';
import { formatDistanceToNow } from 'date-fns';

interface RecentExecutionsProps {
  executions: PipelineExecution[];
}

export const RecentExecutions: React.FC<RecentExecutionsProps> = ({ executions }) => {
  const navigate = useNavigate();

  const getStatusIcon = (status: ExecutionStatus) => {
    switch (status) {
      case ExecutionStatus.COMPLETED:
        return <CheckCircleIcon sx={{ color: 'success.main' }} />;
      case ExecutionStatus.FAILED:
        return <ErrorIcon sx={{ color: 'error.main' }} />;
      case ExecutionStatus.RUNNING:
        return <PlayIcon sx={{ color: 'primary.main' }} />;
      case ExecutionStatus.PAUSED:
        return <PauseIcon sx={{ color: 'warning.main' }} />;
      default:
        return <PlayIcon sx={{ color: 'grey.500' }} />;
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

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
          Recent Executions
        </Typography>
        
        {executions.length === 0 ? (
          <Typography variant="body2" color="text.secondary">
            No recent executions
          </Typography>
        ) : (
          <List disablePadding>
            {executions.map((execution) => (
              <ListItem
                key={execution.execution_id}
                sx={{ 
                  px: 0,
                  cursor: 'pointer',
                  '&:hover': { backgroundColor: 'action.hover' }
                }}
                onClick={() => navigate(`/executions/${execution.execution_id}`)}
              >
                <ListItemIcon sx={{ minWidth: 40 }}>
                  {getStatusIcon(execution.status)}
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2" noWrap>
                        Execution {execution.execution_id.slice(0, 8)}
                      </Typography>
                      <Chip
                        label={execution.status}
                        size="small"
                        color={getStatusColor(execution.status)}
                        variant="outlined"
                      />
                    </Box>
                  }
                  secondary={
                    <Typography variant="caption" color="text.secondary">
                      {formatDistanceToNow(new Date(execution.start_time), { addSuffix: true })}
                    </Typography>
                  }
                />
              </ListItem>
            ))}
          </List>
        )}
      </CardContent>
    </Card>
  );
};
