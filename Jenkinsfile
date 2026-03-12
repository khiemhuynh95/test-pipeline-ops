pipeline {
    agent any

    parameters {
        string(name: 'BRANCH', defaultValue: 'develop', description: 'Branch to build')
    }

    environment {
        LAMBDA_FUNCTION = 'test-pipeline-ops-dev'
        AWS_ENDPOINT    = 'http://localstack:4566'
        AWS_REGION      = 'us-east-1'
    }

    stages {
        stage('Pre-Build') {
            steps {
                echo '🛠️ Installing Python 3.12 and build tools...'
                sh '''
                    apt-get update && apt-get install -y --no-install-recommends \
                        python3 python3-pip python3-venv python3-dev \
                        build-essential make
                    python3 --version
                    make --version | head -1
                '''
            }
        }

        stage('Build') {
            steps {
                echo "🔨 Building from branch: ${params.BRANCH}"
                checkout([$class: 'GitSCM',
                    branches: [[name: "*/${params.BRANCH}"]],
                    userRemoteConfigs: [[url: 'https://github.com/khiemhuynh95/test-pipeline-ops.git']]
                ])
                sh '''
                    make install
                    make build
                '''
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running tests...'
                sh 'make test'
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline passed — build ✓ test ✓'
        }
        failure {
            echo '🔴 Pipeline failed'
        }
    }
}
