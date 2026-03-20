resource "aws_s3_bucket" "terraform_state" {
  bucket = "serverless-order-system-tf-state-avani-001"

  tags = {
    Name        = "Terraform State Bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-lock-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "Terraform Lock Table"
    Environment = "Dev"
  }
}
terraform {
  backend "s3" {
    bucket         = "serverless-order-system-tf-state-avani-001"
    key            = "serverless-order-system/terraform.tfstate"
    region         = "us-east-1"   # ✅ FIXED
    dynamodb_table = "terraform-lock-table"
  }
}