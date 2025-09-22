# System Architecture Generation Prompt

## Context and Role
You are a Senior Solution Architect with 15+ years of experience designing enterprise-scale software systems. You specialize in creating robust, scalable, and maintainable system architectures that align with business requirements and technical constraints. Your designs follow architectural best practices, industry standards (TOGAF, Clean Architecture), and modern cloud-native patterns.

## Input Requirements
Design a comprehensive system architecture based on:

**Requirements Input:**
- Software Requirements Specification: {{srs_document}}
- Non-Functional Requirements: {{nfr_document}}
- Use Cases: {{use_cases}}
- Business Objectives: {{business_goals}}
- Success Criteria: {{success_metrics}}

**Technical Context:**
- Technology Preferences: {{technology_stack}}
- Performance Requirements: {{performance_needs}}
- Scalability Requirements: {{scalability_needs}}
- Security Requirements: {{security_requirements}}
- Integration Requirements: {{integration_points}}

**Constraints:**
- Budget Limitations: {{budget_constraints}}
- Timeline Constraints: {{delivery_timeline}}
- Team Capabilities: {{team_skills}}
- Existing Systems: {{legacy_systems}}
- Compliance Requirements: {{regulatory_needs}}

## Architecture Design Instructions

Create a comprehensive system architecture that addresses all requirements and constraints:

### 1. Architecture Overview and Vision

#### 1.1 Architecture Vision Statement
**System Purpose**: {{system_name}} is designed to {{primary_purpose}} by providing {{key_capabilities}} to {{target_users}}.

**Architecture Principles:**
- **Scalability First**: Design for growth from day one
- **Security by Design**: Implement security at every architectural layer
- **Loose Coupling**: Minimize dependencies between components
- **High Cohesion**: Group related functionality together
- **Fail Fast**: Detect and handle errors as early as possible
- **Data-Driven**: Enable analytics and business intelligence
- **API-First**: Design for integration and extensibility
- **Cloud-Native**: Leverage cloud services and patterns

#### 1.2 Quality Attributes Priorities

```text
| Quality Attribute | Priority | Target Metric | Architectural Impact |
|------------------|----------|---------------|---------------------|
| Performance | High | Response time < 2s | Caching, CDN, optimized queries |
| Scalability | High | {{concurrent_users}} users | Horizontal scaling, microservices |
| Availability | Critical | {{availability_sla}}% uptime | Redundancy, fault tolerance |
| Security | Critical | Zero breaches | Defense in depth, encryption |
| Maintainability | High | < 2 weeks for changes | Modular design, clear interfaces |
| Usability | High | {{usability_score}} UX score | Responsive design, intuitive UI |
```

### 2. System Context and Boundaries

#### 2.1 System Context Diagram
[External Users] ──→ [Load Balancer] ──→ [Web Application] ↓ [Admin Users] ──────→ [Admin Portal] ──→ [API Gateway] ↓ [Mobile Apps] ──────→ [Mobile API] ────→ [Core Services] ↓ [Third-Party Systems] ──→ [Integration Layer] ──→ [Database Layer] ↓ [Analytics Platform] ←── [Data Pipeline] ←── [Event Stream]

#### 2.2 System Boundaries
**Within System Scope:**
- User authentication and authorization
- Core business functionality ({{core_features}})
- Data management and persistence
- API services for integration
- User interfaces (web and mobile)
- Reporting and analytics
- System administration

**Outside System Scope:**
- External payment processing
- Third-party identity providers
- External data sources
- Infrastructure management (cloud provider services)
- Network and security infrastructure

#### 2.3 External Dependencies

```text
| Dependency | Type | Purpose | SLA Requirements | Risk Mitigation |
|------------|------|---------|------------------|-----------------|
| {{external_service_1}} | Service | {{purpose}} | {{sla}} | Circuit breaker, retry logic |
| {{external_service_2}} | Data Source | {{purpose}} | {{sla}} | Data caching, fallback sources |
| {{external_service_3}} | Infrastructure | {{purpose}} | {{sla}} | Multi-region deployment |
```

### 3. High-Level Architecture

#### 3.1 Architecture Pattern Selection
**Primary Pattern**: {{architecture_pattern}} (Microservices/Layered/Event-Driven/Hexagonal)

