
# Ejercicio 6 - Amazon DynamoDB
# Tabla de clientes y pedidos

resource "aws_dynamodb_table" "clientes_pedidos" {
  name         = "clientes-pedidos-ejercicio6"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "PK"
  range_key = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  tags = {
    Project = "Ejercicio-6-BBDD-AWS"
    Course  = "IFCD0078"
  }
}
