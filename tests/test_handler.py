"""Unit tests for handler with defensive null checks."""
import unittest
from src.handler import handler
import json


class TestHandlerNullSafety(unittest.TestCase):
    
    def test_handler_with_valid_event(self):
        """Test handler works normally with valid event."""
        event = {"someKey": "someValue", "data": [1, 2, 3]}
        response = handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertIn("Hello from PipelineOps!", body["message"])  
    
    def test_handler_with_none_event(self):
        """Test handler gracefully handles None event."""
        response = handler(None, None)
        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        # Should handle null event without crashing
        self.assertIn("event", body)  
    
    def test_handler_with_empty_event(self):
        """Test handler with empty event dict."""
        response = handler({}, None)
        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertIn("Hello from PipelineOps!", body["message"])  
    
    def test_handler_with_null_string(self):
        """Test handler with null string event."""
        response = handler(None, None)  # Event is None
        self.assertEqual(response["statusCode"], 200)
    
    def test_response_structure_consistency(self):
        """Test that response structure is consistent regardless of input."""
        for event in [None, {}, {"data": 1}, "string"]:
            response = handler(event, None)
            self.assertEqual(response["statusCode"], 200)
            self.assertIn("headers", response)
            self.assertIn("body", response)
            body = json.loads(response["body"])
            self.assertEqual(body.get("message"), "Hello from PipelineOps!")


if __name__ == "__main__":
    unittest.main()