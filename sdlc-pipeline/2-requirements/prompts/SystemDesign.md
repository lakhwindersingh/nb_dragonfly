# Non-Functional Requirements (NFR) Definition Prompt

## Context and Role
You are a Senior Systems Architect and Performance Engineer with extensive experience in defining and validating non-functional requirements for enterprise software systems. You specialize in translating business needs into measurable, testable, and achievable non-functional requirements that guide system design and ensure successful delivery of quality attributes.

## Input Requirements
Define comprehensive non-functional requirements based on:

**Business Context:**
- Business Objectives: {{business_objectives}}
- User Expectations: {{user_expectations}}
- Service Level Agreements: {{sla_requirements}}
- Business Continuity Needs: {{continuity_requirements}}
- Compliance Requirements: {{regulatory_requirements}}

**Technical Context:**
- System Architecture: {{architecture_approach}}
- Technology Stack: {{technology_choices}}
- Integration Requirements: {{integration_points}}
- Data Volume Projections: {{data_growth}}
- User Load Expectations: {{user_projections}}

**Operational Context:**
- Operating Environment: {{deployment_environment}}
- Support Model: {{support_requirements}}
- Maintenance Windows: {{maintenance_schedule}}
- Budget Constraints: {{cost_limitations}}

## NFR Definition Instructions

Create comprehensive, measurable non-functional requirements across all quality attributes:

### 1. Performance Requirements

#### 1.1 Response Time Requirements

**NFR-PERF-001: User Interface Response Time**
- **Requirement**: All user interface operations shall respond within specified time limits under normal operating conditions
- **Measurement Criteria**:
    - Page load time: ≤ 3 seconds (95th percentile)
    - Form submission: ≤ 2 seconds (95th percentile)
    - Search operations: ≤ 1 second (95th percentile)
    - Report generation: ≤ 10 seconds for standard reports (90th percentile)
- **Test Conditions**:
    - Normal load: {{concurrent_users}} concurrent users
    - Standard network conditions: Broadband (10+ Mbps)
    - Typical browser environment: Chrome, Firefox, Safari latest versions
- **Acceptance Criteria**: Response time thresholds met in load testing
- **Priority**: High
- **Rationale**: User productivity and satisfaction depend on responsive interface

**NFR-PERF-002: API Response Time**
- **Requirement**: All API endpoints shall respond within specified time limits
- **Measurement Criteria**:
    - Simple queries (GET): ≤ 500ms (95th percentile)
    - Data modification (POST/PUT): ≤ 1 second (95th percentile)
    - Complex queries with joins: ≤ 3 seconds (90th percentile)
    - Bulk operations: ≤ 30 seconds (95th percentile)
- **Test Conditions**: API load testing with {{api_concurrent_requests}} concurrent requests
- **Monitoring**: Continuous APM monitoring with alerting
- **Priority**: High

#### 1.2 Throughput Requirements

**NFR-PERF-010: System Throughput**
- **Requirement**: System shall support specified transaction volumes
- **Measurement Criteria**:
    - Read operations: {{read_tps}} transactions per second
    - Write operations: {{write_tps}} transactions per second
    - Peak load handling: {{peak_multiplier}}x normal load for {{peak_duration}} minutes
    - Batch processing: {{batch_records}} records per hour
- **Test Conditions**: Sustained load testing over {{test_duration}} hours
- **Scalability**: Linear scaling with resource allocation
- **Priority**: High

#### 1.3 Resource Utilization Requirements

**NFR-PERF-020: Resource Consumption**
- **Requirement**: System resource utilization shall remain within acceptable limits
- **Measurement Criteria**:
    - CPU utilization: ≤ 80% average, ≤ 95% peak under normal load
    - Memory utilization: ≤ 85% of allocated memory
    - Database connections: ≤ 70% of available connection pool
    - Storage I/O: ≤ 1000 IOPS average, ≤ 5000 IOPS peak
