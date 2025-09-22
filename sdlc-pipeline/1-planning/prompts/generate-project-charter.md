# Project Charter Generation Prompt

## Context and Role
You are a Senior Project Manager with 15+ years of experience in software development projects, certified in PMP and Agile methodologies. You excel at translating business needs into structured project charters that align with PMI standards and serve as the foundation for successful project execution.

## Input Requirements
Based on the following project information, generate a comprehensive project charter:

**Project Overview:**
- Project Name: {{project_name}}
- Business Domain: {{business_domain}}
- Target Users: {{target_users}}
- Technology Preferences: {{technology_preferences}}
- Timeline: {{timeline_months}} months
- Budget Range: {{budget_range}}
- Key Stakeholders: {{stakeholders}}

**Additional Context:**
- Business Problem: {{business_problem}}
- Success Metrics: {{success_metrics}}
- Constraints: {{constraints}}
- Assumptions: {{assumptions}}

## Generation Instructions

Create a detailed project charter that includes:

### 1. Executive Summary
- Provide a compelling 2-3 paragraph overview
- Highlight business value and strategic alignment
- Include key success metrics and timeline

### 2. Business Justification
- **Problem Statement**: Clearly define what business problem this project solves
- **Business Case**: Quantify the value proposition (ROI, cost savings, revenue impact)
- **Strategic Alignment**: How this project supports organizational goals
- **Market Opportunity**: Competitive advantage or market positioning benefits

### 3. Project Objectives (SMART Format)
- **Primary Objectives**: 3-5 main goals that are Specific, Measurable, Achievable, Relevant, Time-bound
- **Secondary Objectives**: Supporting goals that enhance project value
- **Success Criteria**: Quantifiable measures for each objective

### 4. Scope Definition
- **In Scope**: Detailed list of what will be delivered
  - Functional requirements (high-level)
  - Technical deliverables
  - Documentation and training
  - Integration requirements
- **Out of Scope**: Explicitly state what is NOT included
- **Future Scope**: Potential phase 2 or follow-up projects

### 5. Stakeholder Analysis
Create a comprehensive stakeholder matrix:

```text
| Stakeholder | Role | Interest Level | Influence Level | Engagement Strategy |
|-------------|------|----------------|-----------------|-------------------|
| [Name/Role] | [Primary/Secondary] | [High/Medium/Low] | [High/Medium/Low] | [Strategy] |
```

### 6. High-Level Requirements
- **Functional Requirements**: Core system capabilities (5-10 key features)
- **Non-Functional Requirements**: Performance, security, scalability expectations
- **Integration Requirements**: Systems that must interface with this solution
- **Compliance Requirements**: Regulatory or industry standards

### 7. Project Approach and Methodology
- **Development Methodology**: Agile/Scrum/Kanban recommendation with justification
- **Delivery Approach**: Iterative releases, MVP strategy
- **Quality Assurance Strategy**: Testing approach and quality gates
- **Change Management**: How changes will be handled

### 8. Timeline and Milestones
- **Project Phases**: Break down into 4-6 major phases
- **Key Milestones**: Critical delivery dates and decision points
- **Dependencies**: External dependencies that could impact timeline
- **Critical Path**: Identify activities that cannot be delayed

### 9. Resource Requirements
- **Team Structure**: Roles and responsibilities matrix
- **Skill Requirements**: Technical and business skills needed
- **External Resources**: Vendors, consultants, or third-party services
- **Infrastructure Needs**: Hardware, software, cloud resources

### 10. Budget and Financial Projections
- **Development Costs**: Personnel, technology, infrastructure
- **Operational Costs**: Ongoing maintenance and support
- **ROI Analysis**: Expected return on investment over 3 years
- **Cost-Benefit Analysis**: Quantified benefits vs. costs

### 11. Risk Assessment and Mitigation
For each risk, provide:
- **Risk Description**: What could go wrong
- **Probability**: High/Medium/Low
- **Impact**: High/Medium/Low
- **Risk Score**: Calculate using probability × impact
- **Mitigation Strategy**: Specific actions to reduce risk
- **Contingency Plan**: What to do if risk materializes

Common risk categories to address:
- Technical risks (complexity, integration challenges)
- Resource risks (availability, skills gaps)
- Schedule risks (dependencies, scope creep)
- Budget risks (cost overruns, scope changes)
- Business risks (changing requirements, stakeholder alignment)

### 12. Communication Plan
- **Reporting Structure**: Who reports to whom
- **Meeting Cadence**: Regular meetings and their purpose
- **Status Reporting**: Frequency and format of project updates
- **Decision-Making Process**: How decisions will be made and by whom

### 13. Quality and Governance
- **Quality Standards**: Coding standards, documentation requirements
- **Review Gates**: Stage-gate reviews and approval criteria
- **Governance Structure**: Project steering committee, advisory board
- **Compliance Framework**: How regulatory requirements will be met

## Output Format Requirements

Structure the output as a professional project charter document with:
- Professional formatting with clear headings and subheadings
- Tables and bullet points for easy readability
- Quantifiable metrics wherever possible
- Action-oriented language
- Professional tone suitable for executive presentation

## Quality Validation Criteria

Ensure the charter meets these standards:
- [ ] All SMART objectives are clearly defined and measurable
- [ ] Business justification includes quantified value proposition
- [ ] Scope is clearly defined with explicit inclusions and exclusions
- [ ] Risk assessment covers technical, business, and operational risks
- [ ] Timeline is realistic based on scope and resource estimates
- [ ] Stakeholder analysis identifies all key parties and engagement strategies
- [ ] Success criteria are specific and measurable

## Integration with Next Stage

This project charter will feed into the Requirements Analysis stage by providing:
- Clear scope boundaries for requirements gathering
- Stakeholder list for requirements elicitation
- Success criteria for requirements validation
- Timeline constraints for requirements prioritization
- Budget constraints for solution design decisions

Generate a comprehensive, professional project charter that serves as the authoritative foundation for project execution and stakeholder alignment.
