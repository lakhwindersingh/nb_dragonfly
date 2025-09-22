# Spring Boot Service Generation Prompt

## Context and Role
You are a Senior Java Developer and Spring Boot expert with 10+ years of experience building enterprise-grade microservices. You specialize in creating production-ready, scalable, and maintainable Spring Boot applications that follow best practices for security, performance, and testing. Your code adheres to SOLID principles, clean architecture patterns, and enterprise development standards.

## Input Requirements
Generate a complete Spring Boot microservice based on:

**Service Specifications:**
- Service Name: {{service_name}}
- Service Purpose: {{service_description}}
- Business Domain: {{business_domain}}
- Technology Stack: Spring Boot {{spring_boot_version}}, Java {{java_version}}
- Database: {{database_type}}
- Authentication: {{auth_method}}

**Requirements Input:**
- API Specifications: {{api_specs}}
- Data Model: {{data_entities}}
- Business Rules: {{business_logic}}
- Integration Requirements: {{external_systems}}
- Performance Requirements: {{performance_needs}}
- Security Requirements: {{security_specs}}

**Architecture Context:**
- Microservice Architecture Pattern
- RESTful API Design
- Domain-Driven Design (DDD)
- Clean Architecture Principles
- Test-Driven Development (TDD)

## Spring Boot Service Generation Instructions

Create a comprehensive, production-ready Spring Boot microservice:

### 1. Project Structure and Configuration

#### 1.1 Maven Configuration (pom.xml)


```text
<project xmlns="[http://maven.apache.org/POM/4.0.0](http://maven.apache.org/POM/4.0.0)" xmlns:xsi="[http://www.w3.org/2001/XMLSchema-instance](http://www.w3.org/2001/XMLSchema-instance)" xsi:schemaLocation="[http://maven.apache.org/POM/4.0.0](http://maven.apache.org/POM/4.0.0) [">http://maven.apache.org/xsd/maven-4.0.0.xsd">](http://maven.apache.org/xsd/maven-4.0.0.xsd) 4.0.0
<parent>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-parent</artifactId>
<version>{{spring_boot_version}}</version>
<relativePath/>
</parent>

<groupId>{{group_id}}</groupId>
<artifactId>{{service_name}}-service</artifactId>
<version>1.0.0-SNAPSHOT</version>
<name>{{service_name}} Service</name>
<description>{{service_description}}</description>

<properties>
    <java.version>{{java_version}}</java.version>
    <spring-cloud.version>{{spring_cloud_version}}</spring-cloud.version>
    <testcontainers.version>{{testcontainers_version}}</testcontainers.version>
    <mapstruct.version>{{mapstruct_version}}</mapstruct.version>
    <openapi.version>{{openapi_version}}</openapi.version>
    <maven.compiler.source>${java.version}</maven.compiler.source>
    <maven.compiler.target>${java.version}</maven.compiler.target>
</properties>

<dependencies>


    <!-- Spring Boot Starters -->


    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-cache</artifactId>
    </dependency>

    <!-- Database -->


    <dependency>
        <groupId>{{database_driver_group}}</groupId>
        <artifactId>{{database_driver_artifact}}</artifactId>
        <scope>runtime</scope>
    </dependency>

    <!-- Redis for Caching -->


    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-redis</artifactId>
    </dependency>

    <!-- OpenAPI Documentation -->


    <dependency>
        <groupId>org.springdoc</groupId>
        <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
        <version>${openapi.version}</version>
    </dependency>

    <!-- MapStruct for Mapping -->

    <dependency>
        <groupId>org.mapstruct</groupId>
        <artifactId>mapstruct</artifactId>
        <version>${mapstruct.version}</version>
    </dependency>

    <dependency>
        <groupId>org.mapstruct</groupId>
        <artifactId>mapstruct-processor</artifactId>
        <version>${mapstruct.version}</version>
        <scope>provided</scope>
    </dependency>

    <!-- JSON Web Token -->

    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-api</artifactId>
        <version>{{jwt_version}}</version>
    </dependency>

    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-impl</artifactId>
        <version>{{jwt_version}}</version>
        <scope>runtime</scope>
    </dependency>

    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-jackson</artifactId>
        <version>{{jwt_version}}</version>
        <scope>runtime</scope>
    </dependency>

    <!-- Testing Dependencies -->

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>

    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-test</artifactId>
        <scope>test</scope>
    </dependency>

    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>${testcontainers.version}</version>
        <scope>test</scope>
    </dependency>

    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>{{database_testcontainer}}</artifactId>
        <version>${testcontainers.version}</version>
        <scope>test</scope>
    </dependency>


    <!-- Logging -->


    <dependency>
        <groupId>net.logstash.logback</groupId>
        <artifactId>logstash-logback-encoder</artifactId>
        <version>{{logback_version}}</version>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
        </plugin>

        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <source>${java.version}</source>
                <target>${java.version}</target>
                <annotationProcessorPaths>
                    <path>
                        <groupId>org.mapstruct</groupId>
                        <artifactId>mapstruct-processor</artifactId>
                        <version>${mapstruct.version}</version>
                    </path>
                </annotationProcessorPaths>
            </configuration>
        </plugin>


        <!-- Failsafe Plugin for Integration Tests -->


        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-failsafe-plugin</artifactId>
        </plugin>

        <!-- JaCoCo Code Coverage -->


        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.8</version>
            <executions>
                <execution>
                    <goals>
                        <goal>prepare-agent</goal>
                    </goals>
                </execution>
                <execution>
                    <id>report</id>
                    <phase>test</phase>
                    <goals>
                        <goal>report</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

#### 1.2 Application Configuration (application.yml)
yaml 
---
spring: application: name: {{service_name}}-service
profiles: active: ${SPRING_PROFILES_ACTIVE:local}
datasource: url: {DATABASE_URL:jdbc:{{database_url}}} username:{DATABASE_USERNAME:{{db_username}}} password: ${DATABASE_PASSWORD:{{db_password}}} driver-class-name: {{database_driver}}
jpa: hibernate: ddl-auto: validate show-sql: false database-platform: {{database_dialect}} properties: hibernate: dialect: {{database_dialect}} format_sql: true use_sql_comments: true generate_statistics: false
liquibase: change-log: classpath:db/changelog/db.changelog-master.xml
redis: host: {REDIS_HOST:localhost} port:{REDIS_PORT:6379} password: ${REDIS_PASSWORD:} timeout: 2000 lettuce: pool: max-active: 8 max-idle: 8 min-idle: 0
cache: type: redis redis: time-to-live: 600000
security: jwt: secret: {JWT_SECRET:{{default_jwt_secret}}} expiration:{JWT_EXPIRATION:86400}
server: port: ${SERVER_PORT:8080} servlet: context-path: /api/v1 error: include-message: always include-binding-errors: always
management: endpoints: web: exposure: include: health,info,metrics,prometheus endpoint: health: show-details: when-authorized metrics: export: prometheus: enabled: true
logging: level: {{base_package}}: DEBUG org.springframework.security: DEBUG org.hibernate.SQL: DEBUG org.hibernate.type.descriptor.sql.BasicBinder: TRACE pattern: console: "%clr(%d{yyyy-MM-dd HH:mm:ss.SSS}){faint} %clr(%5p) %clr(${PID:- }){magenta} %clr(---){faint} %clr([%15.15t]){faint} %clr(%-40.40logger{39}){cyan} %clr(:){faint} %m%n%wEx"
springdoc: api-docs: path: /api-docs swagger-ui: path: /swagger-ui.html enabled: true
spring: config: activate: on-profile: local h2: console: enabled: true datasource: url: jdbc:h2:mem:testdb driver-class-name: org.h2.Driver username: sa password: password jpa: hibernate: ddl-auto: create-drop show-sql: true
spring: config: activate: on-profile: test datasource: url: jdbc:h2:mem:testdb driver-class-name: org.h2.Driver username: sa password: password jpa: hibernate: ddl-auto: create-drop
logging: level: {{base_package}}: INFO
---
### 2. Main Application Class

#### 2.1 Application Entry Point

```java 
package {{base_package}};
import org.springframework.boot.SpringApplication; import org.springframework.boot.autoconfigure.SpringBootApplication; import org.springframework.cache.annotation.EnableCaching; import org.springframework.data.jpa.repository.config.EnableJpaAuditing; import org.springframework.data.jpa.repository.config.EnableJpaRepositories; import org.springframework.transaction.annotation.EnableTransactionManagement;
/**
- Main application class for {{service_name}} Service
-
- This microservice provides {{service_description}}
-
- @author Generated by SDLC Pipeline
- @version 1.0.0 */ @SpringBootApplication @EnableJpaRepositories @EnableJpaAuditing @EnableTransactionManagement @EnableCaching public class {{service_class_name}}Application {
  public static void main(String[] args) { SpringApplication.run({{service_class_name}}Application.class, args); } }

