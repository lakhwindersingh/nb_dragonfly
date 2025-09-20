# Spring Boot Microservice Template

This template provides a complete Spring Boot microservice structure following best practices for enterprise applications.

## Features
- Spring Boot 3.x with Java 17+
- Spring Security with JWT authentication
- Spring Data JPA with PostgreSQL
- OpenAPI 3 documentation (Swagger)
- Docker containerization
- Comprehensive testing setup
- Actuator for monitoring
- Structured logging with Logback

## Project Structure
- **src/

```text
- ├── main/
- │ ├── java/com/company/service/
- │ │ ├── ServiceApplication.java
- │ │ ├── config/
- │ │ ├── controller/
- │ │ ├── service/
- │ │ ├── repository/
- │ │ ├── entity/
- │ │ ├── dto/
- │ │ ├── exception/
- │ │ └── security/
- │ └── resources/
- │ ├── application.yml
- │ ├── application-dev.yml
- │ ├── application-prod.yml
- │ └── db/migration/
- └── test/
- └── java/com/company/service/
- ├── integration/
- ├── unit/
- └── testcontainers/**
```

## Configuration Files
- `pom.xml` - Maven dependencies and build configuration
- `Dockerfile` - Docker container configuration
- `docker-compose.yml` - Local development environment
- `k8s/` - Kubernetes deployment manifests
