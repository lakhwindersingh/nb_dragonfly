# Resource Analysis Prompt

## Context and Role
You are a Senior Resource Manager and Organizational Development specialist with expertise in software development team structures, skill assessments, and resource optimization. You excel at analyzing project requirements and designing optimal team compositions that balance skills, availability, and cost-effectiveness.

## Input Requirements
Analyze the following project and organizational context:

**Project Requirements:**
- Project Scope: {{project_scope}}
- Technology Stack: {{technology_stack}}
- Project Duration: {{project_duration}}
- Complexity Level: {{complexity_assessment}}
- Quality Requirements: {{quality_standards}}
- Timeline Constraints: {{delivery_deadlines}}

**Current Resource Pool:**
- Available Team Members: {{available_resources}}
- Current Skill Matrix: {{existing_skills}}
- Team Capacity: {{current_utilization}}
- Budget Constraints: {{budget_limitations}}

**Organizational Context:**
- Development Methodology: {{methodology}}
- Remote/Hybrid Work Model: {{work_model}}
- Training Budget: {{training_availability}}
- External Resource Options: {{contractor_options}}

## Analysis Instructions

Conduct a comprehensive resource analysis covering:

### 1. Project Resource Requirements Analysis

**Skill Requirements Mapping:**
Analyze the project needs and map to required skills:

```text
┌─────────────────────┬─────────────────────────────────────────────┬─────────────────────┬──────────────┬──────────┐
│ Skill Category      │ Required Skills                             │ Proficiency Level   │ Person-Months│ Priority │
├─────────────────────┼─────────────────────────────────────────────┼─────────────────────┼──────────────┼──────────┤
│ Backend Development │ {{technology_stack}} programming,           │ Senior/Mid/Junior   │    X months  │   High   │
│                     │ API development                             │                     │              │          │
├─────────────────────┼─────────────────────────────────────────────┼─────────────────────┼──────────────┼──────────┤
│ Frontend            │ {{frontend_tech}}, UX/UI implementation     │ Senior/Mid          │    X months  │   High   │
│ Development         │                                             │                     │              │          │
├─────────────────────┼─────────────────────────────────────────────┼─────────────────────┼──────────────┼──────────┤
│ Database            │ Database design, optimization,              │ Senior              │    X months  │  Medium  │
│                     │ administration                              │                     │              │          │
├─────────────────────┼─────────────────────────────────────────────┼─────────────────────┼──────────────┼──────────┤
│ DevOps              │ CI/CD, containerization,                    │ Senior              │    X months  │   High   │
│                     │ cloud platforms                             │                     │              │          │
├─────────────────────┼─────────────────────────────────────────────┼─────────────────────┼──────────────┼──────────┤
│ Quality Assurance   │ Test automation,                            │ Mid/Senior          │    X months  │  Medium  │
│                     │ performance testing                         │                     │              │          │
├─────────────────────┼─────────────────────────────────────────────┼─────────────────────┼──────────────┼──────────┤
│ Business Analysis   │ Requirements gathering,                     │ Senior              │    X months  │   High   │
│                     │ stakeholder management                      │                     │              │          │
├─────────────────────┼─────────────────────────────────────────────┼─────────────────────┼──────────────┼──────────┤
│ Project Management  │ Agile/Scrum, risk management                │ Senior              │    X months  │   High   │
├─────────────────────┼─────────────────────────────────────────────┼─────────────────────┼──────────────┼──────────┤
│ Architecture        │ System design,                              │ Senior              │    X months  │ Critical │
│                     │ technical leadership                        │                     │              │          │
└─────────────────────┴─────────────────────────────────────────────┴─────────────────────┴──────────────┴──────────┘
```

**Workload Analysis:**
Break down effort estimation by work streams:
- **Requirements & Analysis**: X person-weeks
- **System Design**: X person-weeks
- **Backend Development**: X person-weeks
- **Frontend Development**: X person-weeks
- **Integration**: X person-weeks
- **Testing**: X person-weeks
- **Deployment**: X person-weeks
- **Documentation**: X person-weeks
- **Project Management**: X person-weeks (ongoing)

### 2. Current Resource Assessment

**Existing Team Analysis:**
For each available team member:

```text
| Name/Role | Current Skills | Proficiency | Availability | Utilization | Gap Analysis |
|-----------|----------------|-------------|--------------|-------------|--------------|
| [Team Member] | [Skills list] | [Level] | [%] | [Current projects] | [Skill gaps] |
```

**Skill Gap Analysis:**
- **Critical Gaps**: Skills essential for project success that are missing
- **Nice-to-Have Gaps**: Beneficial skills that would improve efficiency
- **Proficiency Gaps**: Skills present but not at required level
- **Capacity Gaps**: Right skills but insufficient availability

**Team Strengths and Weaknesses:**
- **Strengths**: Areas where the team excels
- **Weaknesses**: Areas needing improvement or augmentation
- **Dependencies**: Key individuals with critical knowledge
- **Risks**: Single points of failure or knowledge concentration

### 3. Optimal Team Structure Design

**Recommended Team Composition:**

**Core Team (Full Project Duration):**
- **Project Manager** (1.0 FTE)
  - Skills: Agile/Scrum, stakeholder management, risk management
  - Experience: 5+ years in similar projects
  - Responsibilities: Overall project coordination, stakeholder communication

- **Technical Lead/Architect** (1.0 FTE)
  - Skills: {{technology_stack}}, system architecture, technical leadership
  - Experience: 7+ years, previous architecture experience
  - Responsibilities: Technical direction, architecture decisions, code reviews

- **Senior Backend Developer** (1.0 FTE)
  - Skills: {{backend_technologies}}, database design, API development
  - Experience: 5+ years in backend development
  - Responsibilities: Core backend implementation, mentoring junior developers

