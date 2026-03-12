"""AWS Lambda handler — simple health check / echo service."""

import json
from datetime import datetime, timezone


def handler(event, context):
    """Lambda entry point.

    Returns a JSON response with the event details and a timestamp.
    Handles edge cases where event might be None or empty.
    """
    # Defensive null check for event parameter
    if event is None:
        body = {
            "message": "Hello from PipelineOps!",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": None,
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