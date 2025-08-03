output "vpc_id" {
  description = "The ID of the VPC."
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of IDs of public subnets."
  value       = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

output "private_subnet_ids" {
  description = "List of IDs of private subnets."
  value       = [aws_subnet.private_a.id, aws_subnet.private_b.id]
}

output "ecr_repository_url" {
  description = "The URL of the ECR repository."
  value       = aws_ecr_repository.api.repository_url
}

output "alb_security_group_id" {
  description = "The ID of the ALB's security group."
  value       = aws_security_group.alb.id
}

output "ecs_service_security_group_id" {
  description = "The ID of the ECS service's security group."
  value       = aws_security_group.ecs_service.id
}

output "db_endpoint" {
  description = "The connection endpoint for the RDS instance."
  value       = aws_db_instance.main.endpoint
}
