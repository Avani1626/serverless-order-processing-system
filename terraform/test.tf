resource "aws_iam_policy" "bad_policy" {
  name = "bad-policy"

  policy = jsonencode({
    Statement = [{
      Action   = "*"
      Effect   = "Allow"
      Resource = "*"
    }]
  })
}