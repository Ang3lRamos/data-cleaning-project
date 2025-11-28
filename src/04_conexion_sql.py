"""
04_conexion_sql.py
==================
Script para cargar los datos limpios a una base de datos SQL.
Utiliza SQLAlchemy.

Autor: Angel Ramos
Fecha: 2025-11-28
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os

class ConectorSQL:
    """
    Clase para manejar la conexión y carga de datos a SQL
    """
    
    def __init__(self, ruta_datos_limpios, ruta_db='data/retail_sales.db'):
        self.ruta_datos = ruta_datos_limpios
        self.ruta_db = ruta_db
        self.engine = None
        self.df = None
        
    def crear_conexion(self):
        """
        Crea la conexión a la base de datos SQLite
        """
        print("Creando conexion a la base de datos")
        
        try:
            # Crear carpeta si no existe
            carpeta_db = os.path.dirname(self.ruta_db)
            if carpeta_db:
                os.makedirs(carpeta_db, exist_ok=True)
            
            # Crear engine de SQLAlchemy
            self.engine = create_engine(f'sqlite:///{self.ruta_db}')
            
            print(f"Conexion establecida: {self.ruta_db}")
            return True
            
        except Exception as e:
            print(f"Error al crear conexion: {e}")
            return False
    
    def cargar_datos(self):
        """
        Carga los datos limpios desde CSV
        """
        print("\nCargando datos limpios")
        
        try:
            self.df = pd.read_csv(self.ruta_datos)
            print(f"Datos cargados: {self.df.shape[0]} registros, {self.df.shape[1]} columnas")
            return True
        except FileNotFoundError:
            print(f"Error: No se encontro {self.ruta_datos}")
            print("Ejecuta primero limpieza.py")
            return False
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return False
    
    def crear_tabla_ventas(self):
        """
        Carga la tabla principal de ventas
        """
        print("\n" + "="*60)
        print("CREANDO TABLA: ventas")
        print("="*60)
        
        try:
            # Cargar datos a SQL
            self.df.to_sql(
                'ventas',
                self.engine,
                if_exists='replace',
                index=False,
                chunksize=500
            )
            
            print(f"Tabla 'ventas' creada exitosamente")
            print(f"Registros insertados: {len(self.df)}")
            
            # Verificar
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) as total FROM ventas"))
                count = result.fetchone()[0]
                print(f"Verificacion: {count} registros en la tabla")
            
            return True
            
        except Exception as e:
            print(f"Error al crear tabla ventas: {e}")
            return False
    
    def crear_tabla_agregada_categoria(self):
        """
        Crea tabla agregada por categoría
        """
        print("\n" + "="*60)
        print("CREANDO TABLA: ventas_por_categoria")
        print("="*60)
        
        try:
            # Agregar por categoría
            ventas_categoria = self.df.groupby('Categoria_Producto').agg({
                'Precio_Total': ['sum', 'mean', 'count'],
                'Cantidad': 'sum'
            }).reset_index()
            
            ventas_categoria.columns = [
                'Categoria_Producto',
                'Revenue_Total',
                'Ticket_Promedio',
                'Num_Transacciones',
                'Unidades_Vendidas'
            ]
            
            # Cargar a SQL
            ventas_categoria.to_sql(
                'ventas_por_categoria',
                self.engine,
                if_exists='replace',
                index=False
            )
            
            print(f"Tabla 'ventas_por_categoria' creada exitosamente")
            print(f"Categorias: {len(ventas_categoria)}")
            
            return True
            
        except Exception as e:
            print(f"Error al crear tabla de categorias: {e}")
            return False
    
    def crear_tabla_agregada_clientes(self):
        """
        Crea tabla agregada por cliente
        """
        print("\n" + "="*60)
        print("CREANDO TABLA: resumen_clientes")
        print("="*60)
        
        try:
            # Agregar por cliente
            resumen_clientes = self.df.groupby('Cliente_ID').agg({
                'Precio_Total': ['sum', 'mean', 'count'],
                'Genero': 'first',
                'Edad': 'first'
            }).reset_index()
            
            resumen_clientes.columns = [
                'Cliente_ID',
                'Total_Gastado',
                'Ticket_Promedio',
                'Num_Compras',
                'Genero',
                'Edad'
            ]
            
            # Cargar a SQL
            resumen_clientes.to_sql(
                'resumen_clientes',
                self.engine,
                if_exists='replace',
                index=False
            )
            
            print(f"Tabla 'resumen_clientes' creada exitosamente")
            print(f"Clientes: {len(resumen_clientes)}")
            
            return True
            
        except Exception as e:
            print(f"Error al crear tabla de clientes: {e}")
            return False
    
    def ejecutar_consultas_ejemplo(self):
        """
        Ejecuta algunas consultas SQL de ejemplo
        """
        print("\n" + "="*60)
        print("EJECUTANDO CONSULTAS SQL DE EJEMPLO")
        print("="*60)
        
        consultas = [
            {
                'nombre': 'Top 5 Categorias por Revenue',
                'sql': """
                    SELECT 
                        Categoria_Producto,
                        Revenue_Total,
                        Num_Transacciones
                    FROM ventas_por_categoria
                    ORDER BY Revenue_Total DESC
                    LIMIT 5
                """
            },
            {
                'nombre': 'Top 10 Clientes',
                'sql': """
                    SELECT 
                        Cliente_ID,
                        Total_Gastado,
                        Num_Compras,
                        Ticket_Promedio
                    FROM resumen_clientes
                    ORDER BY Total_Gastado DESC
                    LIMIT 10
                """
            },
            {
                'nombre': 'Estadisticas por Genero',
                'sql': """
                    SELECT 
                        Genero,
                        COUNT(*) as Num_Transacciones,
                        SUM(Precio_Total) as Revenue_Total,
                        AVG(Precio_Total) as Ticket_Promedio
                    FROM ventas
                    GROUP BY Genero
                    ORDER BY Revenue_Total DESC
                """
            }
        ]
        
        for consulta in consultas:
            print(f"\n{consulta['nombre']}:")
            print("-" * 60)
            
            try:
                resultado = pd.read_sql(consulta['sql'], self.engine)
                print(resultado.to_string(index=False))
            except Exception as e:
                print(f"Error al ejecutar consulta: {e}")
    
    def guardar_consultas_sql(self):
        """
        Guarda consultas SQL útiles en un archivo
        """
        print("\n" + "="*60)
        print("GUARDANDO CONSULTAS SQL")
        print("="*60)
        
        consultas_sql = """
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
"""
        
        carpeta_sql = 'data-cleaning-project/sql'
        os.makedirs(carpeta_sql, exist_ok=True)
        
        ruta_consultas = f'{carpeta_sql}/consultas.sql'
        with open(ruta_consultas, 'w', encoding='utf-8') as f:
            f.write(consultas_sql)
        
        print(f"Consultas guardadas en: {ruta_consultas}")
    
    def generar_reporte_final(self):
        """
        Genera reporte final de la carga
        """
        print("\n" + "="*60)
        print("REPORTE FINAL - CARGA A BASE DE DATOS")
        print("="*60)
        
        print(f"\nBase de datos: {self.ruta_db}")
        print(f"Tamaño del archivo: {os.path.getsize(self.ruta_db) / 1024:.2f} KB")
        
        # Listar tablas
        with self.engine.connect() as conn:
            result = conn.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ))
            tablas = [row[0] for row in result]
        
        print("\nTablas creadas:")
        for tabla in tablas:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {tabla}"))
                count = result.fetchone()[0]
                print(f"  - {tabla}: {count} registros")
        
        print("\n" + "="*60)
        print("Carga completada exitosamente")
        print("="*60)
        print("\nAhora puedes conectarte a la base de datos con:")
        print(f"  sqlite3 {self.ruta_db}")
        print("\nO usar cualquier cliente SQL para explorar los datos")
    
    def ejecutar_carga_completa(self):
        """
        Ejecuta el proceso completo de carga a SQL
        """
        print("\nINICIANDO CARGA DE DATOS A BASE DE DATOS SQL\n")
        
        if not self.crear_conexion():
            return False
        
        if not self.cargar_datos():
            return False
        
        # Crear tablas
        self.crear_tabla_ventas()
        self.crear_tabla_agregada_categoria()
        self.crear_tabla_agregada_clientes()
        
        # Ejecutar consultas de ejemplo
        self.ejecutar_consultas_ejemplo()
        
        # Guardar consultas
        self.guardar_consultas_sql()
        
        # Reporte final
        self.generar_reporte_final()
        
        return True
    
    def cerrar_conexion(self):
        """
        Cierra la conexión a la base de datos
        """
        if self.engine:
            self.engine.dispose()
            print("\nConexion cerrada")

def main():
    """
    Función principal
    """
    conector = ConectorSQL('data-cleaning-project/data/processed/retail_sales_clean.csv')
    
    try:
        conector.ejecutar_carga_completa()
    finally:
        conector.cerrar_conexion()
    
    print("\nPipeline completado:")
    print("  1. Datos generados")
    print("  2. Datos limpiados")
    print("  3. Datos procesados")
    print("  4. Datos cargados a SQL")
    print("\nProximo paso: Crear README.md y subir a GitHub")

if __name__ == "__main__":
    main()