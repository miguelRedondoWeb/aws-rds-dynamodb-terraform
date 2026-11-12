
-- Ejercicio 6 - Bases de datos en AWS
-- Creacion de tablas para Amazon RDS MySQL

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL
);

-- Tabla de pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    pedido_id INT PRIMARY KEY,
    cliente_id INT NOT NULL,
    producto VARCHAR(100) NOT NULL,
    importe DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_pedidos_clientes
        FOREIGN KEY (cliente_id)
        REFERENCES clientes(cliente_id)
);
