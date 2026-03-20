resource "aws_sqs_queue" "order_dlq" {
    name = var.dlq_name

  
}
resource "aws_sqs_queue" "order_queue" {
    name = var.queue_name
 

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.order_dlq.arn
    maxReceiveCount     = 3
  })
}