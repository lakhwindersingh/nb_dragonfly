import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { PipelineExecution } from '../../types/pipeline';
import apiService from '../../services/api/APIService';

interface ExecutionsState {
  executions: PipelineExecution[];
  currentExecution: PipelineExecution | null;
  loading: boolean;
  error: string | null;
}

const initialState: ExecutionsState = {
  executions: [],
  currentExecution: null,
  loading: false,
  error: null,
};

export const fetchExecutions = createAsyncThunk(
  'executions/fetchExecutions',
  async (pipelineId?: string) => {
    const response = await apiService.getExecutions(pipelineId);
    return response;
  }
);

export const fetchExecution = createAsyncThunk(
  'executions/fetchExecution',
  async (executionId: string) => {
    const response = await apiService.getExecution(executionId);
    return response;
  }
);

export const pauseExecution = createAsyncThunk(
  'executions/pauseExecution',
  async (executionId: string) => {
    await apiService.pauseExecution(executionId);
    const response = await apiService.getExecution(executionId);
    return response;
  }
);

export const resumeExecution = createAsyncThunk(
  'executions/resumeExecution',
  async (executionId: string) => {
    await apiService.resumeExecution(executionId);
    const response = await apiService.getExecution(executionId);
    return response;
  }
);

export const cancelExecution = createAsyncThunk(
  'executions/cancelExecution',
  async (executionId: string) => {
    await apiService.cancelExecution(executionId);
    const response = await apiService.getExecution(executionId);
    return response;
  }
);

const executionsSlice = createSlice({
  name: 'executions',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchExecutions.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchExecutions.fulfilled, (state, action: PayloadAction<PipelineExecution[]>) => {
        state.loading = false;
        state.executions = action.payload;
      })
      .addCase(fetchExecutions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch executions';
      })
      .addCase(fetchExecution.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchExecution.fulfilled, (state, action: PayloadAction<PipelineExecution>) => {
        state.loading = false;
        state.currentExecution = action.payload;
      })
      .addCase(fetchExecution.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch execution';
      })
      .addCase(pauseExecution.fulfilled, (state, action: PayloadAction<PipelineExecution>) => {
        state.currentExecution = action.payload;
      })
      .addCase(resumeExecution.fulfilled, (state, action: PayloadAction<PipelineExecution>) => {
        state.currentExecution = action.payload;
      })
      .addCase(cancelExecution.fulfilled, (state, action: PayloadAction<PipelineExecution>) => {
        state.currentExecution = action.payload;
      });
  },
});

export default executionsSlice.reducer;
