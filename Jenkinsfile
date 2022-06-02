pipeline {

  agent any

  stages {
     
    stage('Checkout Source') {
      steps {
	    checkout([$class: 'GitSCM', branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'riodevelop_token', url: 'https://github.com/ysoftware/musictheatre.git']]])
      }
    }

    stage("Build image") {
      steps {
         script {
                 myapp = docker.build("atm-srv-02:32003/repository/bot-musictheatre/bot-musictheatre:${env.BUILD_ID}")
                }
          }
        }
    
      stage("Push image to nexus") {
            steps {
                script {
                    docker.withRegistry('http://atm-srv-02:32003', 'nexus') {
                            myapp = docker.build("atm-srv-02:32003/repository/bot-musictheatre/bot-musictheatre:${env.BUILD_ID}")
                            myapp.push("latest")
                            myapp.push("${env.BUILD_ID}")
                    }
                }
            }
        }

    stage('Deploy/Rollout Musictheatre bot') {
      steps {
        withKubeConfig([credentialsId: 'jenkins-robot', serverUrl: 'https://k8s-cluster:6443']){
          sh 'echo "Starting Musictheatre bot Deployment"'
                      sh '''
                          if kubectl get deployments -n prod | grep musictheatre
                          then
                              kubectl rollout restart deployment bot-musictheatre -n prod
                          else
                              kubectl apply -f bot_musictheatre.yml -n prod
                          fi
                      '''
        }
      }

    }

  }

}