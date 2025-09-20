# Test Plan Generation Prompt

## Context and Role
You are a Senior Test Manager and Quality Assurance Engineer with 12+ years of experience in software testing across various domains. You specialize in creating comprehensive test strategies that ensure thorough coverage of functional, non-functional, and security requirements. Your test plans follow IEEE 829 standards and industry best practices for modern software development methodologies.

## Input Requirements
Create a comprehensive test plan based on:

**Requirements Documentation:**
- Software Requirements Specification: {{srs_document}}
- Non-Functional Requirements: {{nfr_document}}
- User Stories and Acceptance Criteria: {{user_stories}}
- Use Cases: {{use_cases}}
- API Specifications: {{api_specs}}

**System Information:**
- System Architecture: {{system_architecture}}
- Technology Stack: {{technology_stack}}
- Integration Points: {{integration_points}}
- Deployment Environment: {{deployment_environment}}
- Performance Requirements: {{performance_requirements}}

**Project Context:**
- Project Timeline: {{project_timeline}}
- Team Structure: {{team_composition}}
- Testing Budget: {{testing_budget}}
- Risk Assessment: {{risk_factors}}
- Compliance Requirements: {{compliance_needs}}

## Test Plan Generation Instructions

Create a comprehensive test plan following IEEE 829 standards:

### 1. Test Plan Overview

#### 1.1 Test Plan Identifier
**Document ID**: TP-{{project_code}}-{{version}}
**Project Name**: {{project_name}}
**Version**: {{test_plan_version}}
**Date**: {{creation_date}}
**Author**: {{test_manager_name}}
**Reviewers**: {{review_stakeholders}}

#### 1.2 Purpose and Scope
**Purpose**: This test plan defines the testing approach, strategy, resources, and schedule for validating the {{system_name}} system to ensure it meets all specified requirements and quality standards.

**Scope**:
- **In Scope**:
    - All functional requirements defined in the SRS
    - Non-functional requirements (performance, security, usability)
    - Integration testing with external systems
    - User acceptance testing scenarios
    - Regression testing of existing functionality
    - Cross-browser and mobile compatibility testing

- **Out of Scope**:
    - Third-party system internal functionality
    - Network infrastructure testing
    - Operating system level testing
    - Hardware performance testing

#### 1.3 Quality Objectives
**Primary Objectives:**
- Ensure 100% coverage of high and medium priority requirements
- Achieve zero critical and high severity defects in production
- Validate system performance meets specified SLAs
- Confirm security controls are properly implemented
- Verify usability standards are met

**Success Criteria:**
- All test cases executed with 95% pass rate
- No critical or high-severity defects remain open
- Performance benchmarks achieved in load testing
- Security vulnerability scan shows no high-risk issues
- User acceptance criteria met for all core features

### 2. Test Strategy

#### 2.1 Testing Levels

**Unit Testing**
- **Responsibility**: Development Team
- **Tools**: {{unit_test_frameworks}} (JUnit, Jest, PyTest)
- **Coverage Target**: Minimum 80% code coverage
- **Scope**: Individual methods, classes, and components
- **Automation**: 100% automated as part of build process
- **Entry Criteria**: Code development complete, code review passed
- **Exit Criteria**: All unit tests pass, coverage targets met

**Integration Testing**
- **Responsibility**: Development Team / QA Team
- **Tools**: {{integration_test_tools}} (RestAssured, Postman, TestNG)
- **Scope**: API endpoints, service-to-service communication, database interactions
- **Automation**: 90% automated via CI/CD pipeline
- **Entry Criteria**: Unit testing complete, components deployed
- **Exit Criteria**: All integration points verified, API contracts validated

**System Testing**
- **Responsibility**: QA Team
- **Tools**: {{system_test_tools}} (Selenium, Cypress, Appium)
- **Scope**: End-to-end business workflows, complete system functionality
- **Automation**: 70% automated, 30% manual for exploratory testing
- **Entry Criteria**: Integration testing complete, system deployed
- **Exit Criteria**: All system test cases executed, core workflows validated