- **Monitoring**: Real-time resource monitoring with alerting
- **Auto-scaling**: Automatic resource scaling based on utilization thresholds
- **Priority**: Medium

### 2. Scalability Requirements

#### 2.1 User Scalability

**NFR-SCALE-001: Concurrent User Support**
- **Requirement**: System shall support growing user base without performance degradation
- **Measurement Criteria**:
    - Current capacity: {{current_users}} concurrent users
    - 1-year capacity: {{year1_users}} concurrent users
    - 3-year capacity: {{year3_users}} concurrent users
    - Peak load multiplier: {{peak_factor}}x normal capacity
- **Scaling Strategy**: Horizontal scaling with load balancing
- **Test Validation**: Load testing at each capacity level
- **Priority**: High

#### 2.2 Data Scalability

**NFR-SCALE-010: Data Volume Support**
- **Requirement**: System shall handle growing data volumes efficiently
- **Measurement Criteria**:
    - Current data volume: {{current_data_size}}
    - Annual growth rate: {{growth_rate}}% per year
    - Query performance maintained with data growth
    - Storage efficiency through compression and archiving
- **Architecture Support**: Partitioning, sharding, and archival strategies
- **Priority**: Medium

#### 2.3 Geographic Scalability

**NFR-SCALE-020: Multi-Region Support**
- **Requirement**: System shall support users across multiple geographic regions
- **Measurement Criteria**:
    - Regional response time: ≤ 200ms additional latency per region
    - Data consistency: Eventual consistency within {{consistency_time}} seconds
    - Failover time: ≤ {{failover_time}} minutes between regions
- **Implementation**: CDN, regional databases, content replication
- **Priority**: {{geographic_priority}}

### 3. Availability and Reliability Requirements

#### 3.1 System Availability

**NFR-AVAIL-001: System Uptime**
- **Requirement**: System shall maintain high availability during business operations
- **Measurement Criteria**:
    - Business hours availability: {{business_hours_sla}}% ({{business_hours}})
    - 24/7 availability: {{full_time_sla}}%
    - Maximum unplanned downtime: {{max_downtime}} minutes per month
    - Planned maintenance windows: {{maintenance_windows}}
- **Calculation**: Measured monthly, excluding planned maintenance
- **Penalties**: SLA penalties for availability breaches
- **Priority**: Critical

**NFR-AVAIL-002: Service Recovery**
- **Requirement**: System shall recover from failures within specified timeframes
- **Measurement Criteria**:
    - Mean Time to Detect (MTTD): ≤ {{mttd_minutes}} minutes
    - Mean Time to Respond (MTTR): ≤ {{mttr_minutes}} minutes
    - Mean Time to Recover (MTTR): ≤ {{recovery_time}} minutes
    - Recovery Point Objective (RPO): ≤ {{rpo_time}} minutes data loss
- **Implementation**: Automated monitoring, alerting, and failover
- **Priority**: High

#### 3.2 Fault Tolerance

**NFR-AVAIL-010: Fault Tolerance**
- **Requirement**: System shall continue operating despite component failures
- **Measurement Criteria**:
    - Single point of failure elimination: No critical SPOFs
    - Graceful degradation: Core functions available during partial failures
    - Automatic failover: ≤ {{failover_time}} seconds for critical components
    - Circuit breaker: Automatic isolation of failing services
- **Architecture**: Redundancy, clustering, microservices resilience
- **Priority**: High

### 4. Security Requirements

#### 4.1 Authentication and Authorization

**NFR-SEC-001: User Authentication**
- **Requirement**: System shall enforce strong authentication mechanisms
- **Measurement Criteria**:
    - Password policy: Minimum {{password_complexity}} requirements
    - Multi-factor authentication: Required for {{mfa_roles}} roles
    - Session management: Secure sessions with {{session_timeout}} timeout
    - Account lockout: {{lockout_attempts}} failed attempts trigger {{lockout_duration}} lockout
- **Standards Compliance**: NIST 800-63B authentication guidelines
- **Priority**: Critical

