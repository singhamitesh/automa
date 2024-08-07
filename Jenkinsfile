// jenkinsfile for bot pipe line 

pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("trading-bot:${env.BUILD_ID}")
                }
            }
        }
        
        stage('Push to Docker Registry') {
            steps {
                script {
                    docker.withRegistry('https://your-docker-registry-url', 'docker-registry-credentials') {
                        docker.image("trading-bot:${env.BUILD_ID}").push()
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    kubernetesDeploy(
                        configs: "kubernetes-deployment.yaml",
                        kubeconfigId: "kubeconfig-credentials-id",
                        enableConfigSubstitution: true
                    )
                }
            }
        }
    }
}