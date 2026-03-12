"""AWS Lambda handler — simple health check / echo service."""

import json
from datetime import datetime, timezone


def handler(event, context):
    """Lambda entry point.

    Returns a JSON response with the event details and a timestamp.
    
    Handles None/null events gracefully to prevent NullPointerExceptions.
    """
    # Guard against null/None event - prevents NPE when event is missing or null
    if event is None:
        body = {
            "message": "Hello from PipelineOps!",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": None,
            "warning": "Event payload was null/empty",
        }
    else:
        # Safe access with .get() to avoid KeyError on missing keys
        event_message = getattr(event, 'get', lambda x: None)('message', '')
        
        body = {
            "message": f"Hello from PipelineOps! (event message: {event_message})",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }