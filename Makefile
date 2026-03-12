.PHONY: install test build clean

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