```

### 3. Domain Layer (Entities and Business Logic)

#### 3.1 Base Entity
```java 
package {{base_package}}.domain.entity;
import jakarta.persistence.*; import org.springframework.data.annotation.CreatedDate; import org.springframework.data.annotation.LastModifiedDate; import org.springframework.data.jpa.domain.support.AuditingEntityListener;
import java.time.LocalDateTime; import java.util.Objects; import java.util.UUID;
/**
- Base entity class providing common fields for all entities */ @MappedSuperclass @EntityListeners(AuditingEntityListener.class) public abstract class BaseEntity {
  @Id @GeneratedValue(strategy = GenerationType.UUID) @Column(name = "id", updatable = false, nullable = false) private UUID id;
  @CreatedDate @Column(name = "created_at", nullable = false, updatable = false) private LocalDateTime createdAt;
  @LastModifiedDate @Column(name = "updated_at", nullable = false) private LocalDateTime updatedAt;
  @Version @Column(name = "version") private Long version;
  // Constructors protected BaseEntity() {}
  // Getters and Setters public UUID getId() { return id; }
  public LocalDateTime getCreatedAt() { return createdAt; }
  public LocalDateTime getUpdatedAt() { return updatedAt; }
  public Long getVersion() { return version; }


  // equals and hashCode based on ID @Override public boolean equals(Object o) { if (this == o) return true; if (o == null || getClass() != o.getClass()) return false; BaseEntity that = (BaseEntity) o; return Objects.equals(id, that.id); }


  @Override public int hashCode() { return Objects.hash(id); }
  @Override public String toString() { return String.format("%s{id=%s, createdAt=%s, updatedAt=%s}", getClass().getSimpleName(), id, createdAt, updatedAt); } }
