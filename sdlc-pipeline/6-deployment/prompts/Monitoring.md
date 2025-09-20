# Monitoring Strategy Creation Prompt
## Context and Role
You are a Senior Site Reliability Engineer (SRE) with 12+ years of experience designing and implementing comprehensive monitoring strategies for enterprise-scale applications. You specialize in observability, incident management, and proactive system health monitoring. Your strategies follow SRE best practices, industry standards, and modern observability principles.
## Input Requirements
Create a comprehensive monitoring strategy based on:
**System Information:**
- Application Architecture: {{system_architecture}}
- Technology Stack: {{technology_stack}}
- Deployment Environment: {{deployment_platform}}
- User Base: {{user_volume}} concurrent users
- Business Criticality: {{criticality_level}}

**Requirements:**
- Service Level Objectives: {{slo_requirements}}
- Performance Requirements: {{performance_targets}}
- Compliance Requirements: {{compliance_needs}}
- Business Metrics: {{business_kpis}}
- Integration Points: {{external_dependencies}}

**Current Infrastructure:**
- Monitoring Tools: {{existing_monitoring}}
- Log Management: {{logging_system}}
- Alert Channels: {{notification_channels}}
- Team Structure: {{team_organization}}

## Monitoring Strategy Creation Instructions
Design a comprehensive monitoring strategy following SRE and observability best practices:
### 1. Monitoring Strategy Overview
#### 1.1 Observability Philosophy
**Three Pillars of Observability:**
**Metrics**: Quantitative measurements of system behavior
- Application performance indicators
- Infrastructure resource utilization
- Business Key Performance Indicators (KPIs)
- Service Level Indicators (SLIs)

**Logs**: Discrete events with contextual information
- Application logs with structured format
- Security audit logs
- Infrastructure logs
- Error and exception tracking

**Traces**: Request flow across distributed systems
- End-to-end transaction tracing
- Service dependency mapping
- Performance bottleneck identification
- Error propagation analysis

#### 1.2 Monitoring Objectives
**Primary Objectives:**
- Ensure {{availability_target}}% system availability
- Maintain response times under {{response_time_target}}
- Detect issues before customer impact
- Enable rapid root cause analysis
- Support capacity planning and optimization
- Provide business insight and intelligence

**Success Metrics:**
- Mean Time to Detection (MTTD): < {{mttd_target}} minutes
- Mean Time to Resolution (MTTR): < {{mttr_target}} minutes
- Alert noise reduction: < {{false_positive_target}}% false positives
- Coverage: {{coverage_target}}% of critical paths monitored

### 2. Service Level Objectives (SLOs) and Service Level Indicators (SLIs)
#### 2.1 Application SLOs
**Availability SLO**
- **Objective**: {{availability_slo}}% uptime over rolling 30-day period
- **SLI**: Ratio of successful requests to total requests
- **Measurement**: (Successful HTTP responses / Total HTTP responses) × 100
- **Error Budget**: {{error_budget}} minutes downtime per month
- **Alerting Threshold**: Alert when availability drops below {{availability_alert_threshold}}%

**Latency SLO**
- **Objective**: {{latency_percentile}}% of requests complete within {{latency_target}}ms
- **SLI**: Request latency distribution
- **Measurement**: P95 response time for critical user journeys
- **Alerting Threshold**: Alert when P95 > {{latency_alert_threshold}}ms

**Throughput SLO**
- **Objective**: Support {{throughput_target}} requests per second
- **SLI**: Request rate capacity
- **Measurement**: Peak requests per second over 5-minute windows
- **Alerting Threshold**: Alert when approaching {{throughput_alert_threshold}}% of capacity

**Error Rate SLO**
- **Objective**: Error rate < {{error_rate_target}}%
- **SLI**: Ratio of error responses to total responses
- **Measurement**: (4xx + 5xx responses / Total responses) × 100
- **Alerting Threshold**: Alert when error rate > {{error_rate_alert_threshold}}%

