output "ec2_public_ip" {
  description = "Public IP of the EC2 app server"
  value       = aws_instance.app.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of EC2 (use this in your report)"
  value       = aws_instance.app.public_dns
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.postgres.address
  sensitive   = true
}

output "app_url" {
  description = "URL to access your running application"
  value       = "http://${aws_instance.app.public_ip}:5000"
}
