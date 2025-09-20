# CI/CD Pipeline Creation Prompt

## Context and Role
You are a Senior DevOps Engineer with 10+ years of experience designing and implementing CI/CD pipelines for enterprise applications. You specialize in modern DevOps practices including containerization, Infrastructure as Code, automated testing, and cloud-native deployments. Your pipelines follow industry best practices for security, scalability, and reliability.

## Input Requirements
Design a comprehensive CI/CD pipeline based on:

**Application Context:**
- Application Type: {{application_type}}
- Technology Stack: {{technology_stack}}
- Repository: {{source_repository}}
- Target Environments: {{deployment_environments}}
- Cloud Platform: {{cloud_provider}}

**Requirements:**
- Testing Strategy: {{testing_requirements}}
- Security Requirements: {{security_requirements}}
- Performance Requirements: {{performance_requirements}}
- Compliance Needs: {{compliance_requirements}}
- Deployment Strategy: {{deployment_strategy}}

**Infrastructure:**
- Container Platform: {{container_platform}}
- Monitoring Tools: {{monitoring_stack}}
- Infrastructure as Code: {{iac_tools}}
- Secret Management: {{secret_management}}

## CI/CD Pipeline Creation Instructions

Design a comprehensive, production-ready CI/CD pipeline:

### 1. Pipeline Architecture Overview

#### 1.1 Pipeline Strategy
**Pipeline Type**: Multi-branch pipeline with environment promotion
**Deployment Model**: {{deployment_model}} (Blue-Green/Canary/Rolling)
**Automation Level**: Fully automated with manual approval gates for production

**Pipeline Stages**:
Source → Build → Test → Security → Package → Deploy Dev → Deploy Staging → Deploy Prod
↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ Code Compile Static Container Artifact Smoke Integration Production Commit & Unit & Security Registry Tests Tests Deployment Tests Quality Scan Push

#### 1.2 Pipeline Triggers
- **Automatic Triggers**:
    - Push to feature branches → Build and test
    - Push to develop → Deploy to development environment
    - Push to main/master → Deploy to staging
    - Tag creation → Production deployment candidate

- **Manual Triggers**:
    - Production deployment approval
    - Hotfix deployment
    - Rollback procedures
    - Infrastructure updates

### 2. Source Control and Branch Strategy

#### 2.1 Git Workflow
**Branching Strategy**: GitFlow with environment branches

main (production)

```text
├── develop (development)
├── staging (staging environment)
├── feature/feature-name
├── release/version-number
└── hotfix/fix-description
```

**Branch Protection Rules**:
- Require pull request reviews (minimum 2 approvers)
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Restrict direct pushes to main and develop branches
- Require signed commits for production branches

#### 2.2 Commit Standards
**Conventional Commits Format**:
( ):
[optional body]
[optional footer(s)]

**Commit Types**: feat, fix, docs, style, refactor, perf, test, chore, ci

### 3. Build Stage

#### 3.1 Build Configuration

**GitHub Actions Workflow (.github/workflows/ci-cd.yml)**:
yaml name: CI/CD Pipeline
on: push: branches: [ main, develop, staging ] tags: [ 'v*' ] pull_request: branches: [ main, develop ]
env: REGISTRY: {{container_registry}} IMAGE_NAME: {{application_name}} NODE_VERSION: '{{node_version}}' JAVA_VERSION: '{{java_version}}'
jobs: build: name: Build and Test runs-on: ubuntu-latest
steps:
- name: Checkout code
  uses: actions/checkout@v4
  with:
  fetch-depth: 0

- name: Setup {{runtime_environment}}
  uses: actions/setup-{{runtime}}@v4
  with:
  {{runtime}}-version: ${{ env.{{RUNTIME}}_VERSION }}
  cache: '{{package_manager}}'

- name: Cache dependencies
  uses: actions/cache@v3
  with:
  path: {{cache_path}}
  key: ${{ runner.os }}-{{package_manager}}-${{ hashFiles('{{lockfile}}') }}
  restore-keys: |
  ${{ runner.os }}-{{package_manager}}-

- name: Install dependencies
  run: {{install_command}}

- name: Run linting
  run: {{lint_command}}

- name: Run unit tests
  run: {{test_command}}
  env:
  NODE_ENV: test

- name: Generate test coverage
  run: {{coverage_command}}

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
  file: ./coverage/lcov.info
  flags: unittests
  name: codecov-umbrella

- name: Build application
  run: {{build_command}}
  env:
  NODE_ENV: production

- name: Upload build artifacts
  uses: actions/upload-artifact@v3
  with:
  name: build-artifacts
  path: {{build_output_path}}
  retention-days: 30
  security-scan: name: Security Scanning runs-on: ubuntu-latest needs: build
  steps:
- name: Checkout code
  uses: actions/checkout@v4

- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
  scan-type: 'fs'
  scan-ref: '.'
  format: 'sarif'
  output: 'trivy-results.sarif'

- name: Upload Trivy scan results
  uses: github/codeql-action/upload-sarif@v2
  with:
  sarif_file: 'trivy-results.sarif'

- name: Run SonarCloud analysis
  uses: SonarSource/sonarcloud-github-action@master
  env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

- name: Dependency vulnerability check
  run: {{dependency_audit_command}}
  integration-tests: name: Integration Tests runs-on: ubuntu-latest needs: build
  services:
  postgres:
  image: postgres:{{postgres_version}}
  env:
  POSTGRES_PASSWORD: testpassword
  POSTGRES_DB: testdb
  options: >-
  --health-cmd pg_isready
  --health-interval 10s
  --health-timeout 5s
  --health-retries 5

  redis:
  image: redis:{{redis_version}}
  options: >-
  --health-cmd "redis-cli ping"
  --health-interval 10s
  --health-timeout 5s
  --health-retries 5

steps:
- name: Checkout code
  uses: actions/checkout@v4

- name: Setup {{runtime_environment}}
  uses: actions/setup-{{runtime}}@v4
  with:
  {{runtime}}-version: ${{ env.{{RUNTIME}}_VERSION }}

- name: Download build artifacts
  uses: actions/download-artifact@v3
  with:
  name: build-artifacts
  path: {{build_output_path}}

- name: Install dependencies
  run: {{install_command}}

- name: Run integration tests
  run: {{integration_test_command}}
  env:
  DATABASE_URL: postgresql://postgres:testpassword@localhost:5432/testdb
  REDIS_URL: redis://localhost:6379
  NODE_ENV: test

- name: Upload test results
  uses: actions/upload-artifact@v3
  if: always()
  with:
  name: integration-test-results
  path: test-results/
  build-docker: name: Build Docker Image runs-on: ubuntu-latest needs: [build, security-scan, integration-tests] if: github.event_name == 'push'
  outputs:
  image: ${{ steps.image.outputs.image }}
  digest: ${{ steps.build.outputs.digest }}

steps:
- name: Checkout code
  uses: actions/checkout@v4

- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Log in to Container Registry
  uses: docker/login-action@v3
  with:
  registry: ${{ env.REGISTRY }}
  username: ${{ github.actor }}
  password: ${{ secrets.GITHUB_TOKEN }}

- name: Extract metadata
  id: meta
  uses: docker/metadata-action@v5
  with:
  images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
  tags: |
  type=ref,event=branch
  type=ref,event=pr
  type=sha,prefix={{branch}}-
  type=raw,value=latest,enable={{is_default_branch}}
  type=semver,pattern={{version}}
  type=semver,pattern={{major}}.{{minor}}

- name: Download build artifacts
  uses: actions/download-artifact@v3
  with:
  name: build-artifacts
  path: {{build_output_path}}

- name: Build and push Docker image
  id: build
  uses: docker/build-push-action@v5
  with:
  context: .
  file: ./Dockerfile
  platforms: linux/amd64,linux/arm64
  push: true
  tags: ${{ steps.meta.outputs.tags }}
  labels: ${{ steps.meta.outputs.labels }}
  cache-from: type=gha
  cache-to: type=gha,mode=max
  build-args: |
  NODE_ENV=production
  BUILD_DATE=${{ fromJSON(steps.meta.outputs.json).labels['org.opencontainers.image.created'] }}
  VCS_REF=${{ github.sha }}

- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
  image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
  format: spdx-json
  output-file: sbom.spdx.json

- name: Upload SBOM
  uses: actions/upload-artifact@v3
  with:
  name: sbom
  path: sbom.spdx.json

- name: Set image output
  id: image
  run: |
  echo "image=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}" >> $GITHUB_OUTPUT

