resource "aws_security_group" "alb" {
  name        = "embedding-studio-alb-sg"
  description = "Controls traffic for the Application Load Balancer"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow HTTP traffic from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "embedding-studio-alb-sg"
  }
}

resource "aws_security_group" "ecs_service" {
  name        = "embedding-studio-ecs-service-sg"
  description = "Controls traffic for the ECS Fargate service"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow traffic from the ALB on port 8000"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "embedding-studio-ecs-service-sg"
  }
}
