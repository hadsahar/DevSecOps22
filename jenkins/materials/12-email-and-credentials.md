# Email Notifications and Credentials Management in Jenkins

## Table of Contents
1. [Credentials — Overview](#credentials--overview)
2. [Credential Types](#credential-types)
3. [Adding Credentials in the UI](#adding-credentials-in-the-ui)
4. [Using Credentials in Pipelines](#using-credentials-in-pipelines)
5. [Credentials Scopes](#credentials-scopes)
6. [Credentials as Code (JCasC)](#credentials-as-code-jcasc)
7. [Email Notifications — Configuration](#email-notifications--configuration)
8. [Email Extension Plugin (Mailer)](#email-extension-plugin-mailer)
9. [Advanced Email Patterns](#advanced-email-patterns)
10. [Complete Pipeline with Credentials and Email](#complete-pipeline-with-credentials-and-email)

---

## Credentials — Overview

Jenkins Credentials Plugin provides a secure, encrypted store for secrets:

- Passwords, tokens, API keys
- SSH private keys
- TLS certificates
- Docker / registry credentials
- Kubernetes kubeconfig files

Secrets are stored **encrypted** in `$JENKINS_HOME/credentials.xml` using a master key. They are **never printed** in console logs (Jenkins masks them as `****`).

---

## Credential Types

| Type | Use Case | Example |
|------|---------|---------|
| **Secret text** | API tokens, passwords | GitHub token, Slack webhook |
| **Username with password** | Registry logins, DB access | DockerHub, Nexus, database |
| **SSH Username with private key** | SSH agent connections | GitHub SSH, deploy servers |
| **Secret file** | Kubeconfig, `.env`, certificates | K8s config, TLS cert |
| **Certificate** | PKCS#12 keystores | Code signing |
| **AWS Credentials** | AWS access key + secret | ECR, S3, EKS |

---

## Adding Credentials in the UI

1. Go to **Manage Jenkins → Credentials → System → Global credentials (unrestricted)**
2. Click **Add Credentials**
3. Fill in the form:

### Secret Text

```
Kind:   Secret text
Scope:  Global
Secret: ghp_xxxxxxxxxxxxxxxxxxxx
ID:     github-token
Description: GitHub Personal Access Token
```

### Username with Password

```
Kind:     Username with password
Scope:    Global
Username: myuser
Password: mypassword
ID:       dockerhub-creds
Description: DockerHub push credentials
```

### SSH Username with Private Key

```
Kind:        SSH Username with private key
Scope:       Global
Username:    jenkins
Private Key: [Enter directly] — paste private key content
ID:          deploy-server-key
Description: SSH key for production deploy server
```

### Secret File

```
Kind:  Secret file
Scope: Global
File:  [Upload kubeconfig file]
ID:    prod-kubeconfig
Description: Production cluster kubeconfig
```

---

## Using Credentials in Pipelines

### Method 1: `environment {}` with `credentials()`

```groovy
pipeline {
    agent any

    environment {
        // Secret text → single variable
        SONAR_TOKEN = credentials('sonarqube-token')

        // Username/password → creates DOCKER_CREDS_USR and DOCKER_CREDS_PSW
        DOCKER_CREDS = credentials('dockerhub-creds')

        // SSH key → creates file path variable
        DEPLOY_KEY = credentials('deploy-server-key')
    }

    stages {
        stage('Scan') {
            steps {
                sh "sonar-scanner -Dsonar.login=${SONAR_TOKEN}"
            }
        }

        stage('Push') {
            steps {
                sh "docker login -u ${DOCKER_CREDS_USR} -p ${DOCKER_CREDS_PSW}"
                sh "docker push myapp:latest"
            }
        }

        stage('Deploy') {
            steps {
                sh "scp -i ${DEPLOY_KEY} app.jar user@server:/opt/app/"
            }
        }
    }
}
```

### Method 2: `withCredentials()` Block (Recommended for Minimal Scope)

```groovy
stages {
    stage('Deploy') {
        steps {
            // Secret text
            withCredentials([string(credentialsId: 'api-token', variable: 'API_TOKEN')]) {
                sh 'curl -H "Authorization: Bearer $API_TOKEN" https://api.example.com/deploy'
            }

            // Username + password
            withCredentials([usernamePassword(
                credentialsId: 'db-creds',
                usernameVariable: 'DB_USER',
                passwordVariable: 'DB_PASS'
            )]) {
                sh 'mysql -u $DB_USER -p$DB_PASS mydb < migration.sql'
            }

            // Secret file (e.g., kubeconfig)
            withCredentials([file(credentialsId: 'prod-kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                sh 'kubectl --kubeconfig=$KUBECONFIG_FILE get pods -n production'
            }

            // SSH private key
            withCredentials([sshUserPrivateKey(
                credentialsId: 'deploy-key',
                keyFileVariable: 'SSH_KEY',
                usernameVariable: 'SSH_USER'
            )]) {
                sh 'scp -i $SSH_KEY app.jar $SSH_USER@server:/opt/'
            }

            // Multiple credentials at once
            withCredentials([
                string(credentialsId: 'slack-token', variable: 'SLACK_TOKEN'),
                usernamePassword(credentialsId: 'nexus-creds', usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')
            ]) {
                sh './release.sh'
            }
        }
    }
}
```

### Method 3: SSH Agent Plugin

```groovy
stage('Deploy via SSH') {
    steps {
        sshagent(credentials: ['deploy-server-key']) {
            sh 'ssh -o StrictHostKeyChecking=no user@server "cd /app && git pull && restart-service"'
            sh 'scp -r dist/ user@server:/var/www/html/'
        }
    }
}
```

---

## Credentials Scopes

| Scope | Visibility |
|-------|-----------|
| **Global** | Available to all jobs and nodes |
| **System** | Jenkins internals only (not in pipelines) |
| **Folder** | Only jobs inside a specific folder |
| **Item** | Only a specific job |

Use **Folder**-scoped credentials to isolate team secrets:

```
Jenkins Folders:
├── team-frontend/
│   └── Credentials: frontend-deploy-key (Folder scope)
│   └── Jobs: frontend-build, frontend-deploy
└── team-backend/
    └── Credentials: backend-deploy-key (Folder scope)
    └── Jobs: backend-build, backend-deploy
```

---

## Credentials as Code (JCasC)

Use Jenkins Configuration as Code plugin to define credentials in YAML:

```yaml
# jenkins.yaml (JCasC config)
credentials:
  system:
    domainCredentials:
      - domain:
          name: "global"
        credentials:
          - string:
              id: "github-token"
              description: "GitHub PAT"
              secret: "${GITHUB_TOKEN}"    # reads from env var

          - usernamePassword:
              id: "dockerhub-creds"
              description: "DockerHub credentials"
              username: "${DOCKER_USER}"
              password: "${DOCKER_PASS}"

          - basicSSHUserPrivateKey:
              id: "deploy-key"
              description: "Deploy server SSH key"
              username: "jenkins"
              privateKeySource:
                directEntry:
                  privateKey: "${DEPLOY_SSH_KEY}"
```

> **Best Practice:** Never hardcode secrets in JCasC YAML. Always use `${ENV_VAR}` references and inject values from a secret manager (Vault, AWS Secrets Manager) at startup.

---

## Email Notifications — Configuration

### Install Required Plugins

- **Email Extension Plugin** (mailer) — provides `emailext` step
- **Mailer Plugin** — provides basic `mail` step

### Configure SMTP in Jenkins

**Manage Jenkins → System → E-mail Notification** (basic mailer):

```
SMTP server:     smtp.gmail.com
Default user email suffix: @example.com
Use SMTP Authentication: ✅
User Name: jenkins@example.com
Password:  (app password)
Use SSL: ✅
SMTP Port: 465
Reply-To Address: no-reply@example.com
```

Test by clicking **Test configuration by sending test e-mail**.

### Configure Email Extension Plugin

**Manage Jenkins → System → Extended E-mail Notification**:

```
SMTP server:     smtp.gmail.com
SMTP Port:       587
Use SMTP Authentication: ✅
  User Name: jenkins@example.com
  Password:  (app password)
Use TLS:         ✅
Default Recipients: team@example.com
Default Subject:  $PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS
Default Content:  (See examples below)
```

---

## Email Extension Plugin (Mailer)

### Basic `mail` Step

```groovy
post {
    failure {
        mail(
            to:      'team@example.com',
            subject: "Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body:    "Build failed. See: ${env.BUILD_URL}"
        )
    }
}
```

### Advanced `emailext` Step

```groovy
post {
    failure {
        emailext(
            to:           'team@example.com',
            cc:           'manager@example.com',
            replyTo:      'no-reply@example.com',
            subject:      "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body:         '''${SCRIPT, template="groovy-html.template"}''',
            attachLog:    true,
            compressLog:  true,
            mimeType:     'text/html'
        )
    }
    success {
        emailext(
            to:      'team@example.com',
            subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body:    '<p>Build passed. <a href="${BUILD_URL}">View build</a></p>',
            mimeType: 'text/html'
        )
    }
}
```

### Notify Only Committer (culprits)

```groovy
post {
    failure {
        emailext(
            recipientProviders: [
                [$class: 'DevelopersRecipientProvider'],   // People who committed
                [$class: 'CulpritsRecipientProvider'],     // Who broke the build
                [$class: 'RequesterRecipientProvider']     // Who triggered build
            ],
            subject: "You broke the build: ${env.JOB_NAME}",
            body:    'Please check: ${BUILD_URL}'
        )
    }
}
```

### HTML Email Template

```groovy
post {
    always {
        emailext(
            to:      '${DEFAULT_RECIPIENTS}',
            subject: '${DEFAULT_SUBJECT}',
            mimeType: 'text/html',
            body: """
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; }
    .header { background: #336699; color: white; padding: 10px; }
    .success { color: green; font-weight: bold; }
    .failure { color: red; font-weight: bold; }
    table { border-collapse: collapse; width: 100%; }
    td, th { border: 1px solid #ddd; padding: 8px; }
  </style>
</head>
<body>
  <div class="header">
    <h2>Jenkins Build Notification</h2>
  </div>
  <table>
    <tr><th>Job</th><td>${env.JOB_NAME}</td></tr>
    <tr><th>Build</th><td>#${env.BUILD_NUMBER}</td></tr>
    <tr><th>Status</th><td class="${currentBuild.result?.toLowerCase()}">${currentBuild.result}</td></tr>
    <tr><th>Branch</th><td>${env.BRANCH_NAME ?: 'N/A'}</td></tr>
    <tr><th>Duration</th><td>${currentBuild.durationString}</td></tr>
    <tr><th>URL</th><td><a href="${env.BUILD_URL}">${env.BUILD_URL}</a></td></tr>
  </table>
  <p>Console output: <a href="${env.BUILD_URL}console">Click here</a></p>
</body>
</html>
            """.stripIndent()
        )
    }
}
```

---

## Advanced Email Patterns

### Email Only on State Change (Fixed or Broken)

```groovy
post {
    fixed {
        emailext(
            to:      'team@example.com',
            subject: "FIXED: ${env.JOB_NAME} is back to normal",
            body:    "Build #${env.BUILD_NUMBER} passed after failures. ${env.BUILD_URL}"
        )
    }
    regression {
        emailext(
            to:      'team@example.com',
            subject: "REGRESSION: ${env.JOB_NAME} broke!",
            body:    "Build #${env.BUILD_NUMBER} failed after a success. ${env.BUILD_URL}"
        )
    }
}
```

### Email with Test Results Attached

```groovy
post {
    unstable {
        emailext(
            to:           'qa-team@example.com',
            subject:      "Test Failures: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body:         'Test failures detected. See attached report.',
            attachmentsPattern: '**/target/surefire-reports/*.xml',
            attachLog:    false
        )
    }
}
```

### Per-Stage Email on Failure

```groovy
stages {
    stage('Deploy') {
        steps {
            sh './deploy.sh'
        }
        post {
            failure {
                emailext(
                    to:      'ops-team@example.com',
                    subject: "Deployment FAILED: ${env.JOB_NAME}",
                    body:    "Deployment step failed in build #${env.BUILD_NUMBER}. ${env.BUILD_URL}"
                )
            }
        }
    }
}
```

---

## Complete Pipeline with Credentials and Email

```groovy
pipeline {
    agent any

    environment {
        APP_NAME     = 'payment-service'
        REGISTRY     = 'registry.example.com'
        TEAM_EMAIL   = 'payments-team@example.com'
        DOCKER_CREDS = credentials('registry-credentials')
        SONAR_TOKEN  = credentials('sonarqube-token')
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Test') {
            steps {
                sh 'mvn test -B'
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
                failure {
                    emailext(
                        to:      "${TEAM_EMAIL}",
                        subject: "Tests FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body:    "Unit tests failed. See ${env.BUILD_URL}",
                        attachLog: true
                    )
                }
            }
        }

        stage('Code Quality') {
            steps {
                sh "sonar-scanner -Dsonar.login=${SONAR_TOKEN} -Dsonar.projectKey=${APP_NAME}"
            }
        }

        stage('Build & Push Image') {
            steps {
                sh "docker build -t ${REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER} ."
                sh "docker login -u ${DOCKER_CREDS_USR} -p ${DOCKER_CREDS_PSW} ${REGISTRY}"
                sh "docker push ${REGISTRY}/${APP_NAME}:${env.BUILD_NUMBER}"
            }
        }

        stage('Deploy to Staging') {
            steps {
                withCredentials([file(credentialsId: 'staging-kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        helm upgrade --install ${APP_NAME} ./helm \
                            --namespace staging \
                            --set image.tag=${env.BUILD_NUMBER} \
                            --kubeconfig=$KUBECONFIG
                    """
                }
            }
        }

        stage('Approve & Deploy to Production') {
            when { branch 'main' }
            steps {
                input message: "Deploy ${env.BUILD_NUMBER} to production?", ok: 'Deploy'
                withCredentials([file(credentialsId: 'prod-kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        helm upgrade --install ${APP_NAME} ./helm \
                            --namespace production \
                            --set image.tag=${env.BUILD_NUMBER} \
                            --kubeconfig=$KUBECONFIG
                    """
                }
            }
        }
    }

    post {
        success {
            emailext(
                to:       "${TEAM_EMAIL}",
                subject:  "SUCCESS: ${APP_NAME} #${env.BUILD_NUMBER} deployed",
                mimeType: 'text/html',
                body:     """
                    <p>Build <strong>#${env.BUILD_NUMBER}</strong> of <strong>${APP_NAME}</strong> 
                    deployed successfully.</p>
                    <p>Branch: ${env.BRANCH_NAME}</p>
                    <p><a href="${env.BUILD_URL}">View Build</a></p>
                """
            )
        }
        failure {
            emailext(
                to:        "${TEAM_EMAIL}",
                subject:   "FAILED: ${APP_NAME} #${env.BUILD_NUMBER}",
                body:      "Build failed. See: ${env.BUILD_URL}console",
                attachLog: true
            )
        }
        fixed {
            emailext(
                to:      "${TEAM_EMAIL}",
                subject: "FIXED: ${APP_NAME} build is back to normal",
                body:    "Build #${env.BUILD_NUMBER} is passing again."
            )
        }
        cleanup {
            cleanWs()
        }
    }
}
```

---

## Summary

| Topic | Key Point |
|-------|-----------|
| **Credential types** | Secret text, user/pass, SSH key, secret file |
| **`credentials()` in `environment {}`** | Creates `_USR` / `_PSW` variants automatically |
| **`withCredentials()`** | Tightly scoped — prefer this over global env |
| **`sshagent()`** | Cleanest way to use SSH keys in pipeline |
| **Credential scopes** | Use Folder scope to isolate team secrets |
| **JCasC credentials** | Reference env vars with `${VAR}` — never hardcode |
| **`mail` step** | Simple, basic email notification |
| **`emailext` step** | HTML, attachments, recipient providers, templates |
| **`fixed` / `regression`** | Notify on state change, not every build |
