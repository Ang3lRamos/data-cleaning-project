
-- ===================================================================
-- CONSULTAS SQL UTILES PARA EL PROYECTO
-- Base de datos: retail_sales.db
-- ===================================================================

-- 1. Revenue total por categoria
SELECT 
    Categoria_Producto,
    Revenue_Total,
    Num_Transacciones,
    ROUND(Revenue_Total * 100.0 / SUM(Revenue_Total) OVER(), 2) as Porcentaje_Revenue
FROM ventas_por_categoria
ORDER BY Revenue_Total DESC;

-- 2. Top 20 mejores clientes
SELECT 
    Cliente_ID,
    Total_Gastado,
    Num_Compras,
    ROUND(Ticket_Promedio, 2) as Ticket_Promedio,
    Genero,
    Edad
FROM resumen_clientes
ORDER BY Total_Gastado DESC
LIMIT 20;

-- 3. Ventas por metodo de pago
SELECT 
    Metodo_Pago,
    COUNT(*) as Num_Transacciones,
    SUM(Precio_Total) as Revenue_Total,
    ROUND(AVG(Precio_Total), 2) as Ticket_Promedio
FROM ventas
GROUP BY Metodo_Pago
ORDER BY Revenue_Total DESC;

-- 4. Distribucion de ventas por edad
SELECT 
    CASE 
        WHEN Edad BETWEEN 18 AND 25 THEN '18-25'
        WHEN Edad BETWEEN 26 AND 35 THEN '26-35'
        WHEN Edad BETWEEN 36 AND 50 THEN '36-50'
        ELSE '51+'
    END as Rango_Edad,
    COUNT(*) as Num_Transacciones,
    SUM(Precio_Total) as Revenue_Total
FROM ventas
GROUP BY Rango_Edad
ORDER BY Revenue_Total DESC;

-- 5. Productos mas vendidos por cantidad
SELECT 
    Categoria_Producto,
    SUM(Cantidad) as Total_Unidades,
    COUNT(*) as Num_Transacciones,
    ROUND(AVG(Precio_Unitario), 2) as Precio_Promedio
FROM ventas
GROUP BY Categoria_Producto
ORDER BY Total_Unidades DESC;

-- 6. Analisis temporal (si tienes columnas de fecha)
SELECT 
    strftime('%Y-%m', Fecha) as Año_Mes,
    COUNT(*) as Num_Transacciones,
    SUM(Precio_Total) as Revenue
FROM ventas
GROUP BY Año_Mes
ORDER BY Año_Mes;

-- 7. Clientes frecuentes (mas de 5 compras)
SELECT 
    Cliente_ID,
    Num_Compras,
    Total_Gastado,
    Genero
FROM resumen_clientes
WHERE Num_Compras > 5
ORDER BY Num_Compras DESC;

-- 8. Revenue promedio por categoria y genero
SELECT 
    Categoria_Producto,
    Genero,
    COUNT(*) as Num_Transacciones,
    ROUND(AVG(Precio_Total), 2) as Ticket_Promedio
FROM ventas
GROUP BY Categoria_Producto, Genero
ORDER BY Ticket_Promedio DESC;

-- 9. Verificar integridad de datos
SELECT 
    COUNT(*) as Total_Registros,
    COUNT(DISTINCT Transaction_ID) as Transacciones_Unicas,
    COUNT(DISTINCT Cliente_ID) as Clientes_Unicos
FROM ventas;

-- 10. Estadisticas generales
SELECT 
    COUNT(*) as Total_Transacciones,
    ROUND(SUM(Precio_Total), 2) as Revenue_Total,
    ROUND(AVG(Precio_Total), 2) as Ticket_Promedio,
    ROUND(MIN(Precio_Total), 2) as Venta_Minima,
    ROUND(MAX(Precio_Total), 2) as Venta_Maxima
FROM ventas;
