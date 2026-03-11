# test-pipeline-ops

Simple AWS Lambda handler for testing the PipelineOps self-healing pipeline.

## Setup

```bash
make install
```

## Commands

| Command | Description |
|---|---|
| `make install` | Install dependencies |
| `make test` | Run unit tests |
| `make build` | Build Lambda zip package |
| `make deploy` | Deploy to LocalStack (dev) |
| `make all` | Test → Build → Deploy |
| `make clean` | Remove build artifacts |

## Project Structure

```
test-pipeline-ops/
├── src/
│   ├── __init__.py
│   └── handler.py        # Lambda handler
├── tests/
│   ├── __init__.py
│   └── test_handler.py   # Unit tests
├── Makefile               # Build + deploy commands
├── pyproject.toml         # Poetry config
└── README.md
```