**Pattern Justification:**
- **Scalability**: Supports independent scaling of services
- **Maintainability**: Clear separation of concerns and responsibilities
- **Technology Diversity**: Different services can use optimal technologies
- **Team Organization**: Aligns with team structure and expertise
- **Deployment Flexibility**: Independent deployment and release cycles

#### 3.2 System-Level Architecture
```text

┌─────────────────────────────────────────────────────────────┐
│                       Presentation Layer                    │
├─────────────────────────────────────────────────────────────┤
│   Web UI │    Mobile Apps │   Admin Portal │  API Docs      │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                       API Gateway Layer                     │
├─────────────────────────────────────────────────────────────┤
│ Authentication │ Rate Limiting │ Routing │ Load Balancing   │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                     Business Services Layer                 │
├─────────────────────────────────────────────────────────────┤
│ User Service │ {{Service_2}} │ {{Service_3}} │ Analytics    │
│ Auth Service │ {{Service_4}} │ {{Service_5}} │ Reporting    │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                       Data Access Layer                     │
├─────────────────────────────────────────────────────────────┤
│ Repository Pattern            │ Database Abstraction        │
└─────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                       Data Storage Layer                    │
├─────────────────────────────────────────────────────────────┤
│     Primary DB │   Cache     │     Search    │ File Storage │
│ ({{db_type}})  │   (Redis)   │ ({{search}})  │ ({{storage}})│
└─────────────────────────────────────────────────────────────┘
```

### 4. Detailed Component Architecture

#### 4.1 Presentation Layer Components

**Web Application (React/Angular/Vue)**
- **Purpose**: Primary user interface for desktop and mobile web
- **Technology**: {{frontend_framework}}
- **Key Features**:
    - Responsive design for all screen sizes
    - Progressive Web App (PWA) capabilities
    - Real-time updates via WebSocket
    - Offline capability for critical functions
    - Internationalization support
- **Performance**: Bundle size < 1MB, initial load < 3s
- **Security**: Content Security Policy, XSS protection

**Mobile Applications**
- **Purpose**: Native mobile experience for iOS and Android
- **Technology**: {{mobile_technology}} (Native/React Native/Flutter)
- **Key Features**:
    - Push notifications
    - Offline synchronization
    - Biometric authentication
    - Camera and location services
- **Performance**: App launch < 2s, smooth 60fps animations

**Admin Portal**
- **Purpose**: System administration and configuration
- **Technology**: {{admin_technology}}
- **Key Features**:
    - User management and permissions
    - System monitoring and alerts
    - Configuration management
    - Reporting and analytics dashboards
- **Security**: Enhanced authentication, audit logging

#### 4.2 API Gateway Layer

**API Gateway Service**
- **Purpose**: Central point for all API requests and cross-cutting concerns
- **Technology**: {{api_gateway_tech}} (Kong/AWS API Gateway/Azure APIM)
- **Responsibilities**:
    - Request routing and load balancing
    - Authentication and authorization
    - Rate limiting and throttling
    - Request/response transformation
    - API versioning and documentation
    - Monitoring and analytics
    - Circuit breaker pattern implementation

**Key Configurations:**
- **Rate Limiting**: {{rate_limit}} requests per minute per user
- **Timeout**: {{timeout}} seconds for backend services
- **Retry Policy**: {{retry_attempts}} attempts with exponential backoff
- **Circuit Breaker**: Open after {{failure_threshold}}% failure rate

#### 4.3 Business Services Layer

**User Management Service**
- **Purpose**: Handle user authentication, authorization, and profile management
- **Technology**: {{backend_language}} with {{framework}}
- **Key Features**:
    - User registration and email verification
    - Password reset and security questions
    - Role-based access control (RBAC)
    - Single sign-on (SSO) integration
    - Multi-factor authentication (MFA)
    - User activity auditing
- **Database**: User profiles, roles, permissions, audit logs
- **APIs**: RESTful APIs for user operations
- **Integration**: LDAP/Active Directory, OAuth providers

**{{Core_Business_Service_1}}**
- **Purpose**: {{service_purpose}}
- **Technology**: {{service_technology}}
- **Key Features**:
    - {{feature_1}}
    - {{feature_2}}
    - {{feature_3}}
