"""Tests for the handler module."""

import pytest
from src.handler import handler


def test_handler_returns_valid_response():
    """Test that handler returns a valid response structure."""
    result = handler({"key": "value"}, None)
    
    assert result["statusCode"] == 200
    assert "headers" in result
    assert "Content-Type" in result["headers"]
    assert result["headers"]["Content-Type"] == "application/json"
    

def test_handler_handles_empty_event():
    """Test that handler works with empty event."""
    result = handler({}, None)
    
    assert result["statusCode"] == 200
    assert "message" in result["body"]


def test_handler_handles_none_event():
    """Test that handler converts None to empty dict."""
    result = handler(None, None)
    
    assert result["statusCode"] == 200
    assert isinstance(result["event"], dict)


def test_handler_response_is_json_serializable():
    """Test that response body is valid JSON."""
    import json
    result = handler({"test": "data"}, None)
    
    # Should be able to parse the response body as JSON
    parsed = json.loads(result["body"])
    assert parsed["message"] == "Hello from PipelineOps!"
    assert "timestamp" in parsed
    assert parsed["event"] == {"test": "data"}