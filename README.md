# AWS Databases — Amazon RDS MySQL & DynamoDB

## Overview

Exercise 6 for IFCD0078 — Cloud & Data Engineering (November 2026).

Deployment, data loading, queries and cleanup of relational and NoSQL databases in AWS Europe (Spain), `eu-south-2`. The infrastructure was deployed for the exercise and subsequently destroyed.

## Objectives and outcomes

- Provision Amazon RDS MySQL 8.4.13 and a DynamoDB table with Terraform.
- Load the same four customers and five orders from JSON files.
- Run MySQL `JOIN` and `GROUP BY` queries.
- Demonstrate DynamoDB `GetItem`, `Query` and `Scan`.
- Create, verify and delete a manual RDS snapshot.
- Destroy the infrastructure and verify that the exercise resources are absent.

All exercise tasks were completed and checked. Evidence and the reasoned comparison are documented in [`docs/evidencias.pdf`](docs/evidencias.pdf).

## Architecture

- **RDS MySQL:** a relational `tienda` database with `clientes` and `pedidos` tables connected by a foreign key.
- **DynamoDB:** a single table `clientes-pedidos-ejercicio6`, keyed by `PK` (for example `CLIENTE#1`) and `SK` (`PERFIL` or `PEDIDO#101`).
- **Network:** existing VPC, a DB subnet group and a security group permitting MySQL traffic only from a configured IPv4 `/32` during the exercise.
- **Authentication:** AWS CLI `terraform` profile, temporary credentials and an RDS-managed secret in Secrets Manager; TLS verified for MySQL.

## Technologies

Terraform 1.16.6, AWS Provider 5.100.0, AWS CLI 2.38.4, Amazon RDS MySQL 8.4.13, DynamoDB, Python 3.11.9, PyMySQL, boto3, SQL, Git and VS Code.

## Project structure

```text
.
├── terraform/
│   ├── main.tf
│   ├── dynamodb.tf
│   ├── network.tf
│   ├── rds.tf
│   ├── variables.tf
│   ├── terraform.tfvars.example
│   └── .terraform.lock.hcl
├── data/
│   ├── clientes.json
│   ├── pedidos.json
│   ├── get-item-key.json
│   └── query-values.json
├── sql/
│   ├── schema.sql
│   └── consultas.sql
├── scripts/
│   ├── conectar_mysql.py
│   ├── crear_tablas.py
│   ├── cargar_mysql.py
│   ├── consultar_mysql.py
│   └── cargar_dynamodb.py
├── docs/
│   ├── modelo-datos.md
│   └── evidencias.pdf
├── requirements.txt
├── .gitignore
└── README.md
```

## Reproduction outline

> **Cost notice:** running `terraform apply` provisions billable cloud resources. Review the expected costs and permissions first. Never leave exercise resources running unnecessarily.

1. Configure an AWS CLI profile and temporary credentials, with permissions for RDS, DynamoDB, VPC and Secrets Manager.
2. Update the account-specific network identifiers in `terraform/network.tf`. Copy `terraform.tfvars.example` to the ignored local file `terraform.tfvars` and set the authorized current public IPv4 in CIDR `/32` form.
3. In `terraform/`, run `terraform init`, `terraform fmt`, `terraform validate`, `terraform plan`, and only after reviewing the plan, `terraform apply`.
4. In the project root, create and activate a Python virtual environment, then run `python -m pip install -r requirements.txt`.
5. Download the public RDS CA trust bundle from AWS into the local `certs/global-bundle.pem` path (the `.pem` file is intentionally excluded from Git). Run `python scripts/conectar_mysql.py`, `python scripts/crear_tablas.py`, `python scripts/cargar_mysql.py`, and `python scripts/consultar_mysql.py`.
6. Run `python scripts/cargar_dynamodb.py`, then execute the AWS CLI `get-item`, `query` and `scan` requests described in the PDF evidence report.
7. Create and verify a manual RDS snapshot, then delete it.
8. Run `terraform destroy` and verify that the RDS instance, DynamoDB table, manual snapshot and associated resources no longer exist.

## Results

The MySQL query combining `LEFT JOIN`, `GROUP BY`, `COUNT` and `SUM` returned:
- Ana Martin: 2 orders, EUR 875
- Luis Garcia: 1 order, EUR 220
- Marta Lopez: 2 orders, EUR 160
- Carlos Ruiz: 0 orders, EUR 0

DynamoDB `GetItem` returned Ana's profile, `Query` returned her two orders, and `Scan` counted nine items.

Terraform reported `Destroy complete! Resources: 4 destroyed.` The local Terraform state was empty, and follow-up AWS calls reported the databases as not found.

## RDS vs DynamoDB

RDS MySQL makes relational joins, grouping and ad hoc aggregation straightforward. DynamoDB provides direct keyed reads and efficient queries when its partition and sort keys are designed around known access patterns. DynamoDB does not provide the same relational JOIN workflow; grouped totals require application-side processing or maintained aggregates for this design.

## Security and cleanup

Do not commit `terraform.tfvars`, `.tfstate`, `.env`, credentials or the Python virtual environment. The exercise used restricted public MySQL access to a single IP and TLS; it is not intended as a production configuration. The observed manual snapshot was unencrypted, which is documented as a limitation in the evidence report. The manual snapshot and deployed infrastructure were removed after testing.

## Academic context

IFCD0078 — Architecture and Development of Cloud Systems & Data Engineering. Exercise 6: Databases on AWS, November 2026.
