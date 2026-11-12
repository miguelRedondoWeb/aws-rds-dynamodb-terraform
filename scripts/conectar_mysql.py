
# Ejercicio 6 - Conexion a Amazon RDS MySQL
# Primera fase: comprobar configuracion AWS

import boto3
import json
import ssl
from pathlib import Path
import pymysql



REGION = "eu-south-2"
PROFILE = "terraform"
DB_IDENTIFIER = "ejercicio6-mysql"


def main():
    # Crear sesion utilizando nuestro perfil AWS
    session = boto3.Session(
        profile_name=PROFILE,
        region_name=REGION
    )

    # Crear cliente para consultar Amazon RDS
    rds = session.client("rds")

    # Obtener informacion de la instancia MySQL
    response = rds.describe_db_instances(
        DBInstanceIdentifier=DB_IDENTIFIER
    )

    db = response["DBInstances"][0]

    # Consultar datos de conexion
    endpoint = db["Endpoint"]["Address"]
    port = db["Endpoint"]["Port"]
    status = db["DBInstanceStatus"]

    # Consultar estado del secreto
    secret = db["MasterUserSecret"]
    secret_status = secret["SecretStatus"]
    
    
    # Obtener el secreto administrado por Amazon RDS
    secrets_client = session.client("secretsmanager")

    secret_response = secrets_client.get_secret_value(
        SecretId=secret["SecretArn"]
    )

    credentials = json.loads(
        secret_response["SecretString"]
    )

    # Verificar los campos sin mostrar sus valores
    if credentials.get("username") and credentials.get("password"):
        print("Credenciales MySQL recuperadas correctamente.")
    else:
        raise ValueError("El secreto no contiene las credenciales esperadas.")
    

    # Localizar el certificado de confianza de Amazon RDS
    project_dir = Path(__file__).resolve().parent.parent
    ca_file = project_dir / "certs" / "global-bundle.pem"

    # Crear contexto TLS con verificacion del certificado
    ssl_context = ssl.create_default_context(
        cafile=str(ca_file)
    )

    # Conectar al servidor MySQL
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
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()[0]

            print(f"Conexion MySQL correcta. Version: {version}")

            cursor.execute("SHOW STATUS LIKE 'Ssl_cipher';")
            tls_result = cursor.fetchone()

            if tls_result and tls_result[1]:
                print(f"Conexion TLS activa: {tls_result[1]}")
            else:
                raise RuntimeError(
                    "No se ha podido verificar el cifrado TLS."
                )
    finally:
        connection.close()
        print("Conexion MySQL cerrada.")



    print("Amazon RDS MySQL")
    print("-------------------------")
    print(f"Instancia: {DB_IDENTIFIER}")
    print(f"Endpoint: {endpoint}")
    print(f"Puerto: {port}")
    print(f"Estado RDS: {status}")
    print(f"Estado del secreto: {secret_status}")

    if status == "available" and secret_status == "active":
        print("Configuracion AWS verificada correctamente.")
    else:
        print("La instancia o el secreto no estan disponibles.")


if __name__ == "__main__":
    main()
