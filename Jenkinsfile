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
        stage('Build') {
            steps {
                echo "🔨 Building from branch: ${params.BRANCH}"
                checkout([$class: 'GitSCM',
                    branches: [[name: "*/${params.BRANCH}"]],
                    userRemoteConfigs: [[url: 'https://github.com/khiemhuynh95/test-pipeline-ops.git']]
                ])
                sh '''
                    echo "Installing dependencies..."
                    pip install poetry
                    poetry install --no-interaction
                    echo "✅ Build complete"
                '''
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running tests...'
                sh '''
                    poetry run pytest tests/ -v --tb=short
                    echo "✅ All tests passed"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Deploying to dev environment..."
                sh '''
                    echo "Building Lambda zip..."
                    make build

                    echo "Deploying to LocalStack..."
                    aws --endpoint-url=${AWS_ENDPOINT} lambda update-function-code \
                        --function-name ${LAMBDA_FUNCTION} \
                        --zip-file fileb://lambda.zip \
                        --region ${AWS_REGION} \
                        2>/dev/null || \
                    aws --endpoint-url=${AWS_ENDPOINT} lambda create-function \
                        --function-name ${LAMBDA_FUNCTION} \
                        --runtime python3.12 \
                        --handler src.handler.handler \
                        --role arn:aws:iam::000000000000:role/lambda-role \
                        --zip-file fileb://lambda.zip \
                        --region ${AWS_REGION}

                    echo "✅ Deployed to dev"
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline passed — build ✓ test ✓ deploy (dev) ✓'
        }
        failure {
            echo '🔴 Pipeline failed'
        }
    }
}
