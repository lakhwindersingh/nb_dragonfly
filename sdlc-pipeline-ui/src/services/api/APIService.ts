import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { 
  PipelineDefinition, 
  PipelineExecution, 
  UserInputs, 
  ApprovalRequest,
  RepositoryType 
} from '../types/pipeline';

class APIService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for auth
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        (config.headers as any).Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Pipeline Management
  async createPipeline(pipeline: PipelineDefinition): Promise<string> {
    const response: AxiosResponse<{ pipeline_id: string }> = await this.client.post('/api/pipelines', pipeline);
    return response.data.pipeline_id;
  }

  async getPipelines(): Promise<PipelineDefinition[]> {
    const response: AxiosResponse<{ pipelines: PipelineDefinition[] }> = await this.client.get('/api/pipelines');
    return response.data.pipelines;
  }

  async getPipeline(pipelineId: string): Promise<PipelineDefinition> {
    const response: AxiosResponse<PipelineDefinition> = await this.client.get(`/api/pipelines/${pipelineId}`);
    return response.data;
  }

  async updatePipeline(pipelineId: string, pipeline: PipelineDefinition): Promise<void> {
    await this.client.put(`/api/pipelines/${pipelineId}`, pipeline);
  }

  async deletePipeline(pipelineId: string): Promise<void> {
    await this.client.delete(`/api/pipelines/${pipelineId}`);
  }

  async duplicatePipeline(pipelineId: string, newName: string): Promise<string> {
    const response: AxiosResponse<{ pipeline_id: string }> = await this.client.post(`/api/pipelines/${pipelineId}/duplicate`, {
      name: newName
    });
    return response.data.pipeline_id;
  }

  // Pipeline Execution
  async executePipeline(pipelineId: string, userInputs: UserInputs, options?: any): Promise<string> {
    const response: AxiosResponse<{ execution_id: string }> = await this.client.post(`/api/pipelines/${pipelineId}/execute`, {
      user_inputs: userInputs,
      execution_options: options
    });
    return response.data.execution_id;
  }

  async getExecutions(pipelineId?: string): Promise<PipelineExecution[]> {
    const url = pipelineId ? `/api/executions?pipeline_id=${pipelineId}` : '/api/executions';
    const response: AxiosResponse<{ executions: PipelineExecution[] }> = await this.client.get(url);
    return response.data.executions;
  }

  async getExecution(executionId: string): Promise<PipelineExecution> {
    const response: AxiosResponse<PipelineExecution> = await this.client.get(`/api/executions/${executionId}`);
    return response.data;
  }

  async pauseExecution(executionId: string): Promise<void> {
    await this.client.post(`/api/executions/${executionId}/pause`);
  }

  async resumeExecution(executionId: string): Promise<void> {
    await this.client.post(`/api/executions/${executionId}/resume`);
  }

  async cancelExecution(executionId: string): Promise<void> {
    await this.client.post(`/api/executions/${executionId}/cancel`);
  }

  // Approval Management
  async getApprovalRequests(executionId?: string): Promise<ApprovalRequest[]> {
    const url = executionId ? `/api/approvals?execution_id=${executionId}` : '/api/approvals';
    const response: AxiosResponse<{ approvals: ApprovalRequest[] }> = await this.client.get(url);
    return response.data.approvals;
  }

  async approveRequest(approvalId: string, comments?: string): Promise<void> {
    await this.client.post(`/api/approvals/${approvalId}/approve`, { comments });
  }

  async rejectRequest(approvalId: string, comments?: string): Promise<void> {
    await this.client.post(`/api/approvals/${approvalId}/reject`, { comments });
  }

  // Templates
  async getTemplates(): Promise<PipelineDefinition[]> {
    const response: AxiosResponse<{ templates: PipelineDefinition[] }> = await this.client.get('/api/templates');
    return response.data.templates;
  }

  async createFromTemplate(templateId: string, projectName: string): Promise<string> {
    const response: AxiosResponse<{ pipeline_id: string }> = await this.client.post(`/api/templates/${templateId}/create`, {
      project_name: projectName
    });
    return response.data.pipeline_id;
  }

  // Repository management
  async testRepositoryConnection(type: RepositoryType, config: Record<string, any>): Promise<{ success: boolean; message?: string }> {
    const response: AxiosResponse<{ success: boolean; message?: string }> = await this.client.post(`/api/repositories/test/${type}` , config);
    return response.data;
  }

  async saveRepositoryConfig(type: RepositoryType, name: string, config: Record<string, any>): Promise<void> {
    await this.client.post(`/api/repositories/${type}/save`, { name, config });
  }
}

const apiService = new APIService();
export default apiService;
