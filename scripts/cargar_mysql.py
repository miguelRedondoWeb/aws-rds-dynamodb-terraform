
# Ejercicio 6 - Cargar datos en Amazon RDS MySQL

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

    # Obtener informacion de RDS
    rds = session.client("rds")
    response = rds.describe_db_instances(
        DBInstanceIdentifier=DB_IDENTIFIER
    )
    db = response["DBInstances"][0]

    # Recuperar credenciales desde Secrets Manager
    secrets_client = session.client("secretsmanager")
    secret_response = secrets_client.get_secret_value(
        SecretId=db["MasterUserSecret"]["SecretArn"]
    )
    credentials = json.loads(secret_response["SecretString"])

    # Leer datos JSON
    clientes = json.loads(
        (project_dir / "data" / "clientes.json").read_text(
            encoding="utf-8"
        )
    )
    pedidos = json.loads(
        (project_dir / "data" / "pedidos.json").read_text(
            encoding="utf-8"
        )
    )

    # Preparar TLS
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
        connect_timeout=10
    )

    try:
        with connection.cursor() as cursor:

            # Insertar clientes
            for cliente in clientes:
                cursor.execute(
                    """
                    INSERT INTO clientes
                    (cliente_id, nombre, ciudad)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        nombre = VALUES(nombre),
                        ciudad = VALUES(ciudad)
                    """,
                    (
                        cliente["cliente_id"],
                        cliente["nombre"],
                        cliente["ciudad"]
                    )
                )

            # Insertar pedidos
            for pedido in pedidos:
                cursor.execute(
                    """
                    INSERT INTO pedidos
                    (pedido_id, cliente_id, producto, importe)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        cliente_id = VALUES(cliente_id),
                        producto = VALUES(producto),
                        importe = VALUES(importe)
                    """,
                    (
                        pedido["pedido_id"],
                        pedido["cliente_id"],
                        pedido["producto"],
                        pedido["importe"]
                    )
                )

        connection.commit()
        print("Datos cargados correctamente en MySQL.")

        # Comprobar registros
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM clientes")
            total_clientes = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM pedidos")
            total_pedidos = cursor.fetchone()[0]

        print(f"Clientes: {total_clientes}")
        print(f"Pedidos: {total_pedidos}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
