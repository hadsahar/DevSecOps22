# What is CI/CD and What is a Pipeline?

## Table of Contents
1. [The Problem CI/CD Solves](#the-problem-cicd-solves)
2. [What is Continuous Integration (CI)?](#what-is-continuous-integration-ci)
3. [What is Continuous Delivery (CD)?](#what-is-continuous-delivery-cd)
4. [What is Continuous Deployment?](#what-is-continuous-deployment)
5. [CI vs CD vs Continuous Deployment](#ci-vs-cd-vs-continuous-deployment)
6. [What is a Pipeline?](#what-is-a-pipeline)
7. [Jenkins Pipeline Types](#jenkins-pipeline-types)
8. [The Software Delivery Lifecycle with CI/CD](#the-software-delivery-lifecycle-with-cicd)
9. [Real-World CI/CD Example](#real-world-cicd-example)

---

## The Problem CI/CD Solves

Before CI/CD, teams integrated code manually every few weeks. This caused:

- **Merge hell** — huge conflicts when branches diverged for weeks
- **"It works on my machine"** — inconsistent environments
- **Slow feedback** — bugs found weeks after they were introduced
- **Manual deployments** — error-prone, undocumented, irreversible steps
- **Big-bang releases** — all risk concentrated in one deployment event

CI/CD replaces these practices with an automated, repeatable, and fast delivery process.

---

## What is Continuous Integration (CI)?

**Continuous Integration (CI)** is the practice of automatically building and testing every code change as soon as it is pushed to a shared repository.

### CI Workflow

```
Developer writes code
      │
      ▼
   git push
      │
      ▼
 CI Server detects change (webhook/polling)
      │
      ▼
 ┌────────────────────────────────────────┐
 │           CI Pipeline                  │
 │  1. Checkout source code               │
 │  2. Install dependencies               │
 │  3. Run linting / static analysis      │
 │  4. Compile / build                    │
 │  5. Run unit tests                     │
 │  6. Run integration tests              │
 │  7. Generate test coverage report      │
 │  8. Publish build artifact             │
 └────────────────────────────────────────┘
      │
      ▼
  Pass ✅ or Fail ❌ → Notify developer
```

### CI Principles
- Every commit triggers a build
- Builds should complete in under 10 minutes
- If the build breaks, fixing it is the team's top priority
- The main branch must always be in a deployable state

---

## What is Continuous Delivery (CD)?

**Continuous Delivery** extends CI by automatically preparing the release artifact and making it **ready to deploy** to production — but a human approves the final deployment step.

```
CI Pipeline (automated)
      │
      ▼
 Artifact is versioned & stored
      │
      ▼
 Deploy to Staging (automated)
      │
      ▼
 Run smoke tests / acceptance tests (automated)
      │
      ▼
 ┌─────────────────────────────────┐
 │   Manual Approval Gate          │
 │   "Ready for Production?"       │
 │   ✅ Approve  /  ❌ Reject       │
 └─────────────────────────────────┘
      │
      ▼
 Deploy to Production (automated after approval)
```

### Why Keep a Manual Gate?
- Regulatory compliance (banking, healthcare)
- Business stakeholders need sign-off
- Risk management for critical systems

---

## What is Continuous Deployment?

**Continuous Deployment** removes the manual gate entirely. Every change that passes all automated tests is deployed to production automatically.

```
Commit → CI → Tests pass → Deploy to Production (no human needed)
```

### When to Use Continuous Deployment
- High test coverage (>80%)
- Mature monitoring and alerting
- Feature flags to decouple deploy from release
- Ability to roll back instantly
- Teams like Netflix, Facebook, Amazon use this model

---

## CI vs CD vs Continuous Deployment

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   Commit ──► Build ──► Test                              │
│   └──────────────────────────── CI ──────────────────┘  │
│                                                          │
│   Commit ──► Build ──► Test ──► Stage ──► [Approve]      │
│   └────────────────────────────────────── CD ────────┘  │
│                                                          │
│   Commit ──► Build ──► Test ──► Stage ──► Production     │
│   └────────────────────────────── Continuous Deploy ─┘  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

| Practice | Automation Level | Human Gate |
|----------|-----------------|------------|
| CI | Build + Test | No gate |
| Continuous Delivery | Build + Test + Stage | Before production |
| Continuous Deployment | Build + Test + Stage + Prod | None |

---

## What is a Pipeline?

A **pipeline** is the automated sequence of steps that carries code from a commit to production. In Jenkins, a pipeline is defined as code (using Groovy DSL) and stored in a `Jenkinsfile`.

### Why Pipeline as Code?

- **Version controlled** — lives in the same repo as the app
- **Reviewable** — changes to the pipeline go through code review
- **Reproducible** — same pipeline runs everywhere
- **Auditable** — full history of pipeline changes

### Anatomy of a Jenkins Pipeline

```groovy
pipeline {
    agent any                        // Where to run

    triggers {
        pollSCM('H/5 * * * *')       // When to trigger
    }

    environment {
        APP_NAME = 'my-app'          // Variables
    }

    stages {
        stage('Checkout') {          // Step 1
            steps {
                git 'https://github.com/org/repo.git'
            }
        }
        stage('Build') {             // Step 2
            steps {
                sh 'mvn clean package'
            }
        }
        stage('Test') {              // Step 3
            steps {
                sh 'mvn test'
            }
        }
        stage('Deploy') {            // Step 4
            steps {
                sh './deploy.sh'
            }
        }
    }

    post {
        always {
            junit '**/target/surefire-reports/*.xml'
        }
        failure {
            mail to: 'team@example.com', subject: 'Build Failed!'
        }
    }
}
```

### Pipeline Stages Explained

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐
│ Checkout │→ │  Build   │→ │   Test   │→ │  Stage   │→ │  Deploy    │
│   Code   │  │ Compile  │  │  Unit &  │  │  to Dev/ │  │ Production │
│  Lint    │  │ Package  │  │  Integ.  │  │ Staging  │  │ (Approval) │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └────────────┘
```

---

## Jenkins Pipeline Types

### 1. Declarative Pipeline (Recommended)
Structured, opinionated syntax. Easier to read and validate.

```groovy
pipeline {
    agent any
    stages {
        stage('Hello') {
            steps {
                echo 'Hello World'
            }
        }
    }
}
```

### 2. Scripted Pipeline (Advanced)
Full Groovy power, more flexible but more complex.

```groovy
node {
    stage('Hello') {
        echo 'Hello World'
    }
}
```

### 3. Multibranch Pipeline
Automatically creates a pipeline per branch. Ideal for GitFlow.

```
repository/
├── main          → Pipeline auto-created
├── develop       → Pipeline auto-created
├── feature/login → Pipeline auto-created
└── Jenkinsfile   (shared pipeline definition)
```

### 4. Pipeline from SCM
Pipeline defined in a `Jenkinsfile` in the repository — the standard approach.

---

## The Software Delivery Lifecycle with CI/CD

```
┌──────────────────────────────────────────────────────────────────────┐
│                     SOFTWARE DELIVERY LIFECYCLE                      │
├──────────┬───────────┬───────────┬───────────┬────────────┬──────────┤
│  PLAN    │   CODE    │   BUILD   │   TEST    │  RELEASE   │ MONITOR  │
│          │           │           │           │            │          │
│ Jira     │ Git       │ Maven     │ JUnit     │ Helm       │Prometheus│
│ Trello   │ GitHub    │ Gradle    │ Selenium  │ ArgoCD     │ Grafana  │
│ Notion   │ GitLab    │ npm       │ SonarQube │ Spinnaker  │ ELK      │
│          │           │ Docker    │ OWASP     │            │ Datadog  │
└──────────┴───────────┴───────────┴───────────┴────────────┴──────────┘
              Jenkins covers BUILD + TEST + RELEASE automation
```

---

## Real-World CI/CD Example

**Scenario:** A Node.js application deployed to AWS EKS.

### The Jenkinsfile

```groovy
pipeline {
    agent { label 'docker' }

    environment {
        IMAGE_NAME = "myorg/myapp"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        AWS_REGION = "us-east-1"
        ECR_REPO   = "123456789.dkr.ecr.us-east-1.amazonaws.com"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install & Lint') {
            steps {
                sh 'npm ci'
                sh 'npm run lint'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test -- --coverage'
            }
            post {
                always {
                    publishHTML target: [
                        reportDir: 'coverage/lcov-report',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ]
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to ECR') {
            steps {
                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
                    sh "aws ecr get-login-password | docker login --username AWS --password-stdin ${ECR_REPO}"
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ECR_REPO}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker push ${ECR_REPO}/${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh "helm upgrade --install myapp ./helm --set image.tag=${IMAGE_TAG} --namespace staging"
            }
        }

        stage('Approval') {
            steps {
                input message: 'Deploy to Production?', ok: 'Deploy'
            }
        }

        stage('Deploy to Production') {
            steps {
                sh "helm upgrade --install myapp ./helm --set image.tag=${IMAGE_TAG} --namespace production"
            }
        }
    }

    post {
        success {
            slackSend color: 'good', message: "Build ${env.BUILD_NUMBER} deployed to production!"
        }
        failure {
            slackSend color: 'danger', message: "Build ${env.BUILD_NUMBER} FAILED!"
        }
    }
}
```

### What This Pipeline Does

| Stage | Action |
|-------|--------|
| Checkout | Clone source code |
| Install & Lint | `npm ci` + ESLint |
| Test | Jest unit tests + coverage |
| Build Docker Image | `docker build` |
| Push to ECR | Push image to AWS ECR |
| Deploy to Staging | Helm deploy to staging namespace |
| Approval | Human gate for production |
| Deploy to Production | Helm deploy to production namespace |

---

## Summary

| Term | Definition |
|------|-----------|
| **CI** | Auto-build and test on every commit |
| **CD** | Auto-prepare release, human approves production |
| **Continuous Deployment** | Fully automated to production |
| **Pipeline** | Code-defined sequence of automation steps |
| **Jenkinsfile** | The file that defines the pipeline, stored in Git |
| **Stage** | A logical group of steps in a pipeline |
| **Post** | Actions run after stages (success/failure/always) |
