
# Ejercicio 6 - Amazon RDS MySQL

resource "aws_db_instance" "mysql" {
  identifier = "ejercicio6-mysql"

  # Motor y capacidad
  engine            = "mysql"
  engine_version    = "8.4.13"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  storage_type      = "gp3"

  # Base de datos inicial
  db_name  = "tienda"
  username = "adminmysql"

  # AWS administra la contrasena
  manage_master_user_password = true

  # Configuracion de red
  db_subnet_group_name   = aws_db_subnet_group.mysql.name
  vpc_security_group_ids = [aws_security_group.mysql.id]
  publicly_accessible    = true

  # Configuracion para la practica
  multi_az                = false
  backup_retention_period = 0
  skip_final_snapshot     = true
  deletion_protection     = false

  tags = {
    Project = "Ejercicio-6-BBDD-AWS"
    Course  = "IFCD0078"
  }
}
