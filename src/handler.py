"""AWS Lambda handler — simple health check / echo service."""

import json
from datetime import datetime, timezone


def handler(event, context):
    """Lambda entry point.

    Returns a JSON response with the event details and a timestamp.
    """
    # Defensive null checks to prevent NullPointerException
    if event is None:
        body = {
            "message": "Hello from PipelineOps!",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "<null>",
        }
    else:
        # Safely handle nested null values in event
        event_str = event if isinstance(event, str) else str(event)
        body = {
            "message": "Hello from PipelineOps!",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event_str,
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }