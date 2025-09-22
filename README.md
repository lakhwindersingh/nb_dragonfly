# 🚀 NB Dragonfly - AI-Powered SDLC Pipeline System

> *A comprehensive, end-to-end Software Development Life Cycle (SDLC) automation platform powered by Generative AI, designed to accelerate software development while maintaining enterprise-grade quality and governance.*

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-green.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-4.9.5-blue.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [SDLC Stages](#-sdlc-stages)
- [AI Prompts & Templates](#-ai-prompts--templates)
- [Technology Stack](#-technology-stack)
- [Installation & Setup](#-installation--setup)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Integration Guide](#-integration-guide)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

**NB Dragonfly** is an innovative AI-powered platform that revolutionizes software development by automating the entire SDLC process. From initial project planning to deployment and maintenance, the system leverages cutting-edge GenAI technology to generate high-quality artifacts, documentation, and code while maintaining strict adherence to industry standards.

### 🎯 Vision
Transform software development from a manual, time-intensive process into an intelligent, automated pipeline that delivers consistent, high-quality results at unprecedented speed.

### 🏆 Mission
Empower development teams to focus on innovation and business value while the platform handles routine SDLC activities through intelligent automation.

---

## 🏗️ Architecture

The platform consists of three integrated components working in harmony:

```mermaid
graph TB
    UI[Web Interface<br/>React + TypeScript] --> Engine[Pipeline Engine<br/>Python + AsyncIO]
    Engine --> Templates[SDLC Templates<br/>Stage-based Artifacts]
    Engine --> AI[AI Processors<br/>Multi-Provider Support]
    Engine --> Storage[Artifact Manager<br/>Version Control]
    Engine --> Repos[Repository Connectors<br/>Git, Confluence, Jira]

    subgraph "AI Providers"
        OpenAI[OpenAI GPT-4]
        Claude[Anthropic Claude]
        Azure[Azure OpenAI]
    end

    AI --> OpenAI
    AI --> Claude
    AI --> Azure
```

### Core Components

1. **🎨 SDLC Pipeline UI** - Modern React-based web interface
2. **⚙️ Pipeline Engine** - Async Python orchestration engine
3. **📚 SDLC Templates** - Structured stage-based templates and prompts
4. **📁 Artifact Storage** - Centralized artifact management with version control

---

## ✨ Key Features

### 🤖 AI-Powered Automation
- **Multi-Provider Support**: OpenAI GPT-4, Anthropic Claude, Azure OpenAI
- **Intelligent Prompt Chaining**: Context flows seamlessly between SDLC stages
- **Quality Validation**: Built-in quality gates and validation rules
- **Adaptive Learning**: Prompts improve based on feedback and results

### 🔄 Complete SDLC Coverage
- **Planning**: Project charters, resource allocation, risk assessment
- **Requirements**: SRS documents, user stories, acceptance criteria
- **Design**: System architecture, database design, API specifications
- **Implementation**: Code generation, best practices enforcement
- **Testing**: Test plans, automated test scripts, quality metrics
- **Deployment**: CI/CD pipelines, infrastructure as code
- **Maintenance**: Monitoring setup, incident response procedures

### 🌐 Enterprise Integration
- **Repository Connectors**: Git, Confluence, SharePoint, Jira, Azure DevOps
- **Security**: Encrypted credentials, role-based access control
- **Scalability**: Async processing, horizontal scaling support
- **Monitoring**: Comprehensive metrics, logging, and alerting

### 🎨 Modern User Experience
- **Visual Pipeline Designer**: Drag-and-drop interface for pipeline creation
- **Real-time Monitoring**: Live execution tracking with detailed progress
- **Approval Workflows**: Human-in-the-loop quality control gates
- **Responsive Design**: Mobile-friendly interface with dark/light themes

---

## 📁 Project Structure
```text
nb_dragonfly/ 
├── 🌐 sdlc-pipeline-ui/        # React TypeScript Web Interface 
│   ├── src/ 
│   │ ├── components/           # Reusable UI components 
│   │ ├── pages/                # Main application pages 
│   │ ├── services/             # API and business logic 
│   │ ├── hooks/                # Custom React hooks 
│   │ └── types/                # TypeScript definitions 
│   ├── public/                 # Static assets 
│   ├── package.json            # Dependencies and scripts 
│   └── Dockerfile              # Container configuration 
│ 
├── ⚙️ sdlc-pipeline-engine/        # Python Orchestration Engine 
│       ├── sdlc_pipeline_engine/   # Core engine package 
│       ├── ai_prompt_processors.py # AI integration layer 
│       ├── artifact_manager.py     # Artifact storage and versioning 
│       ├── workflow_engine.py      # Pipeline orchestration 
│       ├── validation_engine.py    # Quality validation 
│       ├── repository_connectors.py # External system integrations 
│       ├── requirements.txt        # Python dependencies 
│       └── config.yml              # Engine configuration 
│ 
├── 📋 sdlc-pipeline/               # Templates and Prompts 
│       ├── 1-planning/             # Project planning stage 
│       ├── 2-requirements/         # Requirements analysis 
│       ├── 3-design/               # System and software design 
│       ├── 4-implementation/       # Development and coding 
│       ├── 5-testing/              # Quality assurance 
│       ├── 6-deployment/           # Release and deployment 
│       ├── 7-maintenance/          # Operations and maintenance 
│       └── shared/                 # Common templates and utilities 
│       
├── 📦 artifacts/                   # Generated Artifacts Storage 
│ 
├── executions/                     # Pipeline execution results 
│ 
├── templates/                      # Processed templates 
│ 
├── backups/                        # Artifact backups 
│ 
└── metadata/                       # Artifact metadata and indexing 
│ 
├── 📚 archive/                     # Historical data and backups 
└── 🔧 Configuration Files 
├── .gitignore 
├── docker-compose.yml 
└── create_folders.sh
```
---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** with pip
- **Node.js 16+** with npm/yarn
- **Docker** (optional, for containerized deployment)
- **Git** for version control

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-org/nb_dragonfly.git
   cd nb_dragonfly
   ```

2. **Setup Environment**
   ```bash
   # Create folder structure
   ./create_folders.sh
   
   # Set up Python environment
   cd sdlc-pipeline-engine
   pip install -r requirements.txt
   
   # Set up React environment
   cd ../sdlc-pipeline-ui
   npm install
   ```

3. **Configure API Keys**
   ```bash
   # Copy environment template
   cp sdlc-pipeline-engine/.env.example sdlc-pipeline-engine/.env
   
   # Edit with your API keys
   nano sdlc-pipeline-engine/.env
   ```

4. **Start the Platform**
   ```bash
   # Terminal 1: Start Backend Engine
   cd sdlc-pipeline-engine
   python main.py
   
   # Terminal 2: Start Frontend UI
   cd sdlc-pipeline-ui
   npm start
   ```

5. **Access the Interface**
    - Web UI: http://localhost:3000
    - API Documentation: http://localhost:8000/docs

---

## 🔄 SDLC Stages

Each stage builds upon the previous, creating a seamless flow of information:

### 1. 📋 Planning
**Generates:** Project Charter, Resource Plan, Risk Assessment
- Executive summary and business objectives
- Technical requirements and constraints
- Timeline with realistic milestones
- Budget allocation and resource requirements

### 2. 📝 Requirements
**Generates:** SRS Document, User Stories, Acceptance Criteria
- Functional and non-functional requirements
- Use case diagrams and user journey maps
- API contracts and data requirements
- Validation and acceptance criteria

### 3. 🎨 Design
**Generates:** System Architecture, Database Design, UI/UX Mockups
- High-level and detailed design documents
- Database schemas and data models
- API specifications and integration patterns
- Security architecture and compliance requirements

### 4. 💻 Implementation
**Generates:** Source Code, Documentation, Code Reviews
- Full-stack application development
- Microservices and API implementations
- Database migration scripts
- Comprehensive code documentation

### 5. 🧪 Testing
**Generates:** Test Plans, Automated Tests, Quality Reports
- Unit, integration, and end-to-end tests
- Performance and security testing
- Test automation scripts and CI/CD integration
- Quality metrics and coverage reports

### 6. 🚀 Deployment
**Generates:** CI/CD Pipelines, Infrastructure Code, Monitoring
- Containerization and orchestration
- Infrastructure as Code (Terraform, CloudFormation)
- Monitoring and alerting setup
- Deployment automation and rollback procedures

### 7. 🔧 Maintenance
**Generates:** Monitoring Dashboards, Incident Procedures, Optimization Plans
- Application performance monitoring
- Log aggregation and analysis
- Incident response procedures
- Continuous improvement recommendations

---

## 🤖 AI Prompts & Templates

### Prompt Engineering Excellence

Our prompt templates follow advanced engineering principles:

#### 🎯 **Chain of Thought Prompting**
```markdown
## Analysis Framework
Step 1: Analyze business requirements
- Review stakeholder needs
- Identify core processes
- Map user journeys

Step 2: Define technical constraints
- Performance specifications
- Security requirements
- Integration needs

Step 3: Generate solution design
- Select architectural patterns
- Design data models
- Specify APIs
```

#### 📊 **Few-Shot Learning Examples**
```markdown
Example Requirement:
- ID: FR-001
- Title: User Authentication
- Priority: High

Description: Users must authenticate via email/password

Acceptance Criteria:
- Login with valid credentials succeeds
- Invalid attempts are logged and limited
- Password reset functionality available
- Session timeout after 30 minutes
```

#### ✅ **Self-Validation Mechanisms**
```markdown
Quality Checklist:
- [ ] All requirements have unique identifiers
- [ ] Acceptance criteria are measurable
- [ ] Business objectives are addressed
- [ ] Technical constraints are satisfied
- [ ] Stakeholder needs are covered
```

### 📚 Template Library

Comprehensive templates covering:
- **Project Management**: PMI, PRINCE2 compliant
- **Requirements Engineering**: IEEE 830 standard
- **Architecture Design**: TOGAF framework
- **Security Standards**: OWASP guidelines
- **Testing Methodologies**: ISO/IEC 25010 quality model

---

## 🛠️ Technology Stack

### Backend Engine (Python)
- **Runtime**: Python 3.9+ with AsyncIO
- **Web Framework**: FastAPI for high-performance APIs
- **AI Integration**: OpenAI, Anthropic, Azure OpenAI clients
- **Database**: SQLAlchemy ORM with PostgreSQL/MySQL support
- **Caching**: Redis for session and artifact caching
- **Monitoring**: Prometheus metrics and structured logging

### Frontend Interface (TypeScript/React)
- **Framework**: React 18.2.0 with TypeScript 4.9.5
- **State Management**: Redux Toolkit with RTK Query
- **UI Components**: Material-UI (MUI) 5.14.17
- **Routing**: React Router 6.18.0
- **Forms**: Formik 2.4.5 with Yup validation
- **Charts**: Recharts 2.8.0 for analytics dashboards
- **Code Editor**: Monaco Editor for code review

### DevOps & Infrastructure
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose and Kubernetes ready
- **CI/CD**: GitHub Actions, Jenkins, Azure DevOps support
- **Monitoring**: Prometheus + Grafana + ELK stack
- **Security**: HashiCorp Vault, encrypted secrets

### Repository Integrations
- **Version Control**: Git (GitHub, GitLab, Bitbucket)
- **Documentation**: Confluence, SharePoint, Notion
- **Project Management**: Jira, Azure DevOps, Linear
- **Communication**: Slack, Microsoft Teams webhooks

---

## ⚙️ Installation & Setup

### Development Environment

1. **Python Backend Setup**
   ``` bash
   cd sdlc-pipeline-engine
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Configure environment variables
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

2. **React Frontend Setup**
   ``` bash
   cd sdlc-pipeline-ui
   npm install
   # or yarn install
   
   # Start development server
   npm start
   ```

3. **Database Setup** (Optional)

    ``` bash
    # PostgreSQL using Docker
    docker run --name pipeline-db -p 5432:5432 \
     -e POSTGRES_DB=pipeline \
     -e POSTGRES_USER=pipeline \
     -e POSTGRES_PASSWORD=pipeline123 \
     -d postgres:15
    ```

### Production Deployment

#### Docker Compose (Recommended)

    ``` bash
    # Clone and configure
    git clone [https://github.com/your-org/nb_dragonfly.git](https://github.com/your-org/nb_dragonfly.git) cd nb_dragonfly
    # Configure environment
    cp .env.example .env
    # Edit .env with production settings
    # Deploy with Docker Compose
    docker-compose up -d
    ```

#### Kubernetes Deployment

    ```bash
    # Apply Kubernetes manifests
    kubectl apply -f k8s/namespace.yaml kubectl apply -f k8s/configmap.yaml kubectl apply -f k8s/secrets.yaml kubectl apply -f k8s/deployment.yaml kubectl apply -f k8s/service.yaml kubectl apply -f k8s/ingress.yaml
    ```

#### Cloud Platform Deployment
- **AWS**: ECS Fargate + RDS + ElastiCache
- **Azure**: Container Instances + PostgreSQL + Redis Cache
- **Google Cloud**: Cloud Run + Cloud SQL + Memorystore

---

## 💡 Usage Examples

### Example 1: Creating a Web Application Pipeline

    ```python
    # Define pipeline configuration
    pipeline_config = { "name": "E-commerce Web App", "business_domain": "retail", "technology": "react-node-postgresql", "timeline_months": 6, "budget_range": "$100k-250k" }
    # Execute pipeline
    async with SDLCPipelineOrchestrator() as orchestrator: results = await orchestrator.execute_pipeline(
    ```

### Example 2: Individual Stage Execution
    ```python
    # Execute only requirements analysis
    requirements_result = await orchestrator.execute_stage(
    ```

### Example 3: Custom Pipeline Creation
    ```yaml
    # custom-pipeline.yml
    name: "Microservices API Pipeline" stages:
    - id: "api-design" type: "design" ai_config: model: "gpt-4" temperature: 0.2 prompt_template: | Design a RESTful API for {{ domain }} with:
        - OpenAPI 3.0 specification
        - JWT authentication
        - Rate limiting
        - Comprehensive error handling 
    ```


## ⚙️ Configuration

### Environment Variables
    ```bash
        # AI Provider Configuration
        OPENAI_API_KEY=sk-your-openai-key 
        ANTHROPIC_API_KEY=sk-ant-your-anthropic-key 
        AZURE_OPENAI_ENDPOINT=[https://your-resource.openai.azure.com/](https://your-resource.openai.azure.com/) 
        AZURE_OPENAI_API_KEY=your-azure-key
        # Database Configuration
        DATABASE_URL=postgresql://user:pass@localhost:5432/pipeline 
        REDIS_URL=redis://localhost:6379/0
        # Repository Integrations
        GITHUB_TOKEN=ghp_your-github-token 
        CONFLUENCE_URL=[https://your-domain.atlassian.net](https://your-domain.atlassian.net) 
        CONFLUENCE_TOKEN=your-confluence-token JIRA_URL=[https://your-domain.atlassian.net](https://your-domain.atlassian.net) 
        JIRA_TOKEN=your-jira-token
        # Security
        JWT_SECRET=your-jwt-secret-key 
        ENCRYPTION_KEY=your-32-byte-encryption-key
        # Monitoring
        PROMETHEUS_PORT=9090 LOG_LEVEL=INFO
    ```
### Pipeline Configuration

    ```yaml
    
    # config.yml
    pipeline_defaults: ai_model: "gpt-4" temperature: 0.3 max_tokens: 4000 timeout_minutes: 15
    quality_gates: enable_validation: true require_approvals: true min_quality_score: 0.85
    repository_settings: default_branch: "main" auto_commit: true commit_message_template: "[SDLC] {stage}: {artifact_name}"
    notification_settings: slack_webhook: "[https://hooks.slack.com/](https://hooks.slack.com/)..." email_enabled: true approval_notifications: true
    ```

---

## 🔗 Integration Guide

### Repository Connectors

#### Git Integration
    ```python 
    
    git_config = { "type": "git", "url": "[https://github.com/your-org/project.git](https://github.com/your-org/project.git)", "branch": "main", "token": os.getenv("GITHUB_TOKEN"), "path_mappings": { "requirements": "docs/requirements/", "design": "docs/architecture/", "code": "src/" } }
    ```
#### Confluence Integration
    ```python 
    confluence_config = { "type": "confluence", "base_url": "[https://your-domain.atlassian.net](https://your-domain.atlassian.net)", "username": "api-user@company.com", "token": os.getenv("CONFLUENCE_TOKEN"), "space_key": "PROJ", "parent_page": "Software Development" }
    ```

#### Jira Integration
    ```python 
    jira_config = { "type": "jira", "server": "[https://your-domain.atlassian.net](https://your-domain.atlassian.net)", "username": "api-user@company.com", "token": os.getenv("JIRA_TOKEN"), "project_key": "PROJ", "issue_mappings": { "requirements": "Story", "bugs": "Bug", "tasks": "Task" } }
    ```

### API Integration

#### RESTful API Endpoints
    ```bash
    # Pipeline Management
    POST /api/v1/pipelines # Create pipeline GET /api/v1/pipelines/{id} # Get pipeline PUT /api/v1/pipelines/{id} # Update pipeline DELETE /api/v1/pipelines/{id} # Delete pipeline
    # Execution Management
    POST /api/v1/executions # Start execution GET /api/v1/executions/{id} # Get execution status POST /api/v1/executions/{id}/pause # Pause execution POST /api/v1/executions/{id}/resume # Resume execution
    # Artifact Management
    GET /api/v1/artifacts # List artifacts GET /api/v1/artifacts/{id} # Download artifact POST /api/v1/artifacts/{id}/approve # Approve artifact
    
    ```

#### WebSocket Integration
    ```javascript 
    // Real-time execution monitoring const ws = new WebSocket('ws://localhost:8000/ws/executions/{executionId}');
    ws.onmessage = (event) => { const update = JSON.parse(event.data); console.log(`Stage: ${update.stage}, Status: ${update.status}`); };
    
    ```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/nb_dragonfly.git
   cd nb_dragonfly
   git checkout -b feature/your-feature-name
   ```

2. **Setup Development Environment**
   ```bash
   # Backend
   cd sdlc-pipeline-engine
   pip install -r requirements.txt -r requirements-dev.txt
   
   # Frontend  
   cd ../sdlc-pipeline-ui
   npm install
   ```

3. **Run Tests**
   ```bash
   # Python tests
   cd sdlc-pipeline-engine
   pytest tests/
   
   # React tests
   cd ../sdlc-pipeline-ui  
   npm test
   ```

### Contribution Guidelines

- **Code Style**: Follow PEP 8 for Python, ESLint config for TypeScript
- **Testing**: Maintain >90% code coverage
- **Documentation**: Update README and inline documentation
- **Commits**: Use conventional commit messages

### Areas for Contribution

- 🤖 **AI Prompt Templates**: Improve prompt quality and coverage
- 🔌 **Repository Connectors**: Add support for new platforms
- 🎨 **UI/UX Improvements**: Enhance user experience and accessibility
- 🧪 **Testing**: Expand test coverage and automation
- 📚 **Documentation**: Improve guides and examples
- 🚀 **Performance**: Optimize processing speed and resource usage

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License
Copyright (c) 2024 NB Dragonfly Contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```
---

## 🆘 Support & Community

- **📚 Documentation**: [Full Documentation](https://docs.nbdragonfly.dev)
- **💬 Discord Community**: [Join our Discord](https://discord.gg/nbdragonfly)
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/your-org/nb_dragonfly/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/your-org/nb_dragonfly/discussions)
- **📧 Email Support**: support@nbdragonfly.dev

---

## 🏆 Acknowledgments

Special thanks to:
- **AI Research Community** for advancing GenAI capabilities
- **Open Source Contributors** who make tools like React, FastAPI, and others possible
- **Software Engineering Community** for SDLC best practices and standards
- **Beta Users** who provided valuable feedback during development

---

## 🔮 Roadmap

### Q1 2024
- [ ] Advanced AI model support (GPT-4 Turbo, Claude-3)
- [ ] Enhanced repository connectors (Azure DevOps, GitLab)
- [ ] Mobile-responsive UI improvements
- [ ] Advanced analytics and reporting

### Q2 2024  
- [ ] Multi-tenant architecture
- [ ] Enterprise SSO integration
- [ ] Advanced workflow customization
- [ ] AI model fine-tuning capabilities

### Q3 2024
- [ ] Marketplace for custom templates
- [ ] Advanced collaboration features  
- [ ] Integration with major cloud platforms
- [ ] Advanced security and compliance features

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by the NB Dragonfly Team

[Website](https://nbdragonfly.dev) • [Documentation](https://docs.nbdragonfly.dev) • [Community](https://discord.gg/nbdragonfly)

</div>