.PHONY: install test build clean deploy

# Install dependencies
install:
	poetry install

# Run tests
test:
	poetry run pytest tests/ -v

# Build Lambda zip package
build: clean
	mkdir -p dist
	cp -r src/ dist/
	cd dist && zip -r ../lambda.zip . -x '__pycache__/*' '*.pyc'
	@echo "✅ Built lambda.zip"

# Clean build artifacts
clean:
	rm -rf dist/ lambda.zip
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true

# Deploy to LocalStack (dev)
deploy: build
	aws --endpoint-url=http://localhost:4566 lambda update-function-code \
		--function-name test-pipeline-ops-dev \
		--zip-file fileb://lambda.zip \
		--region us-east-1 \
		2>/dev/null || \
	aws --endpoint-url=http://localhost:4566 lambda create-function \
		--function-name test-pipeline-ops-dev \
		--runtime python3.12 \
		--handler src.handler.handler \
		--role arn:aws:iam::000000000000:role/lambda-role \
		--zip-file fileb://lambda.zip \
		--region us-east-1
	@echo "✅ Deployed to LocalStack (dev)"

# Run all: test, build, deploy
all: test build deploy
