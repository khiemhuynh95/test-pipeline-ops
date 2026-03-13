"""AWS Lambda handler — simple health check / echo service.

import json
from datetime import datetime, timezone


def handler(event, context):
    """Lambda entry point.

    Returns a JSON response with the event details and a timestamp.

    Args:
        event: The input event object (may be None or empty)
        context: Lambda context object

    Returns:
        dict: A structured HTTP response containing statusCode, headers,
               and body as JSON string.
    """
    # Defensive check for None/null event with graceful degradation
    if event is None:
        event = {}
    
    # Safe access to nested properties with defaults
    http_method = getattr(event, 'httpMethod', '').upper() if isinstance(event, dict) else ''
    path = getattr(event, 'path', '') if isinstance(event, dict) else ''
    
    body = {
        "message": "Hello from PipelineOps!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "metadata": {
            "method": http_method,
            "path": path
        }
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", "Cache-Control": "no-cache"},
        "body": json.dumps(body),
    }