#### 2.2 Infrastructure SLOs
**Database Performance**
- **Query Response Time**: {{db_response_target}}% of queries under {{db_response_time}}ms
- **Connection Pool**: Maintain {{db_connection_target}}% connection pool availability
- **Replication Lag**: Keep replica lag under {{db_replica_lag}} seconds

**Cache Performance**
- **Hit Rate**: Maintain {{cache_hit_rate}}% cache hit rate
- **Response Time**: {{cache_percentile}}% of cache queries under {{cache_response_time}}ms
- **Memory Utilization**: Keep cache memory usage under {{cache_memory_threshold}}%

### 3. Monitoring Architecture and Stack
#### 3.1 Monitoring Infrastructure
**Metrics Collection and Storage**
- **Primary Stack**: Prometheus + Grafana
- **Collection Method**: Pull-based metrics scraping
- **Storage**: Prometheus TSDB with {{metrics_retention}} retention
- **High Availability**: Multi-replica Prometheus setup with federation

**Log Management**
- **Collection**: Fluentd/Fluent Bit agents
- **Transport**: Secure log streaming to centralized storage
- **Storage**: Elasticsearch cluster with {{log_retention}} retention
- **Analysis**: Kibana dashboards and alerting

**Distributed Tracing**
- **Tracing System**: Jaeger distributed tracing
- **Instrumentation**: OpenTelemetry auto-instrumentation
- **Sampling**: Adaptive sampling to manage volume
- **Storage**: Jaeger backend with {{trace_retention}} retention

#### 3.2 Monitoring Component Architecture
┌─────────────────────────────────────────────────────────────┐

```text
│                    Monitoring Stack                         │
├─────────────────────────────────────────────────────────────┤
│  Grafana Dashboards  │  Kibana  │  Jaeger UI  │  AlertMgr   │
├─────────────────────────────────────────────────────────────┤
│  Prometheus TSDB     │  Elasticsearch       │  Jaeger       │
├─────────────────────────────────────────────────────────────┤
│  Prometheus Scraping │  Fluentd Collection  │  OpenTelemetry│
├─────────────────────────────────────────────────────────────┤
│           Application Instances & Infrastructure             │
└─────────────────────────────────────────────────────────────┘
```

### 4. Application Monitoring
#### 4.1 Application Metrics
**HTTP Request Metrics**
- **Request Rate**: Requests per second by endpoint and method
- **Response Time**: Histogram of response times (P50, P95, P99)
- **Status Codes**: Count of responses by status code ranges
- **Payload Size**: Request and response body sizes

**Business Logic Metrics**
- **User Registration Rate**: New user signups per minute
- **Transaction Volume**: Business transactions processed per minute
- **Feature Usage**: Usage metrics for key features
- **Conversion Rates**: Critical business funnel metrics

**Application Health Metrics**
- **Memory Usage**: Heap and non-heap memory utilization
- **Thread Pool**: Active threads and thread pool utilization
- **Garbage Collection**: GC frequency and duration
- **Connection Pools**: Database and external service connections

**Custom Business Metrics**
# Example Prometheus metrics configuration
# Request duration histogram
http_request_duration_seconds{method="GET", endpoint="/api/users", status="200"}

# Business transaction counter
business_transactions_total{type="purchase", status="successful"}

# Feature usage gauge
active_feature_users{feature="premium_dashboard"}

# Error rate by service
service_error_rate{service="user-service", error_type="timeout"}
#### 4.2 Application Performance Monitoring (APM)
**Performance Tracking**
- **Response Time Distribution**: Track P50, P95, P99 response times
- **Apdex Score**: Application Performance Index calculation
- **Throughput Monitoring**: Requests per minute/second tracking
- **Error Rate Analysis**: Error categorization and trending

**Database Monitoring**
- **Query Performance**: Slow query detection and analysis
- **Connection Health**: Pool utilization and connection timeouts
- **Lock Detection**: Database deadlocks and long-running transactions
- **Replication Status**: Master-slave lag and sync status

