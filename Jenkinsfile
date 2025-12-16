pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        // Docker images
        BANDIT_IMAGE     = "aryanvaghasiya/bandit"
        SPECIALITY_IMAGE = "aryanvaghasiya/speciality"
        FRONTEND_IMAGE   = "aryanvaghasiya/frontend"

        // Ansible
        ANSIBLE_INVENTORY = "Ansible/hosts.ini"
        ANSIBLE_PLAYBOOK  = "Ansible/deploy.yml"

        // Kubernetes
        KUBECONFIG = "$HOME/.kube/config"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main2', url: 'https://github.com/aryanvaghasiya/CareCompass'
            }
        }

        stage('Start / Verify Minikube') {
            steps {
                sh '''
                set -e

                echo "==> Checking Minikube status"
                minikube status || minikube start --driver=docker

                echo "==> Updating kube context"
                minikube update-context

                echo "==> Verifying cluster"
                kubectl get nodes
                '''
            }
        }

        stage('Pull Docker Images') {
            steps {
                sh '''
                set -e
                docker pull aryanvaghasiya/bandit:latest
                docker pull aryanvaghasiya/speciality:latest
                docker pull aryanvaghasiya/frontend:latest
                '''
            }
        }

        stage('Deploy with Ansible') {
            steps {
                sh '''
                set -e
                ansible-playbook -i ${ANSIBLE_INVENTORY} ${ANSIBLE_PLAYBOOK}
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully"
        }
        failure {
            echo "❌ Pipeline failed — check logs"
        }
    }
}


