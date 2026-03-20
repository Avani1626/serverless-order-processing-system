
module "sqs" {
  source     = "./modules/sqs"
  queue_name = "order-queue"
  dlq_name   = "order-dlq"
}
output "sqs_queue_url" {
  value = module.sqs.queue_url
}

module "lambda" {
  source = "./modules/lambda"

  function_name = "order-handler-terraform"
  filename      = "../lambdas/order-handler/order-handler.zip"
  handler       = "index.handler"
  runtime       = "python3.12"
  role_arn      = "arn:aws:iam::368096590367:role/lambda-execution-role-manual"

  sqs_queue_url = module.sqs.queue_url
}

module "dynamodb" {
  source = "./modules/dynamodb"

  table_name = "orders"
  hash_key   = "order_id"
}