### 5. Infrastructure Monitoring
#### 5.1 System-Level Monitoring
**CPU and Memory Monitoring**
- **CPU Utilization**: Per-core and system-wide CPU usage
- **Memory Usage**: RAM utilization, swap usage, memory leaks
- **Load Average**: System load over 1, 5, and 15-minute intervals
- **Process Monitoring**: Individual process resource consumption

**Network Monitoring**
- **Bandwidth Utilization**: Inbound/outbound network traffic
- **Connection Tracking**: TCP connections, socket states
- **Latency Monitoring**: Network round-trip times
- **Packet Loss**: Network reliability metrics

**Storage Monitoring**
- **Disk Space**: Used/available disk space by mount point
- **I/O Performance**: Read/write IOPS, queue depth, latency
- **File System Health**: Inode usage, filesystem errors
- **Backup Status**: Backup job success/failure tracking

#### 5.2 Container and Orchestration Monitoring
**Kubernetes Monitoring**
- **Cluster Health**: Node status, API server availability
- **Pod Monitoring**: Pod lifecycle, restarts, resource usage
- **Resource Quotas**: Namespace resource utilization
- **Network Policies**: Service mesh communication health

**Container Metrics**
- **Container Resource Usage**: CPU, memory, network per container
- **Image Vulnerability**: Security scanning results
- **Registry Health**: Container registry availability and performance
- **Build Pipeline**: CI/CD pipeline success rates and durations

### 6. Business and User Experience Monitoring
#### 6.1 Real User Monitoring (RUM)
**User Experience Metrics**
- **Page Load Times**: Time to first byte, first contentful paint
- **JavaScript Errors**: Frontend error rates and types
- **User Journeys**: Conversion funnel analysis
- **Geographic Performance**: Performance by user location

**Synthetic Monitoring**
- **Uptime Monitoring**: Synthetic tests from multiple locations
- **Transaction Monitoring**: Critical user journey automation
- **API Monitoring**: Endpoint availability and performance
- **SSL Certificate**: Certificate expiration monitoring

#### 6.2 Business Metrics Dashboard
**Key Performance Indicators**
- **Daily Active Users (DAU)**: Unique users per day
- **Monthly Active Users (MAU)**: Unique users per month
- **Revenue Metrics**: Revenue per user, transaction volumes
- **Feature Adoption**: New feature usage and adoption rates

**Customer Satisfaction**
- **Net Promoter Score (NPS)**: Customer satisfaction tracking
- **Support Ticket Volume**: Help desk ticket metrics
- **User Feedback**: In-app feedback and rating trends
- **Churn Rate**: User retention and churn analysis

### 7. Security Monitoring
#### 7.1 Security Event Monitoring
**Authentication and Authorization**
- **Failed Login Attempts**: Brute force attack detection
- **Privilege Escalation**: Unauthorized access attempts
- **Session Management**: Abnormal session patterns
- **API Abuse**: Rate limiting violations and suspicious patterns

**Application Security**
- **Injection Attempts**: SQL injection, XSS attempt detection
- **Data Breaches**: Unauthorized data access patterns
- **File Upload Security**: Malicious file upload attempts
- **Input Validation**: Invalid input pattern detection

#### 7.2 Security Compliance Monitoring
**Audit Trail Monitoring**
- **Data Access Logs**: Who accessed what data when
- **Configuration Changes**: Infrastructure and application changes
- **Compliance Violations**: GDPR, HIPAA, SOX compliance issues
- **Certificate Management**: SSL/TLS certificate expiration tracking

### 8. Alerting Strategy
#### 8.1 Alert Prioritization
**Critical Alerts (P1)**
- **Criteria**: Service completely unavailable, data loss risk
- **Response Time**: Immediate (page on-call engineer)
- **Examples**: Total service outage, database unavailable, security breach
- **Escalation**: If no response in 15 minutes, escalate to manager

