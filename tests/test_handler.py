"""Tests for the Lambda handler with null safety."""
import unittest
from src.handler import handler


class TestHandlerNullSafety(unittest.TestCase):
    """Test cases to verify NullPointerException prevention."""

    def test_none_event(self):
        """Test that None event is handled gracefully."""
        result = handler(None, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('Hello from PipelineOps!', result['body'])

    def test_empty_event(self):
        """Test that empty dict/event works correctly."""
        result = handler({}, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('Hello from PipelineOps!', result['body'])

    def test_valid_event(self):
        """Test normal operation with valid event data."""
        test_event = {"userId": "123", "action": "purchase"}
        result = handler(test_event, None)
        self.assertEqual(result['statusCode'], 200)
        # Event should be serialized to string
        self.assertIn('event', result['body'])

    def test_string_event(self):
        """Test with JSON string event."""
        import json
        json_event = json.dumps({"data": "test"})
        result = handler(json_event, None)
        self.assertEqual(result['statusCode'], 200)

    def test_invalid_json_string(self):
        """Test with invalid JSON string - should not crash."""
        result = handler("invalid json {", None)
        self.assertEqual(result['statusCode'], 200)
        # Should handle gracefully and show (empty/null) or partial data

    def test_null_values_in_event(self):
        """Test event containing null values."""
        event_with_nones = {
            "id": 1,
            "name": None,
            "value": None,
            "active": True
        }
        result = handler(event_with_nones, None)
        self.assertEqual(result['statusCode'], 200)
        # Should filter out null values

    def test_list_event(self):
        """Test with list as event."""
        result = handler([1, 2, 3], None)
        self.assertEqual(result['statusCode'], 200)

    def test_integer_event(self):
        """Test with integer as event."""
        result = handler(42, None)
        self.assertEqual(result['statusCode'], 200)


class TestHandlerOutputFormat(unittest.TestCase):
    """Verify output format is consistent."""

    def test_response_structure(self):
        """Check that response has correct structure."""
        result = handler({"test": "data"}, None)
        self.assertIn('statusCode', result)
        self.assertIn('headers', result)
        self.assertIn('body', result)
        
    def test_headers_content_type(self):
        """Verify Content-Type header is set correctly."""
        result = handler(None, None)
        content_type = result['headers'].get('Content-Type')
        self.assertEqual(content_type, 'application/json')


if __name__ == '__main__':
    unittest.main()