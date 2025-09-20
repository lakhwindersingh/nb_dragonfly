# User Stories Creation Prompt

## Context and Role
You are an experienced Agile Business Analyst and Product Owner with deep expertise in user story creation, user experience design, and agile development methodologies. You excel at translating business requirements into well-crafted user stories that are valuable, estimable, small, and testable (VEST). Your stories follow the standard format and include comprehensive acceptance criteria that guide development and testing.

## Input Requirements
Create comprehensive user stories based on:

**Project Context:**
- Project Objectives: {{project_objectives}}
- Business Requirements: {{business_requirements}}
- User Personas: {{user_personas}}
- Business Processes: {{business_processes}}
- Success Metrics: {{success_metrics}}

**User Research:**
- User Journey Maps: {{user_journeys}}
- Pain Points: {{user_pain_points}}
- User Goals: {{user_goals}}
- Usage Scenarios: {{usage_contexts}}
- Workflow Analysis: {{current_workflows}}

**Technical Context:**
- System Capabilities: {{system_features}}
- Integration Points: {{integration_requirements}}
- Performance Expectations: {{performance_requirements}}
- Security Requirements: {{security_needs}}

## User Story Creation Instructions

Generate comprehensive user stories following Agile best practices:

### 1. User Story Framework

**Standard Format:**
"As a [type of user], I want [goal/desire] so that [benefit/value]"

**Story Components:**
- **Role**: Who is the user (persona-based)
- **Goal**: What functionality they want
- **Benefit**: Why they want it (business value)
- **Acceptance Criteria**: Specific conditions of satisfaction
- **Definition of Done**: Quality and completeness criteria

### 2. Epic and Story Hierarchy

**Epic: User Management**
Large user story that encompasses multiple related features

**Story: User Registration**
Smaller, deliverable piece of functionality within the epic

**Task: Email Validation**
Technical implementation details for the story

### 3. User Stories by Epic

#### Epic 1: User Authentication and Profile Management

**US-001: New User Registration**
**As a** prospective user of the {{system_name}} platform
**I want** to create an account with my email and personal information
**So that** I can access the system's features and maintain my personalized profile

**Acceptance Criteria:**
- Given I am on the registration page
- When I enter a valid email address, strong password, and required profile information
- Then I should receive an email verification link
- And my account should be created in pending status
- And I should see a confirmation message with next steps

**Additional Details:**
- Email must be unique in the system
- Password must meet security requirements (8+ chars, mixed case, numbers, symbols)
- Required fields: first name, last name, email, password, confirm password
- Optional fields: phone number, organization, role
- Registration form should have real-time validation
- GDPR compliance: privacy policy acceptance required

**Story Points:** 5
**Priority:** High
**Dependencies:** None
**Assumptions:** Email service is available and configured

---

**US-002: Email Verification**
**As a** newly registered user
**I want** to verify my email address through a secure link
**So that** I can activate my account and ensure account security

**Acceptance Criteria:**
- Given I have registered and received a verification email
- When I click the verification link within 24 hours
- Then my account should be activated
- And I should be redirected to the login page with a success message
- And the verification link should become invalid after use

**Additional Scenarios:**
- If verification link is expired (>24 hours), user should be able to request a new one
- If user is already verified, clicking link should show appropriate message
- Verification links should be unique and secure (cryptographically strong)

**Story Points:** 3
**Priority:** High
**Dependencies:** US-001
**Assumptions:** Email delivery is reliable

---

**US-003: User Login**
**As a** registered and verified user
**I want** to securely log into the system
**So that** I can access my account and use the platform features

**Acceptance Criteria:**
- Given I am on the login page
- When I enter my correct email and password
- Then I should be logged in and redirected to the dashboard
- And my session should be established securely
- And I should see a welcome message with my name

**Additional Scenarios:**
- Invalid credentials should show clear error message
- After 3 failed attempts, account should be temporarily locked (15 minutes)
- "Remember me" option should extend session duration
- Password reset link should be available on login page

**Story Points:** 3
**Priority:** High
**Dependencies:** US-002
**Assumptions:** Authentication service is available

#### Epic 2: Core Business Functionality

**US-010: {{Primary Feature}} Creation**
**As a** authenticated {{user_type}}
**I want** to create new {{business_object}} records
**So that** I can {{business_value}}

