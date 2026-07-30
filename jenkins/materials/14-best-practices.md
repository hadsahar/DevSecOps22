# Jenkins Best Practices

## Table of Contents
1. [Controller Configuration](#controller-configuration)
2. [Pipeline Design Best Practices](#pipeline-design-best-practices)
3. [Agent Best Practices](#agent-best-practices)
4. [Credentials and Secrets Management](#credentials-and-secrets-management)
5. [Performance and Scalability](#performance-and-scalability)
6. [Plugin Management](#plugin-management)
7. [Backup and Disaster Recovery](#backup-and-disaster-recovery)
8. [Monitoring and Observability](#monitoring-and-observability)
9. [Code Organization and Reuse](#code-organization-and-reuse)
10. [Build Hygiene](#build-hygiene)
11. [Naming Conventions](#naming-conventions)
12. [Jenkins as Code (JCasC)](#jenkins-as-code-jcasc)
13. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

---

## Controller Configuration

### Never Run Builds on the Controller

The Controller should **only** orchestrate — it should never execute build steps.

```
Manage Jenkins → Nodes → Built-In Node → Configure
  Number of executors: 0
```

Reasons:
- Build processes can exhaust memory and crash Jenkins
- Builds can access sensitive files in `$JENKINS_HOME`
- Disk space from builds can fill the Jenkins home directory

### Set the Jenkins URL Correctly

```
Manage Jenkins → System → Jenkins URL
  http://jenkins.company.internal:8080/
```

This is used in:
- Email notification links
- Webhook callback URLs
- Git commit status URLs

### Limit Build History

Always configure log rotation to prevent disk exhaustion:

```groovy
options {
    buildDiscarder(logRotator(
        numToKeepStr:  '30',
        daysToKeepStr: '30',
        artifactNumToKeepStr: '10'
    ))
}
```

Or in Freestyle job: **General → Discard old builds → Log Rotation**

### Tune JVM for the Controller

In `/etc/default/jenkins` or Docker env:

```bash
JAVA_OPTS="-Xms512m -Xmx4g \
  -Djava.awt.headless=true \
  -Dfile.encoding=UTF-8 \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -Dhudson.model.DirectoryBrowserSupport.CSP=\"default-src 'self';\""
```

---

## Pipeline Design Best Practices

### Always Use Declarative Pipelines

```groovy
// Good — Declarative
pipeline {
    agent any
    stages { ... }
}

// Avoid in new code — Scripted
node {
    stage('Build') { ... }
}
```

### Keep Jenkinsfile in the Application Repository

```
my-app/
├── src/
├── Dockerfile
├── helm/
└── Jenkinsfile        ← lives here, versioned with code
```

### Fail Fast — Catch Errors Early

Order stages from fastest to slowest and most likely to fail first:

```groovy
stages {
    stage('Lint')            { ... }   // ~30 seconds
    stage('Unit Tests')      { ... }   // ~2 minutes
    stage('Build')           { ... }   // ~3 minutes
    stage('Integration Tests') { ... } // ~10 minutes
    stage('Deploy to Staging') { ... } // ~2 minutes
    stage('E2E Tests')       { ... }   // ~20 minutes
    stage('Deploy to Prod')  { ... }   // ~3 minutes
}
```

### Use Parallel Stages to Reduce Build Time

```groovy
stage('Quality Gates') {
    parallel {
        stage('Unit Tests')    { steps { sh 'mvn test' } }
        stage('SAST Scan')     { steps { sh 'sonar-scanner' } }
        stage('Dependency Check') { steps { sh 'dependency-check.sh' } }
    }
}
```

### Always Use `checkout scm`

```groovy
// Good — uses the SCM configured in the pipeline job
checkout scm

// Avoid — hardcodes URL, doesn't use credentials from job config
git 'https://github.com/org/repo.git'
```

### Set Timeouts to Prevent Stuck Builds

```groovy
options {
    timeout(time: 60, unit: 'MINUTES')  // Kill if > 1 hour
}

// Or per-stage
stage('Long Test') {
    options {
        timeout(time: 30, unit: 'MINUTES')
    }
    steps { sh './run-long-tests.sh' }
}
```

### Avoid Shell Script Injection — Use Single Quotes with User Input

```groovy
// VULNERABLE — user input injected into shell
sh "echo ${params.USER_INPUT}"

// SAFE — pass as environment variable
environment { SAFE_INPUT = params.USER_INPUT }
steps { sh 'echo $SAFE_INPUT' }
```

### Use `returnStatus` Instead of `error()` for Non-Fatal Steps

```groovy
script {
    def status = sh(script: './optional-check.sh', returnStatus: true)
    if (status != 0) {
        echo "Optional check failed (status: ${status}) — continuing"
        // Don't throw, just log
    }
}
```

---

## Agent Best Practices

### Use Ephemeral Agents (Docker/Kubernetes)

Ephemeral agents provide clean, reproducible environments for every build:

```groovy
agent {
    docker { image 'maven:3.9-eclipse-temurin-17' }
}
```

### Use Labels — Never Hardcode Node Names

```groovy
// Good
agent { label 'linux && docker' }

// Avoid
agent { node { label 'linux-agent-01' } }  // brittle — breaks if node renamed
```

### Cache Dependencies on Agents

Mount dependency caches as volumes to speed up builds:

```groovy
agent {
    docker {
        image 'maven:3.9'
        args  '-v $HOME/.m2:/root/.m2'   // Maven cache
    }
}
```

For Kubernetes:

```yaml
volumes:
- name: m2-cache
  persistentVolumeClaim:
    claimName: maven-cache-pvc
containers:
- name: build
  volumeMounts:
  - name: m2-cache
    mountPath: /root/.m2
```

### Clean Workspace After Builds

```groovy
post {
    cleanup {
        cleanWs()   // Always clean — prevents workspace contamination
    }
}
```

---

## Credentials and Secrets Management

### Use `withCredentials()` with Minimum Scope

Only expose credentials for the steps that need them:

```groovy
// Good — scoped
withCredentials([string(credentialsId: 'api-token', variable: 'TOKEN')]) {
    sh './deploy.sh'
}

// Avoid — credentials visible to entire pipeline
environment {
    TOKEN = credentials('api-token')  // Only do this when truly needed globally
}
```

### Never Print Secrets — Jenkins Masks Them, But Still Avoid

```groovy
// Dangerous — even if masked, avoid logging credential variables
echo "Using token: ${env.SECRET_TOKEN}"

// Safe — use the secret in the tool, don't echo it
sh 'curl -H "Authorization: Bearer $SECRET_TOKEN" https://api.example.com'
```

### Use a Naming Convention for Credential IDs

```
{environment}-{service}-{type}

prod-aws-credentials
staging-dockerhub-creds
global-github-token
prod-db-password
dev-sonar-token
```

### Rotate Credentials Regularly

- Use credential expiry reminders in your team's runbook
- Store rotation history outside Jenkins
- Prefer short-lived tokens (OIDC, IRSA) over long-lived access keys

### Prefer IAM Roles Over Access Keys for AWS

```
# BAD: stored long-lived keys
AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY in Jenkins credentials

# GOOD: EC2 instance role or EKS IRSA
No keys needed — role assumed automatically
```

---

## Performance and Scalability

### Increase Controller Executors Wisely

The Controller should run 0 build executors. For pipeline orchestration (non-build steps like `input`, `sh 'echo'`), 2 executors on the Controller is fine.

### Use Multibranch Pipelines with Scan Throttling

Scanning thousands of branches at once can spike CPU. Set:

```
Multibranch Pipeline → Configure → Scan Repository Triggers
  Periodically if not otherwise run: 1 day
  Scan on push (via webhook): recommended
```

### Throttle Concurrent Builds for Heavy Jobs

```groovy
options {
    throttleJobProperty(
        categories: ['heavy-builds'],
        throttleEnabled: true,
        throttleOption: 'category'
    )
}
```

Or simply:

```groovy
options {
    disableConcurrentBuilds()
}
```

### Use Shared Workspaces Carefully

If multiple executors on the same node run the same job, workspace collision can occur. Use `ws()` to create unique workspaces:

```groovy
ws("workspace/${env.JOB_NAME}/${env.BUILD_NUMBER}") {
    checkout scm
    sh './build.sh'
}
```

---

## Plugin Management

### Minimize the Number of Plugins

Each plugin increases:
- Security attack surface
- Update maintenance burden
- Memory footprint
- Startup time

Install only what you actively use.

### Pin Plugin Versions in Dockerfile

```dockerfile
FROM jenkins/jenkins:lts-jdk17

RUN jenkins-plugin-cli --plugins \
  git:5.2.1 \
  workflow-aggregator:596.v8c21c963d92d \
  kubernetes:4029.v5712230ccb_f8
```

### Review Plugin Changelogs Before Updating

```
Manage Jenkins → Plugins → Updates → Read changelog links before updating
```

### Back Up Before Plugin Updates

```bash
sudo systemctl stop jenkins
tar -czvf jenkins-before-plugins-$(date +%Y%m%d).tar.gz /var/lib/jenkins
sudo systemctl start jenkins
```

---

## Backup and Disaster Recovery

### What to Back Up

```
$JENKINS_HOME/
├── config.xml                  ← Main config
├── credentials.xml             ← Encrypted credentials
├── jobs/*/config.xml           ← Job definitions
├── nodes/*/config.xml          ← Agent configs
├── plugins/*.jpi               ← Plugin files
└── secrets/                    ← Master encryption key
    └── master.key              ← CRITICAL — back up separately
```

### Backup Script

```bash
#!/bin/bash
BACKUP_DIR=/backups/jenkins
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/jenkins-${DATE}.tar.gz"

mkdir -p "${BACKUP_DIR}"

tar -czvf "${BACKUP_FILE}" \
    --exclude='/var/lib/jenkins/workspace' \
    --exclude='/var/lib/jenkins/logs' \
    /var/lib/jenkins

# Retain only 30 days of backups
find "${BACKUP_DIR}" -name "jenkins-*.tar.gz" -mtime +30 -delete

echo "Backup completed: ${BACKUP_FILE}"
```

### Restore Procedure

```bash
sudo systemctl stop jenkins
sudo tar -xzvf jenkins-20240115-020000.tar.gz -C /
sudo chown -R jenkins:jenkins /var/lib/jenkins
sudo systemctl start jenkins
```

### Use Job DSL or JCasC for Configuration as Code

The best backup is having everything reproducible from code:

- **JCasC** — Jenkins configuration as YAML
- **Job DSL** — Jobs defined as Groovy scripts
- **Shared Libraries** — Pipeline logic in Git

---

## Monitoring and Observability

### Enable Prometheus Metrics

Install **Prometheus Metrics Plugin**:

```
Metrics exposed at: http://jenkins:8080/prometheus
```

Key metrics to alert on:
- `jenkins_builds_failed_total` — failed builds
- `jenkins_queue_size_value` — build queue depth
- `jenkins_executor_count_value` — executor usage
- `jenkins_node_offline_value` — offline agents

### Add Timestamps to Console Output

```groovy
options {
    timestamps()
}
```

### Set Meaningful Build Display Names

```groovy
stage('Init') {
    steps {
        script {
            currentBuild.displayName = "#${env.BUILD_NUMBER} | ${env.BRANCH_NAME} | ${env.GIT_COMMIT.take(7)}"
            currentBuild.description = "Deployed to ${params.TARGET_ENV} by ${env.BUILD_USER}"
        }
    }
}
```

### Audit Log Plugin

Install **Audit Trail Plugin** to log who made configuration changes:

```
Manage Jenkins → System → Audit Trail
  Log Location: /var/log/jenkins/audit.log
```

---

## Code Organization and Reuse

### Use Shared Libraries for Common Patterns

```groovy
@Library('company-pipeline-lib@main') _

// One line replaces 100 lines
mavenPipeline(image: 'myorg/my-service', namespace: 'staging')
```

### Organize Jobs in Folders

```
Jenkins/
├── team-payments/
│   ├── payment-service
│   ├── payment-worker
│   └── payment-api
├── team-frontend/
│   ├── web-app
│   └── mobile-api
└── infrastructure/
    ├── terraform-apply
    └── k8s-maintenance
```

### Use Multibranch Pipelines

Configure one Multibranch Pipeline per repository. Jenkins auto-discovers and builds every branch that has a `Jenkinsfile`.

---

## Build Hygiene

### Always Clean Workspace Before Build

```groovy
options {
    cleanBeforeCheckout()
}
// or
post { cleanup { cleanWs() } }
```

### Use Specific Image Tags — Never `latest` in Production

```groovy
// Bad
image 'node:latest'

// Good
image 'node:18.19.0-alpine3.19'
```

### Validate Jenkinsfile Syntax Before Merging

```bash
# Via Jenkins CLI
java -jar jenkins-cli.jar -s http://jenkins:8080 \
  -auth admin:token \
  declarative-linter < Jenkinsfile
```

Add this as a pre-commit hook or a PR validation pipeline.

---

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Job name | `{team}-{service}-{type}` | `payments-api-build` |
| Credential ID | `{env}-{service}-{type}` | `prod-aws-credentials` |
| Node label | `{os}-{capability}` | `linux-docker` |
| Shared library | `{org}-pipeline-lib` | `company-pipeline-lib` |
| Docker image tag | `{build#}-{git-sha}` | `42-a1b2c3d` |
| S3 path | `{service}/{env}/{build#}/` | `payments/prod/42/` |

---

## Jenkins as Code (JCasC)

Define your entire Jenkins configuration in a YAML file:

```yaml
# jenkins.yaml
jenkins:
  systemMessage: "Managed by JCasC — do not edit manually"
  numExecutors: 0
  mode: EXCLUSIVE
  agentProtocols:
    - "JNLP4-connect"
  authorizationStrategy:
    roleBased:
      roles:
        global:
          - name: "admin"
            permissions: ["Overall/Administer"]
            assignments:
              - "admin-user"
          - name: "developer"
            permissions: ["Overall/Read", "Job/Build", "Job/Read"]

  clouds:
    - kubernetes:
        name: "kubernetes"
        serverUrl: "https://kubernetes.default.svc"
        namespace: "jenkins"
        jenkinsUrl: "http://jenkins.jenkins.svc.cluster.local:8080"

unclassified:
  location:
    url: "https://jenkins.example.com/"
  slackNotifier:
    teamDomain: "mycompany"
    tokenCredentialId: "slack-token"

credentials:
  system:
    domainCredentials:
      - credentials:
          - string:
              id: "github-token"
              secret: "${GITHUB_TOKEN}"
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Running builds on Controller | Security + stability risk | Set executors = 0 |
| `latest` Docker tags | Non-reproducible builds | Pin to exact versions |
| Hardcoded credentials in Jenkinsfile | Security breach | Use credentials store |
| Giant monolithic pipeline | Hard to debug, slow | Split into parallel stages |
| No build timeouts | Stuck builds block agents | Add `timeout()` options |
| No log rotation | Disk exhaustion | Add `buildDiscarder` options |
| `git` step instead of `checkout scm` | Hardcoded URLs, no credentials | Use `checkout scm` |
| Polling SCM every minute | High load on controller + SCM | Use webhooks instead |
| No workspace cleanup | Disk fills up, stale artifacts | Use `cleanWs()` in post |
| Scripted pipelines for everything | Harder to maintain, read | Use Declarative |
| Shell injection via `${params.X}` | Security vulnerability | Pass params as env vars |
