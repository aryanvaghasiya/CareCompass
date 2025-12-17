# 🩺 **CareCompass – MLOps-Driven Doctor Recommendation System**

An end-to-end Machine Learning + MLOps pipeline for automated **doctor recommendation**, built using **Python, ML, Docker, Kubernetes, Jenkins CI/CD, and Ansible**.

---

## 📌 **Project Overview**

CareCompass is an intelligent healthcare recommendation platform that predicts the **best-suited doctor** for a patient based on symptoms, disease descriptions, and doctor attributes.
The project demonstrates a complete **MLOps pipeline** that automates:

* Model training
* Model versioning and packaging
* Dockerization
* CI/CD using Jenkins
* Automated deployment using Kubernetes
* Infrastructure provisioning using Ansible

This repository is ideal for demonstrating practical **MLOps**, **ML model deployment**, and **DevOps integration** in real-world healthcare AI applications.

---

## 🚀 **Key Features**

### 🔹 **Doctor Recommendation System (ML Model)**

* Uses disease data, symptom descriptions, tests, and medication information
* Maps patient symptoms → disease category → doctor specialty
* Ranks doctors based on:

  * Ratings
  * Experience
  * Availability
  * Distance
  * Cost

### 🔹 **Full MLOps Pipeline**

* Continuous Integration (CI) using Jenkins
* Continuous Delivery (CD) with Docker + Kubernetes
* Automated environment setup using Ansible
* Model training scripts with reproducible pipelines

### 🔹 **Containerized Microservices**

* ML model served through a REST API
* Packaged using Docker
* Scalable deployment via Kubernetes

### 🔹 **Data-Driven Predictions**

* Disease–Symptoms dataset
* Doctor attributes and scoring dataset

---
<!-- 
## 📂 **Project Structure**

```
CareCompass/
│── data/
│   ├── updated_dataframe.csv
│   ├── doctors_data_multireward.csv
│
│── model/
│   ├── model_training.py
│   ├── recommender.py
│   ├── preprocess.py
│   ├── trained_model.pkl
│
│── app/
│   ├── app.py (API layer)
│   ├── utils.py
│   ├── templates/
│   ├── static/
│
│── deployment/
│   ├── Dockerfile
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   ├── ansible/
│       ├── playbook.yml
│
│── Jenkinsfile
│── requirements.txt
│── README.md
```

*(Structure may vary slightly depending on repository contents — adjust as needed.)*

--- -->

## 🧠 **Model Training Details**

### **Training Data Features**

#### **Patient/Disease Features (updated_dataframe.csv):**

* disease
* symptoms
* reason/description
* tests & procedures
* medications

#### **Doctor Features (doctors_data_multireward.csv):**

* specialty
* ratings
* experience
* distance from patient
* availability
* cost

These features together power the two-step recommendation logic:

1. Predict correct **doctor specialty** for a symptom/disease
2. Rank doctors within that specialty

---

## 🛠️ **Tech Stack**

### **Machine Learning**

* Python, Jinja2
* Scikit-learn
* Pandas, NumPy
* Torch, Joblib
* FastAPI, Pydantic

### **MLOps**

* Jenkins
* Docker
* Kubernetes (Minikube)
* Ansible

### **Version Control**

* Git + GitHub

---

## 🐳 **Docker Setup**

Build the image:

```bash
//in root directory
docker compose up --build
```

<!-- Run the container:

```bash
docker run -p 5000:5000 carecompass-app
``` -->

Access the app at:

```
http://localhost:5001
```

---

## ☸️ **Deployment**

Using Minikube (Manual Option):

```bash
minikube start
kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl apply -f deployment/kubernetes/service.yaml
```

Check running pods:

```bash
kubectl get pods
```

Expose service:

```bash
minikube service carecompass-service
```

---

## ⚙️ **CI/CD Pipeline (Jenkins)**

The **Jenkinsfile** automates:

1. Pulling latest code from GitHub
2. Creating Python virtual environment
3. Installing dependencies
4. Running model training
5. Building and pushing Docker image
6. Deploying to Kubernetes using Ansible


---

## 📦 **Ansible Deployment Automation**

Steps automated:

* Install Docker, Kubernetes tools, dependencies
* Create and configure cluster nodes
* Apply deployment manifests
* Expose services

Run manually:

```bash
ansible-playbook -i host.ini deploy.yml \
    -e bandit_image=aryanvaghasiya/bandit-service \
    -e speciality_image=aryanvaghasiya/speciality-service \
    -e frontend_image=aryanvaghasiya/frontend-service \
    -e bandit_tag=latest \
    -e speciality_tag=latest \
    -e frontend_tag=latest

```

---

<!-- ## 🧪 **API Usage Example**

POST request:

```json
{
  "symptoms": "fever, headache, dizziness"
}
```

Response:

```json
{
  "specialty": "General Physician",
  "recommended_doctors": [
    {
      "name": "Dr. A Sharma",
      "rating": 4.8,
      "experience": 12,
      "distance": 3.1
    }
  ]
}
```

--- -->

## 📈 **Future Improvements**

* Real-time model monitoring with Prometheus & Grafana
* A/B testing for doctor ranking models
* AutoML pipeline for model retraining
* Real user feedback to re-rank recommendations

---

## 🤝 **Contributors**

IMT2022046 - Aryan Vaghasiya
IMT2022048 - Areen Vaghasiya
IMT2022109 - Madhav S. Patil