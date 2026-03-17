def handler(event, context):
    print("Received event:", event)

    return {
        "statusCode": 200,
        "body": "Order handler deployed via Terraform 🚀"
    }