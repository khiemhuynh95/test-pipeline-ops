"""AWS Lambda handler — simple health check / echo service."""

import json
from datetime import datetime, timezone


def handler(event, context):
    """Lambda entry point.

    Returns a JSON response with the event details and a timestamp.

    Handles edge cases including missing or null event data gracefully.
    """
    # Handle missing/null event parameter safely
    if not event:
        body = {
            "message": "No event data provided",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": "event is null or empty",
        }
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body),
        }

    # Handle missing keys in event with defaults
    body = {
        "message": "Hello from PipelineOps!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "input_details": {
            "httpMethod": event.get("httpMethod", "unknown"),
            "path": event.get("path", "/"),
            "queryStringParameters": event.get("queryStringParameters", None),
        }
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }