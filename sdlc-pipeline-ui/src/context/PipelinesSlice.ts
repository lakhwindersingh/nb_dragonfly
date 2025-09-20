import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { PipelineDefinition, UserInputs } from '../../types/pipeline';
import apiService from '../../services/api';

interface PipelinesState {
  pipelines: PipelineDefinition[];
  currentPipeline: PipelineDefinition | null;
  templates: PipelineDefinition[];
  loading: boolean;
  error: string | null;
  creating: boolean;
  executing: boolean;
}

const initialState: PipelinesState = {
  pipelines: [],
  currentPipeline: null,
  templates: [],
  loading: false,
  error: null,
  creating: false,
  executing: false,
};

// Async thunks
export const fetchPipelines = createAsyncThunk(
  'pipelines/fetchPipelines',
  async () => {
    const response = await apiService.getPipelines();
    return response;
  }
);

export const fetchPipeline = createAsyncThunk(
  'pipelines/fetchPipeline',
  async (pipelineId: string) => {
    const response = await apiService.getPipeline(pipelineId);
    return response;
  }
);

export const createPipeline = createAsyncThunk(
  'pipelines/createPipeline',
  async (pipeline: PipelineDefinition) => {
    const pipelineId = await apiService.createPipeline(pipeline);
    const createdPipeline = await apiService.getPipeline(pipelineId);
    return createdPipeline;
  }
);

export const updatePipeline = createAsyncThunk(
  'pipelines/updatePipeline',
  async ({ pipelineId, pipeline }: { pipelineId: string; pipeline: PipelineDefinition }) => {
    await apiService.updatePipeline(pipelineId, pipeline);
    const updatedPipeline = await apiService.getPipeline(pipelineId);
    return updatedPipeline;
  }
);

export const deletePipeline = createAsyncThunk(
  'pipelines/deletePipeline',
  async (pipelineId: string) => {
    await apiService.deletePipeline(pipelineId);
    return pipelineId;
  }
);

export const duplicatePipeline = createAsyncThunk(
  'pipelines/duplicatePipeline',
  async ({ pipelineId, newName }: { pipelineId: string; newName: string }) => {
    const newPipelineId = await apiService.duplicatePipeline(pipelineId, newName);
    const duplicatedPipeline = await apiService.getPipeline(newPipelineId);
    return duplicatedPipeline;
  }
);

export const executePipeline = createAsyncThunk(
  'pipelines/executePipeline',
  async ({ pipelineId, userInputs, options }: { 
    pipelineId: string; 
    userInputs: UserInputs; 
    options?: any 
  }) => {
    const executionId = await apiService.executePipeline(pipelineId, userInputs, options);
    return executionId;
  }
);

export const fetchTemplates = createAsyncThunk(
  'pipelines/fetchTemplates',
  async () => {
    const response = await apiService.getTemplates();
    return response;
  }
);

export const createFromTemplate = createAsyncThunk(
  'pipelines/createFromTemplate',
  async ({ templateId, projectName }: { templateId: string; projectName: string }) => {
    const pipelineId = await apiService.createFromTemplate(templateId, projectName);
    const createdPipeline = await apiService.getPipeline(pipelineId);
    return createdPipeline;
  }
);

const pipelinesSlice = createSlice({
  name: 'pipelines',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchPipelines.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchPipelines.fulfilled, (state, action: PayloadAction<PipelineDefinition[]>) => {
        state.loading = false;
        state.pipelines = action.payload;
      })
      .addCase(fetchPipelines.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch pipelines';
      })
      .addCase(fetchPipeline.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchPipeline.fulfilled, (state, action: PayloadAction<PipelineDefinition>) => {
        state.loading = false;
        state.currentPipeline = action.payload;
      })
      .addCase(fetchPipeline.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch pipeline';
      })
      .addCase(createPipeline.pending, (state) => {
        state.creating = true;
      })
      .addCase(createPipeline.fulfilled, (state, action: PayloadAction<PipelineDefinition>) => {
        state.creating = false;
        state.pipelines.push(action.payload);
        state.currentPipeline = action.payload;
      })
      .addCase(createPipeline.rejected, (state, action) => {
        state.creating = false;
        state.error = action.error.message || 'Failed to create pipeline';
      })
      .addCase(updatePipeline.fulfilled, (state, action: PayloadAction<PipelineDefinition>) => {
        const idx = state.pipelines.findIndex(p => p.id === action.payload.id);
        if (idx !== -1) state.pipelines[idx] = action.payload;
        state.currentPipeline = action.payload;
      })
      .addCase(deletePipeline.fulfilled, (state, action: PayloadAction<string>) => {
        state.pipelines = state.pipelines.filter(p => p.id !== action.payload);
        if (state.currentPipeline?.id === action.payload) state.currentPipeline = null;
      })
      .addCase(duplicatePipeline.fulfilled, (state, action: PayloadAction<PipelineDefinition>) => {
        state.pipelines.push(action.payload);
      });
  },
});

export const { clearError } = pipelinesSlice.actions;
export default pipelinesSlice.reducer;
