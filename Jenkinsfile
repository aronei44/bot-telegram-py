pipeline {
  agent any
  environment {
      SERVER_USERNAME = "${env.UBUNTU_USER}"
      SERVER_HOST = "${env.JCC_SERVER_HOST}"
      REGISTRY_URL = "${env.HARBOR_URL}"
      REGISTRY_USERNAME = "${env.JCC_REGISTRY_USERNAME}"
      REGISTRY_PASSWORD = "${env.JCC_REGISTRY_PASSWORD}"
      IMAGE_NAME = "${env.JCC_BOT_IMAGE_NAME}"
      IMAGE_DEPLOY = "${env.JCC_BOT_IMAGE_DEPLOY}"
  }
  options {
    timeout(time: 1, unit: 'HOURS')
  }
  stages {
    stage('Docker Build') {
      steps{
        sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER .'
      }
    }
    stage('Docker Push') {
      steps{
        sh 'docker login -u $REGISTRY_USERNAME -p $REGISTRY_PASSWORD $REGISTRY_URL'
        sh 'docker push $IMAGE_NAME:$BUILD_NUMBER'
      }
    }
    stage('Deploy to Server') {
      steps {
        sh 'ssh -o StrictHostKeyChecking=no $SERVER_USERNAME@$SERVER_HOST \
        "cat .password | docker login -u $REGISTRY_USERNAME --password-stdin $REGISTRY_URL && \
        docker pull $IMAGE_NAME:$BUILD_NUMBER && \
        sed -i \\"s/image:.*/image: $IMAGE_DEPLOY:$BUILD_NUMBER/g\\" deployment.yaml && \
        ./update-config.sh"'
      }
    }
  }
}