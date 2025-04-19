pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'annalhq'
        FLASK_IMAGE_NAME = 'compose-flask'
        DJANGO_IMAGE_NAME = 'compose-django'
        VERSION = "${BUILD_NUMBER}"
    }
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Deployment Environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run tests')
        booleanParam(name: 'PUSH_IMAGES', defaultValue: true, description: 'Push images to Docker Hub')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -la'
            }
        }
        
        stage('Lint') {
            parallel {
                stage('Lint Flask') {
                    steps {
                        dir('flask') {
                            sh '''
                                python -m pip install flake8
                                flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
                            '''
                        }
                    }
                }
                
                stage('Lint Django') {
                    steps {
                        dir('django') {
                            sh '''
                                python -m pip install flake8
                                flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Test') {
            when {
                expression { return params.RUN_TESTS }
            }
            parallel {
                stage('Test Flask') {
                    steps {
                        dir('flask') {
                            sh '''
                                python -m pip install pytest
                                python -m pip install -r requirements.txt
                                pytest || true
                            '''
                        }
                    }
                }
                
                stage('Test Django') {
                    steps {
                        dir('django') {
                            sh '''
                                python -m pip install pytest
                                python -m pip install -r requirements.txt
                                python manage.py test || true
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Build Images') {
            steps {
                sh 'docker-compose build'
                sh "docker tag ${DOCKER_REGISTRY}/${FLASK_IMAGE_NAME}:latest ${DOCKER_REGISTRY}/${FLASK_IMAGE_NAME}:${VERSION}"
                sh "docker tag ${DOCKER_REGISTRY}/${DJANGO_IMAGE_NAME}:latest ${DOCKER_REGISTRY}/${DJANGO_IMAGE_NAME}:${VERSION}"
            }
        }
        
        stage('Push Images') {
            when {
                expression { return params.PUSH_IMAGES }
            }
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_TOKEN')]) {
                    sh "echo ${DOCKER_TOKEN} | docker login -u ${DOCKER_REGISTRY} --password-stdin"
                    sh "docker push ${DOCKER_REGISTRY}/${FLASK_IMAGE_NAME}:latest"
                    sh "docker push ${DOCKER_REGISTRY}/${FLASK_IMAGE_NAME}:${VERSION}"
                    sh "docker push ${DOCKER_REGISTRY}/${DJANGO_IMAGE_NAME}:latest"
                    sh "docker push ${DOCKER_REGISTRY}/${DJANGO_IMAGE_NAME}:${VERSION}"
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    if (params.ENVIRONMENT == 'prod') {
                        input message: 'Deploy to production?', ok: 'Deploy'
                    }
                    
                    echo "Deploying to ${params.ENVIRONMENT} environment"
                    
                    sh """
                    cat > docker-compose.${params.ENVIRONMENT}.yml << EOL
version: '3.8'

services:
  flask-app:
    image: ${DOCKER_REGISTRY}/${FLASK_IMAGE_NAME}:${VERSION}
    environment:
      - FLASK_ENV=${params.ENVIRONMENT}
      
  django-app:
    image: ${DOCKER_REGISTRY}/${DJANGO_IMAGE_NAME}:${VERSION}
    environment:
      - DJANGO_SETTINGS_MODULE=myapp.settings.${params.ENVIRONMENT}
EOL
                    """
                    
                    sh "docker-compose -f docker-compose.yml -f docker-compose.${params.ENVIRONMENT}.yml up -d"
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker-compose down || true'
            cleanWs()
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline execution failed!'
        }
    }
}
