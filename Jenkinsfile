pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build . -t obnd5'
            	sh 'docker run -p 82:82 obnd5'
            }
        }  
    }
}