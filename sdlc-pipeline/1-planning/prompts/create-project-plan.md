# Project Plan Creation Prompt

## Context and Role
You are an experienced Project Manager specializing in software development projects with expertise in Agile methodologies, resource planning, and project scheduling. You create detailed project plans that balance thoroughness with flexibility, ensuring successful project delivery while maintaining adaptability to changing requirements.

## Input Requirements
Based on the approved project charter and the following information:

**Project Charter Information:**
- Project Objectives: {{project_objectives}}
- Project Scope: {{project_scope}}
- Key Milestones: {{key_milestones}}
- Resource Requirements: {{resource_requirements}}
- Timeline Constraints: {{timeline_constraints}}
- Risk Assessment: {{identified_risks}}

**Team Information:**
- Team Size: {{team_size}}
- Team Composition: {{team_roles}}
- Skill Levels: {{skill_matrix}}
- Availability: {{team_availability}}

**Technical Context:**
- Technology Stack: {{technology_stack}}
- Development Approach: {{development_methodology}}
- Integration Requirements: {{integration_needs}}

## Generation Instructions

Create a comprehensive project plan that includes:

### 1. Project Plan Overview
- **Plan Purpose**: How this plan supports project charter objectives
- **Planning Approach**: Methodology used (Agile/Hybrid/Waterfall)
- **Plan Maintenance**: How and when the plan will be updated
- **Assumptions**: Key assumptions underlying the plan

### 2. Work Breakdown Structure (WBS)
Organize project work into hierarchical structure:

**Level 1: Project Phases**
1. **Project Initiation & Setup**
   - Team onboarding and training
   - Environment setup and tooling
   - Initial architecture and design sessions

2. **Requirements & Analysis**
   - Stakeholder interviews and workshops
   - Requirements documentation and validation
   - Business process analysis

3. **System Design & Architecture**
   - Technical architecture design
   - Database design and modeling
   - API design and documentation
   - Security architecture planning

4. **Implementation & Development**
   - Backend development (by feature/module)
   - Frontend development (by component/page)
   - Integration development
   - Code review and quality assurance

5. **Testing & Quality Assurance**
   - Unit testing development
   - Integration testing
   - System testing and UAT
   - Performance and security testing

6. **Deployment & Go-Live**
   - Environment preparation
   - Deployment automation
   - Production deployment
   - Go-live support

7. **Project Closure & Handover**
   - Documentation finalization
   - Knowledge transfer
   - Lessons learned
   - Project closure activities

### 3. Detailed Task Planning
For each WBS element, provide:
- **Task ID**: Unique identifier
- **Task Name**: Descriptive name
- **Description**: What needs to be accomplished
- **Duration**: Estimated effort in person-days
- **Dependencies**: Prerequisites and successor tasks
- **Resources Required**: Roles and skills needed
- **Deliverables**: Expected outputs
- **Acceptance Criteria**: How completion is measured

### 4. Project Schedule and Timeline
Create a detailed schedule with:

**Sprint Planning (if Agile):**
- **Sprint 0**: Setup and planning (2 weeks)
- **Sprint 1-2**: Requirements and initial design (4 weeks)
- **Sprint 3-8**: Core development iterations (12 weeks)
- **Sprint 9-10**: Integration and testing (4 weeks)
- **Sprint 11**: Deployment and go-live (2 weeks)

**Milestone Schedule:**

```text
+-----------------------+-------------+----------------------------+--------------------------------------+--------------------+
|       Milestone       | Target Date |       Dependencies         |           Success Criteria            | Stakeholder Review |
+-----------------------+-------------+----------------------------+--------------------------------------+--------------------+
| Project Kickoff       | Week 1      | Team availability          | Charter approved, team onboarded      | Sponsor            |
| Requirements Baseline | Week 6      | Stakeholder interviews     | SRS approved by stakeholders          | Product Owner      |
| Architecture Review   | Week 10     | Requirements complete      | Design approved by architects         | Technical Lead     |
| MVP Demo              | Week 18     | Core features complete     | Stakeholder acceptance                | Product Owner      |
| UAT Completion        | Week 22     | System testing passed      | Business acceptance                   | Business Users     |
| Production Go-Live    | Week 24     | UAT passed, infra ready    | System live and stable                | All Stakeholders   |
+-----------------------+-------------+----------------------------+--------------------------------------+--------------------+
```

### 5. Resource Planning and Allocation
**Team Roles and Responsibilities:**

```text
+------------------+------------------------------------+--------------+-----------------------------------+----------------------+
|       Role       |           Responsibility           | Allocation % |            Key Skills             |      Duration        |
+------------------+------------------------------------+--------------+-----------------------------------+----------------------+
| Project Manager  | Overall coordination and delivery  |    100%      | PMP, Agile, Communication         | Full project         |
| Technical Lead   | Architecture & technical guidance  |    100%      | {{technology_stack}}, Leadership  | Full project         |
| Senior Developer | Core development and mentoring     |    100%      | {{primary_technologies}}          | Development phases   |
| Developer        | Feature development                |    100%      | {{required_skills}}               | Development phases   |
| QA Engineer      | Testing & quality assurance        |    100%      | Testing tools, Automation         | Testing phases       |
| DevOps Engineer  | Infrastructure & deployment        |     50%      | CI/CD, Cloud, Containers          | Setup & deployment   |
| Business Analyst | Requirements & stakeholder liaison |     75%      | Business analysis, Documentation  | Requirements phase   |
| UX/UI Designer   | UX & interface design              |     50%      | Design tools, User research       | Design & early dev   |
+------------------+------------------------------------+--------------+-----------------------------------+----------------------+
```

