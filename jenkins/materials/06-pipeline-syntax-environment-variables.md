# Pipeline Syntax with Environment Variables

## Table of Contents
1. [What are Environment Variables?](#what-are-environment-variables)
2. [Declaring Variables with `environment {}`](#declaring-variables-with-environment-)
3. [Scope: Pipeline-Level vs Stage-Level](#scope-pipeline-level-vs-stage-level)
4. [Using Variables in Steps](#using-variables-in-steps)
5. [Dynamic Variables with `script {}`](#dynamic-variables-with-script-)
6. [Override Variables at Stage Level](#override-variables-at-stage-level)
7. [Credentials as Environment Variables](#credentials-as-environment-variables)
8. [Variable Interpolation Rules](#variable-interpolation-rules)
9. [Complete Examples](#complete-examples)

---

## What are Environment Variables?

Environment variables in Jenkins are key-value pairs available during pipeline execution. They come from three sources:

1. **Built-in Jenkins variables** — set automatically (e.g., `BUILD_NUMBER`, `JOB_NAME`)
2. **`environment {}` block** — defined in your Jenkinsfile
3. **OS-level variables** — inherited from the agent shell

---

## Declaring Variables with `environment {}`

```groovy
pipeline {
    agent any

    environment {
        APP_NAME    = 'my-application'
        APP_VERSION = '1.0.0'
        DOCKER_REPO = 'myorg/myapp'
    }

    stages {
        stage('Info') {
            steps {
                echo "App: ${env.APP_NAME}"
                echo "Version: ${env.APP_VERSION}"
                sh "echo Building ${APP_NAME}:${APP_VERSION}"
            }
        }
    }
}
```

> All values in `environment {}` are **strings**. Use `.toInteger()` or `.toBoolean()` for type conversions.

---

## Scope: Pipeline-Level vs Stage-Level

### Pipeline-Level (Global) — available to ALL stages

```groovy
pipeline {
    agent any

    environment {
        GLOBAL_VAR = 'available everywhere'
    }

    stages {
        stage('Stage 1') {
            steps { echo "${env.GLOBAL_VAR}" }  // Works
        }
        stage('Stage 2') {
            steps { echo "${env.GLOBAL_VAR}" }  // Works
        }
    }
}
```

### Stage-Level (Local) — available only within that stage

```groovy
pipeline {
    agent any

    environment {
        BASE_URL = 'https://api.example.com'
    }

    stages {
        stage('Build') {
            environment {
                STAGE_ENV  = 'build'
                BUILD_OPTS = '--no-cache'
            }
            steps {
                echo "${env.STAGE_ENV}"  // Works
                echo "${env.BASE_URL}"   // Works (inherited)
            }
        }
        stage('Deploy') {
            steps {
                // env.STAGE_ENV is NOT available here
                echo "${env.BASE_URL}"   // Works (pipeline-level)
            }
        }
    }
}
```

---

## Using Variables in Steps

### Shell Commands — Two Approaches

```groovy
steps {
    // Double quotes: Groovy interpolation before shell sees it
    sh "echo App: ${env.APP_NAME}"

    // Single quotes: resolved by the shell at runtime
    sh 'echo Build: $BUILD_NUMBER'
}
```

### In Other Step Parameters

```groovy
steps {
    archiveArtifacts artifacts: "${env.ARTIFACT_PATH}/*.jar"
    sh "docker build -t ${env.DOCKER_REPO}:${env.APP_VERSION} ."
}
```

---

## Dynamic Variables with `script {}`

For computed or conditional values, assign to `env.*` inside `script {}`:

```groovy
stages {
    stage('Set Variables') {
        steps {
            script {
                // Capture git short SHA
                env.GIT_SHA = sh(
                    script: 'git rev-parse --short HEAD',
                    returnStdout: true
                ).trim()

                // Compute image tag
                env.IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_SHA}"

                // Conditional based on branch
                env.DEPLOY_ENV = (env.BRANCH_NAME == 'main') ? 'production' : 'staging'

                // Date stamp
                env.BUILD_DATE = sh(
                    script: 'date +%Y%m%d',
                    returnStdout: true
                ).trim()
            }
        }
    }

    stage('Build') {
        steps {
            echo "Image tag : ${env.IMAGE_TAG}"
            echo "Deploy to : ${env.DEPLOY_ENV}"
            sh "docker build -t myapp:${env.IMAGE_TAG} ."
        }
    }
}
```

### Conditional Variable Assignment

```groovy
script {
    def branch = env.BRANCH_NAME ?: 'unknown'

    switch (branch) {
        case 'main':
            env.TARGET_ENV = 'production'
            env.REPLICAS   = '3'
            break
        case 'develop':
            env.TARGET_ENV = 'staging'
            env.REPLICAS   = '1'
            break
        default:
            env.TARGET_ENV = 'dev'
            env.REPLICAS   = '1'
    }
}
```

---

## Override Variables at Stage Level

Stage-level declarations **shadow** pipeline-level ones within that stage only:

```groovy
pipeline {
    agent any

    environment {
        LOG_LEVEL = 'INFO'
        TIMEOUT   = '30'
    }

    stages {
        stage('Normal') {
            steps {
                echo "${env.LOG_LEVEL}" // INFO
                echo "${env.TIMEOUT}"   // 30
            }
        }

        stage('Debug') {
            environment {
                LOG_LEVEL = 'DEBUG'   // overrides for THIS stage
                TIMEOUT   = '120'
            }
            steps {
                echo "${env.LOG_LEVEL}" // DEBUG
                echo "${env.TIMEOUT}"   // 120
            }
        }

        stage('Back to Normal') {
            steps {
                echo "${env.LOG_LEVEL}" // INFO (restored)
                echo "${env.TIMEOUT}"   // 30  (restored)
            }
        }
    }
}
```

---

## Credentials as Environment Variables

Use the `credentials()` helper directly inside `environment {}`:

### Username + Password

```groovy
environment {
    // Auto-creates DOCKER_CREDS_USR and DOCKER_CREDS_PSW
    DOCKER_CREDS = credentials('dockerhub-creds')
}

stages {
    stage('Push') {
        steps {
            sh "docker login -u ${DOCKER_CREDS_USR} -p ${DOCKER_CREDS_PSW}"
        }
    }
}
```

### Secret Text

```groovy
environment {
    SONAR_TOKEN = credentials('sonarqube-token')
    SLACK_URL   = credentials('slack-webhook-url')
}

stages {
    stage('Scan') {
        steps {
            sh "sonar-scanner -Dsonar.login=${SONAR_TOKEN}"
        }
    }
}
```

### SSH Private Key File

```groovy
environment {
    DEPLOY_KEY = credentials('deploy-server-ssh-key')
}

stages {
    stage('Deploy') {
        steps {
            sh '''
                chmod 600 $DEPLOY_KEY
                scp -i $DEPLOY_KEY target/app.jar user@server:/opt/app/
            '''
        }
    }
}
```

---

## Variable Interpolation Rules

This is a **common source of bugs**. Know when Groovy resolves a variable vs. the shell:

| Syntax | Resolved By | Use When |
|--------|-------------|----------|
| `"${env.VAR}"` | Groovy | Embedding Jenkins vars in strings |
| `"${VAR}"` | Groovy | Embedding Groovy local vars |
| `'$VAR'` | Shell | Shell-level env vars |
| `'${VAR}'` | Shell | Shell-level env vars (braces) |

### Security Rule — NEVER do this with user input:

```groovy
// DANGEROUS — injects user input into shell
sh "echo ${params.USER_INPUT}"

// SAFE — pass as shell variable
sh 'echo $USER_INPUT'
// with: environment { USER_INPUT = params.USER_INPUT }
```

---

## Complete Examples

### Example 1: Multi-Environment Deployment Pipeline

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'staging', 'production'], description: 'Target environment')
    }

    environment {
        APP_NAME   = 'myapp'
        REGISTRY   = 'registry.example.com'
        GIT_SHA    = ''
        IMAGE_TAG  = ''
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    env.GIT_SHA   = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_SHA}"
                    echo "Image tag will be: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Build') {
            steps {
                sh "docker build -t ${REGISTRY}/${APP_NAME}:${env.IMAGE_TAG} ."
            }
        }

        stage('Test') {
            environment {
                TEST_ENV = 'ci'
                DB_URL   = 'jdbc:h2:mem:testdb'
            }
            steps {
                sh "docker run --rm -e TEST_ENV=${TEST_ENV} ${REGISTRY}/${APP_NAME}:${env.IMAGE_TAG} npm test"
            }
        }

        stage('Push') {
            environment {
                REGISTRY_CREDS = credentials('registry-credentials')
            }
            steps {
                sh "docker login -u ${REGISTRY_CREDS_USR} -p ${REGISTRY_CREDS_PSW} ${REGISTRY}"
                sh "docker push ${REGISTRY}/${APP_NAME}:${env.IMAGE_TAG}"
            }
        }

        stage('Deploy') {
            environment {
                TARGET = "${params.DEPLOY_ENV}"
            }
            steps {
                echo "Deploying ${env.IMAGE_TAG} to ${TARGET}"
                sh "./scripts/deploy.sh --env ${TARGET} --tag ${env.IMAGE_TAG}"
            }
        }
    }

    post {
        always {
            echo "Build: ${env.IMAGE_TAG} on branch: ${env.BRANCH_NAME}"
        }
    }
}
```

### Example 2: Reading Variables from a Properties File

```groovy
stage('Load Config') {
    steps {
        script {
            def props = readProperties file: 'build.properties'
            env.APP_VERSION = props['version']
            env.APP_GROUP   = props['group']
            env.ARTIFACT_ID = props['artifactId']
            echo "Building ${env.APP_GROUP}:${env.ARTIFACT_ID}:${env.APP_VERSION}"
        }
    }
}
```

`build.properties`:
```properties
version=2.3.1
group=com.example
artifactId=my-service
```

---

## Summary

| Concept | Key Point |
|---------|-----------|
| `environment { KEY = 'value' }` | Declare string variables |
| `env.KEY` | Access in Groovy expressions |
| `$KEY` or `${KEY}` | Access in shell (single-quoted string) |
| Stage-level `environment {}` | Overrides pipeline-level for that stage |
| `credentials('id')` | Inject secret; auto-creates `_USR` / `_PSW` variants |
| `script { env.KEY = ... }` | Set dynamic/computed variables |
| Double-quote strings | Groovy resolves `${env.VAR}` before shell sees it |
| Single-quote strings | Shell resolves `$VAR` at runtime |