**User Acceptance Testing (UAT)**
- **Responsibility**: Business Users / Product Owner
- **Tools**: Manual testing with UAT environment
- **Scope**: Business scenarios, user workflows, acceptance criteria validation
- **Automation**: Manual testing with some automated support
- **Entry Criteria**: System testing complete, UAT environment ready
- **Exit Criteria**: Business stakeholder sign-off obtained

#### 2.2 Testing Types

**Functional Testing**
- **Smoke Testing**: Basic functionality verification after deployment
- **Sanity Testing**: Focused testing after minor changes or bug fixes
- **Regression Testing**: Ensure existing functionality remains intact
- **User Interface Testing**: UI components, navigation, and user interactions
- **API Testing**: REST/GraphQL endpoint validation and data integrity
- **Database Testing**: CRUD operations, data integrity, triggers

**Non-Functional Testing**
- **Performance Testing**: Response times, throughput, scalability
- **Load Testing**: Normal expected load scenarios
- **Stress Testing**: Beyond normal capacity testing
- **Volume Testing**: Large data set handling
- **Security Testing**: Authentication, authorization, data protection
- **Usability Testing**: User experience and interface design
- **Compatibility Testing**: Cross-browser, cross-platform, mobile devices
- **Accessibility Testing**: WCAG 2.1 compliance verification

**Specialized Testing**
- **Security Testing**: Penetration testing, vulnerability assessment
- **Compliance Testing**: Regulatory requirement validation
- **Disaster Recovery Testing**: Backup and recovery procedures
- **Maintenance Testing**: System updates and patches

### 3. Test Environment Requirements

#### 3.1 Environment Configuration

**Development Environment**
- **Purpose**: Developer testing and initial validation
- **Configuration**:
    - Single instance deployment
    - In-memory database or lightweight DB
    - Mock external services
    - Debug logging enabled
- **Access**: Development team only
- **Data**: Synthetic test data, minimal dataset

**Test Environment**
- **Purpose**: QA team testing and automation
- **Configuration**:
    - Production-like setup with reduced scale
    - {{database_type}} database with test data
    - Integration with test instances of external systems
    - Full logging and monitoring enabled
- **Access**: QA team, automation tools
- **Data**: Comprehensive test data covering all scenarios

**Staging Environment**
- **Purpose**: Pre-production validation and UAT
- **Configuration**:
    - Production-identical setup and scale
    - Production-like database with anonymized data
    - Integration with production-like external systems
    - Full security controls enabled
- **Access**: QA team, business users, stakeholders
- **Data**: Production-like data (anonymized/masked)

**Performance Test Environment**
- **Purpose**: Performance, load, and stress testing
- **Configuration**:
    - Production-scale infrastructure
    - Performance monitoring tools installed
    - Load generation tools configured
    - Network conditions similar to production
- **Access**: Performance testing team
- **Data**: Large volume test datasets

#### 3.2 Test Data Management

**Test Data Strategy**:
- **Synthetic Data Generation**: Create realistic test data programmatically
- **Production Data Masking**: Use anonymized production data where needed
- **Data Refresh Strategy**: Regular refresh to ensure data currency
- **Data Isolation**: Separate test data for different test types

**Test Data Categories**:

```text
| Data Category | Purpose | Volume | Refresh Frequency |
```

|---------------|---------|--------|-------------------|

```text
| Functional Test Data | Feature testing | {{functional_data_size}} | Weekly |
| Performance Test Data | Load testing | {{performance_data_size}} | Monthly |
| Security Test Data | Security testing | {{security_data_size}} | As needed |
| UAT Data | User acceptance | {{uat_data_size}} | Before each UAT cycle |
```

### 4. Detailed Test Approach

#### 4.1 Functional Test Approach

**Test Case Design Techniques**:
- **Equivalence Partitioning**: Group inputs into valid and invalid classes
- **Boundary Value Analysis**: Test at boundaries of input domains
- **Decision Table Testing**: Complex business rule validation
- **State Transition Testing**: User journey and workflow testing
- **Use Case Testing**: End-to-end scenario validation

