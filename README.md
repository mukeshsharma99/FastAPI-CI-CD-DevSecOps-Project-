# 🚀 FastAPI CI/CD | DevOps & DevSecOps Project

A **production-style FastAPI backend** with **PostgreSQL, Docker, GitHub Actions CI/CD, and AWS cloud deployment**. The project demonstrates automated testing, containerization, secure AWS authentication, and automated deployment to EC2.

## 🛠️ Tech Stack

**Backend:** Python, FastAPI, REST API, SQLAlchemy  
**Database:** PostgreSQL  
**Testing:** Pytest  
**Containerization:** Docker  
**CI/CD:** GitHub Actions  
**AWS:** EC2, ECR, SSM, IAM  
**Security:** GitHub OIDC, IAM Roles  
**Server:** Uvicorn, Linux

## 🏗️ Architecture

```text
Developer
   │
   ▼
GitHub Repository
   │
   ▼
GitHub Actions
   │
   ├── Pytest
   ├── Docker Build
   ├── AWS OIDC Authentication
   └── Push Image → Amazon ECR
                         │
                         ▼
                    AWS SSM
                         │
                         ▼
                    Amazon EC2
                         │
                         ▼
                 FastAPI Container
                         │
                         ▼
                    PostgreSQL
```

## ⚡ Key Features

- Developed **RESTful CRUD APIs** using FastAPI and Python
- Integrated **PostgreSQL** using SQLAlchemy
- Containerized application using **Docker**
- Implemented automated **CI/CD pipeline with GitHub Actions**
- Automated **Pytest** execution before deployment
- Built and pushed Docker images to **Amazon ECR**
- Automated EC2 deployment using **AWS Systems Manager (SSM)**
- Implemented **GitHub OIDC + AWS IAM Roles** for secure authentication
- Added automated **post-deployment health checks**
- Eliminated manual SSH-based deployment from the CI/CD workflow

## 🔄 CI/CD Pipeline

```text
Code Push
   ↓
GitHub Actions
   ↓
Automated Tests
   ↓
Docker Build
   ↓
Amazon ECR
   ↓
AWS SSM
   ↓
Amazon EC2
   ↓
Container Deployment
   ↓
Health Check ✅
```

**Deployment is performed automatically only after successful tests.**

## 🧪 Testing

```bash
pytest
```

Current test coverage includes:

- API health checks
- CRUD operations
- User validation
- Duplicate email handling
- Error handling

**Test Result: 9 passed ✅**

## 📡 API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application status |
| GET | `/health` | Health check |
| GET | `/users` | Get users |
| POST | `/users` | Create user |
| GET | `/users/{id}` | Get user |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |

Interactive API documentation:

```text
http://<EC2-PUBLIC-IP>:8000/docs
```

## 🔐 DevSecOps Practices

- **AWS IAM** for least-privilege access
- **GitHub OIDC** instead of long-lived AWS credentials
- Automated testing before deployment
- Containerized deployment
- AWS SSM instead of direct SSH deployment

## 📈 Future Improvements

- Trivy container vulnerability scanning
- SonarQube code quality analysis
- AWS Secrets Manager
- CloudWatch monitoring and logging
- HTTPS with Application Load Balancer
- Terraform Infrastructure as Code
- Automated rollback

## 👨‍💻 Author

**Mukesh Sharma**

**Software Developer | Backend | DevOps | Cloud | AI/ML**

GitHub: [mukeshsharma99](https://github.com/mukeshsharma99)