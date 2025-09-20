import { configureStore } from '@reduxjs/toolkit';
import pipelinesReducer from './slices/pipelinesSlice';
import executionsReducer from './slices/executionsSlice';
import appReducer from './slices/appSlice';
import repositoriesReducer from './slices/repositoriesSlice';
import approvalsReducer from './slices/approvalsSlice';

export const store = configureStore({
  reducer: {
    app: appReducer,
    pipelines: pipelinesReducer,
    executions: executionsReducer,
    repositories: repositoriesReducer,
    approvals: approvalsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