**Resource Leveling:**
- Identify resource conflicts and overallocation
- Propose solutions for resource optimization
- Plan for skill development and knowledge transfer

### 6. Quality Management Plan
**Quality Assurance Framework:**
- **Code Quality Standards**: Coding conventions, review processes
- **Testing Strategy**: Unit, integration, system, and acceptance testing
- **Quality Gates**: Go/no-go criteria for each phase
- **Defect Management**: Bug tracking and resolution process
- **Performance Criteria**: Response times, throughput, scalability metrics

**Review and Approval Process:**
- **Peer Reviews**: Code reviews, design reviews
- **Stakeholder Reviews**: Requirements, design, and user acceptance
- **Quality Audits**: Periodic quality assessments

### 7. Communication Plan
**Communication Matrix:**

```text
+-------------------+-----------------------------------+-----------+-----------------+-------------+
| Stakeholder Group |        Information Needs          | Frequency |      Method     | Responsible |
+-------------------+-----------------------------------+-----------+-----------------+-------------+
| Executive Sponsor | High-level status, risks, budget  | Weekly    | Dashboard/Email | PM          |
| Product Owner     | Sprint progress, scope changes    | Daily/Sprint | Standup/Review | Scrum Master|
| Development Team  | Task assignments, blockers        | Daily     | Standup         | Team        |
| Business Users    | Feature demos, UAT planning       | Sprint    | Demo/Meeting    | PM          |
| IT Operations     | Infrastructure, security, deploy. | As needed | Email/Meeting   | DevOps      |
+-------------------+-----------------------------------+-----------+-----------------+-------------+
```

**Meeting Schedule:**
- **Daily Standups**: Development team sync (15 min)
- **Sprint Planning**: Iteration planning (2 hours bi-weekly)
- **Sprint Review**: Demo and feedback (1 hour bi-weekly)
- **Sprint Retrospective**: Process improvement (1 hour bi-weekly)
- **Stakeholder Review**: Progress and decision making (1 hour weekly)

### 8. Risk Management Plan
**Risk Monitoring and Response:**
For each identified risk:
- **Risk ID**: Unique identifier
- **Risk Category**: Technical, Resource, Schedule, Business
- **Risk Description**: Detailed risk scenario
- **Probability**: Likelihood of occurrence (H/M/L)
- **Impact**: Severity if occurs (H/M/L)
- **Risk Score**: Calculated priority
- **Response Strategy**: Avoid, Mitigate, Transfer, Accept
- **Action Plan**: Specific mitigation steps
- **Owner**: Who monitors and responds
- **Trigger Indicators**: Early warning signs
- **Contingency Plan**: Response if risk materializes

**Risk Review Process:**
- Weekly risk assessment during team meetings
- Monthly risk register updates
- Escalation process for high-impact risks

### 9. Change Management Plan
**Change Control Process:**
- **Change Request Procedure**: How changes are submitted
- **Impact Assessment**: Technical, schedule, budget, resource impact
- **Approval Authority**: Who can approve different types of changes
- **Change Implementation**: How approved changes are executed
- **Change Communication**: How changes are communicated to stakeholders

**Change Categories:**
- **Minor Changes**: < 5% impact, Team Lead approval
- **Major Changes**: 5-15% impact, Project Manager approval
- **Significant Changes**: > 15% impact, Steering Committee approval

### 10. Budget and Cost Management
**Budget Breakdown:**
- **Personnel Costs**: Salary, benefits, contractor fees
- **Technology Costs**: Software licenses, cloud services, tools
- **Infrastructure Costs**: Hardware, network, security
- **Training Costs**: Skill development, certifications
- **Contingency**: Risk mitigation reserve (10-15% of total)

**Cost Monitoring:**
- **Earned Value Management**: Track actual vs. planned progress
- **Budget Burn Rate**: Monitor spending velocity
- **Cost Forecasting**: Predict final project cost
- **Change Impact**: Track cost impact of scope changes

### 11. Success Metrics and KPIs
**Project Success Metrics:**
- **Schedule Performance**: On-time delivery percentage
- **Budget Performance**: Cost variance and cost performance index
- **Quality Metrics**: Defect density, test coverage, code quality scores
- **Stakeholder Satisfaction**: Survey scores and feedback
- **Business Value**: ROI, user adoption, performance improvements

**Tracking and Reporting:**
- **Dashboard**: Real-time project health indicators
- **Weekly Reports**: Progress, risks, issues, and decisions
- **Monthly Reviews**: Comprehensive status and trend analysis

## Output Format Requirements

Present the project plan as a professional document with:
- Clear section headers and sub-sections
- Tables for schedules, resources, and matrices
- Gantt chart representation of timeline (text format)
- Risk register in tabular format
- Professional language suitable for stakeholder review
- Action-oriented deliverables and milestones

## Integration with Next Stage

This project plan will support the Requirements Analysis stage by:
- Providing detailed schedule for requirements activities
- Identifying stakeholders for requirements gathering
- Allocating resources for requirements analysis tasks
- Establishing quality gates for requirements validation
- Setting up communication channels for requirements collaboration

Generate a comprehensive, actionable project plan that ensures successful project delivery while maintaining flexibility for agile adaptation.
