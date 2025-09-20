export interface PipelineDefinition {
  id?: string;
  name: string;
  version: string;
  description: string;
  stages: StageDefinition[];
  global_config: GlobalConfig;
  created_at?: string;
  updated_at?: string;
  created_by?: string;
}

export interface StageDefinition {
  id: string;
  type: StageType;
  name: string;
  description: string;
  dependencies: string[];
  ai_config: AIConfig;
  prompt_template: string;
  validation_rules: ValidationRule[];
  repositories: RepositoryConfig[];
  timeout_minutes: number;
  approval_required: boolean;
  reviewers: string[];
  parallel_execution?: boolean;
  retry_policy?: RetryPolicy;
}

export enum StageType {
  PLANNING = 'planning',
  REQUIREMENTS = 'requirements',
  DESIGN = 'design',
  IMPLEMENTATION = 'implementation',
  TESTING = 'testing',
  DEPLOYMENT = 'deployment',
  MAINTENANCE = 'maintenance'
}

export interface AIConfig {
  model: string;
  temperature: number;
  max_tokens: number;
  additional_inputs?: Record<string, any>;
}

export interface ValidationRule {
  rule: string;
  description: string;
  severity?: 'error' | 'warning' | 'info';
}

export interface RepositoryConfig {
  type: RepositoryType;
  name: string;
  artifact_mappings: ArtifactMapping[];
  config?: Record<string, any>;
}

export enum RepositoryType {
  GIT = 'git',
  CONFLUENCE = 'confluence',
  SHAREPOINT = 'sharepoint',
  JIRA = 'jira'
}

export interface ArtifactMapping {
  output_key: string;
  artifact_name: string;
  artifact_type: string;
  transformation_script?: TransformationScript;
}

export interface TransformationScript {
  type: string;
  script: string;
}

export interface RetryPolicy {
  max_retries: number;
  retry_delay_seconds?: number;
}

export interface GlobalConfig {
  retry_policy: RetryPolicy;
  notification_config: NotificationConfig;
  artifact_retention: ArtifactRetention;
  security_config: SecurityConfig;
}

export interface NotificationConfig {
  email_notifications: boolean;
  slack_notifications: boolean;
  webhook_notifications: boolean;
}

export interface ArtifactRetention {
  days: number;
  backup_strategy: string;
}

export interface SecurityConfig {
  encrypt_artifacts: boolean;
  access_logging: boolean;
  compliance_validation: boolean;
}

export interface PipelineExecution {
  execution_id: string;
  pipeline_id: string;
  status: ExecutionStatus;
  current_stage?: string;
  completed_stages: string[];
  start_time: string;
  end_time?: string;
  progress: number;
  user_inputs: Record<string, any>;
  stage_outputs: Record<string, StageOutput>;
  error_message?: string;
}

export enum ExecutionStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
  PAUSED = 'paused',
  CANCELLED = 'cancelled'
}

export interface StageOutput {
  outputs: Record<string, any>;
  validation: ValidationResult;
  repositories: Record<string, RepositoryResult>;
  execution_time: number;
  status: string;
  error?: string;
}

export interface ValidationResult {
  passed: boolean;
  errors: string[];
  warnings: string[];
  score?: number;
}

export interface RepositoryResult {
  status: string;
  stored_files?: any[];
  stored_pages?: any[];
  created_issues?: any[];
  error?: string;
}

export interface UserInputs {
  project_name: string;
  business_domain: string;
  target_users: string;
  technology_preferences: string;
  timeline_months: number;
  budget_range: string;
  [key: string]: any;
}

export interface ApprovalRequest {
  id: string;
  execution_id: string;
  stage_id: string;
  stage_name: string;
  outputs: Record<string, any>;
  reviewers: string[];
  created_at: string;
  status: 'pending' | 'approved' | 'rejected';
  approver?: string;
  approved_at?: string;
  comments?: string;
}