**High Priority Alerts (P2)**
- **Criteria**: Major functionality impacted, SLO breach imminent
- **Response Time**: 30 minutes during business hours, 1 hour after hours
- **Examples**: High error rates, slow response times, partial outage
- **Escalation**: If no response in 1 hour, escalate to senior engineer

**Medium Priority Alerts (P3)**
- **Criteria**: Minor functionality impacted, early warning indicators
- **Response Time**: 4 hours during business hours
- **Examples**: Disk space low, cache miss rate high, queue backlog
- **Escalation**: If no response in 8 hours, escalate to team lead

**Low Priority Alerts (P4)**
- **Criteria**: Informational, no immediate impact
- **Response Time**: Next business day
- **Examples**: Batch job failures, non-critical service degradation
- **Escalation**: Track in ticket system, no immediate escalation

#### 8.2 Alert Configuration
**Alert Rules Example (Prometheus AlertManager)**
``
groups:
- name: application.rules
  rules:
  # High error rate alert
    - alert: HighErrorRate
      expr: |
      (
      rate(http_requests_total{status=~"5.."}[5m]) /
      rate(http_requests_total[5m])
      ) > 0.05
      for: 2m
      labels:
      severity: critical
      team: backend
      annotations:
      summary: "High error rate detected"

```text
      description: "Error rate is {{ $value | humanizePercentage }} for {{ $labels.instance }}"
```

      runbook_url: "https://runbooks.company.com/high-error-rate"

  # Response time SLO breach
    - alert: ResponseTimeHigh
      expr: |
      histogram_quantile(0.95,
      rate(http_request_duration_seconds_bucket[5m])
      ) > 0.5
      for: 5m
      labels:
      severity: warning
      team: backend
      annotations:
      summary: "95th percentile response time is high"
      description: "95th percentile response time is {{ $value }}s"

  # Database connection pool exhaustion
    - alert: DatabaseConnectionPoolHigh
      expr: |
      (
      db_connection_pool_active /
      db_connection_pool_max
      ) > 0.8
      for: 3m
      labels:
      severity: warning
      team: database
      annotations:
      summary: "Database connection pool utilization high"

```text
      description: "Connection pool is {{ $value | humanizePercentage }} full"
```

- name: infrastructure.rules
  rules:
  # High CPU usage
    - alert: HighCPUUsage
      expr: |
      100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
      for: 5m
      labels:
      severity: warning
      team: infrastructure
      annotations:
      summary: "High CPU usage detected"
      description: "CPU usage is {{ $value }}% on {{ $labels.instance }}"

  # Disk space low
    - alert: DiskSpaceLow
      expr: |
      (
      node_filesystem_avail_bytes /
      node_filesystem_size_bytes
      ) < 0.1
      for: 10m
      labels:
      severity: warning
      team: infrastructure
      annotations:
      summary: "Disk space is running low"

```text
      description: "Only {{ $value | humanizePercentage }} disk space remaining on {{ $labels.instance }}"
```

``

#### 8.3 Alert Routing and Notifications
**Notification Channels**
- **PagerDuty**: Critical and high-priority alerts during and after hours
- **Slack**: All alerts to team channels with context and runbook links
- **Email**: Summary reports and non-urgent notifications
- **SMS**: Backup notification for critical alerts if no acknowledgment

**Team-Based Routing**
``
route:
group_by: ['alertname', 'cluster', 'service']
group_wait: 30s
group_interval: 5m
repeat_interval: 1h
receiver: 'default'
routes:
- match:
  severity: critical
  receiver: 'pagerduty-critical'
  continue: true
- match:
  team: backend
  receiver: 'backend-team'
- match:
  team: frontend
  receiver: 'frontend-team'
- match:
  team: database
  receiver: 'database-team'

receivers:
- name: 'pagerduty-critical'
  pagerduty_configs:
    - service_key: '{{pagerduty_service_key}}'
      description: "{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}"

- name: 'backend-team'
  slack_configs:
    - api_url: '{{slack_webhook_backend}}'
      channel: '#backend-alerts'
      title: 'Alert: {{ .GroupLabels.alertname }}'
      text: "{{ range .Alerts }}{{ .Annotations.description }}{{ end }}"