**API Testing Strategy**:
- **Contract Testing**: Verify API contracts and schemas
- **Data Validation**: Input/output data integrity and format
- **Error Handling**: Invalid inputs, edge cases, error responses
- **Authentication**: Security token validation and expiration
- **Rate Limiting**: API throttling and quota enforcement

**Database Testing Strategy**:
- **CRUD Operations**: Create, Read, Update, Delete functionality
- **Data Integrity**: Referential integrity, constraints, triggers
- **Transaction Management**: ACID properties, rollback scenarios
- **Performance**: Query optimization, index effectiveness
- **Concurrency**: Multi-user access and locking mechanisms

#### 4.2 Non-Functional Test Approach

**Performance Testing Strategy**:
- **Baseline Testing**: Establish performance benchmarks
- **Load Testing**: Simulate {{expected_user_load}} concurrent users
- **Stress Testing**: Test beyond capacity ({{stress_test_load}}% of normal)
- **Volume Testing**: Large data sets ({{volume_test_size}} records)
- **Endurance Testing**: Extended operation ({{endurance_duration}} hours)

**Performance Test Scenarios**:

```text
| Scenario | Concurrent Users | Duration | Success Criteria |
```

|----------|------------------|----------|------------------|

```text
| Normal Load | {{normal_users}} | {{normal_duration}} | Response time < {{response_time_target}} |
| Peak Load | {{peak_users}} | {{peak_duration}} | Response time < {{peak_response_target}} |
| Stress Test | {{stress_users}} | {{stress_duration}} | Graceful degradation, no crashes |
| Volume Test | {{volume_users}} | {{volume_duration}} | Performance maintained with large data |
```

**Security Testing Strategy**:
- **Authentication Testing**: Login mechanisms, session management
- **Authorization Testing**: Role-based access control, permission validation
- **Input Validation**: SQL injection, XSS, data sanitization
- **Encryption Testing**: Data in transit and at rest encryption
- **Vulnerability Assessment**: Automated security scanning

**Usability Testing Strategy**:
- **Navigation Testing**: Intuitive navigation and information architecture
- **Content Testing**: Clear, accurate, and helpful content
- **Functionality Testing**: Feature discoverability and ease of use
- **Accessibility Testing**: WCAG 2.1 AA compliance validation
- **Mobile Responsiveness**: Cross-device and screen size compatibility

### 5. Test Schedule and Milestones

#### 5.1 Testing Timeline

**Phase 1: Test Preparation ({{phase1_duration}} weeks)**
- Test environment setup and configuration
- Test data preparation and generation
- Test tool installation and configuration
- Test script development and automation framework setup
- Test case design and review

**Phase 2: Unit and Integration Testing ({{phase2_duration}} weeks)**
- Developer-driven unit testing execution
- API and service integration testing
- Database integration testing
- Component integration validation
- Test automation script execution

**Phase 3: System Testing ({{phase3_duration}} weeks)**
- Functional system testing execution
- Non-functional testing (performance, security, usability)
- Cross-browser and compatibility testing
- Regression testing of existing functionality
- Defect identification and resolution

**Phase 4: User Acceptance Testing ({{phase4_duration}} weeks)**
- UAT environment preparation and validation
- Business user training and onboarding
- UAT scenario execution by business users
- Feedback collection and defect resolution
- UAT sign-off and approval

**Phase 5: Production Readiness ({{phase5_duration}} weeks)**
- Production deployment testing
- Smoke testing in production environment
- Performance validation in production
- Monitoring and alerting validation
- Go-live support and post-deployment validation

#### 5.2 Key Milestones

```text
| Milestone | Target Date | Deliverables | Success Criteria |
```

|-----------|-------------|--------------|------------------|

```text
| Test Plan Approval | {{milestone1_date}} | Approved test plan, test strategy | Stakeholder sign-off |
| Test Environment Ready | {{milestone2_date}} | Configured environments, test data | Environment validation passed |
| Test Case Development Complete | {{milestone3_date}} | All test cases, automation scripts | Test case review approved |
| System Testing Complete | {{milestone4_date}} | Test execution reports, defect summary | Exit criteria met |
| UAT Sign-off | {{milestone5_date}} | UAT completion report, business approval | User acceptance obtained |
| Production Go-Live | {{milestone6_date}} | Production deployment, smoke test results | System live and stable |
```

### 6. Resource Planning

#### 6.1 Team Structure and Responsibilities

**Test Management**
- **Test Manager** (1.0 FTE)
    - Overall test strategy and planning
    - Resource coordination and risk management
    - Stakeholder communication and reporting
    - Test process improvement and governance

**Test Engineering**
- **Senior Test Engineers** ({{senior_testers}} FTE)
    - Test case design and execution
    - Test automation framework development
    - Complex scenario testing and analysis
    - Junior tester mentoring and guidance

- **Test Engineers** ({{test_engineers}} FTE)
    - Manual test case execution
    - Test data preparation and management
    - Defect reporting and validation
    - Regression testing execution

**Test Automation**
- **Automation Engineers** ({{automation_engineers}} FTE)
    - Test automation script development
    - CI/CD integration and maintenance
    - Framework enhancement and optimization
    - Automation tool evaluation and selection

**Performance Testing**
- **Performance Test Engineer** ({{performance_testers}} FTE)
    - Performance test scenario design
    - Load testing execution and analysis
    - Performance monitoring and tuning
    - Capacity planning recommendations

**Security Testing**
- **Security Test Specialist** ({{security_testers}} FTE)
    - Security test planning and execution
    - Vulnerability assessment and penetration testing
    - Security compliance validation
    - Security defect analysis and remediation

#### 6.2 Tool Requirements

**Test Management Tools**
- **Test Management**: {{test_mgmt_tool}} (TestRail, Zephyr, qTest)
- **Defect Tracking**: {{defect_tool}} (Jira, Azure DevOps, Bugzilla)
- **Test Reporting**: Custom dashboards, automated reports

**Functional Testing Tools**
- **Web Automation**: {{web_automation_tool}} (Selenium, Cypress, Playwright)
- **Mobile Testing**: {{mobile_tool}} (Appium, Espresso, XCTest)
- **API Testing**: {{api_tool}} (RestAssured, Postman, SoapUI)
- **Database Testing**: {{db_tool}} (DbUnit, SQLUnit)

**Performance Testing Tools**
- **Load Testing**: {{load_tool}} (JMeter, LoadRunner, Gatling)
- **Monitoring**: {{monitoring_tool}} (New Relic, AppDynamics, Grafana)
- **Resource Monitoring**: {{resource_tool}} (Prometheus, Datadog)

**Security Testing Tools**
- **Vulnerability Scanning**: {{vuln_tool}} (OWASP ZAP, Nessus, Qualys)
- **Static Analysis**: {{static_tool}} (SonarQube, Checkmarx, Veracode)
- **Dynamic Analysis**: {{dynamic_tool}} (Burp Suite, WebInspect)

### 7. Risk Assessment and Mitigation

#### 7.1 Testing Risks

**High Priority Risks**

**Risk: Insufficient Test Environment Availability**
- **Probability**: Medium
- **Impact**: High
- **Risk Score**: High
- **Mitigation**:
    - Early environment provisioning and setup
    - Backup environment configuration
    - Cloud-based environment scaling capability
    - Service virtualization for external dependencies

**Risk: Test Data Quality and Availability**
- **Probability**: Medium
- **Impact**: Medium
- **Risk Score**: Medium
- **Mitigation**:
    - Automated test data generation tools
    - Data masking and anonymization processes
    - Data refresh automation and scheduling
    - Synthetic data generation for edge cases

