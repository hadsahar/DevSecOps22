# Environments in Jenkins Pipelines

## Table of Contents
1. [What is an Environment in Jenkins?](#what-is-an-environment-in-jenkins)
2. [Deployment Environments Pattern](#deployment-environments-pattern)
3. [Parameterized Environment Targeting](#parameterized-environment-targeting)
4. [Environment-Specific Configuration Files](#environment-specific-configuration-files)
5. [Using Credentials per Environment](#using-credentials-per-environment)
6. [Multi-Environment Pipeline with Approvals](#multi-environment-pipeline-with-approvals)
7. [Environment Promotion Pattern](#environment-promotion-pattern)
8. [Managing Environments with Helm](#managing-environments-with-helm)
9. [Feature Flags and Environment Isolation](#feature-flags-and-environment-isolation)
10. [Complete Multi-Environment Pipeline](#complete-multi-environment-pipeline)

---

## What is an Environment in Jenkins?

In Jenkins, "environment" has two meanings:

1. **Build environment** — the set of environment variables available during a pipeline run (covered in `06-pipeline-syntax-environment-variables.md`)
2. **Deployment environment** — a target infrastructure tier (dev, staging, production)

This tutorial focuses on **managing deployment environments** in Jenkins pipelines.

---

## Deployment Environments Pattern

A typical pipeline deploys through multiple tiers:

```
Code Commit
     │
     ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌────────────┐
│   Dev   │───►│ Staging │───►│   UAT   │───►│ Production │
│ (auto)  │    │ (auto)  │    │(approve)│    │ (approve)  │
└─────────┘    └─────────┘    └─────────┘    └────────────┘
```

Each environment typically has:
- Different **URLs** and **endpoints**
- Different **credentials** and **secrets**
- Different **resource sizing** (replicas, memory)
- Different **approval requirements**

---

## Parameterized Environment Targeting

Allow users to select the target environment at build time:

```groovy
pipeline {
    agent any

    parameters {
        choice(
            name: 'DEPLOY_ENV',
            choices: ['dev', 'staging', 'production'],
            description: 'Target deployment environment'
        )
        string(
            name: 'IMAGE_TAG',
            defaultValue: 'latest',
            description: 'Docker image tag to deploy'
        )
    }

    environment {
        APP_NAME = 'my-service'
    }

    stages {
        stage('Validate Parameters') {
            steps {
                script {
                    if (params.DEPLOY_ENV == 'production' && params.IMAGE_TAG == 'latest') {
                        error("Cannot deploy 'latest' to production. Specify an explicit tag.")
                    }
                }
            }
        }

        stage('Set Environment Config') {
            steps {
                script {
                    switch (params.DEPLOY_ENV) {
                        case 'dev':
                            env.NAMESPACE  = 'development'
                            env.REPLICAS   = '1'
                            env.API_URL    = 'https://dev-api.example.com'
                            env.CRED_ID    = 'dev-kubeconfig'
                            break
                        case 'staging':
                            env.NAMESPACE  = 'staging'
                            env.REPLICAS   = '2'
                            env.API_URL    = 'https://staging-api.example.com'
                            env.CRED_ID    = 'staging-kubeconfig'
                            break
                        case 'production':
                            env.NAMESPACE  = 'production'
                            env.REPLICAS   = '5'
                            env.API_URL    = 'https://api.example.com'
                            env.CRED_ID    = 'prod-kubeconfig'
                            break
                    }
                    echo "Target: ${params.DEPLOY_ENV} | Namespace: ${env.NAMESPACE}"
                }
            }
        }

        stage('Approval for Production') {
            when {
                expression { params.DEPLOY_ENV == 'production' }
            }
            steps {
                input message: "Deploy ${params.IMAGE_TAG} to PRODUCTION?",
                      ok: 'Deploy',
                      submitter: 'release-manager,admin'
            }
        }

        stage('Deploy') {
            steps {
                withKubeConfig([credentialsId: "${env.CRED_ID}"]) {
                    sh """
                        helm upgrade --install ${APP_NAME} ./helm \
                            --namespace ${env.NAMESPACE} \
                            --set image.tag=${params.IMAGE_TAG} \
                            --set replicaCount=${env.REPLICAS} \
                            --set apiUrl=${env.API_URL}
                    """
                }
            }
        }
    }
}
```

---

## Environment-Specific Configuration Files

Store environment configuration in separate files inside your repo:

```
project/
├── src/
├── helm/
├── config/
│   ├── dev.yaml
│   ├── staging.yaml
│   └── production.yaml
└── Jenkinsfile
```

`config/staging.yaml`:
```yaml
replicaCount: 2
image:
  tag: latest
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
ingress:
  host: staging.example.com
```

Load in the pipeline:

```groovy
stage('Deploy') {
    steps {
        script {
            def configFile = "config/${params.DEPLOY_ENV}.yaml"
            sh "helm upgrade --install myapp ./helm -f ${configFile} --set image.tag=${params.IMAGE_TAG}"
        }
    }
}
```

---

## Using Credentials per Environment

Store separate credentials for each environment in Jenkins Credentials Store, then select them dynamically:

```
Jenkins Credentials:
  dev-db-password     → password for dev DB
  staging-db-password → password for staging DB
  prod-db-password    → password for production DB
```

Pipeline:

```groovy
stage('Configure Database') {
    steps {
        script {
            def credId = "${params.DEPLOY_ENV}-db-password"
            withCredentials([string(credentialsId: credId, variable: 'DB_PASS')]) {
                sh "kubectl create secret generic db-secret \
                        --from-literal=password=${DB_PASS} \
                        --namespace ${env.NAMESPACE} \
                        --dry-run=client -o yaml | kubectl apply -f -"
            }
        }
    }
}
```

### Organizing Credentials by Environment (Best Practice)

Use a naming convention:

```
{env}-{service}-{type}

dev-aws-credentials
staging-aws-credentials
prod-aws-credentials

dev-dockerhub-creds
prod-dockerhub-creds
```

---

## Multi-Environment Pipeline with Approvals

```groovy
pipeline {
    agent any

    environment {
        APP   = 'my-api'
        IMAGE = "myregistry/${APP}"
    }

    stages {
        stage('Build & Push') {
            steps {
                script {
                    env.TAG = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                }
                sh "docker build -t ${IMAGE}:${env.TAG} ."
                sh "docker push ${IMAGE}:${env.TAG}"
            }
        }

        stage('Deploy to Dev') {
            steps {
                sh "helm upgrade --install ${APP} ./helm --namespace dev --set image.tag=${env.TAG}"
            }
            post {
                success { echo "Dev deployment successful: ${env.TAG}" }
            }
        }

        stage('Smoke Test Dev') {
            steps {
                sh "curl -f https://dev.example.com/health || exit 1"
            }
        }

        stage('Approve Staging') {
            steps {
                input message: "Promote ${env.TAG} to Staging?", ok: 'Promote'
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh "helm upgrade --install ${APP} ./helm --namespace staging --set image.tag=${env.TAG}"
            }
        }

        stage('Integration Tests') {
            steps {
                sh "npm run test:integration -- --url https://staging.example.com"
            }
        }

        stage('Approve Production') {
            steps {
                input message: "Deploy ${env.TAG} to PRODUCTION?",
                      ok: 'Deploy to Production',
                      submitter: 'release-team'
            }
        }

        stage('Deploy to Production') {
            environment {
                PROD_CREDS = credentials('prod-kubeconfig')
            }
            steps {
                sh "helm upgrade --install ${APP} ./helm --namespace production --set image.tag=${env.TAG} --set replicaCount=5"
            }
        }
    }
}
```

---

## Environment Promotion Pattern

Promotion means pushing the **same immutable artifact** through environments. The image tag never changes — only the target environment changes.

```groovy
pipeline {
    agent any

    parameters {
        string(name: 'PROMOTE_TAG', description: 'Image tag to promote to production')
    }

    stages {
        stage('Verify Image Exists') {
            steps {
                sh "docker pull myregistry/myapp:${params.PROMOTE_TAG}"
            }
        }

        stage('Verify Staging is Healthy') {
            steps {
                sh "curl -f https://staging.example.com/health"
                sh "kubectl rollout status deployment/myapp -n staging"
            }
        }

        stage('Promote to Production') {
            steps {
                input message: "Promote ${params.PROMOTE_TAG} to production?",
                      submitter: 'release-manager'
                sh "helm upgrade myapp ./helm --namespace production --set image.tag=${params.PROMOTE_TAG}"
            }
        }
    }
}
```

---

## Managing Environments with Helm

Helm values files per environment allow clean separation:

```bash
helm upgrade --install myapp ./helm \
  -f helm/values.yaml \
  -f helm/values-${DEPLOY_ENV}.yaml \
  --set image.tag=${IMAGE_TAG}
```

Directory layout:

```
helm/
├── Chart.yaml
├── values.yaml           # Base/shared values
├── values-dev.yaml       # Dev overrides
├── values-staging.yaml   # Staging overrides
└── values-production.yaml # Production overrides
```

---

## Feature Flags and Environment Isolation

Use environment variables to toggle features per environment:

```groovy
stage('Configure Feature Flags') {
    steps {
        script {
            def flags = [
                dev:        [NEW_CHECKOUT: 'true',  DARK_MODE: 'true',  BETA_API: 'true' ],
                staging:    [NEW_CHECKOUT: 'true',  DARK_MODE: 'false', BETA_API: 'false'],
                production: [NEW_CHECKOUT: 'false', DARK_MODE: 'false', BETA_API: 'false']
            ]
            def envFlags = flags[params.DEPLOY_ENV]
            envFlags.each { key, value ->
                sh "kubectl patch configmap feature-flags -n ${env.NAMESPACE} --patch '{\"data\":{\"${key}\":\"${value}\"}}'"
            }
        }
    }
}
```

---

## Complete Multi-Environment Pipeline

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'TARGET_ENV', choices: ['dev', 'staging', 'production'])
        string(name: 'IMAGE_TAG', defaultValue: '')
    }

    environment {
        APP_NAME = 'my-service'
        REGISTRY = 'registry.example.com'
    }

    stages {
        stage('Init') {
            steps {
                script {
                    // Use git SHA if no tag provided
                    if (!params.IMAGE_TAG) {
                        env.DEPLOY_TAG = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    } else {
                        env.DEPLOY_TAG = params.IMAGE_TAG
                    }

                    def cfg = [
                        dev:        [ns: 'development', replicas: '1', url: 'dev.example.com'],
                        staging:    [ns: 'staging',     replicas: '2', url: 'staging.example.com'],
                        production: [ns: 'production',  replicas: '5', url: 'example.com']
                    ]

                    def c = cfg[params.TARGET_ENV]
                    env.NAMESPACE = c.ns
                    env.REPLICAS  = c.replicas
                    env.APP_URL   = c.url

                    echo "Deploying ${env.DEPLOY_TAG} → ${params.TARGET_ENV} (${env.NAMESPACE})"
                }
            }
        }

        stage('Run Tests') {
            when { expression { params.TARGET_ENV != 'production' } }
            steps {
                sh 'mvn test'
            }
            post {
                always { junit '**/target/surefire-reports/*.xml' }
            }
        }

        stage('Approval') {
            when {
                anyOf {
                    expression { params.TARGET_ENV == 'production' }
                    expression { params.TARGET_ENV == 'staging' }
                }
            }
            steps {
                input message: "Deploy to ${params.TARGET_ENV}?", ok: 'Proceed'
            }
        }

        stage('Deploy') {
            steps {
                withKubeConfig([credentialsId: "${params.TARGET_ENV}-kubeconfig"]) {
                    sh """
                        helm upgrade --install ${APP_NAME} ./helm \
                            --namespace ${env.NAMESPACE} \
                            --create-namespace \
                            -f helm/values-${params.TARGET_ENV}.yaml \
                            --set image.repository=${REGISTRY}/${APP_NAME} \
                            --set image.tag=${env.DEPLOY_TAG} \
                            --set replicaCount=${env.REPLICAS}
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                retry(5) {
                    sleep 10
                    sh "curl -f https://${env.APP_URL}/health"
                }
            }
        }
    }

    post {
        success {
            slackSend color: 'good',
                      message: ":white_check_mark: ${APP_NAME} *${env.DEPLOY_TAG}* deployed to *${params.TARGET_ENV}*"
        }
        failure {
            slackSend color: 'danger',
                      message: ":x: Deployment of *${env.DEPLOY_TAG}* to *${params.TARGET_ENV}* FAILED"
        }
    }
}
```

---

## Summary

| Pattern | When to Use |
|---------|------------|
| **Parameterized env choice** | Manual targeted deployments |
| **Branch-based env** | Auto-deploy based on git branch |
| **Config files per env** | Clean separation with Helm values files |
| **Dynamic credential IDs** | Per-env secrets without hardcoding |
| **Approval gates** | Staging → Production promotion |
| **Promotion pipeline** | Deploy exact same artifact through environments |
| **Feature flags** | Progressive rollout per environment |
