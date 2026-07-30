# Pipeline Syntax Basics

## Table of Contents
1. [Declarative vs Scripted Pipeline](#declarative-vs-scripted-pipeline)
2. [Jenkinsfile Structure](#jenkinsfile-structure)
3. [The `pipeline` Block](#the-pipeline-block)
4. [The `agent` Directive](#the-agent-directive)
5. [The `stages` and `stage` Blocks](#the-stages-and-stage-blocks)
6. [The `steps` Block](#the-steps-block)
7. [Common Built-in Steps](#common-built-in-steps)
8. [The `when` Directive (Conditional Stages)](#the-when-directive-conditional-stages)
9. [Parallel Stages](#parallel-stages)
10. [The `options` Directive](#the-options-directive)
11. [The `triggers` Directive](#the-triggers-directive)
12. [The `parameters` Directive](#the-parameters-directive)
13. [Pipeline Snippet Generator](#pipeline-snippet-generator)
14. [Complete Working Examples](#complete-working-examples)

---

## Declarative vs Scripted Pipeline

Jenkins supports two pipeline syntaxes:

### Declarative Pipeline
- **Recommended** for most use cases
- Structured, opinionated, easier to read and lint
- Must start with `pipeline {}`
- Validated by Jenkins before execution

### Scripted Pipeline
- Full Groovy code in a `node {}` block
- More flexible but harder to maintain
- No built-in syntax validation

```groovy
// Declarative
pipeline {
    agent any
    stages {
        stage('Hello') {
            steps {
                echo 'Hello, World!'
            }
        }
    }
}

// Scripted equivalent
node {
    stage('Hello') {
        echo 'Hello, World!'
    }
}
```

> **Rule:** Always use **Declarative** unless you have a specific reason to use Scripted.

---

## Jenkinsfile Structure

A `Jenkinsfile` is a text file placed at the **root of your Git repository**.

```
my-project/
├── src/
├── tests/
├── Dockerfile
├── pom.xml
└── Jenkinsfile         ← pipeline definition lives here
```

The top-level structure of a Declarative Jenkinsfile:

```groovy
pipeline {
    agent { ... }           // Where to run
    options { ... }         // Job-level options
    triggers { ... }        // When to trigger
    parameters { ... }      // Input parameters
    environment { ... }     // Environment variables
    stages {                // Build stages
        stage('name') {
            when { ... }    // Conditional execution
            steps { ... }   // Build steps
            post { ... }    // Stage-level post actions
        }
    }
    post { ... }            // Pipeline-level post actions
}
```

---

## The `pipeline` Block

Everything lives inside the top-level `pipeline {}` block. There must be exactly one.

```groovy
pipeline {
    // Everything here
}
```

---

## The `agent` Directive

The `agent` tells Jenkins **where** to run the pipeline or a specific stage.

### `agent any`
Run on any available agent:

```groovy
agent any
```

### `agent none`
No global agent — each stage must define its own:

```groovy
agent none

stages {
    stage('Build') {
        agent { label 'linux' }
        steps { sh 'make' }
    }
    stage('Deploy') {
        agent { label 'deploy-server' }
        steps { sh './deploy.sh' }
    }
}
```

### `agent { label '...' }`
Run on agents matching a label:

```groovy
agent { label 'linux && docker' }
```

### `agent { docker '...' }`
Run inside a Docker container:

```groovy
agent {
    docker {
        image 'maven:3.9-eclipse-temurin-17'
        args  '-v $HOME/.m2:/root/.m2'
    }
}
```

### `agent { kubernetes { ... } }`
Run in a Kubernetes pod (covered in detail in the Agents tutorial):

```groovy
agent {
    kubernetes {
        yaml '''
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: maven
                image: maven:3.9
        '''
    }
}
```

---

## The `stages` and `stage` Blocks

`stages` is a container for one or more `stage` blocks. Stages run **sequentially** by default.

```groovy
stages {
    stage('Checkout') {
        steps {
            checkout scm
        }
    }

    stage('Build') {
        steps {
            sh 'mvn clean package'
        }
    }

    stage('Test') {
        steps {
            sh 'mvn test'
        }
    }

    stage('Deploy') {
        steps {
            sh './deploy.sh'
        }
    }
}
```

### Stage Nesting (Sequential Stages Inside a Stage)

```groovy
stage('Integration Tests') {
    stages {
        stage('Start Services') {
            steps { sh 'docker-compose up -d' }
        }
        stage('Run Tests') {
            steps { sh 'npm run test:integration' }
        }
        stage('Stop Services') {
            steps { sh 'docker-compose down' }
        }
    }
}
```

---

## The `steps` Block

`steps` contains the actual commands to execute within a stage.

```groovy
steps {
    sh 'echo hello'         // Shell command (Linux/Mac)
    bat 'echo hello'        // Batch command (Windows)
    echo 'A message'        // Print to console
    sleep 5                 // Wait 5 seconds
    dir('/tmp/work') {      // Change directory
        sh 'ls -la'
    }
}
```

### Step Execution Order
Steps within `steps {}` run **sequentially** unless you use `parallel`.

---

## Common Built-in Steps

### `sh` — Run Shell Commands

```groovy
steps {
    sh 'mvn clean package'

    // Multi-line
    sh '''
        echo "Starting build..."
        mvn clean package -DskipTests
        echo "Build finished"
    '''

    // Capture output
    script {
        def output = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
        echo "Commit: ${output}"
    }
}
```

### `checkout` — Checkout Source Code

```groovy
steps {
    // Checkout current pipeline's SCM
    checkout scm

    // Checkout a specific repo
    checkout([
        $class: 'GitSCM',
        branches: [[name: '*/main']],
        userRemoteConfigs: [[
            url: 'https://github.com/org/repo.git',
            credentialsId: 'github-token'
        ]]
    ])
}
```

### `withCredentials` — Inject Secrets

```groovy
steps {
    withCredentials([
        usernamePassword(
            credentialsId: 'my-db-creds',
            usernameVariable: 'DB_USER',
            passwordVariable: 'DB_PASS'
        )
    ]) {
        sh 'mysql -u $DB_USER -p$DB_PASS mydb < schema.sql'
    }
}
```

### `archiveArtifacts` — Save Build Output

```groovy
steps {
    archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
}
```

### `stash` / `unstash` — Pass Files Between Stages

```groovy
// In stage 'Build'
stash name: 'build-output', includes: 'target/*.jar'

// In stage 'Deploy' (different agent)
unstash 'build-output'
sh 'cp target/*.jar /deployments/'
```

### `input` — Manual Approval Gate

```groovy
stage('Approve Production Deploy') {
    steps {
        input message: 'Deploy to production?',
              ok: 'Yes, deploy!',
              submitter: 'admin,release-team'
    }
}
```

### `timeout` — Prevent Stuck Builds

```groovy
steps {
    timeout(time: 10, unit: 'MINUTES') {
        sh './slow-test.sh'
    }
}
```

### `retry` — Retry Flaky Steps

```groovy
steps {
    retry(3) {
        sh './flaky-network-step.sh'
    }
}
```

### `script` — Embed Groovy Logic in Declarative

```groovy
steps {
    script {
        def list = ['a', 'b', 'c']
        for (item in list) {
            echo "Processing: ${item}"
        }
    }
}
```

---

## The `when` Directive (Conditional Stages)

`when` allows a stage to run **only when a condition is true**.

### Run Only on Main Branch

```groovy
stage('Deploy to Production') {
    when {
        branch 'main'
    }
    steps {
        sh './deploy-prod.sh'
    }
}
```

### Run Only When a File Changed

```groovy
stage('Build Frontend') {
    when {
        changeset 'frontend/**'
    }
    steps {
        sh 'npm run build'
    }
}
```

### Run Only When Environment Variable Matches

```groovy
stage('Run Integration Tests') {
    when {
        environment name: 'RUN_INTEGRATION', value: 'true'
    }
    steps {
        sh 'npm run test:integration'
    }
}
```

### Combine Conditions

```groovy
stage('Deploy') {
    when {
        allOf {
            branch 'main'
            not { changeRequest() }
        }
    }
    steps {
        sh './deploy.sh'
    }
}
```

### Available `when` Conditions

| Condition | Description |
|-----------|-------------|
| `branch 'name'` | Branch name matches |
| `tag 'pattern'` | Tag matches pattern |
| `environment name: 'X', value: 'Y'` | Env var matches |
| `expression { ... }` | Groovy expression returns true |
| `changeRequest()` | Is a pull request |
| `changeset 'path'` | Files in path changed |
| `buildingTag()` | Build triggered by a tag |
| `not { ... }` | Negates a condition |
| `allOf { ... }` | All conditions true (AND) |
| `anyOf { ... }` | Any condition true (OR) |

---

## Parallel Stages

Run multiple stages at the same time to reduce total build time:

```groovy
stage('Tests') {
    parallel {
        stage('Unit Tests') {
            agent { label 'linux' }
            steps {
                sh 'mvn test -Dtest=UnitTests'
            }
        }
        stage('Integration Tests') {
            agent { label 'linux' }
            steps {
                sh 'mvn test -Dtest=IntegrationTests'
            }
        }
        stage('Security Scan') {
            agent { label 'linux' }
            steps {
                sh 'dependency-check.sh'
            }
        }
    }
}
```

### Fail Fast in Parallel

```groovy
stage('Parallel Tests') {
    failFast true
    parallel {
        stage('Fast Test') {
            steps { sh 'fast-test.sh' }
        }
        stage('Slow Test') {
            steps { sh 'slow-test.sh' }
        }
    }
}
```

> `failFast true` stops all parallel branches if one fails.

---

## The `options` Directive

`options` configures job-level behaviour:

```groovy
options {
    timeout(time: 1, unit: 'HOURS')         // Kill if takes > 1 hour
    retry(2)                                 // Retry whole pipeline 2x on failure
    disableConcurrentBuilds()                // Only one run at a time
    buildDiscarder(logRotator(             
        numToKeepStr: '10',
        daysToKeepStr: '14'
    ))
    timestamps()                             // Add timestamps to logs
    ansiColor('xterm')                       // Colored console output
    skipStagesAfterUnstable()                // Skip remaining stages if unstable
}
```

---

## The `triggers` Directive

Defines when the pipeline should automatically run:

```groovy
triggers {
    // Poll SCM every 5 minutes
    pollSCM('H/5 * * * *')

    // Run on cron schedule (every day at 2 AM)
    cron('H 2 * * *')

    // Triggered by upstream job
    upstream(upstreamProjects: 'other-job', threshold: hudson.model.Result.SUCCESS)
}
```

> **Prefer webhooks** over `pollSCM` for faster, more efficient triggers.

---

## The `parameters` Directive

Define input parameters that users (or other jobs) can pass at build time:

```groovy
parameters {
    string(name: 'DEPLOY_ENV', defaultValue: 'staging', description: 'Target environment')
    choice(name: 'REGION', choices: ['us-east-1', 'eu-west-1', 'ap-southeast-1'], description: 'AWS region')
    booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run test suite?')
    password(name: 'API_KEY', defaultValue: '', description: 'API key')
    text(name: 'RELEASE_NOTES', defaultValue: '', description: 'Release notes')
}
```

Use parameters in steps:

```groovy
stage('Deploy') {
    steps {
        echo "Deploying to: ${params.DEPLOY_ENV}"
        sh "./deploy.sh --env ${params.DEPLOY_ENV} --region ${params.REGION}"
    }
}
```

---

## Pipeline Snippet Generator

Jenkins has a built-in tool to help generate pipeline syntax:

1. Go to **Any Pipeline Job → Pipeline Syntax**
2. Select a step from the **Sample Step** dropdown
3. Fill in the form fields
4. Click **Generate Pipeline Script**

URL: `http://your-jenkins/pipeline-syntax`

Also useful:
- **Declarative Directive Generator:** `http://your-jenkins/directive-generator`
- **Global Variable Reference:** `http://your-jenkins/pipeline-syntax/globals`

---

## Complete Working Examples

### Example 1: Node.js App

```groovy
pipeline {
    agent { label 'nodejs' }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    triggers {
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh 'npm ci'
            }
        }

        stage('Lint & Test') {
            parallel {
                stage('Lint') {
                    steps {
                        sh 'npm run lint'
                    }
                }
                stage('Unit Tests') {
                    steps {
                        sh 'npm test'
                    }
                }
            }
        }

        stage('Build') {
            steps {
                sh 'npm run build'
                archiveArtifacts artifacts: 'dist/**', fingerprint: true
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                sh './scripts/deploy.sh'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            echo 'Build failed!'
        }
    }
}
```

### Example 2: Docker Build & Push

```groovy
pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag')
    }

    stages {
        stage('Build Image') {
            steps {
                sh "docker build -t myapp:${params.IMAGE_TAG} ."
            }
        }

        stage('Test Image') {
            steps {
                sh "docker run --rm myapp:${params.IMAGE_TAG} npm test"
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "docker login -u $DOCKER_USER -p $DOCKER_PASS"
                    sh "docker push myapp:${params.IMAGE_TAG}"
                }
            }
        }
    }
}
```

---

## Summary

| Directive | Purpose |
|-----------|---------|
| `pipeline {}` | Top-level container |
| `agent` | Where to run |
| `stages / stage` | Logical build phases |
| `steps` | Actual commands |
| `when` | Conditional stage execution |
| `parallel` | Run stages concurrently |
| `options` | Job-level configuration |
| `triggers` | Automated trigger schedule |
| `parameters` | Parameterized builds |
| `script {}` | Groovy code inside declarative |