#### 3.2 Multi-Stage Dockerfile
dockerfile

# Multi-stage build for {{application_type}} application
# Build stage
FROM {{base_image}}:{{base_version}} AS builder
WORKDIR /app
# Copy package files for dependency caching
COPY package*.json ./ COPY {{additional_config_files}} ./
# Install dependencies
RUN {{package_manager}} install --frozen-lockfile --production=false
# Copy source code
COPY . .
# Build application
RUN {{build_command}}
# Production stage
FROM {{runtime_image}}:{{runtime_version}} AS production
# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
# Set working directory
WORKDIR /app
# Copy built application from builder stage
COPY --from=builder --chown=appuser:appuser /app/{{build_output}} ./
# Copy production dependencies if needed
COPY --from=builder --chown=appuser:appuser /app/node_modules ./node_modules
# Install production dependencies only
RUN {{package_manager}} install --frozen-lockfile --production=true &&
{{package_manager}} cache clean --force &&
rm -rf ~/.{{package_manager}}
# Set up health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3

```text
CMD curl -f [http://localhost](http://localhost):{{port}}/health || exit 1
```

# Security: Use non-root user
USER appuser
# Expose port
EXPOSE {{port}}
# Add labels for metadata
LABEL org.opencontainers.image.title="{{application_name}}" LABEL org.opencontainers.image.description="{{application_description}}" LABEL org.opencontainers.image.vendor="{{organization}}" LABEL org.opencontainers.image.licenses="{{license}}" LABEL org.opencontainers.image.source="{{repository_url}}"
# Start application
CMD ["{{start_command}}"]

### 4. Testing Integration

#### 4.1 Automated Test Pipeline

**Test Stages Integration**:

```text
yaml performance-tests: name: Performance Tests runs-on: ubuntu-latest needs: build-docker if: github.ref == 'refs/heads/develop' || github.ref == 'refs/heads/staging'
```

steps:
- name: Checkout code
  uses: actions/checkout@v4

- name: Setup performance test environment
  run: |
  docker-compose -f docker-compose.perf.yml up -d
  sleep 30

- name: Run K6 performance tests
  uses: grafana/k6-action@v0.3.1
  with:
  filename: tests/performance/load-test.js
  env:
  TARGET_URL: http://localhost:{{port}}

- name: Upload performance results
  uses: actions/upload-artifact@v3
  with:
  name: performance-results
  path: performance-results/
  e2e-tests: name: End-to-End Tests runs-on: ubuntu-latest needs: build-docker
  steps:
- name: Checkout code
  uses: actions/checkout@v4

- name: Start application
  run: |
  docker run -d \
  --name app-under-test \
  -p {{port}}:{{port}} \
  -e NODE_ENV=test \
  ${{ needs.build-docker.outputs.image }}

  # Wait for application to be ready
  timeout 60 bash -c 'until curl -f http://localhost:{{port}}/health; do sleep 2; done'

- name: Run Playwright tests
  uses: microsoft/playwright-github-action@v1
  with:
  command: npx playwright test
  env:
  BASE_URL: http://localhost:{{port}}

- name: Upload E2E test results
  uses: actions/upload-artifact@v3
  if: always()
  with:
  name: e2e-results
  path: test-results/
  security-container-scan: name: Container Security Scan runs-on: ubuntu-latest needs: build-docker
  steps:
- name: Run Trivy container scan
  uses: aquasecurity/trivy-action@master
  with:
  image-ref: ${{ needs.build-docker.outputs.image }}
  format: 'sarif'
  output: 'container-scan-results.sarif'

- name: Upload container scan results
  uses: github/codeql-action/upload-sarif@v2
  with:
  sarif_file: 'container-scan-results.sarif'

- name: Check for critical vulnerabilities
  run: |
  # Fail pipeline if critical vulnerabilities found
  trivy image --exit-code 1 --severity CRITICAL ${{ needs.build-docker.outputs.image }}

### 5. Deployment Automation

#### 5.1 Environment-Specific Deployments

**Development Deployment**:
yaml deploy-dev: name: Deploy to Development runs-on: ubuntu-latest needs: [build-docker, integration-tests] if: github.ref == 'refs/heads/develop' environment: development
steps:
- name: Checkout deployment manifests
  uses: actions/checkout@v4
  with:
  path: manifests

- name: Setup kubectl
  uses: azure/setup-kubectl@v3
  with:
  version: '{{kubectl_version}}'

- name: Configure kubectl
  run: |

```text
  echo "${{ secrets.KUBE_CONFIG_DEV }}" | base64 -d > kubeconfig
```

  export KUBECONFIG=kubeconfig

- name: Deploy to Kubernetes
  run: |
  export KUBECONFIG=kubeconfig

  # Update image in deployment manifest
  sed -i 's|IMAGE_PLACEHOLDER|${{ needs.build-docker.outputs.image }}|g' manifests/k8s/dev/deployment.yaml

  # Apply configurations
  kubectl apply -f manifests/k8s/dev/namespace.yaml
  kubectl apply -f manifests/k8s/dev/configmap.yaml
  kubectl apply -f manifests/k8s/dev/secret.yaml
  kubectl apply -f manifests/k8s/dev/deployment.yaml
  kubectl apply -f manifests/k8s/dev/service.yaml
  kubectl apply -f manifests/k8s/dev/ingress.yaml

  # Wait for rollout to complete
  kubectl rollout status deployment/{{app_name}} -n {{namespace}}-dev --timeout=300s

- name: Run smoke tests
  run: |
  # Wait for service to be ready
  sleep 30

  # Run basic health check

```text
  curl -f {{dev_url}}/health || exit 1
```

  # Run smoke test suite

```text
  npm run test:smoke -- --env=dev
```

- name: Notify deployment
  uses: 8398a7/action-slack@v3
  with:
  status: ${{ job.status }}
  channel: '#deployments'
  webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  if: always()

**Staging Deployment with Approval Gate**:
yaml deploy-staging: name: Deploy to Staging runs-on: ubuntu-latest needs: [build-docker, e2e-tests, security-container-scan] if: github.ref == 'refs/heads/main' environment: staging
steps:
- name: Checkout deployment manifests
  uses: actions/checkout@v4

- name: Configure staging deployment
  run: |
  # Use Helm for more complex deployments
  helm upgrade --install {{app_name}} ./helm/{{app_name}} \
  --namespace {{namespace}}-staging \
  --create-namespace \
  --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }} \
  --set image.tag=${{ github.sha }} \
  --set environment=staging \
  --set replicas={{staging_replicas}} \
  --set resources.requests.cpu={{staging_cpu}} \
  --set resources.requests.memory={{staging_memory}} \
  --values helm/{{app_name}}/values-staging.yaml \
  --wait --timeout=600s

- name: Run staging validation tests
  run: |
  # Comprehensive staging validation

```text
  npm run test:integration -- --env=staging
  npm run test:accessibility -- --env=staging
  npm run test:performance -- --env=staging --load=moderate
```

- name: Generate staging report
  run: |
  # Create deployment report
  echo "# Staging Deployment Report" > staging-report.md
  echo "- **Image**: ${{ needs.build-docker.outputs.image }}" >> staging-report.md
  echo "- **Commit**: ${{ github.sha }}" >> staging-report.md
  echo "- **Branch**: ${{ github.ref_name }}" >> staging-report.md
  echo "- **Deployed by**: ${{ github.actor }}" >> staging-report.md
  echo "- **Deployment time**: $(date)" >> staging-report.md
  deploy-production: name: Deploy to Production runs-on: ubuntu-latest needs: deploy-staging if: startsWith(github.ref, 'refs/tags/v') environment: name: production url: {{production_url}}
  steps:
- name: Checkout deployment manifests
  uses: actions/checkout@v4

- name: Production pre-deployment checks
  run: |
  # Verify staging health

```text
  curl -f {{staging_url}}/health || exit 1
```

  # Check production capacity
  kubectl top nodes -n {{namespace}}-prod

  # Verify database migrations if needed

```text
  # npm run db:migrate:check -- --env=production
```

- name: Blue-Green Production Deployment
  run: |
  # Determine current active environment