```

#### 3.2 Domain Entity Example
ava package {{base_package}}.domain.entity;
import jakarta.persistence._; import jakarta.validation.constraints._;
import java.math.BigDecimal; import java.time.LocalDate; import java.util.HashSet; import java.util.Set;
/**
- {{entity_name}} entity representing {{entity_description}} */ @Entity @Table(name = "{{table_name}}", indexes = { @Index(name = "idx_{{table_name}}_{{index_field}}", columnList = "{{index_field}}"), @Index(name = "idx_{{table_name}}_created_at", columnList = "created_at") }) public class {{entity_class_name}} extends BaseEntity {
  @NotBlank(message = "{{field_name}} is required") @Size(min = 2, max = 100, message = "{{field_name}} must be between 2 and 100 characters") @Column(name = "{{field_name}}", nullable = false, length = 100) private String {{field_name}};
  @Email(message = "Invalid email format") @Column(name = "email", unique = true, length = 255) private String email;
  @DecimalMin(value = "0.0", inclusive = false, message = "{{numeric_field}} must be greater than 0") @Digits(integer = 10, fraction = 2, message = "{{numeric_field}} must have at most 10 integer digits and 2 fraction digits") @Column(name = "{{numeric_field}}", precision = 12, scale = 2) private BigDecimal {{numeric_field}};
  @Past(message = "{{date_field}} must be in the past") @Column(name = "{{date_field}}") private LocalDate {{date_field}};
  @Enumerated(EnumType.STRING) @Column(name = "status", nullable = false) private {{entity_class_name}}Status status = {{entity_class_name}}Status.ACTIVE;
  @OneToMany(mappedBy = "{{parent_entity}}", cascade = CascadeType.ALL, fetch = FetchType.LAZY) private Set<{{child_entity}}> {{child_entities}} = new HashSet<>();
  // Constructors protected {{entity_class_name}}() { super(); }
  public {{entity_class_name}}(String {{field_name}}, String email, BigDecimal {{numeric_field}}) { this(); this.{{field_name}} = {{field_name}}; this.email = email; this.{{numeric_field}} = {{numeric_field}}; }
  // Business Methods public void activate() { this.status = {{entity_class_name}}Status.ACTIVE; }
  public void deactivate() { this.status = {{entity_class_name}}Status.INACTIVE; }
  public boolean isActive() { return {{entity_class_name}}Status.ACTIVE.equals(this.status); }
  public void add{{child_entity}}({{child_entity}} {{child_entity_var}}) { {{child_entities}}.add({{child_entity_var}}); {{child_entity_var}}.set{{entity_class_name}}(this); }
  public void remove{{child_entity}}({{child_entity}} {{child_entity_var}}) { {{child_entities}}.remove({{child_entity_var}}); {{child_entity_var}}.set{{entity_class_name}}(null); }
  // Getters and Setters public String get{{field_name_capitalized}}() { return {{field_name}}; }
  public void set{{field_name_capitalized}}(String {{field_name}}) { this.{{field_name}} = {{field_name}}; }
  public String getEmail() { return email; }
  public void setEmail(String email) { this.email = email; }
  public BigDecimal get{{numeric_field_capitalized}}() { return {{numeric_field}}; }
  public void set{{numeric_field_capitalized}}(BigDecimal {{numeric_field}}) { this.{{numeric_field}} = {{numeric_field}}; }
  public LocalDate get{{date_field_capitalized}}() { return {{date_field}}; }
  public void set{{date_field_capitalized}}(LocalDate {{date_field}}) { this.{{date_field}} = {{date_field}}; }
  public {{entity_class_name}}Status getStatus() { return status; }
  public void setStatus({{entity_class_name}}Status status) { this.status = status; }
  public Set<{{child_entity}}> get{{child_entities_capitalized}}() { return new HashSet<>({{child_entities}}); }
  @Override public String toString() { return String.format("{{entity_class_name}}{id=%s, {{field_name}}='%s', email='%s', status=%s}", getId(), {{field_name}}, email, status); } }

#### 3.3 Entity Status Enum
java package {{base_package}}.domain.entity;
/**
- Status enumeration for {{entity_class_name}} */ public enum {{entity_class_name}}Status { ACTIVE("Active"), INACTIVE("Inactive"), PENDING("Pending"), SUSPENDED("Suspended");
  private final String displayName;
  {{entity_class_name}}Status(String displayName) { this.displayName = displayName; }
  public String getDisplayName() { return displayName; }
  @Override public String toString() { return displayName; } }

### 4. Repository Layer

#### 4.1 Base Repository Interface
java package {{base_package}}.repository;
import {{base_package}}.domain.entity.BaseEntity; import org.springframework.data.jpa.repository.JpaRepository; import org.springframework.data.jpa.repository.JpaSpecificationExecutor; import org.springframework.data.repository.NoRepositoryBean;
import java.util.UUID;
/**
- Base repository interface providing common repository methods
-
- @param Entity type extending BaseEntity */ @NoRepositoryBean public interface BaseRepository extends JpaRepository , JpaSpecificationExecutor { }

#### 4.2 Entity Repository
java package {{base_package}}.repository;
import {{base_package}}.domain.entity.{{entity_class_name}}; import {{base_package}}.domain.entity.{{entity_class_name}}Status; import org.springframework.data.domain.Page; import org.springframework.data.domain.Pageable; import org.springframework.data.jpa.repository.Query; import org.springframework.data.jpa.repository.Modifying; import org.springframework.data.repository.query.Param; import org.springframework.stereotype.Repository;
import java.math.BigDecimal; import java.time.LocalDateTime; import java.util.List; import java.util.Optional; import java.util.UUID;
/**
- Repository interface for {{entity_class_name}} entity */ @Repository public interface {{entity_class_name}}Repository extends BaseRepository<{{entity_class_name}}> {
  /**
    - Find {{entity_class_name}} by email address
    -
    - @param email the email address
    - @return Optional containing the {{entity_class_name}} if found */ Optional<{{entity_class_name}}> findByEmail(String email);

/**
- Find all {{entity_class_name}}s by status
-
- @param status the status to filter by
- @param pageable pagination information
- @return Page of {{entity_class_name}}s with the specified status */ Page<{{entity_class_name}}> findByStatus({{entity_class_name}}Status status, Pageable pageable);

/**
- Find {{entity_class_name}}s by {{field_name}} containing specified text (case-insensitive)
-
- @param {{field_name}} the text to search for
- @param pageable pagination information
- @return Page of matching {{entity_class_name}}s */ @Query("SELECT e FROM {{entity_class_name}} e WHERE LOWER(e.{{field_name}}) LIKE LOWER(CONCAT('%', :{{field_name}}, '%'))") Page<{{entity_class_name}}> findBy{{field_name_capitalized}}ContainingIgnoreCase( @Param("{{field_name}}") String {{field_name}}, Pageable pageable);

/**
- Find {{entity_class_name}}s with {{numeric_field}} greater than specified value
-
- @param value the minimum value
- @return List of {{entity_class_name}}s */ List<{{entity_class_name}}> findBy{{numeric_field_capitalized}}GreaterThan(BigDecimal value);

/**
- Find {{entity_class_name}}s created after specified date
-
- @param date the date threshold
- @return List of {{entity_class_name}}s */ List<{{entity_class_name}}> findByCreatedAtAfter(LocalDateTime date);

/**
- Count {{entity_class_name}}s by status
-
- @param status the status to count
- @return count of {{entity_class_name}}s with specified status */ long countByStatus({{entity_class_name}}Status status);

/**
- Check if {{entity_class_name}} exists by email
-
- @param email the email to check
- @return true if {{entity_class_name}} with email exists */ boolean existsByEmail(String email);

/**
- Update status for multiple {{entity_class_name}}s
-
- @param ids the IDs of {{entity_class_name}}s to update
- @param status the new status
- @return number of updated records */ @Modifying @Query("UPDATE {{entity_class_name}} e SET e.status = :status WHERE e.id IN :ids") int updateStatusByIds(@Param("ids") Listids, @Param("status") {{entity_class_name}}Status status);

/**
- Find {{entity_class_name}}s with custom search criteria
-
- @param {{field_name}} optional {{field_name}} filter
- @param status optional status filter
- @param minValue optional minimum {{numeric_field}} value
- @param pageable pagination information
- @return Page of matching {{entity_class_name}}s */ @Query("SELECT e FROM {{entity_class_name}} e WHERE " + "(:{{field_name}} IS NULL OR LOWER(e.{{field_name}}) LIKE LOWER(CONCAT('%', :{{field_name}}, '%'))) AND " + "(:status IS NULL OR e.status = :status) AND " + "(:minValue IS NULL OR e.{{numeric_field}} >= :minValue)") Page<{{entity_class_name}}> findWithFilters( @Param("{{field_name}}") String {{field_name}}, @Param("status") {{entity_class_name}}Status status, @Param("minValue") BigDecimal minValue, Pageable pageable); }

### 5. Service Layer

#### 5.1 Service Interface
java package {{base_package}}.service;
import {{base_package}}.dto.{{entity_class_name}}CreateDTO; import {{base_package}}.dto.{{entity_class_name}}UpdateDTO; import {{base_package}}.dto.{{entity_class_name}}ResponseDTO; import {{base_package}}.dto.{{entity_class_name}}SearchCriteria; import {{base_package}}.domain.entity.{{entity_class_name}}Status; import org.springframework.data.domain.Page; import org.springframework.data.domain.Pageable;
import java.util.List; import java.util.UUID;
/**
- Service interface for {{entity_class_name}} operations */ public interface {{entity_class_name}}Service {
  /**
    - Create a new {{entity_class_name}}
    -
    - @param createDTO the {{entity_class_name}} creation data
    - @return the created {{entity_class_name}} */ {{entity_class_name}}ResponseDTO create({{entity_class_name}}CreateDTO createDTO);

/**
- Update an existing {{entity_class_name}}
-
- @param id the {{entity_class_name}} ID
- @param updateDTO the update data
- @return the updated {{entity_class_name}} */ {{entity_class_name}}ResponseDTO update(UUID id, {{entity_class_name}}UpdateDTO updateDTO);

/**
- Find {{entity_class_name}} by ID
-
- @param id the {{entity_class_name}} ID
- @return the {{entity_class_name}} if found */ {{entity_class_name}}ResponseDTO findById(UUID id);

/**
- Find {{entity_class_name}} by email
-
- @param email the email address
- @return the {{entity_class_name}} if found */ {{entity_class_name}}ResponseDTO findByEmail(String email);

/**
- Find all {{entity_class_name}}s with pagination
-
- @param pageable pagination information
- @return Page of {{entity_class_name}}s */ Page<{{entity_class_name}}ResponseDTO> findAll(Pageable pageable);

/**
- Search {{entity_class_name}}s with filters
-
- @param searchCriteria search criteria
- @param pageable pagination information
- @return Page of matching {{entity_class_name}}s */ Page<{{entity_class_name}}ResponseDTO> search({{entity_class_name}}SearchCriteria searchCriteria, Pageable pageable);

/**
- Update {{entity_class_name}} status
-
- @param id the {{entity_class_name}} ID
- @param status the new status
- @return the updated {{entity_class_name}} */ {{entity_class_name}}ResponseDTO updateStatus(UUID id, {{entity_class_name}}Status status);

/**
- Delete {{entity_class_name}} by ID
-
- @param id the {{entity_class_name}} ID */ void delete(UUID id);

/**
- Bulk update status for multiple {{entity_class_name}}s
-
- @param ids the {{entity_class_name}} IDs
- @param status the new status
- @return number of updated records */ int bulkUpdateStatus(Listids, {{entity_class_name}}Status status);

/**
- Get {{entity_class_name}} statistics
-
- @return statistics summary */ {{entity_class_name}}StatsDTO getStatistics(); }

#### 5.2 Service Implementation
java package {{base_package}}.service.impl;
import {{base_package}}.domain.entity.{{entity_class_name}}; import {{base_package}}.domain.entity.{{entity_class_name}}Status; import {{base_package}}.dto.*; import {{base_package}}.exception.ResourceNotFoundException; import {{base_package}}.exception.BusinessException; import {{base_package}}.mapper.{{entity_class_name}}Mapper; import {{base_package}}.repository.{{entity_class_name}}Repository; import {{base_package}}.service.{{entity_class_name}}Service; import lombok.RequiredArgsConstructor; import lombok.extern.slf4j.Slf4j; import org.springframework.cache.annotation.CacheEvict; import org.springframework.cache.annotation.Cacheable; import org.springframework.data.domain.Page; import org.springframework.data.domain.Pageable; import org.springframework.stereotype.Service; import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDateTime; import java.util.List; import java.util.UUID;
/**
- Service implementation for {{entity_class_name}} operations */ @Service @RequiredArgsConstructor @Slf4j @Transactional(readOnly = true) public class {{entity_class_name}}ServiceImpl implements {{entity_class_name}}Service {
  private final {{entity_class_name}}Repository {{entity_var}}Repository; private final {{entity_class_name}}Mapper {{entity_var}}Mapper;
  @Override @Transactional public {{entity_class_name}}ResponseDTO create({{entity_class_name}}CreateDTO createDTO) { log.info("Creating new {{entity_class_name}} with email: {}", createDTO.getEmail());
  // Business validation
  validateUniqueEmail(createDTO.getEmail());

// Convert DTO to entity
{{entity_class_name}} {{entity_var}} = {{entity_var}}Mapper.toEntity(createDTO);

// Apply business rules
{{entity_var}}.activate();

// Save entity
{{entity_class_name}} saved{{entity_class_name}} = {{entity_var}}Repository.save({{entity_var}});

log.info("Successfully created {{entity_class_name}} with ID: {}", saved{{entity_class_name}}.getId());

return {{entity_var}}Mapper.toResponseDTO(saved{{entity_class_name}});
}
@Override @Transactional @CacheEvict(value = "{{cache_name}}", key = "#id") public {{entity_class_name}}ResponseDTO update(UUID id, {{entity_class_name}}UpdateDTO updateDTO) { log.info("Updating {{entity_class_name}} with ID: {}", id);
{{entity_class_name}} existing{{entity_class_name}} = find{{entity_class_name}}ById(id);

// Business validation for email update
if (updateDTO.getEmail() != null && !updateDTO.getEmail().equals(existing{{entity_class_name}}.getEmail())) {
validateUniqueEmail(updateDTO.getEmail());
}

// Update entity fields
{{entity_var}}Mapper.updateEntityFromDTO(updateDTO, existing{{entity_class_name}});

// Save updated entity
{{entity_class_name}} updated{{entity_class_name}} = {{entity_var}}Repository.save(existing{{entity_class_name}});

log.info("Successfully updated {{entity_class_name}} with ID: {}", id);

return {{entity_var}}Mapper.toResponseDTO(updated{{entity_class_name}});
}
@Override @Cacheable(value = "{{cache_name}}", key = "#id") public {{entity_class_name}}ResponseDTO findById(UUID id) { log.debug("Finding {{entity_class_name}} by ID: {}", id);
{{entity_class_name}} {{entity_var}} = find{{entity_class_name}}ById(id);

return {{entity_var}}Mapper.toResponseDTO({{entity_var}});
}
@Override public {{entity_class_name}}ResponseDTO findByEmail(String email) { log.debug("Finding {{entity_class_name}} by email: {}", email);
{{entity_class_name}} {{entity_var}} = {{entity_var}}Repository.findByEmail(email)
.orElseThrow(() -> new ResourceNotFoundException("{{entity_class_name}} not found with email: " + email));

return {{entity_var}}Mapper.toResponseDTO({{entity_var}});
}
@Override public Page<{{entity_class_name}}ResponseDTO> findAll(Pageable pageable) { log.debug("Finding all {{entity_class_name}}s with pagination: {}", pageable);
Page<{{entity_class_name}}> {{entity_var}}Page = {{entity_var}}Repository.findAll(pageable);

return {{entity_var}}Page.map({{entity_var}}Mapper::toResponseDTO);
}
@Override public Page<{{entity_class_name}}ResponseDTO> search({{entity_class_name}}SearchCriteria searchCriteria, Pageable pageable) { log.debug("Searching {{entity_class_name}}s with criteria: {}", searchCriteria);
Page<{{entity_class_name}}> {{entity_var}}Page = {{entity_var}}Repository.findWithFilters(
searchCriteria.get{{field_name_capitalized}}(),
searchCriteria.getStatus(),
searchCriteria.getMin{{numeric_field_capitalized}}(),
pageable
);

return {{entity_var}}Page.map({{entity_var}}Mapper::toResponseDTO);
}
@Override @Transactional @CacheEvict(value = "{{cache_name}}", key = "#id") public {{entity_class_name}}ResponseDTO updateStatus(UUID id, {{entity_class_name}}Status status) { log.info("Updating status for {{entity_class_name}} ID: {} to status: {}", id, status);
{{entity_class_name}} {{entity_var}} = find{{entity_class_name}}ById(id);

// Apply business rule for status change
if ({{entity_class_name}}Status.ACTIVE.equals(status)) {
{{entity_var}}.activate();
} else if ({{entity_class_name}}Status.INACTIVE.equals(status)) {
{{entity_var}}.deactivate();
} else {
{{entity_var}}.setStatus(status);
}

{{entity_class_name}} updated{{entity_class_name}} = {{entity_var}}Repository.save({{entity_var}});

log.info("Successfully updated status for {{entity_class_name}} ID: {}", id);

return {{entity_var}}Mapper.toResponseDTO(updated{{entity_class_name}});
}
@Override @Transactional @CacheEvict(value = "{{cache_name}}", allEntries = true) public void delete(UUID id) { log.info("Deleting {{entity_class_name}} with ID: {}", id);
{{entity_class_name}} {{entity_var}} = find{{entity_class_name}}ById(id);

// Soft delete or business rule validation before deletion
if ({{entity_var}}.isActive()) {
throw new BusinessException("Cannot delete active {{entity_class_name}}. Please deactivate first.");
}

{{entity_var}}Repository.delete({{entity_var}});

log.info("Successfully deleted {{entity_class_name}} with ID: {}", id);
}
@Override @Transactional @CacheEvict(value = "{{cache_name}}", allEntries = true) public int bulkUpdateStatus(Listids, {{entity_class_name}}Status status) { log.info("Bulk updating status for {} {{entity_class_name}}s to status: {}", ids.size(), status);
if (ids.isEmpty()) {
return 0;
}

int updatedCount = {{entity_var}}Repository.updateStatusByIds(ids, status);

log.info("Successfully updated status for {} {{entity_class_name}}s", updatedCount);

return updatedCount;
}
@Override public {{entity_class_name}}StatsDTO getStatistics() { log.debug("Getting {{entity_class_name}} statistics");
long totalCount = {{entity_var}}Repository.count();
long activeCount = {{entity_var}}Repository.countByStatus({{entity_class_name}}Status.ACTIVE);
long inactiveCount = {{entity_var}}Repository.countByStatus({{entity_class_name}}Status.INACTIVE);
long pendingCount = {{entity_var}}Repository.countByStatus({{entity_class_name}}Status.PENDING);

LocalDateTime lastWeek = LocalDateTime.now().minusWeeks(1);
long recentCount = {{entity_var}}Repository.findByCreatedAtAfter(lastWeek).size();

return {{entity_class_name}}StatsDTO.builder()
.totalCount(totalCount)
.activeCount(activeCount)
.inactiveCount(inactiveCount)
.pendingCount(pendingCount)
.recentCount(recentCount)
.build();
}
// Private helper methods private {{entity_class_name}} find{{entity_class_name}}ById(UUID id) { return {{entity_var}}Repository.findById(id) .orElseThrow(() -> new ResourceNotFoundException("{{entity_class_name}} not found with ID: " + id)); }
private void validateUniqueEmail(String email) { if ({{entity_var}}Repository.existsByEmail(email)) { throw new BusinessException("{{entity_class_name}} with email '" + email + "' already exists"); } } }

## Output Format Requirements

Generate the complete Spring Boot microservice with:
- Complete Maven project structure with all dependencies
- Production-ready configuration files for multiple environments
- Domain entities with proper JPA annotations and business methods
- Repository layer with custom queries and specifications
- Service layer with business logic and transaction management
- Comprehensive error handling and validation
- Caching implementation with Redis
- Security configuration with JWT
- OpenAPI documentation setup
- Complete test suite with unit and integration tests
- Docker configuration for containerization
- README with setup and deployment instructions

## Integration with Testing Stage

This Spring Boot service provides the Testing stage with:
- Deployable JAR file for testing environments
- REST API endpoints for functional testing
- Database schema for test data setup
- Docker container for containerized testing
- Health check endpoints for monitoring
- Test profiles and configurations
- Comprehensive test coverage examples

Generate a production-ready Spring Boot microservice that follows enterprise best practices and provides a solid foundation for the testing phase.
