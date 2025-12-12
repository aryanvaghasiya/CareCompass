
pipeline {
    agent any

    parameters {
        booleanParam(
            name: 'FAST_MODE',
            defaultValue: false,
            description: 'Skip dependency install and Docker build/push to make the pipeline fast'
        )
    }
    
    triggers {
        githubPush()
    }

    environment {
        // DockerHub repositories
        BANDIT_IMAGE        = "aryanvaghasiya/bandit-service"
        SPECIALITY_IMAGE    = "aryanvaghasiya/speciality-service"
        FRONTEND_IMAGE      = "aryanvaghasiya/frontend-service"

        // Ansible settings
        ANSIBLE_INVENTORY = "Ansible/hosts.ini"
        ANSIBLE_PLAYBOOK  = "Ansible/deploy.yml"

        // REQUIRED FOR MINIKUBE DEPLOYMENT
        KUBECONFIG = "/var/lib/jenkins/.kube/config"
    }

    stages {
        
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/aryanvaghasiya/CareCompass'
            }
        }

        /***********************
         * Install & Test
         **********************/
        /*---------------------------------------------------------------------------------------------------------------------------
        stage('Install Dependencies & Test') {
            when { expression { !params.FAST_MODE } }
            steps {
                sh """
                  set -e
                  python3 -m venv venv
                  . venv/bin/activate
                  python -m pip install --upgrade pip setuptools wheel
                  pip install -r requirements.txt    
                  pytest --disable-warnings || true
                   """
            }
        }
        ------------------------------------------------------------------------------------------------------------------------------*/
        
        //##############################################################################################
        stage('Python setup & deps') {
  agent {
    docker {
      image 'python:3.11-slim'
      args '-u root:root'   // run as root so apt / pip works if needed
    }
  }
  steps {
    sh '''
      set -e
      python -m pip install --upgrade pip setuptools wheel
      python -m venv venv
      . venv/bin/activate
      pip install --upgrade pip setuptools wheel
      pip install -r requirements.txt
      # run tests / lint etc. here
    '''
  }
}
//###################################################################################################
        stage('Skip Install & Test (FAST_MODE)') {
            when { expression { params.FAST_MODE } }
            steps {
                echo "FAST_MODE enabled – skipping pip install and pytest."
            }
        }

        /***********************
         * Docker Build / Push
         **********************/
        stage('Build Docker Images') {
            when { expression { !params.FAST_MODE } }
            steps {
                script {
                    echo "📦 Building Docker images..."

                    docker.build("${BANDIT_IMAGE}:${BUILD_NUMBER}", "./main1")
                    docker.build("${SPECIALITY_IMAGE}:${BUILD_NUMBER}", "./main2")
                    docker.build("${FRONTEND_IMAGE}:${BUILD_NUMBER}", ".")
                }
            }
        }

        stage('Skip Docker Build (FAST_MODE)') {
            when { expression { params.FAST_MODE } }
            steps {
                echo "FAST_MODE enabled – skipping Docker image builds."
            }
        }

        stage('Push Docker Images to DockerHub') {
            when { expression { !params.FAST_MODE } }
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {

                        docker.image("${BANDIT_IMAGE}:${BUILD_NUMBER}").push()
                        docker.image("${SPECIALITY_IMAGE}:${BUILD_NUMBER}").push()
                        docker.image("${FRONTEND_IMAGE}:${BUILD_NUMBER}").push()

                        // Push "latest"
                        docker.image("${BANDIT_IMAGE}:${BUILD_NUMBER}").push("latest")
                        docker.image("${SPECIALITY_IMAGE}:${BUILD_NUMBER}").push("latest")
                        docker.image("${FRONTEND_IMAGE}:${BUILD_NUMBER}").push("latest")
                    }
                }
            }
        }

        stage('Skip Docker Push (FAST_MODE)') {
            when { expression { params.FAST_MODE } }
            steps {
                echo "FAST_MODE enabled – skipping Docker push to DockerHub."
            }
        }

        /***********************
         * Prune Old Images
         **********************/
        stage('Prune Old Docker Images') {
            when { expression { !params.FAST_MODE } }
            steps {
                script {
                    echo "🧹 Cleaning up old Docker images..."

                    def images = [
                        BANDIT_IMAGE,
                        SPECIALITY_IMAGE,
                        FRONTEND_IMAGE
                    ]

                    images.each { img ->
                        sh """
                        echo "Pruning old images for ${img}"

                        # List all images of this repo, extract tags, sort numerically (latest = highest)
                        TAGS=\$(docker images --format "{{.Repository}}:{{.Tag}}" | grep "${img}" | grep -v latest | sed 's/.*://' | sort -nr)

                        # Count how many exist
                        COUNT=\$(echo "\$TAGS" | wc -l)

                        # If more than 2, delete older ones
                        if [ "\$COUNT" -gt 2 ]; then
                            # Skip top 2 tags, delete the rest
                            OLD_TAGS=\$(echo "\$TAGS" | tail -n +3)

                            for TAG in \$OLD_TAGS; do
                                echo "Removing old image: ${img}:\$TAG"
                                docker rmi "${img}:\$TAG" || true
                            done
                        fi
                        """
                    }
                }
            }
        }

        stage('Skip Prune (FAST_MODE)') {
            when { expression { params.FAST_MODE } }
            steps {
                echo "FAST_MODE enabled – skipping Docker prune."
            }
        }

        /***********************
         * Ansible Deploy
         **********************/
        stage('Deploy with Ansible') {
            steps {
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









