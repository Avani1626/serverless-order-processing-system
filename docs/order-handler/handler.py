import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('orders')

def lambda_handler(event, context):

    print("Received event:", event)

    order_id = str(uuid.uuid4())

    order_data = {
        "orderId": order_id,
        "status": "RECEIVED"
    }

    table.put_item(Item=order_data)

    response = {
        "message": "Order stored successfully",
        "orderId": order_id
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }