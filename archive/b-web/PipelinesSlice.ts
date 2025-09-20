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
    setCurrentPipeline: (state, action: PayloadAction<PipelineDefinition | null>) => {
      state.currentPipeline = action.payload;
    },
    updateCurrentPipeline: (state, action: PayloadAction<Partial<PipelineDefinition>>) => {
      if (state.currentPipeline) {
        state.currentPipeline = { ...state.currentPipeline, ...action.payload };
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch pipelines
      .addCase(fetchPipelines.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPipelines.fulfilled, (state, action) => {
        state.loading = false;
        state.pipelines = action.payload;
      })
      .addCase(fetchPipelines.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch pipelines';
      })
      
      // Fetch single pipeline
      .addCase(fetchPipeline.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPipeline.fulfilled, (state, action) => {
        state.loading = false;
        state.currentPipeline = action.payload;
      })
      .addCase(fetchPipeline.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch pipeline';
      })
      
      // Create pipeline
      .addCase(createPipeline.pending, (state) => {
        state.creating = true;
        state.error = null;
      })
      .addCase(createPipeline.fulfilled, (state, action) => {
        state.creating = false;
        state.pipelines.push(action.payload);
        state.currentPipeline = action.payload;
      })
      .addCase(createPipeline.rejected, (state, action) => {
        state.creating = false;
        state.error = action.error.message || 'Failed to create pipeline';
      })
      
      // Update pipeline
      .addCase(updatePipeline.fulfilled, (state, action) => {
        const index = state.pipelines.findIndex(p => p.id === action.payload.id);
        if (index !== -1) {
          state.pipelines[index] = action.payload;
        }
        state.currentPipeline = action.payload;
      })
      .addCase(updatePipeline.rejected, (state, action) => {
        state.error = action.error.message || 'Failed to update pipeline';
      })
      
      // Delete pipeline
      .addCase(deletePipeline.fulfilled, (state, action) => {
        state.pipelines = state.pipelines.filter(p => p.id !== action.payload);
        if (state.currentPipeline?.id === action.payload) {
          state.currentPipeline = null;
        }
      })
      .addCase(deletePipeline.rejected, (state, action) => {
        state.error = action.error.message || 'Failed to delete pipeline';
      })
      
      // Duplicate pipeline
      .addCase(duplicatePipeline.fulfilled, (state, action) => {
        state.pipelines.push(action.payload);
      })
      .addCase(duplicatePipeline.rejected, (state, action) => {
        state.error = action.error.message || 'Failed to duplicate pipeline';
      })
      
      // Execute pipeline
      .addCase(executePipeline.pending, (state) => {
        state.executing = true;
        state.error = null;
      })
      .addCase(executePipeline.fulfilled, (state) => {
        state.executing = false;
      })
      .addCase(executePipeline.rejected, (state, action) => {
        state.executing = false;
        state.error = action.error.message || 'Failed to execute pipeline';
      })
      
      // Fetch templates
      .addCase(fetchTemplates.fulfilled, (state, action) => {
        state.templates = action.payload;
      })
      
      // Create from template
      .addCase(createFromTemplate.fulfilled, (state, action) => {
        state.pipelines.push(action.payload);
        state.currentPipeline = action.payload;
      });
  },
});

export const { clearError, setCurrentPipeline, updateCurrentPipeline } = pipelinesSlice.actions;
export default pipelinesSlice.reducer;
