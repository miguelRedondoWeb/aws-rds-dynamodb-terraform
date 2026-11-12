
# Ejercicio 6 - Cargar datos en Amazon DynamoDB

import json
from decimal import Decimal
from pathlib import Path

import boto3

REGION = "eu-south-2"
PROFILE = "terraform"
TABLE_NAME = "clientes-pedidos-ejercicio6"


def main():
    project_dir = Path(__file__).resolve().parent.parent

    # Leer los mismos datos utilizados en MySQL
    clientes = json.loads(
        (project_dir / "data" / "clientes.json").read_text(
            encoding="utf-8"
        )
    )

    pedidos = json.loads(
        (project_dir / "data" / "pedidos.json").read_text(
            encoding="utf-8"
        ),
        parse_float=Decimal
    )

    # Crear sesion AWS
    session = boto3.Session(
        profile_name=PROFILE,
        region_name=REGION
    )

    # Acceder a DynamoDB
    dynamodb = session.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    # Cargar clientes y pedidos
    with table.batch_writer() as batch:

        for cliente in clientes:
            batch.put_item(
                Item={
                    "PK": f"CLIENTE#{cliente['cliente_id']}",
                    "SK": "PERFIL",
                    **cliente
                }
            )

        for pedido in pedidos:
            batch.put_item(
                Item={
                    "PK": f"CLIENTE#{pedido['cliente_id']}",
                    "SK": f"PEDIDO#{pedido['pedido_id']}",
                    **pedido
                }
            )

    print("Datos cargados correctamente en DynamoDB.")
    print(f"Clientes procesados: {len(clientes)}")
    print(f"Pedidos procesados: {len(pedidos)}")
    print(f"Total de elementos: {len(clientes) + len(pedidos)}")


if __name__ == "__main__":
    main()
