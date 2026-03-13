"""Unit tests for handler.py with edge case coverage."""

import pytest
from src.handler import handler


class TestHandler:
    """Test suite covering normal and edge cases for the Lambda handler."""

    def test_normal_event(self):
        """Test handler with a standard API Gateway event structure."""
        event = {
            "httpMethod": "GET",
            "path": "/health",
            "queryStringParameters": {"version": "v1"},
        }
        response = handler(event, None)

        assert response["statusCode"] == 200
        assert "Hello from PipelineOps!" in response["body"]
        assert "event" in json.loads(response["body"])

    def test_null_event(self):
        """Test handler with None as event - edge case."""
        response = handler(None, None)

        assert response["statusCode"] == 400
        assert "No event data provided" in response["body"]
        assert "error" in json.loads(response["body"])

    def test_empty_event(self):
        """Test handler with empty dict as event."""
        response = handler({}, None)

        assert response["statusCode"] == 400
        assert "No event data provided" in response["body"]
        assert "error" in json.loads(response["body"])

    def test_event_with_missing_keys(self):
        """Test handler with partial/missing keys in event."""
        event = {
            "path": "/test",
        }
        response = handler(event, None)

        assert response["statusCode"] == 200
        # Should gracefully handle missing httpMethod and queryStringParameters
        data = json.loads(response["body"])
        assert data.get("input_details", {}).get("httpMethod") == "unknown"
        assert data.get("input_details", {}).get("path") == "/test"

    def test_timestamp_format(self):
        """Test that timestamp is in ISO format."""
        event = {}
        response = handler(event, None)
        import json
        body_data = json.loads(response["body"])

        assert "timestamp" in body_data
        from datetime import datetime
        # Should parse as valid ISO 8601 format
        try:
            parsed = datetime.fromisoformat(body_data["timestamp"])
            assert parsed is not None
        except ValueError:
            pytest.fail("Timestamp not in ISO format")

    def test_response_structure(self):
        """Test that response has correct structure."""
        event = {}
        response = handler(event, None)

        # Check top-level structure
        assert "statusCode" in response
        assert "headers" in response
        assert "body" in response

        # Headers should contain Content-Type
        assert response["headers"]["Content-Type"] == "application/json"

    def test_json_serialization(self):
        """Test that body is valid JSON."""
        event = {}
        response = handler(event, None)

        import json
        # Should be able to parse the body as JSON
        data = json.loads(response["body"])
        assert isinstance(data, dict)
        assert "message" in data
        assert "timestamp" in data