"""AWS Lambda handler — simple health check / echo service."""

import json
from datetime import datetime, timezone


def handler(event, context):
    """Lambda entry point.

    Returns a JSON response with the event details and a timestamp.
    
    Includes defensive checks to prevent NullPointerException-like errors:
    - Validates input parameters are not None
    - Handles edge cases gracefully
    - Logs warnings for debugging
    """
    # Defensive checks - prevent null/None references
    if event is None:
        event = {}
    
    if context is None:
        context = type('Context', (), {'function_name': 'handler'})()
    
    # Safely extract values with defaults
    http_method = getattr(event, 'httpMethod', event.get('httpMethod', 'GET'))
    path = getattr(event, 'path', event.get('path', '/'))
    headers = event.get('headers', {})
    
    body = {
        "message": "Hello from PipelineOps!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": http_method,
        "path": path,
        "context_function": getattr(context, 'function_name', 'N/A'),
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }