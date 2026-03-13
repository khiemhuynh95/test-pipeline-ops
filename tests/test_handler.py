"""Comprehensive tests for the handler module.

Tests cover:
- Normal operation with valid event
- None/empty event (NPE prevention)
- Various edge cases and error scenarios
- Response format validation
"""

import json
from unittest.mock import Mock, MagicMock
from src.handler import handler


class TestHandler(unittest.TestCase):
    """Test suite for the Lambda handler."""
    
    def setUp(self):
        self.context = MagicMock()
    
    def test_normal_operation_with_valid_event(self):
        """Test with a properly formed event object."""
        event = {
            "httpMethod": "GET",
            "path": "/health",
            "headers": {"Content-Type": "application/json"},
            "body": "{}"
        }
        response = handler(event, self.context)
        
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Hello from PipelineOps!", response["body"])
        parsed = json.loads(response["body"])
        self.assertIn("metadata", parsed)
        self.assertEqual(parsed["metadata"]["method"], "GET")
    
    def test_none_event_no_crash(self):
        """Test that None event doesn't cause NPE - CRITICAL TEST."""
        response = handler(None, self.context)
        
        # Should return gracefully with empty dict
        parsed = json.loads(response["body"])
        self.assertEqual(parsed["event"], {})
    
    def test_empty_event(self):
        """Test with truly empty event."""
        response = handler({}, self.context)
        parsed = json.loads(response["body"])
        # Empty dict should remain empty
        self.assertEqual(parsed["event"], {})
    
    def test_null_body_handling(self):
        """Test when event body is None."""
        event = {
            "httpMethod": "POST",
            "path": "/payments",
            "body": None
        }
        response = handler(event, self.context)
        parsed = json.loads(response["body"])
        # Should handle gracefully without crashing
    
    def test_response_headers_present(self):
        """Verify response has proper headers."""
        event = {"httpMethod": "GET", "path": "/test"}
        response = handler(event, self.context)
        
        self.assertIn("Content-Type", response["headers"])
        self.assertEqual(response["headers"]["Content-Type"], "application/json")
    
    def test_response_format(self):
        """Validate response structure matches AWS Lambda expectations."""
        event = {"httpMethod": "GET", "path": "/api/v1/payments"}
        response = handler(event, self.context)
        
        # Check required fields
        assert "statusCode" in response
        assert "headers" in response
        assert "body" in response
        assert isinstance(response["statusCode"], int)
        assert json.loads(response["body"]) is not None
    
    def test_multiple_invocations_idempotent(self):
        """Ensure handler works consistently across multiple calls."""
        event = {"httpMethod": "GET", "path": "/check"}
        responses = [handler(event, self.context) for _ in range(10)]
        
        # All should have same status code and message
        all_status_codes_same = all(r["statusCode"] == 200 for r in responses)
        all_messages_present = all("Hello from PipelineOps!" in r["body"] for r in responses)
        self.assertTrue(all_status_codes_same and all_messages_present)
    
    def test_with_special_characters_in_event(self):
        """Test handling of events with special characters."""
        event = {
            "httpMethod": "POST",
            "path": "/api/v1/payments/\ud83d\ude00",  # emoji
            "headers": {"Content-Type": "text/plain; charset=utf-8"},
            "body": 'key: value with 