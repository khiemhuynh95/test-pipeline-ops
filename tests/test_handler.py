"""Tests for handler.py with NPE prevention."""

import json
from datetime import datetime, timezone
from unittest.mock import Mock
import src.handler as handler_module


def test_handler_with_valid_event():
    """Test handler with a valid event payload."""
    event = {"message": "test", "userId": 123}
    result = handler_module.handler(event, None)
    
    assert result["statusCode"] == 200
    assert "Hello from PipelineOps!" in result["body"]
    data = json.loads(result["body"])
    assert data["event"] == event


def test_handler_with_none_event():
    """Test handler when event is None - prevents NullPointerException."""
    # This would cause NPE without the fix
    result = handler_module.handler(None, None)
    
    assert result["statusCode"] == 200
    data = json.loads(result["body"])
    assert data["event"] is None
    assert "null/empty" in str(data.get("warning", ""))


def test_handler_with_empty_event():
    """Test handler with empty event dict."""
    result = handler_module.handler({}, None)
    
    assert result["statusCode"] == 200
    data = json.loads(result["body"])
    # Should handle gracefully without crashing


def test_handler_with_event_object():
    """Test handler with event as an object (not dict)."""
    mock_event = Mock()
    mock_event.message = "object-event"
    result = handler_module.handler(mock_event, None)
    
    assert result["statusCode"] == 200
    data = json.loads(result["body"])
    # Should use getattr with .get() safely


def test_handler_with_missing_keys():
    """Test handler when event has missing keys."""
    event = {"someOtherKey": "value"}
    result = handler_module.handler(event, None)
    
    assert result["statusCode"] == 200
    data = json.loads(result["body"])
    # Should not crash with KeyError


def test_handler_timestamp_format():
    """Test that timestamp is in ISO format."""
    event = {}
    result = handler_module.handler(event, None)
    
    data = json.loads(result["body"])
    ts = data.get("timestamp", "")
    assert len(ts) > 0
    # Basic check for ISO format components
    assert "T" in ts or ts == ""


def test_handler_json_serializable():
    """Test that response body is valid JSON."""
    event = {"test": "data", "nested": {