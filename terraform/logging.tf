resource "aws_cloudwatch_log_group" "api" {
  name              = "/ecs/embedding-studio-api"
  retention_in_days = 7

  tags = {
    Name = "embedding-studio-api-logs"
  }
}