**Acceptance Criteria:**
- Given I am logged in as a {{user_type}}
- When I navigate to the {{feature}} creation page
- Then I should see a form with all required fields
- And I should be able to enter valid data for each field
- And I should receive real-time validation feedback
- When I submit the form with valid data
- Then the {{business_object}} should be created successfully
- And I should see a success confirmation
- And I should be redirected to the {{business_object}} details page

**Field Requirements:**
- [List specific fields and validation rules]
- [Required vs optional fields]
- [Data format requirements]
- [Business rule validations]

**Story Points:** 8
**Priority:** High
**Dependencies:** US-003 (User must be logged in)

---

**US-011: {{Primary Feature}} Viewing and Search**
**As a** {{user_type}}
**I want** to view and search {{business_object}} records
**So that** I can find and review the information I need

**Acceptance Criteria:**
- Given I am logged in with appropriate permissions
- When I navigate to the {{business_object}} list page
- Then I should see a paginated list of {{business_object}} records I have access to
- And I should see key information for each record ({{key_fields}})
- And I should have search functionality with filters
- When I enter search criteria
- Then the results should be filtered and updated in real-time
- When I click on a record
- Then I should see the detailed view with all information

**Search and Filter Requirements:**
- Text search across key fields
- Date range filters
- Status-based filtering
- Category-based filtering
- Sort by multiple columns
- Export search results

**Story Points:** 5
**Priority:** High
**Dependencies:** US-010

#### Epic 3: Data Management and Reporting

**US-020: Data Import**
**As a** system administrator or power user
**I want** to import {{business_object}} data from CSV/Excel files
**So that** I can efficiently migrate existing data or perform bulk updates

**Acceptance Criteria:**
- Given I have appropriate permissions for data import
- When I access the import functionality
- Then I should be able to upload a CSV or Excel file
- And I should see a preview of the data to be imported
- And I should be able to map file columns to system fields
- When I confirm the import
- Then the system should validate all data
- And I should see a summary of successful and failed imports
- And failed records should be available for download with error descriptions

**Import Requirements:**
- File size limit: 10MB or 50,000 records
- Supported formats: CSV, Excel (.xlsx)
- Column mapping interface with validation
- Error reporting with specific row and field information
- Rollback capability for failed imports
- Progress indicator for large imports

**Story Points:** 13
**Priority:** Medium
**Dependencies:** US-010, US-011

#### Epic 4: System Integration

**US-030: {{External System}} Integration**
**As a** {{user_type}}
**I want** the system to automatically sync with {{external_system}}
**So that** I don't have to manually enter duplicate information

**Acceptance Criteria:**
- Given the integration with {{external_system}} is configured
- When {{trigger_event}} occurs in either system
- Then the relevant data should be synchronized automatically
- And any sync errors should be logged and reported
- And users should be notified of sync status
- When there are data conflicts
- Then the system should follow the configured resolution rules
- And users should be able to review and resolve conflicts manually

**Integration Requirements:**
- Real-time or scheduled synchronization
- Conflict resolution strategy
- Error handling and retry logic
- Audit trail of all sync activities
- Configuration interface for sync rules
- Manual sync trigger capability

**Story Points:** 21
**Priority:** Medium
**Dependencies:** External system API availability

#### Epic 5: Reporting and Analytics

**US-040: Standard Reports**
**As a** {{manager_user_type}}
**I want** to generate standard reports on {{business_metrics}}
**So that** I can track performance and make informed business decisions

**Acceptance Criteria:**
- Given I have reporting permissions
- When I navigate to the reports section
- Then I should see a list of available standard reports
- When I select a report type
- Then I should be able to set parameters (date ranges, filters)
- And I should be able to generate the report
- And I should see the report results in a clear, formatted display
- And I should be able to export the report in multiple formats (PDF, Excel, CSV)

**Report Types:**
- [List specific reports needed]
- [Parameters and filters for each report]
- [Charts and visualizations required]
- [Scheduled report delivery options]

**Story Points:** 8
**Priority:** Medium
**Dependencies:** Sufficient data exists for meaningful reports

#### Epic 6: User Experience and Accessibility

**US-050: Mobile Responsive Interface**
**As a** mobile user
**I want** the interface to work well on my smartphone and tablet
**So that** I can use the system when I'm away from my computer

**Acceptance Criteria:**
- Given I access the system on a mobile device
- When I navigate through the interface
- Then all functionality should be accessible and usable
- And text should be readable without zooming
- And touch targets should be appropriately sized (minimum 44px)
- And forms should be easy to complete on mobile
- When I rotate my device
- Then the interface should adapt to the new orientation

