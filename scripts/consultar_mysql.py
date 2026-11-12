
# Ejercicio 6 - Consultas SQL en Amazon RDS MySQL

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

    # Autenticacion con AWS
    session = boto3.Session(
        profile_name=PROFILE,
        region_name=REGION
    )

    # Obtener endpoint de RDS
    rds = session.client("rds")
    response = rds.describe_db_instances(
        DBInstanceIdentifier=DB_IDENTIFIER
    )
    db = response["DBInstances"][0]

    # Recuperar credenciales
    secrets_client = session.client("secretsmanager")
    secret_response = secrets_client.get_secret_value(
        SecretId=db["MasterUserSecret"]["SecretArn"]
    )
    credentials = json.loads(secret_response["SecretString"])

    # Configurar conexion TLS
    ssl_context = ssl.create_default_context(
        cafile=str(project_dir / "certs" / "global-bundle.pem")
    )

    # Conectar a MySQL
    connection = pymysql.connect(
        host=db["Endpoint"]["Address"],
        port=db["Endpoint"]["Port"],
        user=credentials["username"],
        password=credentials["password"],
        database="tienda",
        ssl=ssl_context,
        connect_timeout=10,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        # Leer archivo SQL
        sql_file = project_dir / "sql" / "consultas.sql"
        sql_script = sql_file.read_text(encoding="utf-8")

        # Separar consultas
        statements = [
            statement.strip()
            for statement in sql_script.split(";")
            if statement.strip()
        ]

        # Ejecutar consultas
        with connection.cursor() as cursor:
            for index, statement in enumerate(statements, start=1):
                cursor.execute(statement)
                results = cursor.fetchall()

                print(f"\nConsulta {index}")
                print("-" * 50)

                for row in results:
                    print(row)

    finally:
        connection.close()


if __name__ == "__main__":
    main()
