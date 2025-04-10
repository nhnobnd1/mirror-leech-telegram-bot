pipeline {
    agent any
    environment {
        REPO_URL = 'https://github.com/nhnobnd1/mirror-leech-telegram-bot.git'
        BRANCH_NAME = 'obnd-77'
        CONTAINER_NAME = 'obnd-77'
        IMAGE_NAME = 'nhnobnd/obnd'
        WEBHOOK_URL = 'https://pushmore.io/webhook/r6Uybjxdr7HKXg7H7dXfaqEW'
        PORT = '7777'
        DOCKER_USERNAME = 'nhnobnd'
        DOCKER_PASSWORD = 'Dunghoi131290'
    }
    stages {
        stage('Checkout source code') {
            steps {
                git branch: env.BRANCH_NAME, url: env.REPO_URL
            }
        }
        stage('Login to Docker Hub') {
            steps {
                sh "echo ${env.DOCKER_PASSWORD} | docker login -u ${env.DOCKER_USERNAME} --password-stdin"
            }
        }
        stage('Remove existing container if it exists') {
            steps {
                script {
                    def containerExists = sh(
                        script: "docker ps -a --format '{{.Names}}' | grep -w ${env.CONTAINER_NAME} || true",
                        returnStdout: true
                    ).trim()
                    
                    if (containerExists) {
                        echo "Stopping and removing existing container: ${env.CONTAINER_NAME}"
                        sh "docker stop ${env.CONTAINER_NAME} || true"
                        sh "docker rm ${env.CONTAINER_NAME} || true"
                    } else {
                        echo "No existing container named ${env.CONTAINER_NAME} found."
                    }
                }
            }
        }
        stage('Build and Push Docker image') {
            steps {
                script {
                    sh "curl -X POST '${env.WEBHOOK_URL}' --data 'build now' || true"
                    sh "docker build -t ${env.IMAGE_NAME}:latest ."
                    sh "docker push ${env.IMAGE_NAME}:latest"
                }
            }
        }
        stage('Pull and Run Docker container') {
            steps {
                script {
                    sh "docker pull ${env.IMAGE_NAME}:latest"
                    sh "docker run -d --name ${env.CONTAINER_NAME} -p ${env.PORT}:${env.PORT} ${env.IMAGE_NAME}:latest"
                }
            }
        }
    }
    post {
        success {
            echo 'The pipeline has completed successfully.'
            sh "curl -X POST '${env.WEBHOOK_URL}' --data 'build done' || true"
        }
        failure {
            echo 'The pipeline has failed.'
            sh "curl -X POST '${env.WEBHOOK_URL}' --data 'build failed' || true"
        }
    }
} 