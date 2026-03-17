resource "aws_lambda_function" "order_handler" {
  function_name = "order-handler-terraform"

  filename      = "../lambdas/order-handler/order-handler.zip"
  handler       = "index.handler"
  runtime       = "python3.12"

  role = "arn:aws:iam::368096590367:role/lambda-execution-role-manual"

  source_code_hash = filebase64sha256("../lambdas/order-handler/order-handler.zip")
}