``

### 9. Dashboard Design
#### 9.1 Executive Dashboard
**High-Level KPIs**
- **Service Availability**: Current availability vs. SLO target
- **User Experience**: Response time trends and user satisfaction
- **Business Metrics**: Revenue, user growth, feature adoption
- **Incident Summary**: Open incidents, MTTR trends

**Executive Dashboard Layout**
Dashboard: Executive Overview

```text
├── Row: Service Health
│   ├── Availability (99.95% target)
│   ├── Response Time (P95 < 2s)
│   ├── Error Rate (< 0.1%)
│   └── Throughput (current vs. capacity)
├── Row: Business Metrics
│   ├── Daily Active Users
│   ├── Revenue Metrics
│   ├── Conversion Rates
│   └── Feature Adoption
├── Row: Infrastructure Health
│   ├── System Resources
│   ├── Database Performance
│   ├── Cache Hit Rate
│   └── Security Events
└── Row: Incident Management
├── Open Incidents
├── MTTR Trends
├── Alert Volume
└── On-Call Schedule
```

#### 9.2 Operational Dashboards
**Application Performance Dashboard**
- **Request Metrics**: Rate, errors, duration (RED method)
- **Resource Utilization**: CPU, memory, network, disk
- **Dependencies**: External service health and response times
- **Error Analysis**: Error types, frequency, and trends

**Infrastructure Dashboard**
- **Cluster Overview**: Node health, resource allocation
- **Network Performance**: Bandwidth, latency, packet loss
- **Storage Performance**: IOPS, latency, capacity utilization
- **Security Monitoring**: Failed authentications, suspicious activities

#### 9.3 Team-Specific Dashboards
**Development Team Dashboard**
- **Code Deployment**: Deployment frequency and success rate
- **Application Errors**: Error rates by component and feature
- **Performance Regression**: Performance trends post-deployment
- **API Usage**: Endpoint usage patterns and performance

**Operations Team Dashboard**
- **System Health**: Infrastructure resource utilization
- **Capacity Planning**: Growth trends and capacity forecasts
- **Backup Status**: Backup job success and recovery testing
- **Maintenance Windows**: Scheduled maintenance and impact

### 10. Incident Response Integration
#### 10.1 Incident Lifecycle Integration
**Automated Incident Creation**
- **Alert Correlation**: Group related alerts into single incident
- **Incident Severity**: Automatic severity assignment based on alert rules
- **Runbook Integration**: Automatic runbook links in incident details
- **Team Assignment**: Route incidents to appropriate response teams

**Incident Escalation**
- **Time-Based Escalation**: Auto-escalate if not acknowledged
- **Severity Escalation**: Escalate based on impact assessment
- **Cross-Team Coordination**: Notify dependent teams for major incidents
- **Management Notification**: Auto-notify leadership for critical incidents

#### 10.2 Post-Incident Analysis
**Automated Data Collection**
- **Timeline Construction**: Automatic incident timeline generation
- **Metric Correlation**: Correlate metrics during incident timeframe
- **Log Analysis**: Extract relevant log entries for root cause analysis
- **Change Correlation**: Identify recent changes that may have contributed

### 11. Capacity Planning and Forecasting
#### 11.1 Growth Monitoring
**Usage Trend Analysis**
- **User Growth Patterns**: Daily/weekly/monthly user growth rates
- **Resource Consumption**: CPU, memory, storage growth trends
- **Traffic Patterns**: Request volume and seasonal variations
- **Feature Adoption**: New feature usage and impact on resources

**Capacity Forecasting**
- **Predictive Modeling**: Statistical models for capacity prediction
- **Scenario Planning**: What-if analysis for growth scenarios
- **Resource Planning**: Infrastructure scaling recommendations
- **Cost Optimization**: Resource efficiency improvement opportunities

