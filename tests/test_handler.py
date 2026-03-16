"""Test for handler function."""

import json
from datetime import datetime, timezone


def test_handler_with_valid_event():
    """Test that handler returns correct response for valid event."""
    result = handler({"key": "value"}, None)
    assert result["statusCode"] == 200
    assert result["headers"]["Content-Type"] == "application/json"
    assert "body" in result
    # Verify body is valid JSON by parsing it
    response_data = json.loads(result["body"])
    assert "message" in response_data
    assert response_data["message"] == "Hello from PipelineOps!"

def test_handler_with_none_event():
    """Test that handler handles None event gracefully."""
    result = handler(None, None)
    assert result["statusCode"] == 200
    # The body should still be valid JSON
    response_data = json.loads(result["body"])
    assert "timestamp" in response_data