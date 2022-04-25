pipeline {

  agent any

  stages {
     
    stage('Checkout necessary files ') {
      steps {
	      fileExists 'telegram_token.txt'
        fileExists 'sessions.pk'
        fileExists 'devs_names.txt'
        fileExists 'admins_names.txt'
      }
    }

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

    stage('Deploy App') {
      steps {
        script {
          kubernetesDeploy(configs: "bot_musictheatre.yml", kubeconfigId: "k8s")
        }
      }
    }

  }

}