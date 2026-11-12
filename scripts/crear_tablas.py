
# Ejercicio 6 - Crear tablas en Amazon RDS MySQL

import json
import ssl
from pathlib import Path

import boto3
import pymysql

REGION = "eu-south-2"
PROFILE = "terraform"
DB_IDENTIFIER = "ejercicio6-mysql"


def main():
    project_dir = Path(__file__).resolve().parent.parent

    # Crear sesion AWS
    session = boto3.Session(
        profile_name=PROFILE,
        region_name=REGION
    )

    # Obtener datos de RDS
    rds = session.client("rds")

    response = rds.describe_db_instances(
        DBInstanceIdentifier=DB_IDENTIFIER
    )

    db = response["DBInstances"][0]

    endpoint = db["Endpoint"]["Address"]
    port = db["Endpoint"]["Port"]

    # Recuperar credenciales de Secrets Manager
    secrets_client = session.client("secretsmanager")

    secret_response = secrets_client.get_secret_value(
        SecretId=db["MasterUserSecret"]["SecretArn"]
    )

    credentials = json.loads(
        secret_response["SecretString"]
    )

    # Preparar conexion TLS
    ssl_context = ssl.create_default_context(
        cafile=str(project_dir / "certs" / "global-bundle.pem")
    )

    # Conectar a MySQL
    connection = pymysql.connect(
        host=endpoint,
        port=port,
        user=credentials["username"],
        password=credentials["password"],
        database="tienda",
        ssl=ssl_context,
        connect_timeout=10
    )

    try:
        # Leer el archivo SQL
        schema_file = project_dir / "sql" / "schema.sql"

        sql_script = schema_file.read_text(
            encoding="utf-8"
        )

        # Separar las instrucciones SQL
        statements = [
            statement.strip()
            for statement in sql_script.split(";")
            if statement.strip()
        ]

        # Ejecutar las instrucciones
        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)

        connection.commit()

        print("Tablas creadas correctamente.")

        # Comprobar las tablas
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")

            for table in cursor.fetchall():
                print(f"Tabla: {table[0]}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
