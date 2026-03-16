provider "aws"{
    region = "us-east-1"
}

resource "aws_dynamodb_table" "orders"{
    name =    "orders_terraform"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "order_id"

    attribute{
        name = "order_id"
        type = "S"
    }
}