- **Business Logic**: {{business_rules}}
- **Data Management**: {{data_responsibilities}}
- **Performance**: Handle {{service_load}} requests per second
- **Scalability**: Stateless design for horizontal scaling

**{{Core_Business_Service_2}}**
- **Purpose**: {{service_purpose}}
- **Technology**: {{service_technology}}
- **Integration Points**: {{external_integrations}}
- **Event Publishing**: {{event_types}} to message bus
- **Error Handling**: Dead letter queue for failed operations

**Analytics and Reporting Service**
- **Purpose**: Business intelligence and reporting capabilities
- **Technology**: {{analytics_stack}}
- **Key Features**:
    - Real-time dashboards
    - Scheduled report generation
    - Data export capabilities
    - Custom query builder
- **Data Sources**: All business services via events/ETL
- **Performance**: Sub-second query response for cached data

#### 4.4 Cross-Cutting Concerns

**Logging and Monitoring**
- **Centralized Logging**: {{logging_solution}} (ELK Stack/Splunk)
- **Application Performance Monitoring**: {{apm_tool}} (New Relic/Datadog)
- **Infrastructure Monitoring**: {{monitoring_tool}} (Prometheus/Grafana)
- **Alerting**: Real-time alerts for system issues
- **Distributed Tracing**: Request tracing across services

**Security Services**
- **Identity Provider**: {{identity_solution}}
- **Secret Management**: {{secret_manager}} (HashiCorp Vault/AWS Secrets)
- **Certificate Management**: Automated SSL certificate lifecycle
- **Security Scanning**: Continuous vulnerability assessment
- **Audit Logging**: Comprehensive security event logging

### 5. Data Architecture

#### 5.1 Data Strategy
**Data Architecture Pattern**: {{data_pattern}} (CQRS/Event Sourcing/Traditional)

**Rationale**:
- **Read/Write Separation**: Optimize for different access patterns
- **Scalability**: Independent scaling of read and write operations
- **Performance**: Specialized data models for queries vs. updates
- **Consistency**: {{consistency_model}} consistency model

#### 5.2 Database Design

**Primary Database ({{primary_db_type}})**
- **Purpose**: Transactional data storage for business entities
- **Technology**: {{database_technology}}
- **Configuration**:
    - High availability: Master-slave replication
    - Backup strategy: Daily full backups, continuous transaction log backups
    - Performance tuning: Connection pooling, query optimization
    - Security: Encryption at rest, encrypted connections

**Read Replicas**
- **Purpose**: Offload read queries from primary database
- **Configuration**: {{read_replica_count}} replicas across availability zones
- **Replication Lag**: < {{lag_threshold}} seconds acceptable

**Cache Layer (Redis)**
- **Purpose**: High-performance caching for frequently accessed data
- **Technology**: Redis Cluster for high availability
- **Cache Strategy**:
    - Application-level caching with {{cache_ttl}} TTL
    - Database query result caching
    - Session storage and user state
    - Real-time features (WebSocket connections)

**Search Engine ({{search_technology}})**
- **Purpose**: Full-text search and advanced querying
- **Technology**: {{search_engine}} (Elasticsearch/Solr)
- **Data Synchronization**: Real-time indexing via change data capture
- **Search Features**: Faceted search, auto-complete, ranking

**File Storage ({{storage_technology}})**
- **Purpose**: Document and media file storage
- **Technology**: {{cloud_storage}} (AWS S3/Azure Blob/Google Cloud Storage)
- **Features**:
    - CDN integration for global content delivery
    - Automatic backup and versioning
    - Secure access with signed URLs
    - Image processing and optimization

#### 5.3 Data Flow Architecture

```text
[Application] ──write──→ [Primary DB] ──replicate──→ [Read Replicas] 
│
│ 
│ 
├──CDC──→ [Search Index] 
│ 
│ 
├────cache────→ [Redis Cache] 
│
└────files────→ [Object Storage] ──CDN──→ [Global Distribution]
```

### 6. Security Architecture

#### 6.1 Security Layers
**Defense in Depth Strategy:**

**1. Network Security**
- **Perimeter Security**: Web Application Firewall (WAF)
- **Network Segmentation**: VPC with private/public subnets
- **DDoS Protection**: Cloud-based DDoS mitigation
- **SSL/TLS**: End-to-end encryption for all communications

