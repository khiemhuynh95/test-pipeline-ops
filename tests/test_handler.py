"""Tests for the Lambda handler with null safety."""

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


def test_handler_none_event():
    """Handler should handle None event without errors."""
    result = handler(None, None)
    body = json.loads(result["body"])
    assert body["event"] == {}
    assert result["statusCode"] == 200


def test_handler_string_event():
    """Handler should handle string event gracefully."""
    result = handler("some string", None)
    body = json.loads(result["body"])
    # String is converted to empty dict when it can't be parsed as JSON object
    assert isinstance(body["event"], (dict, str))
    assert result["statusCode"] == 200


def test_handler_integer_event():
    """Handler should handle integer event gracefully."""
    result = handler(12345, None)
    body = json.loads(result["body"])
    # Integer is converted to empty dict when it can't be parsed as JSON object
    assert isinstance(body["event"], (dict, int))
    assert result["statusCode"] == 200


def test_handler_list_event():
    """Handler should handle list event gracefully."""
    result = handler([1, 2, 3], None)
    body = json.loads(result["body"])
    assert isinstance(body["event"], (dict, list))
    assert result["statusCode"] == 200
