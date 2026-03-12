"""Unit tests for handler.py."""

import pytest
from src.handler import handler


def test_handler_with_valid_event():
    """Test handler with a normal event dictionary."""
    event = {"key": "value", "payload": {"data": 123}}
    result = handler(event, None)
    
    assert result["statusCode"] == 200
    assert "Hello from PipelineOps!" in result["body"]
    assert event in result["body"]
    assert "timestamp" in result["body"]


def test_handler_with_none_event():
    """Test handler when event is None (defensive programming)."""
    result = handler(None, None)
    
    assert result["statusCode"] == 200
    assert "Hello from PipelineOps!" in result["body"]
    # Verify that None is handled gracefully without crashing
    assert "event": null in result["body"] or '"event": null' in result['body']


def test_handler_with_empty_event():
    """Test handler with empty event dictionary."""
    result = handler({}, None)
    
    assert result["statusCode"] == 200
    assert "Hello from PipelineOps!" in result["body"]


def test_handler_response_structure():
    """Test that response has correct structure."""
    event = {"test": True}
    result = handler(event, None)
    
    # Check required fields
    assert "statusCode" in result
    assert "headers" in result
    assert "body" in result
    
    # Parse body and validate JSON structure
    import json
    parsed_body = json.loads(result["body"])
    assert "message" in parsed_body
    assert "timestamp" in parsed_body
    assert "event" in parsed_body


def test_handler_with_complex_event():
    """Test handler with complex nested event structure."""
    event = {
        "httpMethod": "POST",
        "path": "/api/payments",
        "body": {"amount": 100, "currency": "USD"}
    }
    result = handler(event, None)
    
    assert result["statusCode"] == 200
    parsed_body = json.loads(result["body"])
    assert parsed_body["event"]["httpMethod"] == "POST"


def test_handler_timestamp_format():
    """Test that timestamp is in ISO format."""
    event = {}
    result = handler(event, None)
    
    import json
    parsed_body = json.loads(result["body"])
    from datetime import datetime
    # Verify timestamp can be parsed as valid ISO format
    try:
        datetime.fromisoformat(parsed_body["timestamp"])
        assert True  # Valid format
    except ValueError:
        assert False, "Timestamp not in valid ISO format"