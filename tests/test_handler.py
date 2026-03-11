"""Tests for the Lambda handler."""

import json
from src.handler import handler


def test_handler_returns_200():
    """Handler should return statusCode 200."""
    result = handler({"key": "value"}, None)
    assert result["statusCode"] == 200


def test_handler_returns_json_body():
    """Handler body should be valid JSON with expected fields."""
    result = handler({"key": "value"}, None)
    body = json.loads(result["body"])
    assert body["message"] == "Hello from PipelineOps!"
    assert "timestamp" in body
    assert body["event"] == {"key": "value"}


def test_handler_empty_event():
    """Handler should work with an empty event."""
    result = handler({}, None)
    body = json.loads(result["body"])
    assert body["event"] == {}
    assert result["statusCode"] == 200