**2. Application Security**
- **Authentication**: Multi-factor authentication (MFA)
- **Authorization**: Role-based access control (RBAC)
- **Input Validation**: Comprehensive input sanitization
- **Output Encoding**: XSS prevention
- **CSRF Protection**: Anti-CSRF tokens

**3. Data Security**
- **Encryption at Rest**: {{encryption_standard}} encryption
- **Encryption in Transit**: TLS {{tls_version}} minimum
- **Key Management**: Hardware Security Module (HSM)
- **Data Masking**: PII protection in non-production environments

#### 6.2 Authentication and Authorization

**Authentication Flow:**
[User] ──credentials──→ [Auth Service] ──validate──→ [Identity Provider]

```text
│ 
│ ←────JWT Token─────────────┘ 
│ [JWT Token] ──→ [API Gateway] ──verify──→ [Services]
```

**Authorization Model:**
- **Roles**: {{role_definitions}}
- **Permissions**: Granular permissions for each resource and operation
- **Policy Engine**: Centralized policy evaluation
- **Audit**: All authorization decisions logged

### 7. Integration Architecture

#### 7.1 Internal Integration
**Service-to-Service Communication:**
- **Synchronous**: REST APIs for real-time operations
- **Asynchronous**: Message queues for background processing
- **Event-Driven**: Event streaming for data consistency

**Message Bus ({{message_broker}})**
- **Purpose**: Asynchronous communication between services
- **Technology**: {{messaging_technology}} (Apache Kafka/RabbitMQ/AWS SQS)
- **Patterns**: Pub/Sub, Command/Query, Event Sourcing
- **Reliability**: Message durability, dead letter queues, retry logic

#### 7.2 External Integration
**Integration Patterns:**
- **REST APIs**: Standard HTTP-based integration
- **GraphQL**: Flexible data querying for mobile clients
- **WebSocket**: Real-time bidirectional communication
- **Webhook**: Event notifications to external systems

**External System Integrations:**

```text
+------------+----------+------------+----------------+------+
| System     | Protocol | Data Format| Authentication | SLA  |
+------------+----------+------------+----------------+------+
| {{external_1}} | REST    | JSON       | OAuth 2.0      | {{sla_1}} |
| {{external_2}} | SOAP    | XML        | Certificate    | {{sla_2}} |
| {{external_3}} | GraphQL | JSON       | API Key        | {{sla_3}} |
+------------+----------+------------+----------------+------+
```

### 8. Performance Architecture

#### 8.1 Performance Optimization Strategies
**Caching Strategy:**
- **CDN**: Global content distribution for static assets
- **Application Cache**: In-memory caching for frequently accessed data
- **Database Cache**: Query result caching
- **Browser Cache**: Client-side caching for UI components

**Database Optimization:**
- **Indexing Strategy**: Optimized indexes for query patterns
- **Query Optimization**: Stored procedures, query tuning
- **Connection Pooling**: Efficient database connection management
- **Read Replicas**: Load distribution for read operations

**Code Optimization:**
- **Lazy Loading**: Load data only when needed
- **Pagination**: Limit large dataset queries
- **Async Processing**: Non-blocking operations
- **Resource Compression**: Gzip compression for responses

#### 8.2 Scalability Design
**Horizontal Scaling:**
- **Load Balancing**: Distribute requests across service instances
- **Auto-scaling**: Automatic scaling based on metrics
- **Database Sharding**: Distribute data across multiple databases
- **Service Mesh**: Traffic management between services

**Vertical Scaling:**
- **Resource Optimization**: CPU and memory tuning
- **Performance Profiling**: Identify bottlenecks
- **Infrastructure Scaling**: Scale server resources as needed

### 9. Deployment Architecture

#### 9.1 Environment Strategy
**Environment Topology:**
- **Development**: Individual developer environments
- **Testing**: Automated testing environment
- **Staging**: Production-like environment for final testing
- **Production**: Live system serving end users

**Infrastructure as Code:**
- **Technology**: {{iac_tool}} (Terraform/CloudFormation/ARM)
- **Version Control**: Infrastructure definitions in source control
- **Automated Deployment**: CI/CD pipelines for infrastructure changes
- **Environment Parity**: Consistent configuration across environments

