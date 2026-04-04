terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "docker_image" {
  description = "Docker Hub image to deploy"
  type        = string
  default     = "milesjo01/itm350:latest"
}

resource "aws_security_group" "app_sg" {
  name        = "itm350-app-sg"
  description = "Allow HTTP and SSH access to the ITM350 app"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "App port"
    from_port   = 8080
    to_port     = 8080
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
    Name = "itm350-app-sg"
  }
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

resource "aws_instance" "app" {
  ami                    = data.aws_ami.amazon_linux_2.id
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    amazon-linux-extras install docker -y
    service docker start
    usermod -a -G docker ec2-user
    docker pull ${var.docker_image}
    docker run -d -p 8080:8080 --restart=always ${var.docker_image}
  EOF

  tags = {
    Name = "ITM350-App"
  }
}

output "app_url" {
  description = "URL of the deployed application"
  value       = "http://${aws_instance.app.public_ip}:8080"
}

output "public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app.public_ip
}
