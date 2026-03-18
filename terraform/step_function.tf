resource "aws_sfn_state_machine" "order_workflow" {
  name     = "order-workflow"

  role_arn = "arn:aws:iam::368096590367:role/service-role/StepFunctions-order-processing-workflow-role-4gxg8rxl1"

  definition = <<EOF
{
  "StartAt": "CheckInventory",
  "States": {
    "CheckInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:368096590367:function:inventory-check",
      "Next": "SendPaymentToQueue"
    },
    "SendPaymentToQueue": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sqs:sendMessage",
      "Parameters": {
        "QueueUrl": "https://sqs.us-east-1.amazonaws.com/368096590367/payment-processing-queue",
        "MessageBody.$": "$"
      },
      "Next": "UpdateOrderStatus"
    },
    "UpdateOrderStatus": {
      "Type": "Pass",
      "Next": "PublishOrderEvent"
    },
    "PublishOrderEvent": {
      "Type": "Task",
      "Resource": "arn:aws:states:::events:putEvents",
      "Parameters": {
        "Entries": [
          {
            "Source": "order.service",
            "DetailType": "OrderCompleted",
            "Detail.$": "$",
            "EventBusName": "default"
          }
        ]
      },
      "End": true
    }
  }
}
EOF
}