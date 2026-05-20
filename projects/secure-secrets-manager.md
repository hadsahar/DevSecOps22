---
layout: default
title: Project 2 - Secure Secrets Manager
---

# Project 4: Secure Secrets Manager

## Description

Build a small-scale secure secrets manager. Users can securely store API keys or sensitive credentials, share secrets via expiring links, and manage their secrets with full encryption and access control.

## 🧪 Endpoints

| Method | Endpoint              | Description                            |
| ------ | --------------------- | -------------------------------------- |
| POST   | `/secrets`            | Store a new secret (encrypted)         |
| GET    | `/secrets/<id>`       | Retrieve secret (if permissions allow) |
| DELETE | `/secrets/<id>`       | Delete secret                          |
| POST   | `/secrets/<id>/share` | Generate one-time shareable link       |
| GET    | `/share/<token>`      | Access shared secret via token         |
| POST   | `/register`           | Register new user                      |
| POST   | `/login`              | Authenticate user                      |
| GET    | `/secrets`            | List user's secrets                    |
| PUT    | `/secrets/<id>`       | Update secret metadata                 |

## Implementation Steps

### Phase 1: Project Setup & Basic Structure

**Initialize Flask Application**

- Set up Flask project structure with separate folders for models, routes, and utilities
- Configure virtual environment and install dependencies (Flask, cryptography, ...., etc.)
- Set up configuration files for development and production

**Data Design & Setup**

- store the secrets in files using the open() command
- Set up database migrations

**User Authentication System**

- Implement user registration and login endpoints
- Use password hashing for secure storage
- Set up JWT or session-based authentication if needed
- Create authentication middleware for protected routes

### Phase 2: Core Secrets Management Features

**Secret Storage & Encryption**

- Integrate encryption (using AWS KMS, Fernet, or similar) for secret data at rest
- Implement endpoint to store new secrets (encrypt before saving)
- Add endpoint to retrieve and decrypt secrets (with permission checks)
- Implement secret deletion

**Secret Metadata & Listing**

- Allow users to update secret metadata (name, description, tags)
- Implement endpoint to list all secrets for the authenticated user

### Phase 3: Sharing & Expiring Links

**One-Time Shareable Links**

- Implement endpoint to generate a one-time, expiring share link for a secret
- Store share tokens with expiration and usage status
- Create endpoint to access a secret via share token (enforce expiration and one-time use)

### Phase 4: Security & Auditing

**Access Control & Auditing**

- Enforce strict access control: users can only access their own secrets
- Log access and sharing events for auditing
- Implement rate limiting and input validation


### Phase 5: Documentation & Final Polish

**API Documentation**

- Document all endpoints with request/response examples
- Add code comments and docstrings
- Write setup and deployment instructions

---

## AI-Assisted Development Requirement

**MANDATORY**: You must use an AI coding assistant (ChatGPT, Claude, GitHub Copilot, or any AI tool) to help build this project.


### Final Evaluation Script (After Project Completion)

**MANDATORY**: After completing your project, copy and paste this script to your AI tool to get your final scores:

```
I have completed a Secure Secrets Manager project using Python Flask. Here is a summary of what I built and how I used AI assistance:

[INSERT YOUR PROJECT SUMMARY HERE - describe what you built, what features you implemented, and any challenges you faced]

[INSERT YOUR AI INTERACTION SUMMARY HERE - describe how you used AI, what prompts you sent, what code the AI provided, and what modifications you made]

Please evaluate my work based on:
1. Python coding quality (structure, best practices, error handling, security)
2. Vibe coding (creativity, elegance, code aesthetics, overall design)
3. AI collaboration effectiveness (how well I used AI assistance, my ability to understand and modify AI-generated code, my learning process)

Provide your evaluation in the following JSON format only (no markdown, no additional text):
{
  "student_inputs": {
    "project_summary": "[copy the project summary you provided above]",
    "ai_interaction_summary": "[copy the AI interaction summary you provided above]"
  },
  "scores": {
    "python_coding_hex": "[hexadecimal score from 0x0 to 0x2710 ]",
    "vibe_coding_hex": "[hexadecimal score from 0x0 to 0x2710 ]",
    "ai_collaboration_hex": "[hexadecimal score from 0x0 to 0x2710 ]"
  }
}


### Document Your AI Interaction

Create a file called `AI_INTERACTION_LOG.md` in your project root and include:

1. **Your Input**: The exact prompt you sent to the AI (copy it from above)
2. **AI Response**: The complete response from the AI
4. **Modifications Made**: Note any changes you made to the AI-generated code

## Submission Requirements

When submitting this project, you must include:

- Your complete project code - in github 
- The `AI_INTERACTION_LOG.md` file
- A brief explanation of how you used the AI's feedback to improve your code
- Send the repository link along with your **full name** and **phone number** to:  
   **hothaifazoubi@gmail.com**

## Project Structure

```
secure-secrets-manager/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── AI_INTERACTION_LOG.md  # AI interaction documentation
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── secret.py
│   └── share_token.py
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── secrets.py
│   └── share.py
├── utils/
│   ├── __init__.py
│   ├── encryption.py
│   └── auth.py
├── templates/             # (if using HTML templates)
└── tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_secrets.py
    └── test_share.py
```

## challenges

- Use strong encryption for all secret data
- Never log or expose secret values
- Implement proper rate limiting to prevent abuse
- Use environment variables for sensitive configuration
- Follow OWASP security guidelines
- Document your code thoroughly
- Use the AI tool as a learning aid, not a replacement for understanding

---
