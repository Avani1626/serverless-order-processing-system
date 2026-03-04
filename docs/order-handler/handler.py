import json

def lambda_handler(event, context):

    print("Received event:", event)

    response = {
        "message": "Order received successfully",
        "input": event
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }