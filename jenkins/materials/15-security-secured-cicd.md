# Security in Jenkins — Building a Secured CI/CD Pipeline

## Table of Contents
1. [CI/CD Security Threat Model](#cicd-security-threat-model)
2. [Jenkins Authentication](#jenkins-authentication)
3. [Jenkins Authorization (RBAC)](#jenkins-authorization-rbac)
4. [Securing the Controller](#securing-the-controller)
5. [Securing Agents](#securing-agents)
6. [Secrets and Credentials Security](#secrets-and-credentials-security)
7. [Securing the Pipeline Code](#securing-the-pipeline-code)
8. [Supply Chain Security (SBOM, Signing)](#supply-chain-security-sbom-signing)
9. [Static Analysis and SAST](#static-analysis-and-sast)
10. [Dependency Vulnerability Scanning](#dependency-vulnerability-scanning)
11. [Container Image Security](#container-image-security)
12. [Infrastructure Security Scanning](#infrastructure-security-scanning)
13. [Audit Logging](#audit-logging)
14. [Network Security](#network-security)
15. [Complete Secured CI/CD Pipeline](#complete-secured-cicd-pipeline)

---

## CI/CD Security Threat Model

The CI/CD pipeline is a **high-value target** — it has access to:
- Source code and intellectual property
- Build artifacts and signing keys
- Production credentials and kubeconfigs
- Cloud account permissions (ECR, S3, EKS)

### Common Attack Vectors

| Threat | Description | Mitigation |
|--------|-------------|-----------|
| **Credential theft** | Stolen tokens in logs or files | Mask secrets, use credential store |
| **Dependency confusion** | Malicious package replaces internal one | Pin versions, use private registry |
| **Compromised Jenkinsfile** | Attacker adds malicious stage | Protected branches, PR review |
| **Plugin vulnerability** | Outdated plugin with CVE | Regular updates, minimal plugins |
| **Agent compromise** | Build agent running malware | Ephemeral agents, network isolation |
| **Supply chain attack** | Malicious code in dependency | SBOM, Sigstore, hash verification |
| **Privilege escalation** | Developer accesses prod creds | RBAC, folder scoping |
| **Secret leakage** | Password printed in logs | Jenkins secret masking + code review |

---

## Jenkins Authentication

### 1. Disable "Allow users to sign up"

```
Manage Jenkins → Security → Authentication
  Security Realm: Jenkins' own user database
  ✅ Allow users to sign up: UNCHECK THIS
```

### 2. Use External Identity Provider (Recommended)

#### LDAP / Active Directory

```
Manage Jenkins → Security → Authentication
  Security Realm: LDAP
    Server: ldap://ldap.company.internal:389
    Root DN: dc=company,dc=internal
    User search base: ou=users
    User search filter: uid={0}
    Manager DN: cn=jenkins,ou=service-accounts,...
    Manager Password: (stored as Jenkins secret)
```

#### GitHub OAuth

```
Manage Jenkins → Security → Authentication
  Security Realm: GitHub Authentication Plugin
    GitHub Web URI: https://github.com
    Client ID: <OAuth App client ID>
    Client Secret: <OAuth App client secret>  ← store as Jenkins secret
```

#### SAML / SSO (Okta, Azure AD)

Install **SAML Plugin** and configure your IdP metadata URL.

### 3. Enforce Strong Password Policy

For the built-in user database:
- Minimum 12 characters
- Require complexity
- Rotate every 90 days
- Use MFA (via SAML/OIDC IdP)

### 4. Disable the Default Admin Account

After LDAP/SSO is configured and your admin account works, disable or delete the default `admin` user:

```
Manage Jenkins → Users → admin → Disable
```

---

## Jenkins Authorization (RBAC)

### Install Role-Based Authorization Strategy Plugin

**Manage Jenkins → Plugins → Role-based Authorization Strategy**

### Enable RBAC

```
Manage Jenkins → Security → Authorization
  Role-Based Strategy
```

### Define Global Roles

**Manage Jenkins → Security → Manage and Assign Roles**

| Role | Permissions |
|------|-------------|
| `admin` | Everything |
| `developer` | Job/Read, Job/Build, Job/Cancel, View/Read |
| `viewer` | Job/Read, View/Read |
| `release-manager` | Job/Read, Job/Build, Run/Replay, Run/Delete |

### Define Folder/Project Roles

Give teams access only to their own folders:

```
Pattern: team-payments/.*
  Role: payments-developer
  Permissions: Job/Build, Job/Read, Job/Workspace, Job/Cancel
```

```
Pattern: team-frontend/.*
  Role: frontend-developer
  Permissions: Job/Build, Job/Read, Job/Workspace
```

### Principle of Least Privilege

```
Global role: viewer  (everyone can view)
Folder role: developer  (assigned per team)
Specific role: release-manager  (assigned per prod pipeline)
```

Never give all developers `Overall/Administer`.

---

## Securing the Controller

### Disable CLI via HTTP

The Jenkins CLI over HTTP is a historical attack vector:

```
Manage Jenkins → Security → CLI
  ✅ Disable CLI over Remoting
```

Or set system property:

```bash
JAVA_OPTS="-Djenkins.CLI.disabled=true"
```

### Enable CSRF Protection

```
Manage Jenkins → Security
  ✅ Prevent Cross Site Request Forgery exploits
  Crumb Algorithm: Default Crumb Issuer
```

### Disable Groovy Sandbox Escape

Configure **Script Security Plugin** to require admin approval for all scripts:

```
Manage Jenkins → Security
  ✅ Enable Agent → Controller Access Control
```

### Keep Jenkins Updated

```bash
# Check for Jenkins core updates
http://your-jenkins/updateCenter/

# Update via CLI
java -jar jenkins-cli.jar -s http://jenkins:8080 \
  -auth admin:token \
  safe-restart
```

### Run Jenkins Behind a Reverse Proxy with TLS

Never expose Jenkins directly. Use nginx or Traefik:

```nginx
server {
    listen 443 ssl;
    server_name jenkins.example.com;

    ssl_certificate     /etc/ssl/certs/jenkins.crt;
    ssl_certificate_key /etc/ssl/private/jenkins.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-XSS-Protection "1; mode=block";

    location / {
        proxy_pass         http://localhost:8080;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name jenkins.example.com;
    return 301 https://$host$request_uri;
}
```

---

## Securing Agents

### Use Ephemeral Agents (Docker/Kubernetes)

Ephemeral agents are destroyed after each build — no persistent attack surface.

```groovy
agent {
    kubernetes {
        yaml '''
            apiVersion: v1
            kind: Pod
            spec:
              automountServiceAccountToken: false  # No K8s API access by default
              containers:
              - name: build
                image: maven:3.9-eclipse-temurin-17
                securityContext:
                  runAsNonRoot: true
                  runAsUser: 1000
                  readOnlyRootFilesystem: true
                  allowPrivilegeEscalation: false
        '''
    }
}
```

### Restrict Agent-to-Controller Access

```
Manage Jenkins → Security → Agent → Controller Security
  ✅ Enable Agent → Controller Access Control
```

Add rules to whitelist only the file operations agents are allowed:

```
Allow: /var/jenkins_home/workspace/   (read/write)
Deny: /var/jenkins_home/secrets/      (no agent access)
Deny: /var/jenkins_home/credentials.xml
```

### Network Isolation for Agents

- Agents should NOT have internet access by default
- Route all external traffic through a proxy or allowlist
- Agents should only communicate with the Controller on port 50000 (JNLP) or 22 (SSH)

---

## Secrets and Credentials Security

### Never Store Secrets in Code

```groovy
// CRITICAL VULNERABILITY — never do this
def password = "mySecret123!"
sh "mysql -u admin -p${password} mydb"

// Correct approach
withCredentials([string(credentialsId: 'db-password', variable: 'DB_PASS')]) {
    sh 'mysql -u admin -p$DB_PASS mydb'
}
```

### Mask Secrets in Logs

Jenkins automatically masks credentials from `withCredentials()`. For custom secrets:

```groovy
script {
    def secret = 'my-secret-value'
    // Tell Jenkins to mask this value
    sh "echo ::add-mask::${secret}"
    wrap([$class: 'MaskPasswordsBuildWrapper',
          varPasswordPairs: [[password: secret, var: 'MASKED_SECRET']]]) {
        echo "The secret is: ${MASKED_SECRET}"  // prints "The secret is: ****"
    }
}
```

### Integrate with HashiCorp Vault

```groovy
stage('Fetch Secrets from Vault') {
    steps {
        withVault(
            configuration: [
                vaultUrl: 'https://vault.example.com',
                vaultCredentialId: 'vault-approle',
                engineVersion: 2
            ],
            vaultSecrets: [
                [path: 'secret/prod/myapp',
                 secretValues: [
                     [envVar: 'DB_PASSWORD', vaultKey: 'db_password'],
                     [envVar: 'API_TOKEN',   vaultKey: 'api_token']
                 ]]
            ]
        ) {
            sh './deploy.sh'
        }
    }
}
```

### Short-Lived Credentials (OIDC)

Use OIDC federation with AWS, GCP, Azure to get **temporary credentials** instead of long-lived keys:

```groovy
stage('AWS via OIDC') {
    steps {
        withCredentials([[$class: 'WebIdentityTokenCredentialBinding',
                          credentialsId: 'aws-oidc-role',
                          variable: 'AWS_WEB_IDENTITY_TOKEN_FILE']]) {
            sh 'aws sts assume-role-with-web-identity ...'
        }
    }
}
```

---

## Securing the Pipeline Code

### Protect the Main Branch

In GitHub/GitLab:
- Require pull requests before merging to `main`
- Require at least 1 approval
- Require status checks to pass (Jenkins CI)
- Do NOT allow bypassing

This prevents attackers from injecting code into the Jenkinsfile directly.

### Validate Jenkinsfile Syntax in PRs

```groovy
// Separate validation pipeline triggered on PR
pipeline {
    agent any
    stages {
        stage('Lint Jenkinsfile') {
            steps {
                sh '''
                    java -jar jenkins-cli.jar \
                        -s http://jenkins:8080 \
                        -auth $JENKINS_USER:$JENKINS_TOKEN \
                        declarative-linter < Jenkinsfile
                '''
            }
        }
    }
}
```

### Use Script Security Sandbox

Declarative pipelines run inside the sandbox by default. Scripted pipelines require approval for unsafe operations:

```
Manage Jenkins → Script Approval
  Review and approve new Groovy method signatures
```

### Restrict `input` Step to Authorized Users

```groovy
stage('Deploy to Production') {
    steps {
        input message: 'Approve production deployment?',
              ok: 'Deploy',
              submitter: 'release-manager,admin'   // Only these users can approve
    }
}
```

---

## Supply Chain Security (SBOM, Signing)

### Generate a Software Bill of Materials (SBOM)

```groovy
stage('Generate SBOM') {
    steps {
        sh 'syft packages dir:. -o spdx-json > sbom.json'
        archiveArtifacts artifacts: 'sbom.json', fingerprint: true
    }
}
```

### Sign Docker Images with Cosign (Sigstore)

```groovy
stage('Sign Image') {
    steps {
        withCredentials([string(credentialsId: 'cosign-key', variable: 'COSIGN_KEY')]) {
            sh '''
                echo "$COSIGN_KEY" > cosign.key
                cosign sign --key cosign.key \
                    registry.example.com/myapp:${BUILD_NUMBER}
                rm cosign.key
            '''
        }
    }
}

stage('Verify Signature Before Deploy') {
    steps {
        sh '''
            cosign verify \
                --certificate-identity "jenkins@ci.example.com" \
                --certificate-oidc-issuer "https://jenkins.example.com" \
                registry.example.com/myapp:${BUILD_NUMBER}
        '''
    }
}
```

### Verify Checksums of Downloaded Binaries

```groovy
stage('Download and Verify') {
    steps {
        sh '''
            curl -LO https://example.com/tool-v1.0.tar.gz
            curl -LO https://example.com/tool-v1.0.tar.gz.sha256
            sha256sum -c tool-v1.0.tar.gz.sha256
        '''
    }
}
```

---

## Static Analysis and SAST

### SonarQube Integration

```groovy
stage('SAST — SonarQube') {
    steps {
        withSonarQubeEnv('SonarQube') {
            sh 'mvn sonar:sonar -Dsonar.projectKey=my-app'
        }
    }
    post {
        always {
            timeout(time: 10, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: true
            }
        }
    }
}
```

Configure **Quality Gates** in SonarQube to fail the build if:
- Code coverage < 80%
- New critical issues > 0
- Security hotspots unreviewed

### Semgrep for Custom Security Rules

```groovy
stage('SAST — Semgrep') {
    agent { docker { image 'returntocorp/semgrep' } }
    steps {
        sh '''
            semgrep --config=auto \
                    --config=p/jenkins \
                    --config=p/secrets \
                    --json --output=semgrep-report.json \
                    --error \
                    .
        '''
    }
    post {
        always {
            archiveArtifacts artifacts: 'semgrep-report.json', allowEmptyArchive: true
        }
    }
}
```

---

## Dependency Vulnerability Scanning

### OWASP Dependency Check

```groovy
stage('Dependency Vulnerability Scan') {
    steps {
        dependencyCheck(
            additionalArguments: '--project myapp --scan . --format HTML --format JSON',
            odcInstallation: 'OWASP Dependency Check'
        )
    }
    post {
        always {
            dependencyCheckPublisher pattern: 'dependency-check-report.xml'
        }
        unstable {
            error 'Vulnerabilities found — see dependency check report'
        }
    }
}
```

### Trivy for Container and Filesystem Scanning

```groovy
stage('Trivy Scan') {
    steps {
        sh '''
            trivy image --exit-code 1 \
                        --severity HIGH,CRITICAL \
                        --format table \
                        myapp:${BUILD_NUMBER}
        '''
    }
    post {
        always {
            sh 'trivy image --format json --output trivy-report.json myapp:${BUILD_NUMBER} || true'
            archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
        }
    }
}
```

### Snyk Integration

```groovy
stage('Snyk Security Scan') {
    steps {
        snykSecurity(
            snykInstallation: 'snyk@latest',
            snykTokenId: 'snyk-token',
            failOnIssues: true,
            severity: 'high'
        )
    }
}
```

---

## Container Image Security

### Use Minimal Base Images

```dockerfile
# Bad — huge attack surface
FROM ubuntu:latest
RUN apt install -y openjdk-17-jdk

# Good — minimal distroless image
FROM gcr.io/distroless/java17-debian12
COPY target/app.jar /app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

### Run Containers as Non-Root

```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

### Set Kubernetes SecurityContext

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
```

---

## Infrastructure Security Scanning

### Scan Terraform with tfsec / Checkov

```groovy
stage('IaC Security Scan') {
    agent { docker { image 'bridgecrew/checkov:latest' } }
    steps {
        sh 'checkov -d ./terraform --framework terraform --output cli --output junitxml > checkov-report.xml || true'
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'checkov-report.xml'
        }
    }
}
```

### Scan Kubernetes Manifests with kube-score / kubesec

```groovy
stage('K8s Manifest Security') {
    steps {
        sh 'kubesec scan helm/templates/*.yaml > kubesec-report.json'
        sh 'kube-score score helm/templates/*.yaml || true'
    }
    post {
        always {
            archiveArtifacts artifacts: 'kubesec-report.json', allowEmptyArchive: true
        }
    }
}
```

---

## Audit Logging

### Install Audit Trail Plugin

```
Manage Jenkins → Plugins → Audit Trail
```

Configure:

```
Manage Jenkins → System → Audit Trail
  Log location: /var/log/jenkins/audit.log
  Log file size: 100 MB
  Log file count: 5
```

This logs:
- Login/logout events
- Job configuration changes
- Job builds triggered (by whom)
- Credential access
- System configuration changes

### Ship Logs to SIEM

```bash
# Example: ship audit.log to ELK / Splunk via filebeat
filebeat.inputs:
- type: log
  paths:
    - /var/log/jenkins/audit.log
  tags: ["jenkins", "audit"]

output.logstash:
  hosts: ["logstash.example.com:5044"]
```

---

## Network Security

### Allow Only Necessary Ports

| Port | Service | Expose To |
|------|---------|-----------|
| 443 (HTTPS) | Jenkins UI via proxy | Developers, VPN |
| 50000 | JNLP agent port | Internal agents only |
| 8080 | Direct Jenkins | BLOCK externally — proxy only |
| 22 | SSH to agents | Controller only |

### Use Kubernetes NetworkPolicy for Agent Pods

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: jenkins-agent-policy
  namespace: jenkins
spec:
  podSelector:
    matchLabels:
      jenkins: agent
  ingress:
    - from:
      - podSelector:
          matchLabels:
            app: jenkins-controller
      ports:
        - port: 50000
  egress:
    - to:
      - podSelector:
          matchLabels:
            app: jenkins-controller
    - to:   # Allow internet for pulling deps
      - ipBlock:
          cidr: 0.0.0.0/0
          except:
            - 10.0.0.0/8
            - 192.168.0.0/16
      ports:
        - port: 443
        - port: 80
```

---

## Complete Secured CI/CD Pipeline

```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  automountServiceAccountToken: false
                  securityContext:
                    runAsNonRoot: true
                    runAsUser: 1000
                  containers:
                  - name: jnlp
                    image: jenkins/inbound-agent:latest
                  - name: build
                    image: maven:3.9-eclipse-temurin-17
                    command: ["sleep"]
                    args: ["infinity"]
                    securityContext:
                      allowPrivilegeEscalation: false
                      readOnlyRootFilesystem: false
                  - name: trivy
                    image: aquasec/trivy:latest
                    command: ["sleep"]
                    args: ["infinity"]
            '''
        }
    }

    options {
        timeout(time: 60, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '30'))
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        APP_NAME   = 'my-service'
        REGISTRY   = '123456789.dkr.ecr.us-east-1.amazonaws.com'
        IMAGE_TAG  = "${env.BUILD_NUMBER}-${env.GIT_COMMIT?.take(7) ?: 'unknown'}"
        AWS_REGION = 'us-east-1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    currentBuild.displayName = "#${env.BUILD_NUMBER} | ${env.BRANCH_NAME} | ${env.GIT_COMMIT?.take(7)}"
                }
            }
        }

        stage('Security Gates') {
            parallel {
                stage('Dependency Scan (OWASP)') {
                    steps {
                        container('build') {
                            sh 'mvn dependency-check:check -B'
                        }
                    }
                    post {
                        always {
                            dependencyCheckPublisher pattern: 'target/dependency-check-report.xml'
                        }
                    }
                }

                stage('SAST (Semgrep)') {
                    steps {
                        sh 'semgrep --config=auto --error --json --output=semgrep.json . || true'
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'semgrep.json', allowEmptyArchive: true
                        }
                    }
                }

                stage('Secret Detection') {
                    steps {
                        sh 'git secrets --scan || true'
                        sh 'trufflehog filesystem . --only-verified --json > trufflehog.json || true'
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'trufflehog.json', allowEmptyArchive: true
                        }
                    }
                }
            }
        }

        stage('Build & Unit Test') {
            steps {
                container('build') {
                    sh 'mvn clean package -B'
                }
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }

        stage('Code Quality Gate') {
            steps {
                container('build') {
                    withSonarQubeEnv('SonarQube') {
                        sh "mvn sonar:sonar -Dsonar.projectKey=${APP_NAME}"
                    }
                }
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${REGISTRY}/${APP_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Container Scan (Trivy)') {
            steps {
                container('trivy') {
                    sh """
                        trivy image \
                            --exit-code 1 \
                            --severity HIGH,CRITICAL \
                            --format table \
                            ${REGISTRY}/${APP_NAME}:${IMAGE_TAG}
                    """
                }
            }
            post {
                always {
                    container('trivy') {
                        sh "trivy image --format json --output trivy-report.json ${REGISTRY}/${APP_NAME}:${IMAGE_TAG} || true"
                    }
                    archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Generate SBOM') {
            steps {
                sh "syft packages ${REGISTRY}/${APP_NAME}:${IMAGE_TAG} -o spdx-json > sbom.json"
                archiveArtifacts artifacts: 'sbom.json', fingerprint: true
            }
        }

        stage('Push to Registry') {
            when {
                anyOf { branch 'main'; branch 'release/*' }
            }
            steps {
                withAWS(credentials: 'aws-production', region: "${AWS_REGION}") {
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${REGISTRY}"
                    sh "docker push ${REGISTRY}/${APP_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Sign Image') {
            when {
                anyOf { branch 'main'; branch 'release/*' }
            }
            steps {
                withCredentials([string(credentialsId: 'cosign-private-key', variable: 'COSIGN_PRIVATE_KEY')]) {
                    sh '''
                        echo "$COSIGN_PRIVATE_KEY" > cosign.key
                        cosign sign --key cosign.key ${REGISTRY}/${APP_NAME}:${IMAGE_TAG}
                        shred -u cosign.key
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            when { branch 'main' }
            steps {
                withAWS(credentials: 'aws-production', region: "${AWS_REGION}") {
                    sh "aws eks update-kubeconfig --region ${AWS_REGION} --name staging-cluster"
                    sh """
                        helm upgrade --install ${APP_NAME} ./helm \
                            --namespace staging \
                            --set image.repository=${REGISTRY}/${APP_NAME} \
                            --set image.tag=${IMAGE_TAG} \
                            --wait
                    """
                }
            }
        }

        stage('Approve Production') {
            when { branch 'main' }
            steps {
                input message: "Deploy ${IMAGE_TAG} to PRODUCTION?",
                      ok: 'Deploy',
                      submitter: 'release-manager,admin'
            }
        }

        stage('Deploy to Production') {
            when { branch 'main' }
            steps {
                withAWS(credentials: 'aws-production', region: "${AWS_REGION}") {
                    sh "aws eks update-kubeconfig --region ${AWS_REGION} --name production-cluster"
                    sh """
                        helm upgrade --install ${APP_NAME} ./helm \
                            --namespace production \
                            --set image.repository=${REGISTRY}/${APP_NAME} \
                            --set image.tag=${IMAGE_TAG} \
                            --set replicaCount=5 \
                            --wait
                    """
                }
            }
            post {
                failure {
                    sh "helm rollback ${APP_NAME} 0 --namespace production"
                    slackSend color: 'danger', message: ":sos: Production rollback triggered for ${APP_NAME} ${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        success {
            slackSend color: 'good',
                      message: ":white_check_mark: *${APP_NAME}* `${IMAGE_TAG}` deployed to production"
        }
        failure {
            mail to: 'security@example.com,devops@example.com',
                 subject: "FAILED: ${APP_NAME} CI/CD Pipeline",
                 body:    "Build ${IMAGE_TAG} failed. See: ${env.BUILD_URL}"
        }
        always {
            sh "docker rmi ${REGISTRY}/${APP_NAME}:${IMAGE_TAG} || true"
        }
        cleanup {
            cleanWs()
        }
    }
}
```

---

## Security Checklist Summary

### Jenkins Platform
- [ ] Jenkins running behind HTTPS reverse proxy
- [ ] Default admin account disabled / renamed
- [ ] LDAP/SSO authentication configured
- [ ] RBAC with role-based authorization
- [ ] Controller executors set to 0
- [ ] CSRF protection enabled
- [ ] CLI over remoting disabled
- [ ] Audit Trail plugin installed and logging
- [ ] Plugins kept updated
- [ ] JCasC for reproducible configuration

### Pipeline Security
- [ ] No hardcoded secrets in Jenkinsfile
- [ ] All secrets in Jenkins Credentials store
- [ ] `withCredentials()` for minimum-scope secret access
- [ ] Protected `main` branch with required PR reviews
- [ ] Jenkinsfile syntax validation in PRs
- [ ] `input` steps restricted to authorized submitters
- [ ] Shell injection prevention (env vars, not interpolation)

### Build Security
- [ ] SAST scan (SonarQube, Semgrep)
- [ ] Dependency vulnerability scan (OWASP, Snyk, Trivy)
- [ ] Secret detection in code (truffleHog, git-secrets)
- [ ] Container image scan before push
- [ ] IaC scan (Checkov, tfsec)
- [ ] SBOM generated and archived
- [ ] Image signed with Cosign/Notary

### Agent Security
- [ ] Ephemeral agents (Docker/Kubernetes)
- [ ] Non-root container execution
- [ ] Read-only filesystems where possible
- [ ] Network policies restricting agent traffic
- [ ] Agent-to-Controller access control enabled

### Cloud / Deployment
- [ ] IAM roles / IRSA instead of long-lived access keys
- [ ] Credentials scoped to minimum required permissions
- [ ] Automatic rollback on deployment failure
- [ ] Production deployments require manual approval