```text
  CURRENT_ENV=$(kubectl get service {{app_name}}-active -n {{namespace}}-prod -o jsonpath='{.spec.selector.version}' 2>/dev/null || echo "blue")
```

  if [ ; then
  TARGET_ENV="green"
  else
  TARGET_ENV="blue"
  fi

  echo "Deploying to $TARGET_ENV environment"

  # Deploy to target environment
  helm upgrade --install {{app_name}}-$TARGET_ENV ./helm/{{app_name}} \
  --namespace {{namespace}}-prod \
  --create-namespace \
  --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }} \
  --set image.tag=${{ github.sha }} \
  --set environment=production \
  --set version=$TARGET_ENV \
  --set replicas={{production_replicas}} \
  --set resources.requests.cpu={{production_cpu}} \
  --set resources.requests.memory={{production_memory}} \
  --values helm/{{app_name}}/values-production.yaml \
  --wait --timeout=900s

  # Health check new deployment
  kubectl wait --for=condition=ready pod -l app={{app_name}},version=$TARGET_ENV -n {{namespace}}-prod --timeout=300s

  # Run production smoke tests against new deployment
  NEW_SERVICE_URL="http://{{app_name}}-$TARGET_ENV.{{namespace}}-prod.svc.cluster.local"

```text
  npm run test:smoke -- --url=$NEW_SERVICE_URL
```

  # Switch traffic to new deployment
  kubectl patch service {{app_name}}-active -n {{namespace}}-prod \
  -p '{"spec":{"selector":{"version":"'$TARGET_ENV'"}}}'

  # Verify traffic switch
  sleep 30

```text
  curl -f {{production_url}}/health || exit 1
```

  # Clean up old deployment after successful switch

```text
  if [  ]_> || [  ]_>; then
  OLD_ENV=$([  && echo "green" || echo "blue")
```

  kubectl delete deployment {{app_name}}-$OLD_ENV -n {{namespace}}-prod --ignore-not-found=true
  fi

- name: Post-deployment monitoring
  run: |
  # Set up enhanced monitoring for new deployment
  echo "Monitoring deployment for 10 minutes..."

  for i in {1..20}; do
  # Check application health
  if ! curl -f {{production_url}}/health; then
  echo "Health check failed, initiating rollback"
  # Rollback logic here
  exit 1
  fi

      # Check error rates

```text
      ERROR_RATE=$(curl -s {{monitoring_url}}/api/error-rate || echo "0")
      if (( $(echo  0.05" | bc -l) ))">; then
```

        echo "Error rate too high: $ERROR_RATE"
        exit 1
      fi

      sleep 30
  done

  echo "Deployment monitoring completed successfully"

- name: Update deployment status
  run: |
  # Update deployment tracking
  curl -X POST "${{ secrets.DEPLOYMENT_WEBHOOK }}" \
  -H "Content-Type: application/json" \
  -d '{
  "service": "{{app_name}}",
  "environment": "production",
  "version": "${{ github.ref_name }}",
  "image": "${{ needs.build-docker.outputs.image }}",
  "commit": "${{ github.sha }}",
  "deployed_by": "${{ github.actor }}",
  "status": "success"
  }'

- name: Notify production deployment
  uses: 8398a7/action-slack@v3
  with:
  status: ${{ job.status }}
  channel: '#production-deployments'
  webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  custom_payload: |
  {
  "text": "🚀 Production Deployment Successful",
  "attachments": [{
  "color": "good",
  "fields": [
  {"title": "Service", "value": "{{app_name}}", "short": true},
  {"title": "Version", "value": "${{ github.ref_name }}", "short": true},
  {"title": "Commit", "value": "${{ github.sha }}", "short": true},
  {"title": "Deployed by", "value": "${{ github.actor }}", "short": true}
  ]
  }]
  }
  if: success()

### 6. Infrastructure as Code Integration

#### 6.1 Terraform Infrastructure Pipeline
yaml infrastructure: name: Infrastructure Management runs-on: ubuntu-latest if: github.path == 'infrastructure/**'
steps:
- name: Checkout code
  uses: actions/checkout@v4

- name: Setup Terraform
  uses: hashicorp/setup-terraform@v2
  with:
  terraform_version: {{terraform_version}}

- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
  aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
  aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  aws-region: {{aws_region}}

- name: Terraform Init
  run: |
  cd infrastructure
  terraform init \
  -backend-config="bucket={{terraform_bucket}}" \
  -backend-config="key={{app_name}}/terraform.tfstate" \
  -backend-config="region={{aws_region}}"

- name: Terraform Plan
  run: |
  cd infrastructure
  terraform plan \
  -var="environment=${{ github.ref_name }}" \
  -var="app_name={{app_name}}" \
  -out=tfplan

