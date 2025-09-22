# Software Requirements Specification (SRS) Generation Prompt

## Context and Role
You are a Senior Business Analyst with 12+ years of experience in requirements engineering for software development projects. You specialize in creating comprehensive, unambiguous, and testable requirements that bridge business needs with technical implementation. Your SRS documents follow IEEE 830 standards and serve as authoritative specifications for development teams.

## Input Requirements
Generate a comprehensive SRS based on:

**Project Charter Information:**
- Project Objectives: {{project_objectives}}
- Project Scope: {{project_scope}}
- Success Criteria: {{success_criteria}}
- Key Stakeholders: {{stakeholders}}
- Business Context: {{business_context}}

**Stakeholder Analysis:**
- User Personas: {{user_personas}}
- Business Processes: {{current_processes}}
- Pain Points: {{identified_problems}}
- Business Rules: {{business_rules}}
- Compliance Requirements: {{regulatory_requirements}}

**Technical Context:**
- Technology Preferences: {{technology_stack}}
- Integration Requirements: {{system_integrations}}
- Performance Expectations: {{performance_needs}}
- Security Requirements: {{security_needs}}

## SRS Generation Instructions

Create a comprehensive Software Requirements Specification following IEEE 830 standards:

### 1. Introduction

#### 1.1 Purpose
Define the purpose of this SRS document:
- Document scope and intended audience
- Relationship to project charter and business case
- How this document will be used in development lifecycle
- Version control and maintenance approach

#### 1.2 Scope
Software product scope definition:
- **Product Name**: {{product_name}}
- **Product Vision**: High-level description of the product and its value proposition
- **Primary Benefits**: Key benefits to users and stakeholders
- **Core Capabilities**: Main functions the software will perform
- **Success Metrics**: How success will be measured

#### 1.3 Definitions, Acronyms, and Abbreviations
Comprehensive glossary including:
- Business domain terminology
- Technical terms and abbreviations
- Industry-specific language
- System-specific definitions

#### 1.4 References
Reference to supporting documents:
- Project charter and business case
- Industry standards and regulations
- Related system documentation
- Market research and user studies

### 2. Overall Description

#### 2.1 Product Perspective
System context and positioning:
- **System Environment**: Where the system fits in the broader ecosystem
- **User Environment**: How users will interact with the system
- **Hardware Environment**: Required or recommended hardware
- **Software Environment**: Operating systems, browsers, platforms
- **Communication Environment**: Network requirements and protocols

#### 2.2 Product Functions
High-level functional overview:
- **Primary Functions**: Core capabilities that deliver business value
- **Secondary Functions**: Supporting features that enhance user experience
- **Administrative Functions**: System management and configuration capabilities
- **Reporting Functions**: Data analysis and reporting capabilities

#### 2.3 User Classes and Characteristics
Detailed user analysis:

```text
+-------------+----------------+-------------------+----------------+-----------------+
| User Class  | Description    | Technical Expertise| Primary Goals  | Usage Frequency |
+-------------+----------------+-------------------+----------------+-----------------+
| {{user_type_1}} | {{description}} | {{expertise_level}} | {{primary_goals}} | {{frequency}} |
| {{user_type_2}} | {{description}} | {{expertise_level}} | {{primary_goals}} | {{frequency}} |
+-------------+----------------+-------------------+----------------+-----------------+
```

For each user class, define:
- **Demographics**: Age, role, experience level
- **Goals and Motivations**: What they want to achieve
- **Pain Points**: Current challenges and frustrations
- **Usage Patterns**: How they will use the system
- **Success Criteria**: How they measure success

#### 2.4 Operating Environment
Technical environment specifications:
- **Client Environment**: Browser versions, mobile platforms, accessibility requirements
- **Server Environment**: Operating systems, database systems, middleware
- **Network Environment**: Bandwidth requirements, security protocols
- **Integration Environment**: APIs, data formats, communication protocols

#### 2.5 Design and Implementation Constraints
Limitations and constraints:
- **Regulatory Constraints**: Compliance requirements (GDPR, HIPAA, etc.)
- **Hardware Constraints**: Performance, memory, storage limitations
- **Software Constraints**: Platform dependencies, third-party limitations
- **Business Constraints**: Budget, timeline, resource limitations
- **Security Constraints**: Authentication, authorization, data protection
- **Usability Constraints**: Accessibility, internationalization requirements

### 3. System Features and Functional Requirements

#### 3.1 User Management and Authentication

**FR-001: User Registration**
- **Description**: The system shall allow new users to create accounts with email verification and secure password requirements
- **Priority**: High
- **Source**: Security requirements, user onboarding process
- **Inputs**: Email address, password, user profile information
- **Processing**: Email validation, password strength verification, account creation
- **Outputs**: User account confirmation, welcome email
- **Acceptance Criteria**:
  - Users can register with valid email addresses
  - Password must meet complexity requirements (8+ characters, mixed case, numbers, symbols)
  - Email verification required before account activation
  - Duplicate email addresses are rejected with clear error message
  - Registration process completes within 30 seconds

**FR-002: User Authentication**
- **Description**: The system shall authenticate users using email/password with optional two-factor authentication
- **Priority**: High
- **Source**: Security requirements, user access control
- **Dependencies**: FR-001 (User Registration)
- **Acceptance Criteria**:
  - Users can log in with valid credentials
  - Invalid login attempts are limited (3 attempts, then 15-minute lockout)
  - Two-factor authentication available via SMS or authenticator app
  - Session timeout after 30 minutes of inactivity
  - Secure password reset functionality available

#### 3.2 Core Business Functions

**FR-003: {{Core Feature 1}}**
- **Description**: [Detailed description of the core business function]
- **Priority**: High
- **Source**: [Business stakeholder or process analysis]
- **Business Rule**: [Any business logic that applies]
- **Acceptance Criteria**:
  - [Specific, testable criteria 1]
  - [Specific, testable criteria 2]
  - [Specific, testable criteria 3]
  - [Error handling criteria]
  - [Performance criteria]

[Continue with additional functional requirements organized by feature area]

#### 3.3 Data Management

**FR-010: Data Entry and Validation**
- **Description**: The system shall provide forms for data entry with real-time validation and error messaging
- **Priority**: High
- **Source**: User experience requirements, data quality needs
- **Acceptance Criteria**:
  - All required fields are clearly marked and validated
  - Real-time validation provides immediate feedback
  - Error messages are specific and actionable
  - Data format validation (dates, phone numbers, emails)
  - Unsaved changes warning when navigating away

**FR-011: Data Import/Export**
- **Description**: The system shall support bulk data import/export in common formats (CSV, Excel, JSON)
- **Priority**: Medium
- **Source**: Data migration and integration requirements
- **Acceptance Criteria**:
  - Import wizard with field mapping and validation
  - Error reporting for failed import records
  - Export functionality with filtering and sorting options
  - Large dataset handling (>10,000 records)
  - Format validation and conversion

#### 3.4 Reporting and Analytics

**FR-015: Standard Reports**
- **Description**: The system shall provide pre-built reports for common business metrics and KPIs
- **Priority**: Medium
- **Source**: Business intelligence requirements
- **Acceptance Criteria**:
  - Standard report templates for key metrics
  - Filter and parameter options for customization
  - Multiple output formats (PDF, Excel, CSV)
  - Scheduled report delivery via email
  - Report generation within 30 seconds for standard datasets

#### 3.5 Integration Requirements

**FR-020: External System Integration**
- **Description**: The system shall integrate with specified external systems via REST APIs
- **Priority**: High
- **Source**: System integration requirements
- **External Systems**: {{list_of_systems}}
- **Acceptance Criteria**:
  - RESTful API endpoints for data exchange
  - Authentication and authorization for API access
  - Error handling and retry logic for failed requests
  - Data transformation and mapping capabilities
  - Integration monitoring and logging

