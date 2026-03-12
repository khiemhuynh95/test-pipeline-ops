"""AWS Lambda handler — simple health check / echo service."""

import json
from datetime import datetime, timezone


def handler(event, context):
    """Lambda entry point.

    Returns a JSON response with the event details and a timestamp.
    Handles potential None values gracefully to prevent NullPointerExceptions.
    """
    # Safely handle event being None or missing required fields
    if event is None:
        event = {}
    
    # Extract message safely without assuming it exists
    raw_message = getattr(event, 'rawMessage', None)
    if raw_message and isinstance(raw_message, str):
        try:
            parsed = json.loads(raw_message)
            body = {
                "message": f"Hello from PipelineOps! Event: {parsed}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": event,
            }
        except (json.JSONDecodeError, TypeError):
            # Fallback if rawMessage is not valid JSON
            body = {
                "message": "Hello from PipelineOps!",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": event,
            }
    else:
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