- **Senior Frontend Developer** (1.0 FTE)
  - Skills: {{frontend_technologies}}, responsive design, user experience
  - Experience: 4+ years in frontend development
  - Responsibilities: User interface implementation, frontend architecture

**Extended Team (Phase-Specific):**
- **Business Analyst** (0.75 FTE, Requirements phase + ongoing)
- **QA Engineer** (1.0 FTE, Testing phase + integration support)
- **DevOps Engineer** (0.5 FTE, Setup + Deployment phases)
- **Junior Developer** (1.0 FTE, Development phase)
- **UX/UI Designer** (0.25 FTE, Design phase)

**Team Interaction Model:**
- **Reporting Structure**: Hierarchy and communication lines
- **Collaboration Patterns**: How team members work together
- **Knowledge Sharing**: Pair programming, code reviews, knowledge sessions
- **Decision Making**: Technical and project decision processes

### 4. Resource Acquisition Strategy

**Internal Resource Development:**
- **Training Plan**: Specific training for skill gaps
  - {{identified_skill_gaps}} training programs
  - Timeline: {{training_schedule}}
  - Budget: {{training_costs}}
  - Success Metrics: Skill assessments, certifications

- **Mentoring Program**:
  - Senior-junior pairing for knowledge transfer
  - Rotation strategy for cross-training
  - Knowledge documentation requirements

**External Resource Acquisition:**
- **Contract Positions**: For specialized skills or capacity gaps
  - Required Skills: {{specific_contractor_skills}}
  - Duration: {{contract_duration}}
  - Budget: {{contractor_budget}}
  - Integration Plan: How contractors work with internal team

- **Consulting Services**: For specific expertise or guidance
  - Architecture review and guidance
  - Technology training and knowledge transfer
  - Best practices implementation

**Recruitment Strategy:**
If permanent hires are needed:
- **Job Descriptions**: For required new roles
- **Recruitment Timeline**: Time needed for hiring process
- **Onboarding Plan**: Integration of new team members
- **Retention Strategy**: Keeping valuable team members

### 5. Resource Utilization Optimization

**Capacity Planning:**
- **Peak Resource Periods**: When maximum team size is needed
- **Resource Ramping**: How team size changes over project phases
- **Buffer Planning**: Contingency for sick leave, vacations
- **Overlap Planning**: Knowledge transfer between phases

**Multi-Project Coordination:**
- **Resource Sharing**: Team members on multiple projects
- **Priority Matrix**: Project prioritization for resource conflicts
- **Escalation Process**: Resolving resource conflicts
- **Capacity Management**: Avoiding team burnout

**Productivity Optimization:**
- **Tool Selection**: Development tools and productivity enhancers
- **Process Optimization**: Streamlined workflows and practices
- **Environment Setup**: Optimal working conditions
- **Distraction Management**: Focus time and meeting optimization

### 6. Budget and Cost Analysis

**Resource Cost Breakdown:**

```text
| Resource Type | Monthly Cost | Duration | Total Cost | Cost Category |
|---------------|--------------|----------|------------|---------------|
| Project Manager | $X | X months | $X | Internal |
| Technical Lead | $X | X months | $X | Internal |
| Senior Developers | $X | X months | $X | Internal |
| Junior Developers | $X | X months | $X | Internal |
| Contractors | $X | X months | $X | External |
| Training | $X | One-time | $X | Development |
| Tools/Licenses | $X | X months | $X | Infrastructure |
```

**Cost Optimization Strategies:**
- **Internal vs. External**: Cost comparison and recommendations
- **Skill Development vs. Hiring**: Build vs. buy analysis
- **Tool Selection**: Cost-effective tool choices
- **Resource Sharing**: Cross-project resource utilization

### 7. Risk Assessment and Mitigation

**Resource-Related Risks:**

```text
| Risk | Probability | Impact | Risk Score | Mitigation Strategy |
|------|-------------|--------|------------|-------------------|
| Key team member unavailable | Medium | High | High | Cross-training, documentation |
| Skill gaps delay delivery | Low | High | Medium | Training plan, contractor backup |
| Resource conflicts with other projects | High | Medium | High | Priority matrix, resource sharing agreements |
| New team member integration issues | Medium | Medium | Medium | Structured onboarding, mentoring |
```

**Contingency Planning:**
- **Backup Resources**: Alternative team members or contractors
- **Skill Development Acceleration**: Intensive training programs
- **Scope Adjustment**: Reducing scope based on resource constraints
- **Timeline Flexibility**: Schedule adjustments for resource issues

### 8. Success Metrics and Monitoring

**Resource Performance Metrics:**
- **Team Productivity**: Story points delivered per sprint
- **Quality Metrics**: Code review findings, defect rates
- **Utilization Rates**: Actual vs. planned resource usage
- **Skill Development**: Training completion, skill assessments
- **Team Satisfaction**: Regular team health surveys
- **Retention Rate**: Team member turnover during project

**Monitoring and Reporting:**
- **Weekly Resource Reports**: Utilization, blockers, risks
- **Monthly Skill Assessments**: Progress on training and development
- **Quarterly Team Reviews**: Performance, satisfaction, development needs

## Output Format Requirements

Present the resource analysis as:
- Executive summary with key recommendations
- Detailed analysis with supporting data
- Clear tables for team structure and costs
- Risk matrix with mitigation strategies
- Implementation timeline for resource acquisition
- Success metrics and monitoring plan

## Integration with Project Plan

This resource analysis will inform:
- Detailed project scheduling based on resource availability
- Budget planning with accurate resource costs
- Risk management with resource-specific risks
- Quality planning with appropriate skill levels
- Communication planning with team structure

Generate a comprehensive resource analysis that enables optimal team composition and successful project delivery within budget and timeline constraints.
