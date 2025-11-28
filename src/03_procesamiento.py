"""
03_procesamiento.py
===================
Script para realizar procesamiento avanzado y análisis de los datos limpios.
Genera métricas de negocio, agregaciones y estadísticas descriptivas.

Autor: Angel Ramos
Fecha: 2025-11-28
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

class ProcesadorDatos:
    """
    Clase para procesar y analizar datos limpios
    """
    
    def __init__(self, ruta_datos_limpios):
        self.ruta_datos = ruta_datos_limpios
        self.df = None
        self.metricas = {}
        
    def cargar_datos(self):
        """
        Carga los datos limpios
        """
        print("Cargando datos limpios")
        try:
            self.df = pd.read_csv(self.ruta_datos)
            # Convertir fecha a datetime
            self.df['Fecha'] = pd.to_datetime(self.df['Fecha'])
            print(f"Datos cargados correctamente: {self.df.shape[0]} registros")
            return True
        except FileNotFoundError:
            print(f"Error: No se encontro el archivo {self.ruta_datos}")
            print("Ejecuta primero limpieza.py")
            return False
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return False
    
    def calcular_metricas_generales(self):
        """
        Calcula métricas generales del negocio
        """
        print("\n" + "="*60)
        print("METRICAS GENERALES DEL NEGOCIO")
        print("="*60)
        
        # Revenue total
        revenue_total = self.df['Precio_Total'].sum()
        self.metricas['revenue_total'] = revenue_total
        print(f"\nRevenue Total: ${revenue_total:,.2f}")
        
        # Ticket promedio
        ticket_promedio = self.df['Precio_Total'].mean()
        self.metricas['ticket_promedio'] = ticket_promedio
        print(f"Ticket Promedio: ${ticket_promedio:,.2f}")
        
        # Número de transacciones
        num_transacciones = len(self.df)
        self.metricas['num_transacciones'] = num_transacciones
        print(f"Numero de Transacciones: {num_transacciones:,}")
        
        # Clientes únicos
        clientes_unicos = self.df['Cliente_ID'].nunique()
        self.metricas['clientes_unicos'] = clientes_unicos
        print(f"Clientes Unicos: {clientes_unicos:,}")
        
        # Productos vendidos
        productos_vendidos = self.df['Cantidad'].sum()
        self.metricas['productos_vendidos'] = productos_vendidos
        print(f"Productos Vendidos: {productos_vendidos:,}")
        
        # Precio unitario promedio
        precio_promedio = self.df['Precio_Unitario'].mean()
        print(f"Precio Unitario Promedio: ${precio_promedio:,.2f}")
    
    def analizar_por_categoria(self):
        """
        Análisis de ventas por categoría de producto
        """
        print("\n" + "="*60)
        print("ANALISIS POR CATEGORIA DE PRODUCTO")
        print("="*60)
        
        categoria_stats = self.df.groupby('Categoria_Producto').agg({
            'Precio_Total': ['sum', 'mean', 'count'],
            'Cantidad': 'sum'
        }).round(2)
        
        categoria_stats.columns = ['Revenue_Total', 'Ticket_Promedio', 'Num_Transacciones', 'Unidades_Vendidas']
        categoria_stats = categoria_stats.sort_values('Revenue_Total', ascending=False)
        
        print("\n" + categoria_stats.to_string())
        
        # Guardar para usar después
        self.metricas['ventas_por_categoria'] = categoria_stats
        
        return categoria_stats
    
    def analizar_por_genero(self):
        """
        Análisis de ventas por género
        """
        print("\n" + "="*60)
        print("ANALISIS POR GENERO")
        print("="*60)
        
        genero_stats = self.df.groupby('Genero').agg({
            'Precio_Total': ['sum', 'mean', 'count'],
            'Edad': 'mean'
        }).round(2)
        
        genero_stats.columns = ['Revenue_Total', 'Ticket_Promedio', 'Num_Transacciones', 'Edad_Promedio']
        
        print("\n" + genero_stats.to_string())
        
        self.metricas['ventas_por_genero'] = genero_stats
        
        return genero_stats
    
    def analizar_tendencias_temporales(self):
        """
        Análisis de tendencias por mes
        """
        print("\n" + "="*60)
        print("ANALISIS DE TENDENCIAS TEMPORALES")
        print("="*60)
        
        # Ventas por mes
        self.df['Año_Mes'] = self.df['Fecha'].dt.to_period('M')
        
        ventas_mensuales = self.df.groupby('Año_Mes').agg({
            'Precio_Total': 'sum',
            'Transaction_ID': 'count'
        }).round(2)
        
        ventas_mensuales.columns = ['Revenue', 'Num_Transacciones']
        
        print("\nVentas Mensuales:")
        print(ventas_mensuales.to_string())
        
        # Guardar
        self.metricas['ventas_mensuales'] = ventas_mensuales
        
        return ventas_mensuales
    
    def analizar_por_metodo_pago(self):
        """
        Análisis por método de pago
        """
        print("\n" + "="*60)
        print("ANALISIS POR METODO DE PAGO")
        print("="*60)
        
        pago_stats = self.df.groupby('Metodo_Pago').agg({
            'Precio_Total': ['sum', 'count', 'mean']
        }).round(2)
        
        pago_stats.columns = ['Revenue_Total', 'Num_Transacciones', 'Ticket_Promedio']
        pago_stats = pago_stats.sort_values('Revenue_Total', ascending=False)
        
        print("\n" + pago_stats.to_string())
        
        # Calcular porcentaje
        pago_stats['Porcentaje_Revenue'] = (pago_stats['Revenue_Total'] / pago_stats['Revenue_Total'].sum() * 100).round(2)
        
        print("\nDistribucion de Revenue por Metodo de Pago:")
        for metodo, row in pago_stats.iterrows():
            print(f"  {metodo}: {row['Porcentaje_Revenue']}%")
        
        return pago_stats
    
    def analizar_clientes(self):
        """
        Análisis de comportamiento de clientes
        """
        print("\n" + "="*60)
        print("ANALISIS DE CLIENTES")
        print("="*60)
        
        # Valor por cliente
        clientes_stats = self.df.groupby('Cliente_ID').agg({
            'Precio_Total': ['sum', 'mean', 'count']
        }).round(2)
        
        clientes_stats.columns = ['Total_Gastado', 'Ticket_Promedio', 'Num_Compras']
        
        # Top 10 clientes
        top_clientes = clientes_stats.nlargest(10, 'Total_Gastado')
        
        print("\nTop 10 Clientes por Gasto Total:")
        print(top_clientes.to_string())
        
        # Estadísticas generales de clientes
        print("\nEstadisticas de Clientes:")
        print(f"  Gasto promedio por cliente: ${clientes_stats['Total_Gastado'].mean():,.2f}")
        print(f"  Compras promedio por cliente: {clientes_stats['Num_Compras'].mean():.2f}")
        print(f"  Cliente con mayor gasto: ${clientes_stats['Total_Gastado'].max():,.2f}")
        
        return clientes_stats
    
    def crear_segmentacion_clientes(self):
        """
        Segmentación simple de clientes por valor
        """
        print("\n" + "="*60)
        print("SEGMENTACION DE CLIENTES")
        print("="*60)
        
        # Calcular valor por cliente
        valor_cliente = self.df.groupby('Cliente_ID')['Precio_Total'].sum()
        
        # Crear segmentos basados en cuartiles
        segmentos = pd.qcut(valor_cliente, q=4, labels=['Bronce', 'Plata', 'Oro', 'Platino'])
        
        segmentos_df = pd.DataFrame({
            'Valor_Total': valor_cliente,
            'Segmento': segmentos
        })
        
        # Estadísticas por segmento
        segmento_stats = segmentos_df.groupby('Segmento').agg({
            'Valor_Total': ['count', 'mean', 'sum']
        }).round(2)
        
        segmento_stats.columns = ['Num_Clientes', 'Valor_Promedio', 'Valor_Total']
        
        print("\nDistribucion por Segmento:")
        print(segmento_stats.to_string())
        
        return segmentos_df
    
    def generar_estadisticas_descriptivas(self):
        """
        Genera estadísticas descriptivas completas
        """
        print("\n" + "="*60)
        print("ESTADISTICAS DESCRIPTIVAS")
        print("="*60)
        
        columnas_numericas = ['Edad', 'Cantidad', 'Precio_Unitario', 'Precio_Total']
        
        print("\n" + self.df[columnas_numericas].describe().to_string())
    
    def crear_visualizaciones(self):
        """
        Crea visualizaciones básicas y las guarda
        """
        print("\n" + "="*60)
        print("GENERANDO VISUALIZACIONES")
        print("="*60)
        
        # Crear carpeta para gráficos
        carpeta_graficos = 'data-cleaning-project/docs/imagenes'
        os.makedirs(carpeta_graficos, exist_ok=True)
        
        # Configurar estilo
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        
        # 1. Revenue por categoría
        plt.figure(figsize=(10, 6))
        categoria_revenue = self.df.groupby('Categoria_Producto')['Precio_Total'].sum().sort_values(ascending=True)
        categoria_revenue.plot(kind='barh', color='steelblue')
        plt.title('Revenue por Categoria de Producto', fontsize=14, fontweight='bold')
        plt.xlabel('Revenue Total ($)')
        plt.ylabel('Categoria')
        plt.tight_layout()
        plt.savefig(f'{carpeta_graficos}/revenue_por_categoria.png', dpi=300)
        print(f"  Grafico guardado: revenue_por_categoria.png")
        plt.close()
        
        # 2. Distribución de edad
        plt.figure(figsize=(10, 6))
        self.df['Edad'].hist(bins=20, color='coral', edgecolor='black')
        plt.title('Distribucion de Edad de Clientes', fontsize=14, fontweight='bold')
        plt.xlabel('Edad')
        plt.ylabel('Frecuencia')
        plt.tight_layout()
        plt.savefig(f'{carpeta_graficos}/distribucion_edad.png', dpi=300)
        print(f"  Grafico guardado: distribucion_edad.png")
        plt.close()
        
        # 3. Ventas mensuales
        if 'Año_Mes' in self.df.columns:
            plt.figure(figsize=(12, 6))
            ventas_mes = self.df.groupby('Año_Mes')['Precio_Total'].sum()
            ventas_mes.plot(kind='line', marker='o', linewidth=2, color='green')
            plt.title('Tendencia de Ventas Mensuales', fontsize=14, fontweight='bold')
            plt.xlabel('Mes')
            plt.ylabel('Revenue ($)')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f'{carpeta_graficos}/tendencia_ventas.png', dpi=300)
            print(f"  Grafico guardado: tendencia_ventas.png")
            plt.close()
        
        print(f"\nVisualizaciones guardadas en: {carpeta_graficos}/")
    
    def exportar_resultados(self):
        """
        Exporta los resultados del análisis a CSV
        """
        print("\n" + "="*60)
        print("EXPORTANDO RESULTADOS")
        print("="*60)
        
        carpeta_resultados = 'data-cleaning-project/data/processed'
        
        # Exportar ventas por categoría
        if 'ventas_por_categoria' in self.metricas:
            ruta = f'{carpeta_resultados}/analisis_categoria.csv'
            self.metricas['ventas_por_categoria'].to_csv(ruta)
            print(f"  Exportado: analisis_categoria.csv")
        
        # Exportar ventas mensuales
        if 'ventas_mensuales' in self.metricas:
            ruta = f'{carpeta_resultados}/ventas_mensuales.csv'
            self.metricas['ventas_mensuales'].to_csv(ruta)
            print(f"  Exportado: ventas_mensuales.csv")
    
    def generar_reporte_final(self):
        """
        Genera reporte final del procesamiento
        """
        print("\n" + "="*60)
        print("REPORTE FINAL DE PROCESAMIENTO")
        print("="*60)
        
        print("\nRESUMEN DE METRICAS CLAVE:")
        if 'revenue_total' in self.metricas:
            print(f"  Revenue Total: ${self.metricas['revenue_total']:,.2f}")
        if 'ticket_promedio' in self.metricas:
            print(f"  Ticket Promedio: ${self.metricas['ticket_promedio']:,.2f}")
        if 'num_transacciones' in self.metricas:
            print(f"  Transacciones: {self.metricas['num_transacciones']:,}")
        if 'clientes_unicos' in self.metricas:
            print(f"  Clientes Unicos: {self.metricas['clientes_unicos']:,}")
        
        print("\n" + "="*60)
        print("Procesamiento completado exitosamente")
        print("="*60)
    
    def ejecutar_procesamiento_completo(self):
        """
        Ejecuta todo el pipeline de procesamiento
        """
        print("\nINICIANDO PROCESAMIENTO AVANZADO DE DATOS\n")
        
        if not self.cargar_datos():
            return False
        
        # Ejecutar todos los análisis
        self.calcular_metricas_generales()
        self.analizar_por_categoria()
        self.analizar_por_genero()
        self.analizar_tendencias_temporales()
        self.analizar_por_metodo_pago()
        self.analizar_clientes()
        self.crear_segmentacion_clientes()
        self.generar_estadisticas_descriptivas()
        
        # Visualizaciones y exportación
        self.crear_visualizaciones()
        self.exportar_resultados()
        
        # Reporte final
        self.generar_reporte_final()
        
        return True

def main():
    """
    Función principal
    """
    procesador = ProcesadorDatos('data/processed/retail_sales_clean.csv')
    procesador.ejecutar_procesamiento_completo()
    
    print("\nSiguiente paso: ejecutar 04_conexion_sql.py")

if __name__ == "__main__":
    main()