**Mobile Requirements:**
- Responsive design for screen sizes 320px to 1920px
- Touch-friendly interface elements
- Mobile-optimized forms and navigation
- Performance optimized for mobile networks
- Offline capability for critical functions (if applicable)

**Story Points:** 13
**Priority:** Medium
**Dependencies:** Core functionality completion

---

**US-051: Accessibility Compliance**
**As a** user with disabilities
**I want** the system to be accessible using assistive technologies
**So that** I can use all features regardless of my abilities

**Acceptance Criteria:**
- Given I am using screen reader software
- When I navigate through the interface
- Then all content should be properly announced
- And all interactive elements should be keyboard accessible
- And form fields should have proper labels and descriptions
- When I use high contrast mode
- Then all content should remain visible and usable
- And color should not be the only way information is conveyed

**Accessibility Requirements:**
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility (NVDA, JAWS, VoiceOver)
- High contrast and large font support
- Alternative text for all images
- Proper heading structure and landmarks

**Story Points:** 8
**Priority:** High (legal requirement)
**Dependencies:** Core UI components

### 4. Cross-Cutting User Stories

#### Security and Privacy

**US-060: Password Management**
**As a** security-conscious user
**I want** to change my password and enable two-factor authentication
**So that** I can keep my account secure

**US-061: Data Privacy Controls**
**As a** user concerned about privacy
**I want** to control what personal data is collected and how it's used
**So that** I can maintain my privacy while using the system

#### Performance and Reliability

**US-070: Fast Loading**
**As a** user with limited time
**I want** pages to load quickly (under 3 seconds)
**So that** I can complete my tasks efficiently

**US-071: Offline Capability**
**As a** user in areas with poor connectivity
**I want** to continue working when temporarily offline
**So that** I don't lose productivity due to network issues

### 5. Story Sizing and Prioritization

**Story Point Scale (Fibonacci):**
- 1 point: Simple configuration change
- 2 points: Minor UI update or simple validation
- 3 points: Basic CRUD operation
- 5 points: Complex form with validation
- 8 points: Feature with multiple components
- 13 points: Complex integration or major feature
- 21 points: Epic-sized story that should be broken down

**Prioritization Criteria:**
1. **Business Value**: Impact on user satisfaction and business metrics
2. **Risk Reduction**: Technical or business risk mitigation
3. **Dependencies**: Prerequisite for other high-value stories
4. **Learning**: Stories that provide valuable insights for future development

**MoSCoW Prioritization:**
- **Must Have**: Core functionality required for MVP
- **Should Have**: Important features that significantly enhance value
- **Could Have**: Nice-to-have features that improve user experience
- **Won't Have**: Features explicitly excluded from current scope

### 6. Definition of Done

**Story Level DoD:**
- [ ] Acceptance criteria are met and verified
- [ ] Code is reviewed and approved
- [ ] Unit tests written and passing (minimum 80% coverage)
- [ ] Integration tests passing
- [ ] UI/UX review completed
- [ ] Accessibility requirements verified
- [ ] Performance requirements met
- [ ] Security requirements satisfied
- [ ] Documentation updated
- [ ] Stakeholder demo completed and approved

**Epic Level DoD:**
- [ ] All stories in epic completed
- [ ] End-to-end testing completed
- [ ] User documentation created
- [ ] Training materials prepared (if needed)
- [ ] Production deployment successful
- [ ] Monitoring and alerting configured
- [ ] User feedback collected and analyzed

## Output Format Requirements

Present user stories as:
- Clear epic groupings with business value statements
- Standard user story format with consistent structure
- Comprehensive acceptance criteria with Given/When/Then format
- Story points estimation using Fibonacci scale
- Priority levels and dependencies clearly identified
- Assumptions and constraints explicitly stated
- Cross-references to requirements and business objectives

## Quality Validation Criteria

Ensure all user stories meet INVEST criteria:
- [ ] **Independent**: Can be developed independently of other stories
- [ ] **Negotiable**: Details can be discussed and refined
- [ ] **Valuable**: Delivers clear value to users or business
- [ ] **Estimable**: Development team can estimate effort reasonably
- [ ] **Small**: Can be completed within one sprint
- [ ] **Testable**: Clear criteria for determining when story is complete

## Integration with Development

These user stories will guide:
- Sprint planning and backlog prioritization
- Development task breakdown and estimation
- Test case creation and acceptance testing
- UI/UX design and prototyping
- Technical architecture decisions
- Definition of done verification

Generate comprehensive, actionable user stories that enable efficient agile development and ensure user value delivery.
