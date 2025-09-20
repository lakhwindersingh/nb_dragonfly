import React from 'react';
import { Card, CardContent, Typography, Box, Avatar } from '@mui/material';

interface MetricsCardProps {
  title: string;
  value: string;
  icon: React.ReactNode;
  color: string;
  subtitle?: string;
  trend?: {
    value: number;
    direction: 'up' | 'down';
  };
}

export const MetricsCard: React.FC<MetricsCardProps> = ({
  title,
  value,
  icon,
  color,
  subtitle,
  trend
}) => {
  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box>
            <Typography variant="h4" component="div" fontWeight="bold">
              {value}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              {title}
            </Typography>
            {subtitle && (
              <Typography variant="caption" color="text.secondary">
                {subtitle}
              </Typography>
            )}
          </Box>
          <Avatar sx={{ backgroundColor: color, width: 56, height: 56 }}>
            {icon}
          </Avatar>
        </Box>
        
        {trend && (
          <Box sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
            <Typography
              variant="body2"
              color={trend.direction === 'up' ? 'success.main' : 'error.main'}
            >
              {trend.direction === 'up' ? '↗' : '↘'} {Math.abs(trend.value)}%
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
              vs last period
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};
