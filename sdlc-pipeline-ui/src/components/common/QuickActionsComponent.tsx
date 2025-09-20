import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  Add as AddIcon,
  PlayArrow as PlayIcon,
  Assignment as AssignmentIcon,
  Settings as SettingsIcon,
  Help as HelpIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

export const QuickActions: React.FC = () => {
  const navigate = useNavigate();

  const actions = [
    {
      title: 'Create Pipeline',
      description: 'Start with a new pipeline',
      icon: <AddIcon />,
      onClick: () => navigate('/pipelines/new'),
    },
    {
      title: 'View Templates',
      description: 'Browse pipeline templates',
      icon: <AssignmentIcon />,
      onClick: () => navigate('/templates'),
    },
    {
      title: 'Repository Settings',
      description: 'Configure integrations',
      icon: <SettingsIcon />,
      onClick: () => navigate('/settings/repositories'),
    },
    {
      title: 'Documentation',
      description: 'Learn more about pipelines',
      icon: <HelpIcon />,
      onClick: () => window.open('/docs', '_blank'),
    },
  ];

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
          Quick Actions
        </Typography>
        
        <List disablePadding>
          {actions.map((action, index) => (
            <ListItem key={index} disablePadding>
              <ListItemButton onClick={action.onClick}>
                <ListItemIcon>{action.icon}</ListItemIcon>
                <ListItemText
                  primary={action.title}
                  secondary={action.description}
                />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};
