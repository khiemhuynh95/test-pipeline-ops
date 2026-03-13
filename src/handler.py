"""AWS Lambda handler — simple health check / echo service."""

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def handler(event: Dict[str, Any], context: Optional[Any] = None) -> Dict[str, Any]:
    """Lambda entry point.

    Returns a JSON response with the event details and a timestamp.
    
    Args:
        event: The Lambda event payload (may be null/None)
        context: The Lambda context object (optional, may be None)
    
    Returns:
        A dictionary containing statusCode, headers, and body
    """
    # Defensive null checks for input parameters
    if event is None:
        event = {}
    
    if not isinstance(event, dict):
        try:
            event = json.loads(str(event))
        except (TypeError, ValueError):
            event = {"raw": str(event)}
    
    # Safely extract nested values with defaults
    payment_id: Optional[str] = None
    if "paymentId" in event and event["paymentId"]:
        payment_id = str(event["paymentId"])
    else:
        payment_id = None
    
    amount: Optional[float] = None
    if "amount" in event and isinstance(event["amount"], (int, float)):
        amount = float(event["amount"])
    elif "amount" in event and event["amount"]:
        try:
            amount = float(str(event["amount"]))
        except (ValueError, TypeError):
            amount = None
    
    # Safely process customer information if present
    customer: Optional[Dict[str, Any]] = None
    if "customer" in event and isinstance(event["customer"], dict):
        customer = {
            "id": str(event["customer"]["id"]) if "id" in event["customer"] else None,
            "name": str(event["customer"]["name"]) if "name" in event["customer"] else None,
            "email": str(event["customer"]["email"]) if "email" in event["customer"] else None
        }
    elif "customerId" in event:
        customer = {"id": str(event["customerId"])}
    
    # Safely extract order information
    order: Optional[Dict[str, Any]] = None
    if "order" in event and isinstance(event["order"], dict):
        order = {
            "orderId": str(event["order"]["orderId"]) if "orderId" in event["order"] else None,
            "items": list(event["order"].get("items", [])) if "items" in event["order"] else [],
            "total": float(event["order"]["total"]) if "total" in event["order"] and isinstance(event["order"]["total"], (int, float)) else None
        }
    
    # Build response with timestamp
    body = {
        "message": "Hello from PipelineOps!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "processed": {
            "paymentId": payment_id,
            "amount": amount,
            "customer": customer,
            "order": order
        },
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }