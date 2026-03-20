output "queue_url" {
  value = aws_sqs_queue.order_queue.id
}

output "queue_arn" {
  value = aws_sqs_queue.order_queue.arn
}

output "dlq_arn" {
  value = aws_sqs_queue.order_dlq.arn
}