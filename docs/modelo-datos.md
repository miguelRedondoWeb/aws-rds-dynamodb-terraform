
# Data Model — Amazon RDS and DynamoDB

## Amazon RDS MySQL

Relational model with two tables:

- clientes
- pedidos

Relationship:

clientes.cliente_id = pedidos.cliente_id

One customer can have multiple orders.

## Amazon DynamoDB

Single-table design.

Table name: clientes-pedidos

Primary key:
- PK: Partition Key (String)
- SK: Sort Key (String)

### Customer items

PK = CLIENTE#<cliente_id>
SK = PERFIL

Attributes:
- cliente_id
- nombre
- ciudad

### Order items

PK = CLIENTE#<cliente_id>
SK = PEDIDO#<pedido_id>

Attributes:
- pedido_id
- cliente_id
- producto
- importe

## Access Patterns

### GetItem

Retrieve a customer profile using:

PK = CLIENTE#1
SK = PERFIL

### Query

Retrieve orders for a customer using:

PK = CLIENTE#1
SK begins_with PEDIDO#

### Scan

Retrieve all items from the table.

Scan reads through table items and is generally
less efficient than targeted key-based queries.

## Comparison

MySQL uses related tables and SQL JOIN operations.

DynamoDB stores related items under a shared
partition key, allowing queries without SQL JOIN.

The same source data will be used in both systems.