**Risk: Insufficient Testing Time Due to Development Delays**
- **Probability**: High
- **Impact**: High
- **Risk Score**: Critical
- **Mitigation**:
    - Parallel testing approach where possible
    - Risk-based testing prioritization
    - Test automation to accelerate execution
    - Shift-left testing practices

**Risk: Key Resource Unavailability**
- **Probability**: Medium
- **Impact**: High
- **Risk Score**: High
- **Mitigation**:
    - Cross-training team members
    - Documentation of critical processes
    - External contractor backup plan
    - Knowledge sharing sessions

#### 7.2 Technical Risks

**Risk: Performance Requirements Not Met**
- **Probability**: Medium
- **Impact**: High
- **Risk Score**: High
- **Mitigation**:
    - Early performance testing in development cycle
    - Performance requirements validation with stakeholders
    - Performance monitoring throughout testing
    - Performance tuning collaboration with development team

**Risk: Security Vulnerabilities Discovered Late**
- **Probability**: Low
- **Impact**: Critical
- **Risk Score**: High
- **Mitigation**:
    - Security testing throughout development cycle
    - Automated security scanning in CI/CD pipeline
    - Regular security code reviews
    - Third-party security assessment

### 8. Entry and Exit Criteria

#### 8.1 Entry Criteria by Phase

**Unit Testing Entry Criteria**
- [ ] Code development complete for the module/component
- [ ] Code review completed and approved
- [ ] Unit test cases designed and reviewed
- [ ] Development environment configured
- [ ] Unit testing framework and tools available

**Integration Testing Entry Criteria**
- [ ] Unit testing completed with 80% pass rate
- [ ] All critical and high-priority defects from unit testing resolved
- [ ] Integration test environment configured and validated
- [ ] API documentation and contracts available
- [ ] Test data for integration scenarios prepared

**System Testing Entry Criteria**
- [ ] Integration testing completed successfully
- [ ] System test environment configured and stable
- [ ] All system test cases designed, reviewed, and approved
- [ ] Test data loaded and validated
- [ ] System deployment completed successfully

**UAT Entry Criteria**
- [ ] System testing completed with 95% pass rate
- [ ] All critical and high-priority defects resolved
- [ ] UAT environment prepared and validated
- [ ] UAT test scenarios approved by business stakeholders
- [ ] User training completed

#### 8.2 Exit Criteria by Phase

**Unit Testing Exit Criteria**
- [ ] Minimum 80% code coverage achieved
- [ ] All unit test cases executed successfully
- [ ] No critical or high-priority defects remain open
- [ ] Unit test automation integrated into CI/CD pipeline

**Integration Testing Exit Criteria**
- [ ] All integration test cases executed
- [ ] API contracts validated and documented
- [ ] 95% of integration test cases passed
- [ ] All critical and high-priority defects resolved
- [ ] Integration test automation stable and reliable

**System Testing Exit Criteria**
- [ ] All planned system test cases executed
- [ ] 98% of test cases passed successfully
- [ ] No critical defects remain open
- [ ] Performance requirements validated
- [ ] Security requirements satisfied
- [ ] Usability requirements verified

**UAT Exit Criteria**
- [ ] All UAT scenarios executed by business users
- [ ] Business stakeholder acceptance obtained
- [ ] User feedback incorporated or documented for future releases
- [ ] Production readiness confirmed
- [ ] Go-live approval received

### 9. Defect Management

#### 9.1 Defect Classification

**Severity Levels**
- **Critical**: System crash, data loss, security breach, core functionality broken
- **High**: Major functionality impacted, significant user impact, workaround difficult
- **Medium**: Minor functionality issues, moderate user impact, workaround available
- **Low**: Cosmetic issues, minimal impact, enhancement requests

**Priority Levels**
- **P1 - Immediate**: Fix required before release, blocks testing
- **P2 - High**: Fix required before release, impacts functionality
- **P3 - Medium**: Fix required before release if time permits
- **P4 - Low**: Fix can be deferred to future release

#### 9.2 Defect Lifecycle and Process

**Defect States**: New → Assigned → In Progress → Fixed → Verified → Closed

