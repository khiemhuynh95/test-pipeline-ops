"""Tests for handler.py - validates defensive null handling."""

import unittest
from src.handler import handler


class TestHandlerDefensiveChecks(unittest.TestCase):
    """Test that handler handles None/null inputs gracefully."""

    def test_handler_with_none_event(self):
        """Handler should handle None event without error."""
        context = type('Context', (), {'function_name': 'test'})()
        result = handler(None, context)
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('message', result['body'])

    def test_handler_with_none_context(self):
        """Handler should handle None context without error."""
        event = {}
        result = handler(event, None)
        self.assertEqual(result['statusCode'], 200)
        # Should default to 'N/A' for function name
        self.assertIn('N/A', result['body'])

    def test_handler_with_empty_event(self):
        """Handler should handle empty event dict."""
        context = type('Context', (), {'function_name': ''})()
        result = handler({}, context)
        self.assertEqual(result['statusCode'], 200)

    def test_handler_normal_operation(self):
        """Normal operation still works correctly."""
        event = {
            'httpMethod': 'POST',
            'path': '/api/test',
            'headers': {'Authorization': 'Bearer token'}
        }
        context = type('Context', (), {'function_name': 'real'})()
        result = handler(event, context)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['body'].split(',')[1].strip(), '"event_type": "POST"')

    def test_handler_response_format(self):
        """Response format is valid JSON."""
        event = {}
        context = None
        result = handler(event, context)
        
        import json as j
        # Verify body can be parsed
        try:
            parsed = j.loads(result['body'])
            self.assertIn('message', parsed)
            self.assertIn('timestamp', parsed)
        except Exception as e:
            self.fail(f'Failed to parse response body: {e}')


if __name__ == '__main__':
    unittest.main()