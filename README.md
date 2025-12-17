# MLOPS Recommendation System - CareCompass

## Project Overview

This project implements an intelligent doctor recommendation system that identifies the medical specialty for a given set of symptoms and recommends doctors based on the predicted specialty. The system is designed with a comprehensive DevOps framework, leveraging:

-   **Version Control**: Git and GitHub for source code management.
-   **CI/CD Automation**: Jenkins with a declarative pipeline to automate build, test, Docker image creation, and deployment to Kubernetes.
-   **Containerization**: Docker for packaging application services into portable containers.
-   **Orchestration and Scaling**: Kubernetes (Minikube) for deploying and managing containerized applications.
-   **Monitoring and Logging**: An ELK Stack (Elasticsearch, Logstash, Kibana) for centralized collection, storage, and visualization of application logs.

The core application consists of two key services:

1.  **Specialty Predictor Service**: A Flask-based REST API that takes symptoms as input and predicts the relevant medical specialty.
2.  **Doctor Recommendation Service**: A FastAPI-based service that provides doctor recommendations for a given specialty.

## Features

-   Predict medical specialty based on user symptoms.
-   Recommend doctors for the identified specialty.
-   RESTful APIs for seamless integration.
-   Dockerized services for easy deployment.
-   Automated CI/CD pipeline with Jenkins.
-   Kubernetes deployment with Minikube support.
-   Secure sensitive data management using Ansible Vault (if implemented).
-   Centralized Logging with ELK Stack for real-time monitoring.

---

## Installation and Setup

To set up the entire CareCompass project on your system, follow these comprehensive steps:

### Prerequisites

Ensure you have the following tools installed on your system:

-   **Git**: For cloning the repository.
-   **Python 3.7 or higher**: For running application development and scripts.
-   **Docker**: For building and running containerized applications.
-   **Docker Compose**: Essential for orchestrating multi-container applications locally.
-   **Java Development Kit (JDK) 8 or higher**: Required for Jenkins.
-   **Apache Maven**: Often used for Java-based projects, but useful for Jenkins builds.
-   **Minikube**: For local Kubernetes cluster deployment and testing.
-   **kubectl**: Kubernetes command-line tool.
-   **VS Code** (recommended for development)

### 1. Clone the Repository

Start by cloning the project repository to your local machine:

```bash
git clone <repository-url>
cd CareCompass
```

### 2. Python Environment Setup

Install necessary Python libraries. It's recommended to use a virtual environment.

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

To install additional Python libraries in VS Code (if not using a virtual environment globally):
```bash
python3 -m pip install [library name] --break-system-packages
```

To export all installed libraries and their versions:
```bash
python3 -m pip freeze > requirements.txt
```

### 3. Docker Image Preparation

Ensure Docker is running on your system. The project uses Docker to containerize its services. The `Dockerfile` in the root directory builds the frontend application, while `main1/Dockerfile` and `main2/Dockerfile` build the `bandit` and `specialty` services, respectively.

The Jenkins pipeline will automate the building and pushing of these images to Docker Hub.

### 4. Kubernetes (Minikube) Setup

Minikube is used for deploying the application to a local Kubernetes cluster. The Kubernetes manifest files (`main1/ml-service.yaml` and `main2/ml-service2.yaml`) define the deployments and services for your `bandit` and `specialty` applications within Kubernetes.

1.  **Start Minikube**:
    ```bash
    minikube start
    ```
    *What happens*: This command starts a single-node Kubernetes cluster locally using Minikube.

2.  **Apply Kubernetes Manifests** (These are typically handled by Jenkins in a CI/CD pipeline, but you can apply them manually for local testing):
    ```bash
    kubectl apply -f main1/ml-service.yaml
    kubectl apply -f main2/ml-service2.yaml
    ```
    *What happens*: These commands deploy the `bandit` and `specialty` services into your Minikube cluster. The `.yaml` files specify the Docker images to use, the number of replicas, and how to expose these services.

3.  **Check Deployments**:
    ```bash
    kubectl get pods -o wide
    kubectl get services
    ```
    *What happens*: You can verify that your pods are running and services are exposed correctly within the Kubernetes cluster.

### 5. Jenkins CI/CD Pipeline Setup

The `Jenkinsfile` in the project root defines a declarative pipeline to automate the SDLC. It includes stages for building Docker images, running tests, pushing images to Docker Hub, and deploying to Kubernetes.

