import * as React from 'react';
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import {
    Box,
    AppBar,
    Toolbar,
    Typography,
    Drawer,
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Container,
    IconButton,
    useTheme,
    useMediaQuery,
} from '@mui/material';
import {
    Dashboard as DashboardIcon,
    AccountTree as PipelineIcon,
    PlayArrow as ExecutionIcon,
    Menu as MenuIcon,
    Settings as SettingsIcon,
} from '@mui/icons-material';
import { store } from './context/storeConfiguration';
import Dashboard from './pages/Dashboard';
import PipelineDesigner from './pages/PipelineDesigner';
import ExecutionMonitor from './pages/ExecutionMonitor';

const theme = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#dc004e',
        },
    },
    typography: {
        fontFamily: [
            'system-ui',
            '-apple-system',
            'Segoe UI',
            'Roboto',
            'Helvetica',
            'Arial',
            'sans-serif',
        ].join(','),
    },
});

const DRAWER_WIDTH = 240;

interface NavigationItem {
    path: string;
    label: string;
    icon: React.ReactElement;
}

const navigationItems: NavigationItem[] = [
    { path: '/', label: 'Dashboard', icon: <DashboardIcon /> },
    { path: '/pipelines', label: 'Pipeline Designer', icon: <PipelineIcon /> },
    { path: '/executions', label: 'Execution Monitor', icon: <ExecutionIcon /> },
];

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));
    const [mobileOpen, setMobileOpen] = React.useState(false);

    const handleDrawerToggle = () => {
        setMobileOpen(!mobileOpen);
    };

    const drawer = (
        <Box>
            <Toolbar>
                <Typography variant="h6" noWrap component="div">
                    SDLC Pipeline
                </Typography>
            </Toolbar>
            <List>
                {navigationItems.map((item) => (
                    <ListItem key={item.path} disablePadding>
                        <ListItemButton
                            onClick={() => {
                                window.location.pathname = item.path;
                                if (isMobile) setMobileOpen(false);
                            }}
                        >
                            <ListItemIcon>{item.icon}</ListItemIcon>
                            <ListItemText primary={item.label} />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>
        </Box>
    );

    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <AppBar
                position="fixed"
                sx={{
                    width: { sm: `calc(100% - ${DRAWER_WIDTH}px)` },
                    ml: { sm: `${DRAWER_WIDTH}px` },
                }}
            >
                <Toolbar>
                    <IconButton
                        color="inherit"
                        aria-label="open drawer"
                        edge="start"
                        onClick={handleDrawerToggle}
                        sx={{ mr: 2, display: { sm: 'none' } }}
                    >
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
                        SDLC Pipeline Management
                    </Typography>
                    <IconButton color="inherit">
                        <SettingsIcon />
                    </IconButton>
                </Toolbar>
            </AppBar>
            <Box
                component="nav"
                sx={{ width: { sm: DRAWER_WIDTH }, flexShrink: { sm: 0 } }}
            >
                <Drawer
                    variant="temporary"
                    open={mobileOpen}
                    onClose={handleDrawerToggle}
                    ModalProps={{
                        keepMounted: true,
                    }}
                    sx={{
                        display: { xs: 'block', sm: 'none' },
                        '& .MuiDrawer-paper': {
                            boxSizing: 'border-box',
                            width: DRAWER_WIDTH,
                        },
                    }}
                >
                    {drawer}
                </Drawer>
                <Drawer
                    variant="permanent"
                    sx={{
                        display: { xs: 'none', sm: 'block' },
                        '& .MuiDrawer-paper': {
                            boxSizing: 'border-box',
                            width: DRAWER_WIDTH,
                        },
                    }}
                    open
                >
                    {drawer}
                </Drawer>
            </Box>
            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    p: 3,
                    width: { sm: `calc(100% - ${DRAWER_WIDTH}px)` },
                }}
            >
                <Toolbar />
                <Container maxWidth="xl">
                    {children}
                </Container>
            </Box>
        </Box>
    );
};

const App: React.FC = () => {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Provider store={store}>
                <Router>
                    <Layout>
                        <Routes>
                            <Route path="/" element={<Dashboard />} />
                            <Route path="/dashboard" element={<Navigate to="/" replace />} />
                            <Route path="/pipelines" element={<PipelineDesigner />} />
                            <Route path="/pipelines/:id" element={<PipelineDesigner />} />
                            <Route path="/pipelines/new" element={<PipelineDesigner />} />
                            <Route path="/executions" element={<ExecutionMonitor />} />
                            <Route path="/executions/:executionId" element={<ExecutionMonitor />} />
                            <Route path="*" element={<Navigate to="/" replace />} />
                        </Routes>
                    </Layout>
                </Router>
            </Provider>
        </ThemeProvider>
    );
};

const container = document.getElementById('root');
if (!container) {
    throw new Error('Root element not found: #root');
}

const root = createRoot(container);
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);