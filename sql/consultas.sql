
-- Ejercicio 6 - Bases de datos en AWS
-- Consultas para Amazon RDS MySQL

-- Consulta 1: Mostrar todos los clientes
SELECT *
FROM clientes;

-- Consulta 2: Mostrar todos los pedidos
SELECT *
FROM pedidos;

-- Consulta 3: Relacionar clientes con sus pedidos
SELECT
    c.nombre,
    c.ciudad,
    p.pedido_id,
    p.producto,
    p.importe
FROM clientes c
INNER JOIN pedidos p
    ON c.cliente_id = p.cliente_id
ORDER BY c.nombre, p.pedido_id;

-- Consulta 4: Calcular pedidos e importe total por cliente
SELECT
    c.cliente_id,
    c.nombre,
    COUNT(p.pedido_id) AS total_pedidos,
    COALESCE(SUM(p.importe), 0) AS importe_total
FROM clientes c
LEFT JOIN pedidos p
    ON c.cliente_id = p.cliente_id
GROUP BY c.cliente_id, c.nombre
ORDER BY importe_total DESC;