- name: Terraform Apply
  if: github.ref == 'refs/heads/main'
  run: |
  cd infrastructure
  terraform apply tfplan

- name: Update infrastructure documentation
  run: |
  cd infrastructure
  terraform-docs markdown table . > ../docs/infrastructure.md
  git add ../docs/infrastructure.md

```text
  git commit -m "docs: update infrastructure documentation" || true
```

### 7. Security and Compliance Integration

#### 7.1 Security Pipeline Integration
yaml compliance-checks: name: Compliance and Security Checks runs-on: ubuntu-latest needs: build-docker
steps:
- name: Checkout code
  uses: actions/checkout@v4

- name: OWASP Dependency Check
  uses: dependency-check/Dependency-Check_Action@main
  with:
  project: {{app_name}}
  path: .
  format: ALL
  args: >
  --enableRetired
  --enableExperimental
  --failOnCVSS 7

- name: License compliance check
  uses: fossa-contrib/fossa-action@v2
  with:
  api-key: ${{ secrets.FOSSA_API_KEY }}
  project-title: {{app_name}}

- name: Docker image signing
  run: |
  # Install cosign
  curl -O -L "https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64"
  sudo mv cosign-linux-amd64 /usr/local/bin/cosign
  sudo chmod +x /usr/local/bin/cosign

  # Sign the container image
  echo "${{ secrets.COSIGN_PRIVATE_KEY }}" > cosign.key
  cosign sign --key cosign.key ${{ needs.build-docker.outputs.image }}

  # Generate and attach SBOM
  syft ${{ needs.build-docker.outputs.image }} -o spdx-json > sbom.spdx.json
  cosign attach sbom --sbom sbom.spdx.json ${{ needs.build-docker.outputs.image }}

- name: Policy as Code validation
  run: |
  # OPA policy validation
  opa fmt --diff manifests/policies/
  opa test manifests/policies/

  # Conftest policy validation against Kubernetes manifests
  conftest verify --policy manifests/policies/ manifests/k8s/

### 8. Monitoring and Observability Integration

#### 8.1 Monitoring Setup Automation
yaml setup-monitoring: name: Setup Application Monitoring runs-on: ubuntu-latest needs: deploy-production if: success()
steps:
- name: Configure application monitoring
  run: |
  # Create Datadog dashboard
  curl -X POST "https://api.datadoghq.com/api/v1/dashboard" \
  -H "Content-Type: application/json" \
  -H "DD-API-KEY: ${{ secrets.DATADOG_API_KEY }}" \
  -H "DD-APPLICATION-KEY: ${{ secrets.DATADOG_APP_KEY }}" \
  -d @monitoring/datadog-dashboard.json

  # Set up alerts
  curl -X POST "https://api.datadoghq.com/api/v1/monitor" \
  -H "Content-Type: application/json" \
  -H "DD-API-KEY: ${{ secrets.DATADOG_API_KEY }}" \
  -H "DD-APPLICATION-KEY: ${{ secrets.DATADOG_APP_KEY }}" \
  -d @monitoring/alerts.json

- name: Configure log aggregation
  run: |
  # Set up log parsing rules
  kubectl apply -f monitoring/fluentd-config.yaml

  # Configure log-based alerts
  kubectl apply -f monitoring/log-alerts.yaml

### 9. Pipeline Configuration Files

#### 9.1 Environment Configuration

