pipeline {
    agent any
    
    tools {
        python 'Python3'   // Ensure "Python3" is configured in Jenkins Global Tools
    }

    environment {
        // DockerHub repositories (CHANGE THESE TO MATCH YOUR DOCKERHUB USERNAME)
        BANDIT_IMAGE       = "aryanvaghasiya/bandit-service"
        SPECIALITY_IMAGE   = "aryanvaghasiya/speciality-service"
        FRONTEND_IMAGE     = "aryanvaghasiya/frontend-service"

        // Ansible deployment settings
        ANSIBLE_INVENTORY = "Ansible/hosts.ini"
        ANSIBLE_PLAYBOOK  = "Ansible/deploy.yml"
    }

    triggers {
        githubPush()  // Auto-build on GitHub commit
    }

    stages {
        
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/aryanvaghasiya/MLOps-Driven-Doctor-Recommendation-System.git'
            }
        }

        stage('Install Dependencies & Test') {
            steps {
                sh """
                pip install -r requirements.txt
                pytest --disable-warnings || true
                """
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo "Building Docker images..."

                    docker.build("${BANDIT_IMAGE}:${BUILD_NUMBER}", "./main1")
                    docker.build("${SPECIALITY_IMAGE}:${BUILD_NUMBER}", "./main2")
                    docker.build("${FRONTEND_IMAGE}:${BUILD_NUMBER}", ".")
                }
            }
        }

        stage('Push Docker Images to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {

                        def bandit = docker.image("${BANDIT_IMAGE}:${BUILD_NUMBER}")
                        def speciality = docker.image("${SPECIALITY_IMAGE}:${BUILD_NUMBER}")
                        def frontend = docker.image("${FRONTEND_IMAGE}:${BUILD_NUMBER}")

                        bandit.push()
                        speciality.push()
                        frontend.push()

                        // Also push "latest"
                        bandit.push("latest")
                        speciality.push("latest")
                        frontend.push("latest")
                    }
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                script {
                    echo "Running Ansible Deployment..."

                    sh """
                    ansible-playbook -i ${ANSIBLE_INVENTORY} ${ANSIBLE_PLAYBOOK} \
                        -e bandit_tag=${BUILD_NUMBER} \
                        -e speciality_tag=${BUILD_NUMBER} \
                        -e frontend_tag=${BUILD_NUMBER}
                    """
                }
            }
        }
    }

    post {
        success {
            echo "🚀 Build #${BUILD_NUMBER} Successful!"

            emailext(
                to: 'aryanvaghasia12345@gmail.com',
                subject: "SUCCESS: Jenkins Build #${BUILD_NUMBER} ${env.JOB_NAME}",
                body: """
                Hi Aryan,

                Your CI/CD pipeline for project *${env.JOB_NAME}* executed successfully.

                📌 Docker Images Built & Pushed:
                - ${BANDIT_IMAGE}:${BUILD_NUMBER}
                - ${SPECIALITY_IMAGE}:${BUILD_NUMBER}
                - ${FRONTEND_IMAGE}:${BUILD_NUMBER}

                📌 Deployment with Ansible completed.

                Regards,  
                Jenkins CI/CD (Automated)
                """
            )
        }

        failure {
            echo "❌ Build #${BUILD_NUMBER} Failed!"

            emailext(
                to: 'aryanvaghasia12345@gmail.com',
                subject: "FAILED: Jenkins Build #${BUILD_NUMBER} ${env.JOB_NAME}",
                body: """
                Hi Aryan,

                Your CI/CD pipeline for *${env.JOB_NAME}* has failed.

                Please check the Jenkins logs for errors.

                Regards,  
                Jenkins CI/CD
                """
            )
        }
    }
}
