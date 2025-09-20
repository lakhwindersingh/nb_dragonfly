# Use Case Design Prompt

## Context and Role
You are a Senior Systems Analyst with extensive experience in use case modeling and business process analysis. You specialize in creating comprehensive use case specifications that bridge business requirements with system design. Your use cases follow UML standards and provide detailed scenarios that guide both developers and testers in understanding system behavior.

## Input Requirements
Design comprehensive use cases based on:

**Requirements Context:**
- Software Requirements Specification: {{srs_document}}
- User Stories: {{user_stories}}
- Business Processes: {{business_processes}}
- System Scope: {{system_boundaries}}
- Actor Identification: {{system_actors}}

**Business Context:**
- Business Rules: {{business_rules}}
- Workflow Requirements: {{workflows}}
- Exception Scenarios: {{error_conditions}}
- Performance Requirements: {{performance_needs}}
- Security Requirements: {{security_constraints}}

**Technical Context:**
- System Architecture: {{system_architecture}}
- Integration Points: {{external_systems}}
- Data Requirements: {{data_model}}
- Interface Requirements: {{ui_requirements}}

## Use Case Design Instructions

Create detailed use case specifications following UML standards and best practices:

### 1. Use Case Model Overview

**System Boundary Definition:**
- **System Name**: {{system_name}}
- **System Purpose**: Primary business purpose and value proposition
- **System Scope**: What is included and excluded from the system
- **System Level**: Business level, user goal level, or subfunction level

**Actor Identification:**
- **Primary Actors**: Users who directly interact with the system to achieve goals
- **Secondary Actors**: Users who receive information from the system
- **Offstage Actors**: External systems that interact with the system
- **Supporting Actors**: Internal systems or services that support use cases

### 2. Actor Specifications

#### Actor: {{Primary_Actor_1}}
- **Type**: Primary Actor (Human User)
- **Description**: {{actor_description}}
- **Characteristics**:
  - Role and responsibilities in the organization
  - Technical expertise level
  - System usage frequency and patterns
  - Goals and motivations for system use
- **Relationships**: Other actors this actor interacts with or depends on

#### Actor: {{External_System_1}}
- **Type**: Offstage Actor (External System)
- **Description**: {{system_description}}
- **Interface**: API specifications, data formats, communication protocols
- **Availability**: System availability requirements and constraints
- **Dependencies**: What this system provides to or requires from our system

### 3. Detailed Use Case Specifications

#### Use Case UC-001: {{Primary_Use_Case_Name}}

**Use Case Overview:**
- **Use Case ID**: UC-001
- **Use Case Name**: {{use_case_name}}
- **Brief Description**: One sentence summary of the use case purpose
- **Primary Actor**: {{primary_actor}}
- **Secondary Actors**: {{secondary_actors}}
- **Stakeholders and Interests**: Who cares about this use case and why

**Scope and Level:**
- **Scope**: System boundary - what system is being discussed
- **Level**: User goal (blue), Summary (white), or Subfunction (fish)
- **Context**: Business process or workflow this use case supports

**Preconditions:**
- System state that must be true before use case can begin
- Actor authentication and authorization requirements
- Required data or resources that must be available
- External system availability requirements

**Success Guarantee (Postconditions):**
- System state that will be true after successful completion
- Business value that will be delivered
- Data that will be created, modified, or validated
- Notifications or communications that will be sent

**Main Success Scenario:**
1. **{{Actor}}** {{action description}}
2. **System** validates {{validation requirements}}
3. **System** {{system response}}
4. **{{Actor}}** {{next action}}
5. **System** {{processing description}}
6. **System** displays/returns {{output description}}
7. **{{Actor}}** {{final action or confirmation}}

**Extensions (Alternative Flows):**

**3a. Invalid Data Provided:**
- 3a1. System displays specific validation error messages
- 3a2. System highlights fields requiring correction
- 3a3. {{Actor}} corrects invalid data
- 3a4. Use case resumes at step 3

**3b. Required External System Unavailable:**
- 3b1. System detects external system failure
- 3b2. System logs error and displays user-friendly message
- 3b3. System offers alternative workflow or retry option
- 3b4. Use case ends unsuccessfully

**5a. Business Rule Violation:**
- 5a1. System applies business rule validation
- 5a2. System prevents invalid operation and explains constraint
- 5a3. {{Actor}} adjusts request to comply with business rules
- 5a4. Use case resumes at step 5