**NFR-SEC-002: Access Control**
- **Requirement**: System shall enforce role-based access control with principle of least privilege
- **Measurement Criteria**:
    - Role definition: Granular permissions for all system functions
    - Authorization checking: Every operation verified against user permissions
    - Privilege escalation: Documented approval process for elevated access
    - Access review: {{access_review_frequency}} review of user permissions
- **Audit Requirements**: All access attempts logged and monitored
- **Priority**: Critical

#### 4.2 Data Protection

**NFR-SEC-010: Data Encryption**
- **Requirement**: System shall protect sensitive data through encryption
- **Measurement Criteria**:
    - Data at rest: {{encryption_standard}} encryption for sensitive data
    - Data in transit: TLS {{tls_version}} for all external communications
    - Key management: Hardware Security Module (HSM) or equivalent
    - Database encryption: Transparent Data Encryption (TDE) for database
- **Compliance**: {{compliance_standards}} requirements
- **Priority**: Critical

**NFR-SEC-011: Data Privacy**
- **Requirement**: System shall comply with data privacy regulations
- **Measurement Criteria**:
    - Consent management: User consent tracking and management
    - Data minimization: Only necessary data collected and stored
    - Right to erasure: Complete data deletion within {{deletion_timeframe}}
    - Data portability: User data export in standard formats
- **Regulations**: GDPR, CCPA, industry-specific regulations
- **Priority**: Critical

#### 4.3 Security Monitoring

**NFR-SEC-020: Security Monitoring and Auditing**
- **Requirement**: System shall provide comprehensive security monitoring and audit trails
- **Measurement Criteria**:
    - Audit logging: All security-relevant events logged
    - Log retention: {{log_retention}} months of audit logs retained
    - Real-time monitoring: Suspicious activity detection and alerting
    - Incident response: {{incident_response_time}} response to security alerts
- **Implementation**: SIEM integration, security dashboards, automated alerting
- **Priority**: High

### 5. Usability Requirements

#### 5.1 User Experience

**NFR-USAB-001: Ease of Use**
- **Requirement**: System shall be intuitive and easy to use for target user groups
- **Measurement Criteria**:
    - Task completion rate: ≥ {{task_completion_rate}}% for primary tasks
    - Error rate: ≤ {{user_error_rate}}% for trained users
    - Learning time: New users productive within {{learning_time}} hours
    - User satisfaction: ≥ {{satisfaction_score}}/10 average satisfaction score
- **Testing Method**: Usability testing with representative users
- **Priority**: High

**NFR-USAB-002: Accessibility**
- **Requirement**: System shall be accessible to users with disabilities
- **Measurement Criteria**:
    - WCAG compliance: {{wcag_level}} compliance level
    - Screen reader support: Compatible with major screen readers
    - Keyboard navigation: All functions accessible via keyboard
    - Color contrast: {{contrast_ratio}}:1 minimum contrast ratio
- **Standards**: WCAG {{wcag_version}}, Section 508 compliance
- **Testing**: Automated accessibility testing and user testing
- **Priority**: {{accessibility_priority}}

#### 5.2 Multi-Platform Support

**NFR-USAB-010: Browser Compatibility**
- **Requirement**: System shall work consistently across supported browsers and devices
- **Measurement Criteria**:
    - Browser support: {{supported_browsers}} and versions
    - Mobile compatibility: Responsive design for {{screen_sizes}}
    - Feature parity: {{feature_parity}}% feature availability across platforms
    - Performance consistency: ≤ {{performance_variance}}% performance variation
- **Testing**: Cross-browser and cross-device testing
- **Priority**: High

### 6. Maintainability Requirements

#### 6.1 Code Quality

**NFR-MAINT-001: Code Maintainability**
- **Requirement**: System code shall be maintainable and well-documented
- **Measurement Criteria**:
    - Code coverage: ≥ {{code_coverage}}% test coverage
    - Code complexity: Cyclomatic complexity ≤ {{complexity_threshold}}
    - Documentation: All public APIs documented, README files current
    - Code standards: Adherence to {{coding_standards}} guidelines