**Resolution Timeframes**:
- **Critical/P1**: 4 hours response, 24 hours resolution
- **High/P2**: 8 hours response, 72 hours resolution
- **Medium/P3**: 24 hours response, 1 week resolution
- **Low/P4**: 48 hours response, 2 weeks resolution

#### 9.3 Defect Metrics and Reporting

**Key Defect Metrics**:
- Defect detection rate by phase
- Defect resolution time by severity
- Defect escape rate to production
- Defect density by module/component
- Defect trend analysis over time

### 10. Test Execution and Reporting

#### 10.1 Test Execution Process

**Daily Test Execution**:
- Execute planned test cases according to schedule
- Document test results in test management tool
- Report new defects with detailed information
- Verify fixed defects and update status
- Update test execution dashboard and metrics

**Weekly Test Status Reporting**:
- Test execution progress against plan
- Defect summary and trend analysis
- Risk assessment and mitigation updates
- Resource utilization and availability
- Schedule adherence and variance analysis

#### 10.2 Test Reporting and Communication

**Test Status Dashboard**:
- Real-time test execution progress
- Defect summary by severity and status
- Test coverage metrics
- Environment availability status
- Key milestone tracking

**Stakeholder Communication**:

```text
| Stakeholder | Frequency | Format | Content |
```

|-------------|-----------|--------|---------|

```text
| Development Team | Daily | Standup/Email | Defect reports, blockers |
| Project Manager | Weekly | Status Report | Progress, risks, issues |
| Business Stakeholders | Bi-weekly | Executive Summary | Quality status, readiness |
| Executive Leadership | Monthly | Dashboard | High-level metrics, trends |
```

### 11. Success Metrics and KPIs

#### 11.1 Quality Metrics

**Test Coverage Metrics**:
- Requirements coverage: 100% of high/medium priority requirements
- Code coverage: Minimum 80% for critical modules
- Test case coverage: All planned test cases executed
- Defect coverage: All defects tracked and resolved

**Quality Indicators**:
- Defect density: < {{defect_density_target}} defects per KLOC
- Defect escape rate: < {{escape_rate_target}}% to production
- Test effectiveness: > {{effectiveness_target}}% defect detection rate
- Customer satisfaction: > {{satisfaction_target}} satisfaction score

#### 11.2 Process Metrics

**Efficiency Metrics**:
- Test execution velocity: Test cases executed per day
- Automation coverage: {{automation_target}}% of regression tests automated
- Environment utilization: > {{utilization_target}}% effective usage
- Resource productivity: Test cases per person-hour

### 12. Continuous Improvement

#### 12.1 Lessons Learned Process

**Post-Phase Reviews**:
- What worked well in the testing phase
- What challenges were encountered
- What improvements can be made
- Process optimization opportunities

**Knowledge Sharing**:
- Best practices documentation
- Tool and technique sharing
- Cross-team collaboration improvements
- Training and skill development needs

#### 12.2 Process Enhancement

**Automation Enhancement**:
- Continuous expansion of test automation coverage
- Framework improvements and optimization
- New tool evaluation and adoption
- AI/ML integration for intelligent testing

**Quality Process Improvement**:
- Defect prevention strategies
- Shift-left testing practices
- Risk-based testing optimization
- Continuous testing in DevOps pipeline

## Output Format Requirements

Present the test plan as:
- Professional document following IEEE 829 standard
- Clear section numbering and consistent formatting
- Comprehensive tables for schedules, resources, and metrics
- Risk assessment with detailed mitigation strategies
- Traceability matrices linking tests to requirements
- Executive summary with key recommendations

## Integration with Deployment Stage

This test plan provides the Deployment stage with:
- Quality assurance validation and sign-off
- Test automation scripts for CI/CD pipeline integration
- Performance benchmarks and monitoring criteria
- Security validation and compliance reports
- Production readiness assessment and recommendations

Generate a comprehensive test plan that ensures thorough quality validation and successful system deployment.
