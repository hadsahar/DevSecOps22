# Post Actions in Jenkins Pipelines

## Table of Contents
1. [What are Post Actions?](#what-are-post-actions)
2. [Post Conditions](#post-conditions)
3. [Pipeline-Level Post vs Stage-Level Post](#pipeline-level-post-vs-stage-level-post)
4. [Common Post Steps](#common-post-steps)
5. [Execution Order and Behavior](#execution-order-and-behavior)
6. [Real-World Post Action Patterns](#real-world-post-action-patterns)
7. [Complete Example](#complete-example)

---

## What are Post Actions?

The `post {}` block defines steps that run **after** a pipeline or stage completes — regardless of whether the build passed or failed. Post actions are used for:

- Sending notifications (email, Slack)
- Publishing test reports and artifacts
- Cleaning up workspaces or Docker containers
- Updating deployment dashboards
- Rolling back on failure

---

## Post Conditions

Jenkins provides **7 post conditions** that map to different build outcomes:

```groovy
post {
    always    { }   // Runs no matter what
    success   { }   // Runs only on SUCCESS
    failure   { }   // Runs only on FAILURE
    unstable  { }   // Runs when build is UNSTABLE (e.g. test failures)
    aborted   { }   // Runs when build was manually aborted
    changed   { }   // Runs when build result CHANGED from previous
    fixed     { }   // Runs when build is SUCCESS after a FAILURE
    regression{ }   // Runs when build fails after a SUCCESS
    cleanup   { }   // ALWAYS runs LAST, even after other post blocks
}
```

### Condition Summary Table

| Condition | Triggers When |
|-----------|--------------|
| `always` | Every build, regardless of result |
| `success` | Build result is SUCCESS |
| `failure` | Build result is FAILURE |
| `unstable` | Build result is UNSTABLE (test failures recorded) |
| `aborted` | Build was cancelled by a user |
| `changed` | Current result differs from previous build |
| `fixed` | Build is SUCCESS but previous was FAILURE/UNSTABLE |
| `regression` | Build is FAILURE but previous was SUCCESS |
| `cleanup` | Always runs last (use for guaranteed cleanup) |

---

## Pipeline-Level Post vs Stage-Level Post

### Pipeline-Level `post`
Runs after **all stages** complete:

```groovy
pipeline {
    agent any

    stages {
        stage('Build') { steps { sh 'mvn package' } }
        stage('Test')  { steps { sh 'mvn test'    } }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'All stages passed!'
        }
        failure {
            echo 'Pipeline failed. Check console output.'
        }
    }
}
```

### Stage-Level `post`
Runs after a **specific stage** completes:

```groovy
stages {
    stage('Test') {
        steps {
            sh 'mvn test'
        }
        post {
            always {
                // Publish JUnit results even if tests fail
                junit '**/target/surefire-reports/*.xml'
            }
            failure {
                echo 'Tests failed in this stage!'
            }
        }
    }

    stage('Build Docker') {
        steps {
            sh 'docker build -t myapp .'
        }
        post {
            failure {
                sh 'docker system prune -f'
            }
        }
    }
}
```

---

## Common Post Steps

### Publish JUnit Test Results

```groovy
post {
    always {
        junit allowEmptyResults: true,
              testResults: '**/target/surefire-reports/*.xml'
    }
}
```

### Archive Artifacts

```groovy
post {
    success {
        archiveArtifacts artifacts: 'target/*.jar',
                         fingerprint: true,
                         allowEmptyArchive: false
    }
}
```

### Publish HTML Report

```groovy
post {
    always {
        publishHTML([
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'target/site/jacoco',
            reportFiles: 'index.html',
            reportName: 'Code Coverage'
        ])
    }
}
```

### Clean Workspace

```groovy
post {
    always {
        cleanWs()                         // Requires Workspace Cleanup plugin
        // or:
        deleteDir()                       // Delete workspace directory
    }
}
```

### Send Email

```groovy
post {
    failure {
        mail to: 'team@example.com',
             subject: "Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
             body: """
                Build failed!
                Job: ${env.JOB_NAME}
                Build: ${env.BUILD_NUMBER}
                URL: ${env.BUILD_URL}
             """
    }
    fixed {
        mail to: 'team@example.com',
             subject: "Build FIXED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
             body: "The build is back to normal."
    }
}
```

### Slack Notification

```groovy
post {
    success {
        slackSend(
            color: 'good',
            message: ":white_check_mark: *${env.JOB_NAME}* #${env.BUILD_NUMBER} passed\n${env.BUILD_URL}"
        )
    }
    failure {
        slackSend(
            color: 'danger',
            message: ":x: *${env.JOB_NAME}* #${env.BUILD_NUMBER} FAILED\n${env.BUILD_URL}"
        )
    }
}
```

### Docker Cleanup

```groovy
post {
    always {
        sh 'docker-compose down --volumes --remove-orphans || true'
        sh 'docker image prune -f || true'
    }
}
```

### Record Build Status to Git (GitHub/GitLab)

```groovy
post {
    success {
        githubNotify context: 'ci/jenkins', status: 'SUCCESS', description: 'Build passed'
    }
    failure {
        githubNotify context: 'ci/jenkins', status: 'FAILURE', description: 'Build failed'
    }
}
```

---

## Execution Order and Behavior

### Order of Execution

```
Pipeline runs all stages
        │
        ▼
Stage-level post blocks (in order of stages)
        │
        ▼
Pipeline-level post blocks
        │
        ▼
cleanup block (always last)
```

### Multiple Conditions — All Matching Ones Run

```groovy
post {
    always  { echo 'Always runs' }
    success { echo 'Also runs on success' }
    changed { echo 'Also runs if result changed' }
}
```

If the build succeeds AND the result changed from last time, **all three** run.

### `always` vs `cleanup`

```groovy
post {
    always {
        echo 'Runs before cleanup'
        // Could still fail here
    }
    cleanup {
        echo 'Runs last, even if always{} fails'
        cleanWs()   // Guaranteed cleanup
    }
}
```

> Use `cleanup` for actions that must run no matter what — it is the most reliable condition.

### Build Result After Post

If a step inside `post {}` fails, it can change the overall build result. Use `|| true` or `catchError` to prevent post-step failures from masking the real result:

```groovy
post {
    always {
        // Don't let cleanup failure mask build result
        sh 'docker-compose down || true'
        sh 'rm -rf /tmp/build-cache || true'
    }
}
```

---

## Real-World Post Action Patterns

### Pattern 1: Full Notification Strategy

```groovy
post {
    success {
        slackSend color: 'good',
                  message: ":rocket: Deployed ${env.APP_NAME}:${env.IMAGE_TAG} to ${env.TARGET_ENV}"
    }
    failure {
        slackSend color: 'danger',
                  message: ":fire: Build failed for ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        mail to: "${env.TEAM_EMAIL}",
             subject: "FAILED: ${env.JOB_NAME}",
             body: "See: ${env.BUILD_URL}console"
    }
    fixed {
        slackSend color: 'good',
                  message: ":white_check_mark: Build fixed: ${env.JOB_NAME}"
    }
    unstable {
        slackSend color: 'warning',
                  message: ":warning: Unstable build: ${env.JOB_NAME} (test failures)"
    }
}
```

### Pattern 2: Always Collect Reports, Only Archive on Success

```groovy
post {
    always {
        junit allowEmptyResults: true, testResults: '**/test-results/**/*.xml'
        publishHTML([reportDir: 'coverage', reportFiles: 'index.html', reportName: 'Coverage'])
    }
    success {
        archiveArtifacts artifacts: 'dist/**', fingerprint: true
    }
    cleanup {
        cleanWs()
    }
}
```

### Pattern 3: Rollback on Failure

```groovy
stage('Deploy to Production') {
    steps {
        sh "helm upgrade myapp ./helm --set image.tag=${env.IMAGE_TAG}"
    }
    post {
        failure {
            echo 'Deployment failed — rolling back...'
            sh "helm rollback myapp 0"   // 0 = previous release
            slackSend color: 'danger',
                      message: ":sos: Production rollback triggered for ${env.JOB_NAME}"
        }
        success {
            sh "kubectl rollout status deployment/myapp -n production"
        }
    }
}
```

### Pattern 4: Security Scan — Always Report, Fail on Critical

```groovy
stage('OWASP Scan') {
    steps {
        sh 'dependency-check.sh --project myapp --scan ./target'
    }
    post {
        always {
            dependencyCheckPublisher pattern: 'dependency-check-report.xml'
        }
        unstable {
            echo 'Vulnerabilities found — see report for details'
        }
    }
}
```

---

## Complete Example

```groovy
pipeline {
    agent any

    environment {
        APP_NAME  = 'my-service'
        TEAM_EMAIL = 'devteam@example.com'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build') {
            steps { sh 'mvn clean package -DskipTests' }
            post {
                failure {
                    echo 'Build compilation failed!'
                }
            }
        }

        stage('Test') {
            steps { sh 'mvn test' }
            post {
                always {
                    junit testResults: '**/target/surefire-reports/*.xml',
                          allowEmptyResults: true
                }
                unstable {
                    echo 'Some tests failed — marking build unstable'
                }
            }
        }

        stage('Code Quality') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'mvn sonar:sonar'
                }
            }
            post {
                always {
                    publishHTML([
                        reportDir: 'target/site',
                        reportFiles: 'index.html',
                        reportName: 'SonarQube Report'
                    ])
                }
            }
        }

        stage('Docker Build & Push') {
            steps {
                sh "docker build -t ${APP_NAME}:${env.BUILD_NUMBER} ."
                sh "docker push ${APP_NAME}:${env.BUILD_NUMBER}"
            }
            post {
                failure {
                    sh 'docker image prune -f || true'
                }
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps {
                sh "./deploy.sh --tag ${env.BUILD_NUMBER}"
            }
            post {
                failure {
                    sh './rollback.sh'
                    slackSend color: 'danger',
                              message: ":sos: Deployment FAILED and rolled back — ${env.BUILD_URL}"
                }
                success {
                    slackSend color: 'good',
                              message: ":rocket: Successfully deployed ${APP_NAME} #${env.BUILD_NUMBER}"
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'target/*.jar', allowEmptyArchive: true
            echo "Total build duration: ${currentBuild.durationString}"
        }
        failure {
            mail to: "${TEAM_EMAIL}",
                 subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Build failed. See: ${env.BUILD_URL}console"
        }
        fixed {
            mail to: "${TEAM_EMAIL}",
                 subject: "FIXED: ${env.JOB_NAME} is back to normal",
                 body: "Build #${env.BUILD_NUMBER} passed."
        }
        cleanup {
            cleanWs()
        }
    }
}
```

---

## Summary

| Condition | Use For |
|-----------|---------|
| `always` | Reports, logs, metrics |
| `success` | Archive artifacts, deploy notifications |
| `failure` | Alert team, rollback, debug info |
| `unstable` | Test failure warnings |
| `aborted` | Notify when someone cancelled |
| `changed` | Track flaky builds |
| `fixed` | Celebrate recovery |
| `regression` | Alert when stable build breaks |
| `cleanup` | Guaranteed last-step cleanup |
