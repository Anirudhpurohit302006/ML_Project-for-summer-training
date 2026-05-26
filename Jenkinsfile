pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'adaptive-expense-intelligence-system'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
                sh 'docker tag $DOCKER_IMAGE:$DOCKER_TAG $DOCKER_IMAGE:latest'
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                docker stop expense-app || true
                docker rm expense-app || true

                docker run -d \
                    --name expense-app \
                    -p 5000:5000 \
                    $DOCKER_IMAGE:latest
                '''
            }
        }
    }
}