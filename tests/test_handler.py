"""Tests for the payments handler with defensive null handling."""

import unittest
from src.handler import handler
import json


class TestHandler(unittest.TestCase):
    """Test cases for the Lambda handler with various input scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_event = {
            "paymentId": "PAY-123456",
            "amount": 99.99,
            "customer": {
                "id": "CUST-789",
                "name": "John Doe",
                "email": "john@example.com"
            },
            "order": {
                "orderId": "ORD-001",
                "items": ["item1", "item2"],
                "total": 99.99
            }
        }
        
    def test_valid_event(self):
        """Test handler with valid event payload."""
        result = handler(self.valid_event)
        self.assertEqual(result["statusCode"], 200)
        self.assertIn("message", json.loads(result["body"]["event"])
        
    def test_none_event(self):
        """Test handler with None event (simulates NullPointerException scenario)."""
        result = handler(None)
        self.assertEqual(result["statusCode"], 200)
        # Should handle gracefully, not crash
        parsed = json.loads(result["body"]["event"])
        self.assertIsInstance(parsed, dict)
        
    def test_empty_event(self):
        """Test handler with empty event."""
        result = handler({})
        self.assertEqual(result["statusCode"], 200)
        parsed = json.loads(result["body"]["event"])
        self.assertEqual(parsed, {})
    
    def test_mixed_null_fields(self):
        """Test handler with some null/missing fields."""
        partial_event = {
            "paymentId": None,
            "customer": None,
        }
        result = handler(partial_event)
        self.assertEqual(result["statusCode"], 200)
    
    def test_invalid_types(self):
        """Test handler with invalid input types."""
        # String event
        result = handler("invalid string")
        self.assertEqual(result["statusCode"], 200)
        
        # List event
        result = handler([1, 2, 3])
        self.assertEqual(result["statusCode"], 200)
    
    def test_missing_nested_fields(self):
        """Test handler when nested objects have missing fields."""
        partial_event = {
            "customer": {"id": None},  # id field is None
            "order": {
                "orderId": "ORD-001",
                "total": None  # total is None
            }
        }
        result = handler(partial_event)
        self.assertEqual(result["statusCode"], 200)
    
    def test_large_numbers(self):
        """Test handler with large number values."""
        event = {
            "amount": 1e15,  # Large float
            "paymentId": "PAY-" + "9" * 20
        }
        result = handler(event)
        self.assertEqual(result["statusCode"], 200)
    
    def test_special_characters(self):
        """Test handler with special characters in strings."""
        event = {
            "paymentId": 'PAY-\u0001\u0002\u0003',
            "customer": {"name": 'John \\n Doe'}
        }
        result = handler(event)
        self.assertEqual(result["statusCode"], 200)
    
    def test_boolean_values(self):
        """Test handler with boolean values in event."""
        event = {
            "flag": True,
            "disabled": False
        }
        result = handler(event)
        self.assertEqual(result["statusCode"], 200)
    
    def test_zero_values(self):
        """Test handler with zero values."""
        event = {
            "amount": 0.0,
            "orderId": ""
        }
        result = handler(event)
        self.assertEqual(result["statusCode"], 200)
    
    def test_unicode_content(self):
        """Test handler with unicode content."""
        event = {
            "paymentId": "PAY-日本語",
            "customer": {"name": "张三"

