resource "aws_db_subnet_group" "main" {
  name       = "embedding-studio-db-subnet-group"
  subnet_ids = [aws_subnet.private_a.id, aws_subnet.private_b.id]

  tags = {
    Name = "Embedding Studio DB Subnet Group"
  }
}

resource "aws_security_group" "db" {
  name        = "embedding-studio-db-sg"
  description = "Allow inbound traffic from the ECS service"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow Postgres traffic from the ECS Service"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_service.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "embedding-studio-db-sg"
  }
}

resource "aws_db_instance" "main" {
  identifier             = "embedding-studio-db"
  allocated_storage      = 20
  instance_class         = "db.t3.micro"
  engine                 = "postgres"
  engine_version         = "16"
  username               = "appuser"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]
  publicly_accessible    = false
  skip_final_snapshot    = true

  tags = {
    Name = "embedding-studio-database"
  }
}
