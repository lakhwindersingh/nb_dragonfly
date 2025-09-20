import { io, Socket } from 'socket.io-client';
import { PipelineExecution, ExecutionStatus } from '../types/pipeline';

export interface WebSocketEvents {
  executionUpdate: (execution: PipelineExecution) => void;
  stageCompleted: (data: { executionId: string; stageId: string; output: any }) => void;
  approvalRequired: (data: { executionId: string; approvalId: string; stageId: string }) => void;
  systemAlert: (data: { type: string; message: string; severity: string }) => void;
}

class WebSocketService {
  private socket: Socket | null = null;
  private listeners: Map<string, Set<Function>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  connect(): void {
    if (this.socket?.connected) {
      return;
    }

    const token = localStorage.getItem('auth_token');
    
    this.socket = io(process.env.REACT_APP_WS_URL || 'ws://localhost:8000', {
      auth: {
        token
      },
      transports: ['websocket', 'polling']
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    });

    this.socket.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason);
      if (reason === 'io server disconnect') {
        // Server initiated disconnect, don't reconnect automatically
        return;
      }
      this.handleReconnection();
    });

    this.socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      this.handleReconnection();
    });

    // Pipeline execution updates
    this.socket.on('execution_status', (data: PipelineExecution) => {
      this.emit('executionUpdate', data);
    });

    // Stage completion notifications
    this.socket.on('stage_completed', (data: any) => {
      this.emit('stageCompleted', data);
    });

    // Approval requests
    this.socket.on('approval_required', (data: any) => {
      this.emit('approvalRequired', data);
    });

    // System alerts
    this.socket.on('system_alert', (data: any) => {
      this.emit('systemAlert', data);
    });

    // Error handling
    this.socket.on('error', (error: any) => {
      console.error('WebSocket error:', error);
    });
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
    this.listeners.clear();
  }

  private handleReconnection(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      
      setTimeout(() => {
        console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        this.connect();
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
      this.emit('systemAlert', {
        type: 'connection_error',
        message: 'Lost connection to server. Please refresh the page.',
        severity: 'error'
      });
    }
  }

  // Event subscription management
  on<K extends keyof WebSocketEvents>(event: K, callback: WebSocketEvents[K]): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
  }

  off<K extends keyof WebSocketEvents>(event: K, callback: WebSocketEvents[K]): void {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.delete(callback);
    }
  }

  private emit(event: string, data: any): void {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error('Error in WebSocket event callback:', error);
        }
      });
    }
  }

  // Pipeline-specific methods
  subscribeToExecution(executionId: string): void {
    if (this.socket?.connected) {
      this.socket.emit('subscribe_execution', { executionId });
    }
  }

  unsubscribeFromExecution(executionId: string): void {
    if (this.socket?.connected) {
      this.socket.emit('unsubscribe_execution', { executionId });
    }
  }

  subscribeToPipeline(pipelineId: string): void {
    if (this.socket?.connected) {
      this.socket.emit('subscribe_pipeline', { pipelineId });
    }
  }

  unsubscribeFromPipeline(pipelineId: string): void {
    if (this.socket?.connected) {
      this.socket.emit('unsubscribe_pipeline', { pipelineId });
    }
  }

  // Send messages to server
  requestExecutionUpdate(executionId: string): void {
    if (this.socket?.connected) {
      this.socket.emit('get_execution_status', { executionId });
    }
  }

  sendApprovalResponse(approvalId: string, approved: boolean, comments?: string): void {
    if (this.socket?.connected) {
      this.socket.emit('approval_response', { approvalId, approved, comments });
    }
  }

  // Connection status
  isConnected(): boolean {
    return this.socket?.connected || false;
  }

  getConnectionState(): string {
    if (!this.socket) return 'disconnected';
    return this.socket.connected ? 'connected' : 'connecting';
  }
}

export const websocketService = new WebSocketService();
export default websocketService;
