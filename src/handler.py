"""AWS Lambda handler — simple health check / echo service."""

import json
from datetime import datetime, timezone


def handler(event, context):
    """Lambda entry point.

    Returns a JSON response with the event details and a timestamp.
    Handles potential null/None inputs gracefully to prevent NullPointerExceptions.
    """
    # Defensive programming: handle None/null event gracefully
    safe_event = event if event is not None else {}
    
    # Ensure we have at least an empty dict for event data
    if isinstance(event, (dict, list)):
        event_data = {k: v for k, v in safe_event.items() if v is not None}
    elif isinstance(event, str):
        try:
            event_data = json.loads(event) or {}
        except (json.JSONDecodeError, TypeError):
            event_data = {}
    else:
        event_data = {}

    body = {
        "message": "Hello from PipelineOps!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": str(event_data) if event_data else "(empty/null)",
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }