# 🏥 CareCompass

**MLOps-Driven Doctor Recommendation System**

CareCompass is a microservices-based healthcare recommendation system that takes patient symptoms and recommends suitable medical specialists and doctors.
The project demonstrates **MLOps + DevOps practices** using **Docker, Kubernetes (Minikube), Ansible, Jenkins, and ELK Stack**.

---

## 🧩 System Architecture

The system consists of **three independent microservices**:

| Service                  | Technology       | Purpose                      | Port   |
| ------------------------ | ---------------- | ---------------------------- | ------ |
| **Bandit Service**       | FastAPI          | Doctor recommendation logic  | `8000` |
| **Speciality Predictor** | Flask            | Predicts medical specialties | `5000` |
| **Frontend**             | FastAPI + Jinja2 | Web UI                       | `5001` |

---

## 📁 Project Structure

```
CareCompass/
│
├── main1/                      # Bandit Service
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── main2/                      # Speciality Predictor
│   ├── server.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── templates/                  # Frontend HTML templates
├── static/                     # Frontend static files
├── app.py                      # Frontend FastAPI app
├── Dockerfile                  # Frontend Dockerfile
├── requirements.txt            # Frontend dependencies
│
├── docker-compose.yml          # Local multi-service execution
│
├── kubernetes/                 # Kubernetes manifests
│   ├── bandit-deployment.yaml
│   ├── speciality-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── services.yaml
│
├── Ansible/
│   ├── deploy.yml              # Ansible deployment playbook
│   ├── hosts.ini               # Inventory
│   └── vault.yml               # Encrypted secrets (Ansible Vault)
│
├── Jenkinsfile
└── README.md
```

---

## 🚀 Option 1: Run Manually (No Docker, No Jenkins)

### Prerequisites

* Python 3.10+
* pip
* virtualenv

### Setup

```bash
git clone https://github.com/aryanvaghasiya/CareCompass
cd CareCompass

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run services (open **3 terminals**)

#### 1️⃣ Bandit Service

```bash
cd main1
uvicorn app.server:app --host 0.0.0.0 --port 8000
```

#### 2️⃣ Speciality Predictor

```bash
cd main2
python server.py
```

#### 3️⃣ Frontend

```bash
cd ..
uvicorn app:app --host 0.0.0.0 --port 5001
```

### Access UI

```
http://localhost:5001
```

---

## 🐳 Option 2: Run Manually Using Docker Compose (Recommended)

### Prerequisites

* Docker
* Docker Compose

### Run all services

```bash
git clone https://github.com/aryanvaghasiya/CareCompass
cd CareCompass
docker compose up --build
```

### Access services

| Service        | URL                                                            |
| -------------- | -------------------------------------------------------------- |
| Frontend       | [http://localhost:5001](http://localhost:5001)                 |
| Bandit API     | [http://localhost:8000/docs](http://localhost:8000/docs)       |
| Speciality API | [http://localhost:8082/predict](http://localhost:8082/predict) |

This option is ideal for **local testing and demos** without Kubernetes.

---

## ☸️ Option 3: Manual Kubernetes Deployment (Minikube + Ansible, No Jenkins)

This option demonstrates **real production-style deployment** without CI/CD automation.

### Prerequisites

* Docker
* Minikube
* kubectl
* Ansible

---

### Step 1: Start Minikube

```bash
minikube start --driver=docker
kubectl get nodes
```

---

### Step 2: Deploy Using Ansible (Manual)

Ansible is used as the **orchestration layer**.
Inside the Ansible playbook:

✔ Kubernetes YAMLs are templated
✔ `kubectl apply` commands are executed
✔ Rollout status is verified using `kubectl rollout status`

Run deployment manually:

```bash
ansible-playbook -i Ansible/hosts.ini Ansible/deploy.yml --ask-vault-pass
```

🔐 You will be prompted for the **Ansible Vault password**.

---

### Step 3: Verify Deployment

```bash
kubectl get pods
kubectl get services
```

To access frontend:

```bash
minikube service frontend --url
```

---

## 🔐 Ansible Vault (Secrets Management)

Sensitive values (image names, tags, secrets) are encrypted using **Ansible Vault**.

Edit vault file:(pass in readme comments)
<!-- ansible vault pass-> aryan --->
```bash
ansible-vault edit Ansible/vault.yml
```

Vault is unlocked during deployment using:

```bash
--ask-vault-pass
```

or via Jenkins credentials (CI/CD mode).

---

## 📊 Logging (ELK Stack)

The project supports centralized logging using:

* **Filebeat**
* **Elasticsearch**
* **Kibana**

Logs from all microservices are collected and visualized in Kibana.

---

## ✅ Key DevOps / MLOps Features

* Microservices architecture
* Dockerized services
* Kubernetes orchestration (Minikube)
* Ansible-based deployments
* Ansible Vault for secret management
* Jenkins CI/CD (optional)
* Centralized logging using ELK Stack

---

## 🧪 End-to-End Workflow

1. User enters symptoms in UI
2. Frontend calls Speciality Predictor
3. Speciality Predictor returns top specialties
4. Frontend calls Bandit Service
5. Bandit Service returns doctor recommendations
6. Results rendered in UI

---

## 👥 Collaborators

* **Aryan Vaghasiya**
* **Areen Vaghasiya**
* **Madhav Patil**

---
