"""Unit tests for handler.py to ensure robustness against null inputs."""

import unittest
from src.handler import handler


class TestHandler(unittest.TestCase):
    def test_handler_with_valid_event(self):
        """Test handler with a valid event dictionary."""
        result = handler({"key": "value"}, None)
        self.assertEqual(result['statusCode'], 200)
        assert 'message' in result['body']

    def test_handler_with_empty_event(self):
        """Test handler with an empty event dictionary."""
        result = handler({}, None)
        self.assertEqual(result['statusCode'], 200)
        assert 'message' in result['body']

    def test_handler_with_none_event(self):
        """Test handler with None/null as the event - this was causing NullPointerException."""
        result = handler(None, None)
        self.assertEqual(result['statusCode'], 200)
        # Should handle gracefully without crashing
        assert 'message' in result['body']

    def test_handler_response_structure(self):
        """Test that response has correct structure."""
        result = handler({"test": "data"}, None)
        self.assertIn('statusCode', result)
        self.assertIn('headers', result)
        self.assertIn('body', result)
        self.assertEqual(result['statusCode'], 200)

    def test_handler_timestamp_present(self):
        """Test that timestamp is always included in response."""
        result = handler({"any": "data"}, None)
        import json
        parsed = json.loads(result['body'])
        self.assertIn('timestamp', parsed)


if __name__ == '__main__':
    unittest.main()