#### 11.2 Performance Optimization Monitoring
**Performance Baseline Tracking**
- **Response Time Trends**: Long-term performance trend analysis
- **Database Performance**: Query performance optimization opportunities
- **Cache Effectiveness**: Cache hit rates and optimization recommendations
- **Resource Efficiency**: CPU, memory, and network utilization optimization

### 12. Compliance and Audit Monitoring
#### 12.1 Regulatory Compliance Monitoring
**Data Protection Monitoring**
- **GDPR Compliance**: Data access, retention, and deletion tracking
- **PCI DSS**: Payment data handling and security monitoring
- **HIPAA**: Healthcare data access and audit trail monitoring
- **SOX**: Financial data access and control monitoring

**Audit Trail Management**
- **Access Logging**: Complete audit trail of data access
- **Change Management**: Track all system and configuration changes
- **Retention Management**: Ensure log retention meets compliance requirements
- **Report Generation**: Automated compliance report generation

### 13. Monitoring Strategy Implementation
#### 13.1 Implementation Phases
**Phase 1: Foundation (Weeks 1-4)**
- Set up core monitoring infrastructure (Prometheus, Grafana)
- Implement basic application metrics (RED method)
- Configure essential infrastructure monitoring
- Set up basic alerting for critical services

**Phase 2: Enhancement (Weeks 5-8)**
- Add distributed tracing with Jaeger
- Implement comprehensive log management
- Create team-specific dashboards
- Set up advanced alerting rules and routing

**Phase 3: Optimization (Weeks 9-12)**
- Implement SLOs and error budgets
- Add business metrics and RUM
- Set up automated incident response
- Create capacity planning and forecasting

**Phase 4: Advanced Features (Weeks 13-16)**
- Add security monitoring and compliance tracking
- Implement predictive alerting and anomaly detection
- Set up automated remediation for common issues
- Create advanced analytics and reporting

#### 13.2 Success Metrics and KPIs
**Monitoring Effectiveness**
- **Alert Noise Reduction**: < {{false_positive_target}}% false positive rate
- **Mean Time to Detection**: < {{mttd_target}} minutes for critical issues
- **Coverage**: {{coverage_target}}% of critical user journeys monitored
- **Availability Tracking**: Accurate SLO measurement and reporting

**Team Productivity**
- **Incident Response Time**: {{incident_response_improvement}}% improvement in MTTR
- **Proactive Issue Detection**: {{proactive_detection_rate}}% of issues detected before customer impact
- **Capacity Planning**: {{capacity_accuracy}}% accuracy in capacity forecasts
- **Cost Optimization**: {{cost_reduction_target}}% reduction in infrastructure costs through optimization

## Output Format Requirements
Present the monitoring strategy as:
- Comprehensive strategy document with clear objectives
- Technical implementation details and configuration examples
- Dashboard designs with specific metrics and visualizations
- Alert rules and escalation procedures
- Implementation roadmap with timelines and milestones
- Success metrics and measurement criteria

## Integration with Overall SDLC
This monitoring strategy supports the complete SDLC by:
- Providing feedback loops to development teams
- Enabling continuous improvement through data-driven insights
- Supporting deployment decisions through performance validation
- Facilitating incident response and post-mortem analysis
- Enabling capacity planning and infrastructure optimization

Generate a comprehensive monitoring strategy that ensures system reliability, performance, and business success through effective observability and proactive monitoring.

This comprehensive set of prompts covers all seven SDLC stages with detailed, professional-grade prompts that can generate high-quality artifacts. Each prompt is designed to:

1. **Provide clear context and expertise level** for the AI
2. **Include comprehensive input requirements** with placeholder variables
3. **Generate specific, actionable outputs** that follow industry standards
4. **Ensure seamless integration** between stages
5. **Include quality validation criteria** and best practices
6. **Support modern development practices** like DevOps, cloud-native, and agile methodologies

The prompts are production-ready and can be used to generate complete SDLC artifacts that feed into each other, creating a comprehensive automated pipeline for software development projects.
