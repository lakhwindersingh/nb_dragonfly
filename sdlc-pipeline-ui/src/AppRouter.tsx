import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { Provider } from 'react-redux';
import { store } from './store';
import { AppLayout } from './components/Layout/AppLayout';
import Dashboard from './components/Dashboard/Dashboard';
import PipelineDesigner from './components/PipelineDesigner/PipelineDesigner';
import ExecutionMonitor from './components/ExecutionMonitor/ExecutionMonitor';
import PipelineList from './components/PipelineList/PipelineList';
import ExecutionList from './components/ExecutionList/ExecutionList';
import RepositorySettings from './components/Settings/RepositorySettings';
import Templates from './components/Templates/Templates';
import websocketService from './services/websocket';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          borderRadius: 8,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
  },
});

function App() {
  useEffect(() => {
    // Initialize WebSocket connection
    websocketService.connect();
    
    return () => {
      websocketService.disconnect();
    };
  }, []);

  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <AppLayout>
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/pipelines" element={<PipelineList />} />
              <Route path="/pipelines/new" element={<PipelineDesigner />} />
              <Route path="/pipelines/:id" element={<PipelineDesigner />} />
              <Route path="/pipelines/:id/edit" element={<PipelineDesigner />} />
              <Route path="/pipelines/:id/execute" element={<ExecutionMonitor />} />
              <Route path="/executions" element={<ExecutionList />} />
              <Route path="/executions/:executionId" element={<ExecutionMonitor />} />
              <Route path="/templates" element={<Templates />} />
              <Route path="/settings/repositories" element={<RepositorySettings />} />
            </Routes>
          </AppLayout>
        </Router>
      </ThemeProvider>
    </Provider>
  );
}

export default App;