#### 9.2 Container Architecture
**Containerization Strategy:**
- **Container Technology**: Docker with {{orchestration}} (Kubernetes/Docker Swarm)
- **Service Mesh**: {{service_mesh}} (Istio/Linkerd) for service communication
- **Configuration Management**: Environment-specific configurations
- **Secret Management**: Secure handling of sensitive configuration

**Kubernetes Architecture:**

```text
┌───────────────────────────────────────────────────────────┐
│                    Ingress Controller                     │
├───────────────────────────────────────────────────────────┤
│ Service 1       │ Service 2       │ Service 3             │
│ [Pod Pool]      │ [Pod Pool]      │ [Pod Pool]            │
├───────────────────────────────────────────────────────────┤
│ ConfigMaps      │ Secrets                                 │
├───────────────────────────────────────────────────────────┤
│ Persistent Volumes               │ Network Policies       │
└───────────────────────────────────────────────────────────┘
```

### 10. Monitoring and Observability

#### 10.1 Observability Stack
**Three Pillars of Observability:**

**1. Metrics**
- **Application Metrics**: Response times, error rates, throughput
- **Infrastructure Metrics**: CPU, memory, disk, network usage
- **Business Metrics**: User engagement, conversion rates, revenue

**2. Logs**
- **Structured Logging**: JSON format with correlation IDs
- **Centralized Collection**: Log aggregation and analysis
- **Log Levels**: Appropriate logging levels for different environments

**3. Tracing**
- **Distributed Tracing**: Request flow across microservices
- **Performance Profiling**: Identify bottlenecks and optimize
- **Error Tracking**: Detailed error context and stack traces

#### 10.2 Alerting and SLA Monitoring
**Alert Categories:**
- **Critical**: Immediate response required (page on-call)
- **High**: Response within {{high_priority_sla}}
- **Medium**: Response within {{medium_priority_sla}}
- **Low**: Response within {{low_priority_sla}}

**SLA Monitoring:**
- **Availability**: System uptime and health checks
- **Performance**: Response time and throughput monitoring
- **Error Rate**: Application and infrastructure error tracking
- **Business KPIs**: User experience and business metric tracking

### 11. Disaster Recovery and Business Continuity

#### 11.1 Backup and Recovery Strategy
**Backup Strategy:**
- **Data Backup**: {{backup_frequency}} automated backups
- **Cross-Region Replication**: Geographic distribution
- **Point-in-Time Recovery**: Restore to specific timestamps
- **Testing**: Regular backup restoration testing

**Recovery Objectives:**
- **Recovery Time Objective (RTO)**: {{rto_target}}
- **Recovery Point Objective (RPO)**: {{rpo_target}}
- **Maximum Tolerable Downtime**: {{mtd_target}}

#### 11.2 High Availability Design
**Fault Tolerance:**
- **No Single Points of Failure**: Redundancy at all levels
- **Circuit Breakers**: Prevent cascading failures
- **Health Checks**: Proactive failure detection
- **Graceful Degradation**: Core functionality during partial failures

### 12. Architecture Governance

#### 12.1 Architecture Principles Compliance
**Validation Criteria:**
- [ ] Scalability requirements addressed
- [ ] Security requirements implemented
- [ ] Performance targets achievable
- [ ] Integration requirements satisfied
- [ ] Maintainability principles followed
- [ ] Cost constraints respected
- [ ] Technology standards compliant

#### 12.2 Architecture Evolution
**Change Management:**
- **Architecture Review Board**: Technical governance
- **Impact Assessment**: Change impact analysis
- **Migration Strategy**: Plan for architecture changes
- **Deprecation Policy**: Legacy system phase-out

## Output Format Requirements

Present the system architecture as:
- Executive summary with key architectural decisions
- Visual architecture diagrams at multiple levels
- Detailed component specifications
- Technology stack justification
- Performance and scalability analysis
- Security and compliance assessment
- Implementation roadmap and priorities

## Integration with Implementation Stage

This system architecture will guide the Implementation stage by providing:
- Detailed component specifications for development
- Technology stack and framework selections
- API contracts and interface definitions
- Database schemas and data models
- Security implementation requirements
- Deployment and infrastructure specifications
- Performance and monitoring requirements

Generate a comprehensive system architecture that enables successful implementation and meets all business and technical requirements.
