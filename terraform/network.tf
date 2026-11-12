
# Ejercicio 6 - Configuracion de red para Amazon RDS

# Grupo de subredes para RDS
resource "aws_db_subnet_group" "mysql" {
  name = "ejercicio6-mysql-subnets"

  subnet_ids = [
    "subnet-06c9ea8b79d4b30d3",
    "subnet-05a2c903cc74f0856",
    "subnet-0af60001d31507c96"
  ]

  tags = {
    Project = "Ejercicio-6-BBDD-AWS"
    Course  = "IFCD0078"
  }
}

# Security Group para MySQL
resource "aws_security_group" "mysql" {
  name        = "ejercicio6-mysql-sg"
  description = "Acceso restringido a MySQL para el ejercicio 6"
  vpc_id      = "vpc-087943f488e15cdad"

  ingress {
    description = "MySQL desde IP autorizada"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = [var.mi_ip_publica]
  }

  tags = {
    Project = "Ejercicio-6-BBDD-AWS"
    Course  = "IFCD0078"
  }
}