**environments/development.env**:
bash NODE_ENV=development LOG_LEVEL=debug DATABASE_URL={DEV_DATABASE_URL} REDIS_URL={DEV_REDIS_URL} API_BASE_URL=[https://api-dev](https://api-dev).{{domain}} CORS_ORIGINS=[https://dev](https://dev).{{domain}},[http://localhost:3000](http://localhost:3000) RATE_LIMIT_WINDOW_MS=60000 RATE_LIMIT_MAX_REQUESTS=1000

**environments/staging.env**:
bash NODE_ENV=staging LOG_LEVEL=info DATABASE_URL={STAGING_DATABASE_URL} REDIS_URL={STAGING_REDIS_URL} API_BASE_URL=[https://api-staging](https://api-staging).{{domain}} CORS_ORIGINS=[https://staging](https://staging).{{domain}} RATE_LIMIT_WINDOW_MS=60000 RATE_LIMIT_MAX_REQUESTS=500

**environments/production.env**:
bash NODE_ENV=production LOG_LEVEL=warn DATABASE_URL={PROD_DATABASE_URL} REDIS_URL={PROD_REDIS_URL} API_BASE_URL=[https://api](https://api).{{domain}} CORS_ORIGINS=https://{{domain}} RATE_LIMIT_WINDOW_MS=60000 RATE_LIMIT_MAX_REQUESTS=100

#### 9.2 Pipeline Quality Gates
yaml quality-gates: unit-tests: coverage-threshold: 80 required: true
integration-tests: pass-rate: 95 required: true
security-scan: max-critical: 0 max-high: 0 required: true
performance-tests: response-time: 2000ms error-rate: 0.1% required-for: [staging, production]
code-quality: sonarqube-gate: passed complexity-threshold: 10 duplication-threshold: 3% required: true

### 10. Rollback and Recovery Procedures

#### 10.1 Automated Rollback

```yaml
  rollback:
    name: Emergency Rollback
    runs-on: ubuntu-latest
    if: github.event.inputs.rollback == 'true'
    environment: production

    steps:
    - name: Get previous stable version
      run: |
        PREVIOUS_VERSION=$(helm history {{app_name}} -n {{namespace}}-prod --max 2 -o json | jq -r '.[1].revision')
        echo "PREVIOUS_VERSION=$PREVIOUS_VERSION" >> $GITHUB_ENV

    - name: Rollback deployment
      run: |
        helm rollback {{app_name}} $PREVIOUS_VERSION -n {{namespace}}-prod --wait --timeout=300s

    - name: Verify rollback
      run: |
        sleep 30
        curl -f {{production_url}}/health || exit 1

        # Check error rates post-rollback
        ERROR_RATE=$(curl -s {{monitoring_url}}/api/error-rate || echo "0")
        if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
          echo "Error rate still high after rollback: $ERROR_RATE"
          exit 1
        fi

    - name: Notify rollback
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        channel: '#production-deployments'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        custom_payload: |
          {
            "text": "⚠️ Production Rollback Completed",
            "attachments": [{
              "color": "warning",
              "fields": [
                {"title": "Service", "value": "{{app_name}}", "short": true},
                {"title": "Rolled back to", "value": "${{ env.PREVIOUS_VERSION }}", "short": true},
                {"title": "Initiated by", "value": "${{ github.actor }}", "short": true}
              ]
            }]
          }

### 11. Pipeline Optimization and Performance
#### 11.1 Build Optimization
- **Parallel Jobs**: Run independent jobs concurrently
- **Caching Strategy**: Aggressive caching of dependencies and build artifacts
- **Incremental Builds**: Only rebuild changed components
- **Registry Optimization**: Multi-layer Docker builds with optimal layer caching

#### 11.2 Pipeline Monitoring
  pipeline-metrics:
    name: Pipeline Performance Tracking
    runs-on: ubuntu-latest
    if: always()

    steps:
    - name: Collect pipeline metrics
      run: |
        # Track pipeline execution time
        PIPELINE_DURATION=$(($(date +%s) - ${{ github.event.head_commit.timestamp }}))

        # Send metrics to monitoring system
        curl -X POST "${{ secrets.METRICS_ENDPOINT }}" \
          -H "Content-Type: application/json" \
          -d '{
            "pipeline_duration": "'$PIPELINE_DURATION'",
            "pipeline_status": "${{ job.status }}",
            "repository": "${{ github.repository }}",
            "branch": "${{ github.ref_name }}",
            "commit": "${{ github.sha }}"
          }'

## Output Format Requirements
Present the CI/CD pipeline as:
- Complete GitHub Actions workflow files
- Comprehensive Dockerfile with security best practices
- Environment-specific configuration files
- Infrastructure as Code templates
- Monitoring and alerting configurations
- Security and compliance automation
- Documentation for setup and maintenance

## Integration with Maintenance Stage
This CI/CD pipeline provides the Maintenance stage with:
- Automated deployment and rollback capabilities
- Comprehensive monitoring and alerting integration
- Security scanning and compliance automation
- Performance tracking and optimization
- Infrastructure management automation
- Incident response automation triggers

Generate a production-ready CI/CD pipeline that enables reliable, secure, and efficient software delivery with comprehensive observability and maintenance automation.
