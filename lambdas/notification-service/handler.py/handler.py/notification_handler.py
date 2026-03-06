import json

def handler(event, context):

    print("Order completion event received")

    order_id = event["detail"]["orderId"]
    status = event["detail"]["status"]

    print(f"Order {order_id} status: {status}")
    print("Sending order confirmation notification")

    return {
        "statusCode": 200,
        "body": json.dumps("Notification sent")
    }