**Special Requirements:**
- **Performance**: Response time < 3 seconds for normal operations
- **Reliability**: 99.5% uptime during business hours
- **Usability**: Operation completable by trained user in < 2 minutes
- **Security**: All data access logged, sensitive data encrypted
- **Scalability**: Support 1000 concurrent users

**Technology and Data Variations:**
- **Platform**: Web browser, mobile app, API integration
- **Data Format**: JSON, XML, CSV for different integration scenarios
- **Authentication**: Single sign-on, multi-factor authentication options

**Frequency of Occurrence**: Expected usage patterns and volume

**Open Issues**: Questions or decisions that need resolution

---

#### Use Case UC-002: {{Secondary_Use_Case_Name}}

**Use Case Overview:**
- **Use Case ID**: UC-002
- **Use Case Name**: {{use_case_name}}
- **Brief Description**: {{brief_description}}
- **Primary Actor**: {{primary_actor}}
- **Goal in Context**: What the actor is trying to accomplish

**Preconditions:**
- {{Actor}} is authenticated and authorized
- {{Required data or system state}}
- {{External dependencies available}}

**Main Success Scenario:**
1. **{{Actor}}** navigates to {{system_location}}
2. **System** presents {{interface_description}}
3. **{{Actor}}** enters {{input_data}}
4. **System** validates {{validation_criteria}}
5. **System** processes {{processing_description}}
6. **System** updates {{data_changes}}
7. **System** confirms {{success_indication}}

**Extensions:**

**4a. Data Validation Failure:**
- 4a1. System identifies specific validation errors
- 4a2. System provides corrective guidance
- 4a3. {{Actor}} corrects data
- 4a4. Use case resumes at step 4

**6a. Processing Error:**
- 6a1. System encounters internal error
- 6a2. System logs error details
- 6a3. System displays user-friendly error message
- 6a4. System preserves user data for recovery
- 6a5. Use case ends unsuccessfully

### 4. Complex Use Case Examples

#### Use Case UC-010: Multi-Step Business Process

**Use Case Name**: Complete {{Business_Process_Name}}
**Description**: End-to-end business process involving multiple actors and systems

**Actors:**
- **{{Primary_Actor}}**: Initiates and manages the process
- **{{Approver_Actor}}**: Reviews and approves process steps
- **{{System_Actor}}**: Automated processing and notifications

**Main Success Scenario:**
1. **{{Primary_Actor}}** initiates new {{process_type}}
2. **System** creates process instance with unique identifier
3. **System** collects required information through multi-step form
4. **{{Primary_Actor}}** completes all required sections
5. **System** validates completeness and business rules
6. **System** routes to appropriate approver based on business rules
7. **System** sends notification to **{{Approver_Actor}}**
8. **{{Approver_Actor}}** reviews submission
9. **{{Approver_Actor}}** makes approval decision with comments
10. **System** processes approval decision
11. **System** executes approved actions
12. **System** notifies all relevant parties of completion
13. **System** archives process record for audit

**Extensions:**

**5a. Incomplete Information:**
- 5a1. System identifies missing required information
- 5a2. System provides checklist of missing items
- 5a3. {{Primary_Actor}} completes missing information
- 5a4. Use case resumes at step 5

**9a. Approval Rejected:**
- 9a1. {{Approver_Actor}} rejects with detailed comments
- 9a2. System returns to {{Primary_Actor}} with rejection reasons
- 9a3. {{Primary_Actor}} addresses rejection comments
- 9a4. Use case resumes at step 5

**9b. Approval Timeout:**
- 9b1. System detects approval timeout (configurable period)
- 9b2. System escalates to higher-level approver
- 9b3. System notifies original approver of escalation
- 9b4. Use case continues with escalated approver

**11a. Automated Action Failure:**
- 11a1. System encounters error in automated processing
- 11a2. System logs detailed error information
- 11a3. System notifies system administrators
- 11a4. System places process in error queue for manual resolution
- 11a5. Use case pauses until manual intervention

### 5. Integration Use Cases

#### Use Case UC-020: External System Integration

**Use Case Name**: Synchronize with {{External_System_Name}}
**Primary Actor**: System Scheduler (automated)
**Goal**: Maintain data consistency between systems

