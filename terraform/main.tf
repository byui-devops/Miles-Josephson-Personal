terraform {
  required_version = ">= 1.8"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # S3 backend for state — matches your ITM 300 lab experience
  backend "s3" {
    bucket = "jdm-legacy-tfstate"   # create this bucket manually first
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# ── Data Sources ────────────────────────────────────────────────────────────

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

# ── Security Groups ─────────────────────────────────────────────────────────

resource "aws_security_group" "ec2_sg" {
  name        = "jdm-legacy-ec2-sg"
  description = "Allow HTTP and SSH for JDM Legacy EC2"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "App port"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "jdm-legacy-ec2-sg" }
}

resource "aws_security_group" "rds_sg" {
  name        = "jdm-legacy-rds-sg"
  description = "Allow PostgreSQL from EC2 only"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description     = "PostgreSQL from EC2"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "jdm-legacy-rds-sg" }
}

# ── RDS PostgreSQL ──────────────────────────────────────────────────────────

resource "aws_db_instance" "postgres" {
  identifier        = "jdm-legacy-db"
  engine            = "postgres"
  engine_version    = "16"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  storage_type      = "gp2"

  db_name  = "jdmlegacy"
  username = "jdmuser"
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot    = true
  publicly_accessible    = false

  tags = { Name = "jdm-legacy-db" }
}

# ── EC2 Instance ────────────────────────────────────────────────────────────

resource "aws_instance" "app" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    systemctl start docker
    systemctl enable docker

    # Pull and run the JDM Legacy container
    docker pull ${var.dockerhub_username}/jdm-legacy:${var.image_tag}
    docker run -d \
      --name jdm-legacy \
      --restart always \
      -p 5000:5000 \
      -e DATABASE_URL="postgresql://jdmuser:${var.db_password}@${aws_db_instance.postgres.address}:5432/jdmlegacy" \
      ${var.dockerhub_username}/jdm-legacy:${var.image_tag}
  EOF

  tags = { Name = "jdm-legacy-app" }

  depends_on = [aws_db_instance.postgres]
}
