import json

def handler(event, context):

    print("Order completion event received")

    # Safe access (prevents crashes)
    order_id = event.get("detail", {}).get("orderId")
    status = event.get("detail", {}).get("status")

    print(f"Order {order_id} status: {status}")
    print("Sending order confirmation notification")

    return {
        "statusCode": 200,
        "body": json.dumps("Notification sent")
    }