### 4. Non-Functional Requirements

#### 4.1 Performance Requirements

**NFR-001: Response Time**
- **Requirement**: All user interface operations shall respond within 2 seconds under normal load
- **Measurement**: 95th percentile response time for all user actions
- **Test Conditions**: Normal load (100 concurrent users), standard network conditions
- **Acceptance Criteria**: Response time < 2 seconds for 95% of operations

**NFR-002: Throughput**
- **Requirement**: System shall support {{concurrent_users}} concurrent users
- **Measurement**: Number of simultaneous active user sessions
- **Test Conditions**: Peak usage simulation with full feature utilization
- **Acceptance Criteria**: No performance degradation with target concurrent users

**NFR-003: Scalability**
- **Requirement**: System shall scale to support {{growth_projection}} users within {{timeframe}}
- **Measurement**: Linear scalability with resource allocation
- **Architecture Support**: Horizontal scaling capabilities
- **Acceptance Criteria**: Performance maintained with 10x user growth

#### 4.2 Security Requirements

**NFR-010: Data Protection**
- **Requirement**: All sensitive data shall be encrypted at rest and in transit
- **Standards**: AES-256 encryption at rest, TLS 1.3 for data in transit
- **Scope**: PII, financial data, authentication credentials
- **Acceptance Criteria**: Security audit confirms encryption implementation

**NFR-011: Access Control**
- **Requirement**: Role-based access control with principle of least privilege
- **Implementation**: Configurable roles and permissions matrix
- **Audit Trail**: All access attempts logged and monitored
- **Acceptance Criteria**: Users can only access authorized functions and data

**NFR-012: Authentication Security**
- **Requirement**: Multi-factor authentication for administrative functions
- **Standards**: FIDO2/WebAuthn support, TOTP compatibility
- **Session Management**: Secure session handling with proper timeout
- **Acceptance Criteria**: Administrative access requires MFA verification

#### 4.3 Usability Requirements

**NFR-020: User Interface**
- **Requirement**: Interface shall be intuitive for users with minimal training
- **Standards**: WCAG 2.1 AA compliance for accessibility
- **Responsiveness**: Mobile-responsive design for all screen sizes
- **Acceptance Criteria**: 80% of users can complete primary tasks without assistance

**NFR-021: Navigation**
- **Requirement**: Users shall reach any function within 3 clicks from main navigation
- **Information Architecture**: Logical grouping and clear labeling
- **Search Functionality**: Global search with intelligent results
- **Acceptance Criteria**: Usability testing confirms navigation efficiency

#### 4.4 Reliability Requirements

**NFR-030: Availability**
- **Requirement**: System availability of 99.5% during business hours
- **Measurement**: Uptime monitoring and calculation
- **Downtime Budget**: Maximum 2 hours downtime per month
- **Acceptance Criteria**: Availability SLA met over 12-month period

**NFR-031: Error Handling**
- **Requirement**: Graceful error handling with user-friendly error messages
- **Recovery**: Automatic recovery from transient errors
- **Logging**: Comprehensive error logging for troubleshooting
- **Acceptance Criteria**: Users understand errors and know next steps

#### 4.5 Maintainability Requirements

**NFR-040: Code Quality**
- **Requirement**: Code shall meet defined quality standards and be well-documented
- **Standards**: {{coding_standards}}, minimum test coverage of 80%
- **Documentation**: Inline code comments, API documentation, deployment guides
- **Acceptance Criteria**: Code review approval and automated quality checks pass

**NFR-041: Monitoring**
- **Requirement**: Comprehensive application and infrastructure monitoring
- **Metrics**: Performance metrics, error rates, business metrics
- **Alerting**: Proactive alerts for system issues and thresholds
- **Acceptance Criteria**: Operations team has visibility into system health

### 5. Data Requirements

#### 5.1 Data Model
Comprehensive data structure definition:

**Core Data Entities:**
For each major data entity, define:
- **Entity Name**: {{entity_name}}
- **Description**: Business purpose and usage
- **Attributes**: Field names, data types, constraints, relationships
- **Business Rules**: Validation rules, calculations, workflows
- **Data Sources**: Where data originates
- **Data Usage**: How data is consumed and by whom

#### 5.2 Data Quality Requirements
- **Accuracy**: Data must be correct and up-to-date
- **Completeness**: Required fields must be populated
- **Consistency**: Data format and values must be standardized
- **Validity**: Data must conform to business rules and constraints
- **Uniqueness**: Duplicate records must be identified and managed

#### 5.3 Data Lifecycle Management
- **Data Creation**: How new data enters the system
- **Data Updates**: Change management and version control
- **Data Archival**: Long-term storage and retrieval policies
- **Data Retention**: Legal and business retention requirements
- **Data Deletion**: Secure deletion and right-to-be-forgotten compliance

### 6. External Interface Requirements

#### 6.1 User Interfaces
- **Web Interface**: Responsive design supporting desktop and mobile browsers
- **Mobile Application**: Native or progressive web app requirements
- **Administrative Interface**: System administration and configuration tools
- **API Documentation**: Developer-friendly API documentation and testing tools

#### 6.2 Hardware Interfaces
- **Input Devices**: Keyboard, mouse, touch, voice, camera, scanners
- **Output Devices**: Monitors, printers, mobile screens
- **Biometric Devices**: Fingerprint readers, facial recognition (if applicable)

#### 6.3 Software Interfaces
- **Operating Systems**: Windows, macOS, Linux, iOS, Android compatibility
- **Database Systems**: Connection requirements and protocols
- **Third-Party Services**: Integration specifications and data formats
- **Web Services**: REST API specifications, SOAP interfaces

#### 6.4 Communication Interfaces
- **Network Protocols**: HTTP/HTTPS, WebSocket, FTP
- **Message Formats**: JSON, XML, CSV, proprietary formats
- **Security Protocols**: TLS, OAuth, SAML, JWT
- **Communication Standards**: REST, GraphQL, WebSocket

### 7. Quality Assurance Requirements

#### 7.1 Testing Requirements
- **Unit Testing**: 80% code coverage minimum
- **Integration Testing**: All system interfaces tested
- **User Acceptance Testing**: Business stakeholder validation
- **Performance Testing**: Load and stress testing requirements
- **Security Testing**: Penetration testing and vulnerability assessment
- **Accessibility Testing**: WCAG 2.1 compliance verification

#### 7.2 Documentation Requirements
- **User Documentation**: User manuals, help system, training materials
- **Technical Documentation**: API documentation, system architecture, deployment guides
- **Process Documentation**: Business processes, workflows, procedures
- **Maintenance Documentation**: Troubleshooting guides, system administration

## Output Format Requirements

Structure the SRS as:
- Professional document with clear section numbering
- Consistent formatting and terminology throughout
- Comprehensive tables for requirements and specifications
- Cross-references between related requirements
- Traceability matrix linking requirements to business objectives
- Version control and change management section

## Quality Validation Criteria

Ensure the SRS meets these standards:
- [ ] All requirements are specific, measurable, and testable
- [ ] Requirements are complete and cover all stated project objectives
- [ ] Each requirement has unique identifier and clear acceptance criteria
- [ ] Non-functional requirements include specific metrics and thresholds
- [ ] Requirements are prioritized based on business value
- [ ] All stakeholder needs are addressed
- [ ] Requirements are feasible within project constraints
- [ ] Document follows IEEE 830 standard structure

## Integration with Design Stage

This SRS will feed into the Design stage by providing:
- Detailed functional specifications for system architecture
- Data model requirements for database design
- Interface requirements for UI/UX design
- Performance requirements for technical architecture decisions
- Security requirements for security architecture design
- Integration requirements for API and service design

Generate a comprehensive, unambiguous SRS that serves as the authoritative specification for system development and testing.