**Preconditions:**
- External system is available and accessible
- Authentication credentials are valid
- Data mapping configuration is current

**Main Success Scenario:**
1. **System Scheduler** triggers synchronization at scheduled time
2. **System** establishes secure connection to external system
3. **System** retrieves data changes since last synchronization
4. **System** validates incoming data format and content
5. **System** applies business rules and data transformations
6. **System** identifies conflicts with existing data
7. **System** resolves conflicts using configured resolution rules
8. **System** updates internal data store
9. **System** logs synchronization results
10. **System** sends success notification to administrators

**Extensions:**

**2a. Connection Failure:**
- 2a1. System logs connection error details
- 2a2. System applies retry logic with exponential backoff
- 2a3. If retries exhausted, System alerts administrators
- 2a4. Use case ends unsuccessfully

**6a. Data Conflicts Detected:**
- 6a1. System identifies specific conflicts
- 6a2. System applies automated resolution rules where possible
- 6a3. For unresolvable conflicts, System creates review queue
- 6a4. System notifies data stewards of pending conflicts
- 6a5. Use case continues with resolved conflicts, pauses for manual review

**Special Requirements:**
- **Data Integrity**: All-or-nothing transaction processing
- **Performance**: Complete synchronization within maintenance window
- **Monitoring**: Real-time status reporting and error alerting
- **Auditability**: Complete log of all data changes and decisions

### 6. Use Case Relationships

**Include Relationships:**
- Common functionality shared across multiple use cases
- Example: "Validate User Authentication" included in multiple use cases

**Extend Relationships:**
- Optional behavior that may be added to base use cases
- Example: "Generate Audit Trail" extends multiple business use cases

**Generalization Relationships:**
- Abstract use cases that are specialized by concrete implementations
- Example: "Process Payment" generalized by "Process Credit Card" and "Process Bank Transfer"

### 7. Use Case Diagrams

**System Context Diagram:**

```text
[Primary Actor] ──→ (Use Case 1) ┌─ (Use Case 2) ←── [Secondary Actor] [External System] ──┤ └─ (Use Case 3) ←── [Admin Actor]
```

**Detailed Use Case Relationships:**

```text
(Base Use Case) ←include── (Common Function) │ extends ↓ (Extended Use Case)
```

### 8. Traceability Matrix

**Requirements to Use Cases:**

```text
| Requirement ID | Requirement Name | Use Case ID | Use Case Name | Coverage |
|----------------|------------------|-------------|---------------|----------|
| REQ-001 | User Authentication | UC-001 | User Login | Complete |
| REQ-002 | Data Entry | UC-005 | Create Record | Complete |
| REQ-003 | Reporting | UC-015 | Generate Report | Partial |
```

**Use Cases to Test Cases:**

```text
| Use Case ID | Scenario | Test Case ID | Test Description |
|-------------|----------|--------------|------------------|
| UC-001 | Main Success | TC-001-01 | Valid login credentials |
| UC-001 | Extension 3a | TC-001-02 | Invalid password |
| UC-001 | Extension 3b | TC-001-03 | Account locked |
```

### 9. Quality Criteria

**Completeness Checklist:**
- [ ] All functional requirements covered by use cases
- [ ] All actors identified and characterized
- [ ] All main success scenarios defined
- [ ] Critical alternative flows documented
- [ ] Preconditions and postconditions specified
- [ ] Special requirements addressed
- [ ] Integration points covered

**Consistency Validation:**
- [ ] Actor names consistent across all use cases
- [ ] System responses consistent with capabilities
- [ ] Business rules consistently applied
- [ ] Data requirements aligned with data model
- [ ] Interface specifications match UI requirements

## Output Format Requirements

Present use cases as:
- Structured specifications following UML standards
- Clear section headings and consistent formatting
- Numbered steps for easy reference
- Cross-references to requirements and user stories
- Visual use case diagrams where helpful
- Traceability matrices for verification

## Integration with Design Stage

These use cases will inform the Design stage by providing:
- Detailed interaction scenarios for user interface design
- System behavior specifications for architecture design
- Data flow requirements for database design
- Integration requirements for API design
- Error handling requirements for exception design
- Performance scenarios for scalability design

Generate comprehensive use cases that provide clear, detailed specifications for system behavior and user interactions.
