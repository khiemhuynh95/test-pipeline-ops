"""Tests for handler.py - ensures no NullPointerExceptions occur."""

import unittest
from src.handler import handler
import json


class TestHandler(unittest.TestCase):
    
    def test_handler_with_valid_event(self):
        """Test normal operation with a valid event."""
        event = {"rawMessage": '{"someKey": "someValue"}', "otherField": 123}
        result = handler(event, None)
        
        self.assertEqual(result["statusCode"], 200)
        self.assertIn("Hello from PipelineOps!", result["body"])
        self.assertIsNotNone(result.get("timestamp"))
    
    def test_handler_with_none_event(self):
        """Test that handler handles None event without NullPointerException."""
        # This was causing the original issue - accessing methods on None
        event = None
        result = handler(event, None)
        
        self.assertEqual(result["statusCode"], 200)
        self.assertIn("Hello from PipelineOps!", result["body"])
    
    def test_handler_with_empty_event(self):
        """Test handler with empty event dictionary."""
        event = {}
        result = handler(event, None)
        
        self.assertEqual(result["statusCode"], 200)
    
    def test_handler_response_format(self):
        """Verify response format is correct JSON."""
        event = {"test": True}
        result = handler(event, None)
        
        # Should be valid JSON
        parsed = json.loads(result["body"])
        self.assertIn("message", parsed)
        self.assertIn("timestamp", parsed)
    
    def test_handler_with_invalid_raw_message(self):
        """Test handler with malformed rawMessage - should not crash."""
        event = {"rawMessage": "not valid json {{{{"}
        result = handler(event, None)
        
        self.assertEqual(result["statusCode"], 200)
    
    def test_handler_with_numeric_event(self):
        """Test handler with numeric event - edge case."""
        event = 12345
        result = handler(event, None)
        
        self.assertEqual(result["statusCode"], 200)


if __name__ == "__main__":
    unittest.main()