- **Tools**: Static analysis, automated code quality checks
- **Priority**: Medium

#### 6.2 Monitoring and Diagnostics

**NFR-MAINT-010: System Observability**
- **Requirement**: System shall provide comprehensive monitoring and diagnostic capabilities
- **Measurement Criteria**:
    - Application monitoring: Real-time performance metrics
    - Infrastructure monitoring: System resource monitoring
    - Log aggregation: Centralized logging with search capabilities
    - Alerting: Proactive alerts for system issues
- **Implementation**: APM tools, log management, monitoring dashboards
- **Priority**: High

### 7. Compliance and Legal Requirements

#### 7.1 Regulatory Compliance

**NFR-COMP-001: {{Regulation_Name}} Compliance**
- **Requirement**: System shall comply with applicable regulations
- **Measurement Criteria**:
    - Data handling: Compliant data collection, processing, and storage
    - Audit trails: Complete audit logs for compliance reporting
    - Controls: Required security and privacy controls implemented
    - Reporting: Compliance reports generated as required
- **Validation**: Regular compliance audits and assessments
- **Priority**: Critical

### 8. Environmental Requirements

#### 8.1 Operating Environment

**NFR-ENV-001: Production Environment**
- **Requirement**: System shall operate reliably in production environment
- **Measurement Criteria**:
    - Operating systems: {{supported_os}} versions
    - Database systems: {{database_versions}}
    - Network requirements: {{network_specifications}}
    - Climate conditions: Standard data center environment
- **Deployment**: Cloud-native deployment with containerization
- **Priority**: High

### 9. NFR Validation and Testing

#### 9.1 Performance Testing Strategy
- **Load Testing**: Simulated user load at various levels
- **Stress Testing**: Beyond-capacity testing to find breaking points
- **Volume Testing**: Large data volume performance validation
- **Endurance Testing**: Extended operation under normal load

#### 9.2 Security Testing Strategy
- **Penetration Testing**: External security assessment
- **Vulnerability Scanning**: Automated security scanning
- **Code Security Analysis**: Static and dynamic code analysis
- **Compliance Auditing**: Regular compliance validation

#### 9.3 Usability Testing Strategy
- **User Testing**: Real user task completion testing
- **Accessibility Testing**: Assistive technology compatibility
- **Cross-platform Testing**: Multi-browser and device testing
- **Performance Perception**: Subjective performance evaluation

### 10. NFR Monitoring and Governance

#### 10.1 Performance Monitoring
- **Real-time Dashboards**: Key performance indicators
- **Automated Alerting**: Threshold-based notifications
- **Trend Analysis**: Performance trend tracking
- **Capacity Planning**: Proactive scaling recommendations

#### 10.2 Quality Gates
- **Development Gates**: NFR validation before deployment
- **Testing Gates**: Performance and security testing completion
- **Production Gates**: Production readiness assessment
- **Maintenance Gates**: Ongoing NFR compliance verification

## Output Format Requirements

Present NFRs as:
- Structured requirements with unique identifiers
- Specific, measurable criteria with thresholds
- Clear testing and validation approaches
- Priority levels and business justification
- Traceability to business requirements
- Implementation guidance and constraints

## Quality Validation Criteria

Ensure all NFRs meet these standards:
- [ ] Specific and unambiguous language
- [ ] Measurable criteria with quantified thresholds
- [ ] Achievable within technical and budget constraints
- [ ] Relevant to business objectives and user needs
- [ ] Testable with defined validation methods
- [ ] Complete coverage of all quality attributes
- [ ] Consistent terminology and measurement units

## Integration with Design Stage

These NFRs will guide the Design stage by providing:
- Performance targets for architecture design
- Security requirements for security architecture
- Scalability requirements for system architecture
- Usability requirements for user interface design
- Reliability requirements for infrastructure design
- Compliance requirements for data architecture

Generate comprehensive, testable non-functional requirements that ensure system quality and business success.
