# Jenkins and AWS Connectivity

## Table of Contents
1. [Overview of Jenkins + AWS](#overview-of-jenkins--aws)
2. [AWS Authentication Methods](#aws-authentication-methods)
3. [Storing AWS Credentials in Jenkins](#storing-aws-credentials-in-jenkins)
4. [Using AWS Credentials in Pipelines](#using-aws-credentials-in-pipelines)
5. [IAM Roles for EC2 / EKS (No Keys Needed)](#iam-roles-for-ec2--eks-no-keys-needed)
6. [Pushing Docker Images to Amazon ECR](#pushing-docker-images-to-amazon-ecr)
7. [Deploying to Amazon EKS](#deploying-to-amazon-eks)
8. [Storing Artifacts in S3](#storing-artifacts-in-s3)
9. [Secrets from AWS Secrets Manager](#secrets-from-aws-secrets-manager)
10. [Dynamic EC2 Agents](#dynamic-ec2-agents)
11. [Complete AWS CI/CD Pipeline](#complete-aws-cicd-pipeline)

---

## Overview of Jenkins + AWS

Jenkins integrates with AWS services across the entire CI/CD workflow:

```
┌──────────────────────────────────────────────────────────────────┐
│                    Jenkins + AWS Integration                     │
├────────────────────┬─────────────────────────────────────────────┤
│  BUILD PHASE       │  Docker image → Amazon ECR                  │
│  TEST PHASE        │  S3 → download test fixtures                │
│  ARTIFACT STORAGE  │  S3 → store JARs, dist bundles             │
│  SECRET MANAGEMENT │  AWS Secrets Manager / Parameter Store      │
│  DEPLOYMENT        │  EKS (kubectl/helm) or ECS or Lambda        │
│  INFRASTRUCTURE    │  CloudFormation / Terraform via CLI         │
│  AGENTS            │  EC2 instances spun up on demand            │
└────────────────────┴─────────────────────────────────────────────┘
```

---

## AWS Authentication Methods

### Method 1: IAM User Access Keys (Simplest — Not Recommended for Production)

Create an IAM user with programmatic access, store the key/secret in Jenkins Credentials.

**IAM → Users → Create User → Attach Policies**

Minimum required policies per use case:
- ECR push: `AmazonEC2ContainerRegistryPowerUser`
- EKS: `AmazonEKSWorkerNodePolicy` + custom policy
- S3: `AmazonS3FullAccess` (or scoped bucket policy)
- Secrets Manager: `SecretsManagerReadWrite`

### Method 2: IAM Role on EC2 (Recommended for Jenkins on EC2)

Attach an IAM Role to the EC2 instance running Jenkins. No keys needed — credentials are fetched from the instance metadata service.

```
EC2 Instance (Jenkins Controller) → IAM Role → Policies
```

### Method 3: IAM Role for Service Account on EKS (Recommended for Jenkins on K8s)

Use IRSA (IAM Roles for Service Accounts) to give the Jenkins pod AWS access without keys.

```bash
# Associate OIDC provider with cluster
eksctl utils associate-iam-oidc-provider \
  --region us-east-1 \
  --cluster my-cluster \
  --approve

# Create IAM service account
eksctl create iamserviceaccount \
  --name jenkins \
  --namespace jenkins \
  --cluster my-cluster \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser \
  --attach-policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess \
  --approve
```

---

## Storing AWS Credentials in Jenkins

### Install AWS Credentials Plugin

**Manage Jenkins → Plugins → Available → Search: "AWS Credentials"**

### Add Credentials

**Manage Jenkins → Credentials → System → Global → Add Credentials**

```
Kind:              AWS Credentials
ID:                aws-production
Description:       AWS Production Account
Access Key ID:     AKIAIOSFODNN7EXAMPLE
Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

---

## Using AWS Credentials in Pipelines

### Using `withAWS()` Step (AWS Steps Plugin)

```groovy
pipeline {
    agent any

    stages {
        stage('AWS Operations') {
            steps {
                withAWS(credentials: 'aws-production', region: 'us-east-1') {
                    sh 'aws sts get-caller-identity'
                    sh 'aws s3 ls'
                    sh 'aws ecr describe-repositories'
                }
            }
        }
    }
}
```

### Using `withCredentials()` for Manual AWS CLI Setup

```groovy
stage('Deploy') {
    steps {
        withCredentials([[
            $class:            'AmazonWebServicesCredentialsBinding',
            credentialsId:     'aws-production',
            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
            secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        ]]) {
            sh '''
                export AWS_DEFAULT_REGION=us-east-1
                aws sts get-caller-identity
                aws s3 sync dist/ s3://my-bucket/app/
            '''
        }
    }
}
```

### AWS Profile from Secret File

```groovy
stage('S3 Upload') {
    steps {
        withCredentials([file(credentialsId: 'aws-credentials-file', variable: 'AWS_CREDS')]) {
            sh '''
                mkdir -p ~/.aws
                cp $AWS_CREDS ~/.aws/credentials
                aws s3 sync . s3://my-bucket/builds/
            '''
        }
    }
}
```

---

## IAM Roles for EC2 / EKS (No Keys Needed)

When Jenkins runs on an EC2 with an IAM role, or on EKS with IRSA, AWS CLI automatically uses instance/pod credentials:

```groovy
pipeline {
    agent any

    stages {
        stage('AWS Without Keys') {
            steps {
                // No credentials block needed — role is assumed automatically
                sh 'aws sts get-caller-identity'
                sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com'
            }
        }
    }
}
```

### Minimum IAM Policy for Jenkins CI/CD

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ECRAccess",
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:PutImage"
      ],
      "Resource": "*"
    },
    {
      "Sid": "S3Artifacts",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::my-ci-artifacts",
        "arn:aws:s3:::my-ci-artifacts/*"
      ]
    },
    {
      "Sid": "EKSAccess",
      "Effect": "Allow",
      "Action": ["eks:DescribeCluster"],
      "Resource": "arn:aws:eks:us-east-1:123456789:cluster/my-cluster"
    }
  ]
}
```

---

## Pushing Docker Images to Amazon ECR

### ECR Login and Push

```groovy
environment {
    AWS_REGION  = 'us-east-1'
    AWS_ACCOUNT = '123456789012'
    ECR_REPO    = "${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    IMAGE_NAME  = 'my-app'
    IMAGE_TAG   = "${env.BUILD_NUMBER}"
}

stages {
    stage('Build Image') {
        steps {
            sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
        }
    }

    stage('Push to ECR') {
        steps {
            withAWS(credentials: 'aws-production', region: "${AWS_REGION}") {
                sh '''
                    aws ecr get-login-password --region $AWS_REGION \
                      | docker login --username AWS --password-stdin $ECR_REPO
                '''
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ECR_REPO}/${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ECR_REPO}/${IMAGE_NAME}:latest"
                sh "docker push ${ECR_REPO}/${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${ECR_REPO}/${IMAGE_NAME}:latest"
            }
        }
    }
}
```

### Create ECR Repository if Not Exists

```groovy
stage('Ensure ECR Repo') {
    steps {
        withAWS(credentials: 'aws-production', region: 'us-east-1') {
            sh '''
                aws ecr describe-repositories --repository-names my-app 2>/dev/null || \
                aws ecr create-repository \
                    --repository-name my-app \
                    --image-scanning-configuration scanOnPush=true \
                    --encryption-configuration encryptionType=AES256
            '''
        }
    }
}
```

---

## Deploying to Amazon EKS

### Step 1 — Update kubeconfig

```groovy
stage('Configure kubectl for EKS') {
    steps {
        withAWS(credentials: 'aws-production', region: 'us-east-1') {
            sh '''
                aws eks update-kubeconfig \
                    --region us-east-1 \
                    --name my-eks-cluster \
                    --alias my-cluster
            '''
        }
    }
}
```

### Step 2 — Deploy with kubectl

```groovy
stage('Deploy to EKS') {
    steps {
        withAWS(credentials: 'aws-production', region: 'us-east-1') {
            sh '''
                aws eks update-kubeconfig --region us-east-1 --name my-cluster
                kubectl set image deployment/my-app \
                    my-app=${ECR_REPO}/my-app:${BUILD_NUMBER} \
                    --namespace production
                kubectl rollout status deployment/my-app -n production --timeout=5m
            '''
        }
    }
}
```

### Step 3 — Deploy with Helm to EKS

```groovy
stage('Helm Deploy to EKS') {
    steps {
        withAWS(credentials: 'aws-production', region: 'us-east-1') {
            sh "aws eks update-kubeconfig --region us-east-1 --name my-cluster"
            sh """
                helm upgrade --install my-app ./helm \
                    --namespace production \
                    --create-namespace \
                    --set image.repository=${ECR_REPO}/my-app \
                    --set image.tag=${IMAGE_TAG} \
                    --set replicaCount=3 \
                    --wait --timeout=5m
            """
        }
    }
}
```

---

## Storing Artifacts in S3

### Upload Build Artifacts

```groovy
stage('Upload Artifacts to S3') {
    steps {
        withAWS(credentials: 'aws-production', region: 'us-east-1') {
            // Upload a single file
            sh """
                aws s3 cp target/app.jar \
                    s3://my-artifacts-bucket/builds/${env.JOB_NAME}/${env.BUILD_NUMBER}/app.jar \
                    --metadata build=${env.BUILD_NUMBER},branch=${env.BRANCH_NAME}
            """

            // Upload a directory
            sh """
                aws s3 sync dist/ \
                    s3://my-artifacts-bucket/frontend/${env.BUILD_NUMBER}/ \
                    --delete
            """

            // Print S3 URL
            echo "Artifact: s3://my-artifacts-bucket/builds/${env.JOB_NAME}/${env.BUILD_NUMBER}/app.jar"
        }
    }
}
```

### Download Artifact for Deployment

```groovy
stage('Download Artifact') {
    steps {
        withAWS(credentials: 'aws-production', region: 'us-east-1') {
            sh """
                aws s3 cp \
                    s3://my-artifacts-bucket/builds/${env.JOB_NAME}/${params.BUILD_TO_DEPLOY}/app.jar \
                    ./app.jar
            """
        }
    }
}
```

### Use S3 Plugin for Jenkins

```groovy
// Using the S3 publisher plugin
post {
    success {
        s3Upload(
            bucket:         'my-ci-artifacts',
            path:           "builds/${env.JOB_NAME}/${env.BUILD_NUMBER}/",
            includePathPattern: 'target/*.jar',
            profileName:    'aws-production'
        )
    }
}
```

---

## Secrets from AWS Secrets Manager

Retrieve secrets at build time instead of storing them in Jenkins:

```groovy
stage('Fetch Secrets') {
    steps {
        withAWS(credentials: 'aws-production', region: 'us-east-1') {
            script {
                // Get a secret JSON and parse it
                def secretJson = sh(
                    script: '''
                        aws secretsmanager get-secret-value \
                            --secret-id prod/myapp/database \
                            --query SecretString \
                            --output text
                    ''',
                    returnStdout: true
                ).trim()

                def secret = readJSON text: secretJson
                env.DB_HOST     = secret.host
                env.DB_PORT     = secret.port
                env.DB_NAME     = secret.dbname
                // Note: do NOT echo passwords!
                env.DB_PASSWORD = secret.password
            }
        }
    }
}
```

### Using AWS SSM Parameter Store

```groovy
stage('Get Config from SSM') {
    steps {
        withAWS(credentials: 'aws-production', region: 'us-east-1') {
            script {
                env.APP_ENV_VAR = sh(
                    script: 'aws ssm get-parameter --name /myapp/prod/api-url --with-decryption --query Parameter.Value --output text',
                    returnStdout: true
                ).trim()
            }
        }
    }
}
```

---

## Dynamic EC2 Agents

The **Amazon EC2 Plugin** provisions EC2 instances as Jenkins agents on demand, terminating them after builds complete.

### Configure EC2 Cloud

**Manage Jenkins → Clouds → New Cloud → Amazon EC2**

```
Name:            ec2-agents
AWS Region:      us-east-1
EC2 Key Pair:    jenkins-agent-key
Instance Type:   t3.medium
AMI ID:          ami-0xxxxxxxxxx (Ubuntu 22.04 with Java pre-installed)
Remote user:     ubuntu
Remote FS root:  /home/ubuntu/jenkins
Labels:          ec2 linux
Max instances:   5
Idle termination: 30 minutes
```

### Use EC2 Agent in Pipeline

```groovy
pipeline {
    agent { label 'ec2 && linux' }

    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }
}
```

---

## Complete AWS CI/CD Pipeline

```groovy
pipeline {
    agent any

    environment {
        AWS_REGION  = 'us-east-1'
        AWS_ACCOUNT = '123456789012'
        ECR_REPO    = "${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        APP_NAME    = 'payment-service'
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        CLUSTER     = 'production-cluster'
        NAMESPACE   = 'production'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Test') {
            steps { sh 'mvn test -B' }
            post {
                always { junit '**/target/surefire-reports/*.xml' }
            }
        }

        stage('Build') {
            steps { sh 'mvn clean package -DskipTests -B' }
        }

        stage('Build & Push to ECR') {
            steps {
                withAWS(credentials: 'aws-production', region: "${AWS_REGION}") {
                    sh '''
                        aws ecr get-login-password --region $AWS_REGION \
                          | docker login --username AWS \
                            --password-stdin $ECR_REPO
                    '''
                    sh "docker build -t ${ECR_REPO}/${APP_NAME}:${IMAGE_TAG} ."
                    sh "docker push ${ECR_REPO}/${APP_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Security Scan') {
            steps {
                withAWS(credentials: 'aws-production', region: "${AWS_REGION}") {
                    sh """
                        aws ecr start-image-scan \
                            --repository-name ${APP_NAME} \
                            --image-id imageTag=${IMAGE_TAG}
                    """
                    sleep 30
                    sh """
                        CRITICAL=\$(aws ecr describe-image-scan-findings \
                            --repository-name ${APP_NAME} \
                            --image-id imageTag=${IMAGE_TAG} \
                            --query 'imageScanFindings.findingSeverityCounts.CRITICAL' \
                            --output text)
                        if [ "\$CRITICAL" != "None" ] && [ "\$CRITICAL" -gt 0 ]; then
                            echo "CRITICAL vulnerabilities found: \$CRITICAL"
                            exit 1
                        fi
                    """
                }
            }
        }

        stage('Upload Artifact to S3') {
            steps {
                withAWS(credentials: 'aws-production', region: "${AWS_REGION}") {
                    sh """
                        aws s3 cp target/${APP_NAME}.jar \
                            s3://my-artifacts/${APP_NAME}/${IMAGE_TAG}/${APP_NAME}.jar
                    """
                }
            }
        }

        stage('Deploy to EKS') {
            when { branch 'main' }
            steps {
                input message: "Deploy ${IMAGE_TAG} to production?", ok: 'Deploy'
                withAWS(credentials: 'aws-production', region: "${AWS_REGION}") {
                    sh "aws eks update-kubeconfig --region ${AWS_REGION} --name ${CLUSTER}"
                    sh """
                        helm upgrade --install ${APP_NAME} ./helm \
                            --namespace ${NAMESPACE} \
                            --set image.repository=${ECR_REPO}/${APP_NAME} \
                            --set image.tag=${IMAGE_TAG} \
                            --wait --timeout=5m
                    """
                    sh "kubectl rollout status deployment/${APP_NAME} -n ${NAMESPACE}"
                }
            }
        }
    }

    post {
        success {
            withAWS(credentials: 'aws-production', region: "${AWS_REGION}") {
                sh """
                    aws sns publish \
                        --topic-arn arn:aws:sns:us-east-1:${AWS_ACCOUNT}:deployments \
                        --message "SUCCESS: ${APP_NAME} ${IMAGE_TAG} deployed to production" \
                        --subject "Jenkins Deploy Success"
                """
            }
        }
        failure {
            mail to: 'team@example.com',
                 subject: "FAILED: ${APP_NAME} deployment",
                 body:    "Build ${IMAGE_TAG} failed. See: ${env.BUILD_URL}"
        }
        cleanup {
            sh 'docker rmi ${ECR_REPO}/${APP_NAME}:${IMAGE_TAG} || true'
            cleanWs()
        }
    }
}
```

---

## Summary

| AWS Service | Jenkins Integration |
|------------|-------------------|
| **IAM** | Credentials (access key/secret) or IAM Role |
| **ECR** | `aws ecr get-login-password` → `docker push` |
| **EKS** | `aws eks update-kubeconfig` → `kubectl` / `helm` |
| **S3** | `aws s3 cp/sync` for artifacts |
| **Secrets Manager** | `aws secretsmanager get-secret-value` |
| **SSM Parameter Store** | `aws ssm get-parameter` |
| **EC2 (agents)** | Amazon EC2 plugin — dynamic agents on demand |
| **SNS** | `aws sns publish` for deployment notifications |
| **Best Auth Method** | IAM Role (EC2/EKS) > AWS Credentials plugin > Hardcoded keys (never) |