1.  **Install Jenkins**: Follow the official Jenkins documentation for installation on your operating system (e.g., [https://www.jenkins.io/doc/book/installing/](https://www.jenkins.io/doc/book/installing/)).


3.  **Create a Jenkins Pipeline Job**:
    *   In Jenkins, create a new `Pipeline` job.
    *   Under `Pipeline` -> `Definition`, select `Pipeline script from SCM`.
    *   Set `SCM` to `Git`, provide your repository URL, and specify `credentials` if your repo is private.
    *   Set `Script Path` to `Jenkinsfile`.
    *   Enable `GitHub hook trigger for GITScm polling` under `Build Triggers`.

    *What happens*: Jenkins is configured to monitor your GitHub repository for changes. Upon a push, the pipeline defined in `Jenkinsfile` will automatically execute, performing the following stages:
    *   **Build**: Builds Docker images for your application services.
    *   **Test**: Runs automated tests.
    *   **Push Docker Images**: Pushes the newly built Docker images to Docker Hub.
    *   **Deploy to Kubernetes**: Deploys the updated application to your configured Kubernetes cluster (e.g., Minikube).

### 6. ELK Stack (Monitoring and Logging) Setup

1.  **Create ELK Stack Configuration Files**:
    Navigate to the root of your project and create the necessary directories:
    ```bash
    mkdir -p elk-stack/logstash/config
    ```
    Then, create the `docker-compose.yml` for the ELK stack inside `elk-stack` and the `logstash.conf` inside `elk-stack/logstash/config`. You can find the detailed content for these files in the project's documentation.

2.  **Modify `app.py` for Logging**:
    Ensure your `app.py` is configured to write logs to `application.log` within the `/app/logs` directory. This directory is shared as a Docker volume with Logstash. Refer to the project's documentation for specific modifications.

3.  **Update Main `docker-compose.yml` for Application Integration**:
    Modify your project's main `docker-compose.yml` to connect your application services to the ELK network and mount the `app_logs` volume. Refer to the project's documentation for specific modifications.

4.  **Start the ELK Stack**:
    Navigate to the `elk-stack` directory and run:
    ```bash
    cd elk-stack
    docker-compose up -d
    ```
    *What happens*: This starts Elasticsearch (data store), Logstash (log processor), and Kibana (visualization dashboard) as Docker containers.

5.  **Access Kibana and Configure Index Pattern**:
    *   Open your web browser to `http://localhost:5601`.
    *   In Kibana, go to **Stack Management** -> **Index Patterns** -> **Create index pattern**.
    *   Enter `carecompass-app-logs-*` as the index pattern and select `@timestamp` as the time field.
    *   Navigate to the **Discover** tab to view your application logs in real-time.

---

## Running the Application Locally (using Docker Compose)

After setting up the ELK stack and updating your `app.py` and main `docker-compose.yml` as described above, you can run the entire application locally using Docker Compose:

1.  **Ensure ELK Stack is Running (from Step 6.4)**.

2.  **Start your main application services**:
    Navigate to the root of your project (`CareCompass`) and execute:
    ```bash
    docker-compose up -d --build
    ```
    *What happens*: This command builds (if changes were made) and starts your `bandit`, `specialty`, and `frontend` services, connected to the `elk-network`, with logs being sent to the ELK stack.

Access the main application page at: [http://localhost:5001/](http://localhost:5001/)

---

## Docker Commands

This section provides general Docker commands useful for development and debugging.

### Build and Run Individual Containers (Example)
1.  Build and run the Doctor Recommendation container:
    ```bash
    docker build -t bandit .
    docker run --name bandit_v1 -p 8000:8000 bandit
    ```

2.  Build and Run the Specialty Predictor container:
    ```bash
    docker build -t specialty_predictor .
    docker run --name second_v1 -p 8080:5000 sunnykaushik007/flask-specialty-predictor
    ```

### Inspect Docker Images
Inspect image metadata:
```bash
docker image inspect <image-name>
```

### Push to Docker Hub
1. Tag the image:
   ```bash
   docker tag bandits:latest sunnykaushik007/bandits:latest
   ```
2. Push to Docker Hub:
   ```bash
   docker push sunnykaushik007/bandits:latest
   ```

### Remove Unused Containers and Images
- Remove all stopped containers:
  ```bash
  docker container prune
  ```
- Remove unused images:
  ```bash
  docker image prune
  ```

---