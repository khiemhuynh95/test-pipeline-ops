"""AWS Lambda handler — simple health check / echo service."""

import json
from datetime import datetime, timezone


def handler(event, context):
    """Lambda entry point.

    Returns a JSON response with the event details and a timestamp.
    
    Handles potential None/null values for event and context gracefully.
    """
    # Handle null/None inputs to prevent NullPointerException-like errors
    if event is None:
        event = {}
    else:
        # Ensure we have an empty dict if event has no usable attributes
        if not hasattr(event, 'get'):
            try:
                # Try to extract data from various formats
                event = json.loads(json.dumps(event))
            except (TypeError, ValueError):
                event = {}
    
    body = {
        "message": "Hello from PipelineOps!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }