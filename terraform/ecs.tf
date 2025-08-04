resource "aws_ecs_cluster" "main" {
  name = "embedding-studio-cluster"
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs_task_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_policy" "bedrock_access" {
  name = "BedrockInvokeModelPolicy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "bedrock:InvokeModel"
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bedrock_policy_attachment" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.bedrock_access.arn
}

resource "aws_iam_policy" "secrets_manager_access" {
  name = "SecretsManagerReadDbPasswordPolicy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = "secretsmanager:GetSecretValue",
        Effect   = "Allow",
        Resource = "arn:aws:secretsmanager:us-east-1:215288576473:secret:embedding-studio/db-password-*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "secrets_manager_policy_attachment" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.secrets_manager_access.arn
}

resource "aws_ecs_task_definition" "api" {
  family                   = "embedding-studio-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "embedding-studio-api"
      image     = aws_ecr_repository.api.repository_url
      cpu       = 256
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.api.name,
          "awslogs-region"        = var.aws_region,
          "awslogs-stream-prefix" = "ecs"
        }
      }
      secrets = [
        {
          "name" : "POSTGRES_PASSWORD",
          "valueFrom" : "arn:aws:secretsmanager:us-east-1:215288576473:secret:embedding-studio/db-password:password::"
        }
      ]
      environment = [
        { name = "POSTGRES_USER", value = "appuser" },
        { name = "POSTGRES_DB", value = "appdb" },
        { name = "POSTGRES_SERVER", value = split(":", aws_db_instance.main.endpoint)[0] },
        { name = "POSTGRES_PORT", value = "5432" },
        { name = "AWS_REGION", value = var.aws_region }
      ]
    }
  ])
}

resource "aws_ecs_service" "main" {
  name            = "embedding-studio-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  enable_execute_command = true

  network_configuration {
    subnets          = [aws_subnet.private_a.id, aws_subnet.private_b.id]
    security_groups  = [aws_security_group.ecs_service.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "embedding-studio-api"
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.http]
}
