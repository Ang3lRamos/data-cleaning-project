"""
test_procesamiento.py
=====================
Tests unitarios para el módulo de procesamiento de datos

Ejecutar con: pytest tests/test_procesamiento.py -v
"""

import pytest
import pandas as pd
from datetime import datetime


class TestCalculosMetricas:
    """
    Tests para cálculos de métricas de negocio
    """
    
    @pytest.fixture
    def df_ventas(self):
        """
        Crea un DataFrame de ventas para pruebas
        """
        data = {
            'Transaction_ID': [1, 2, 3, 4, 5],
            'Cliente_ID': [100, 101, 100, 102, 101],
            'Categoria_Producto': ['Ropa', 'Hogar', 'Ropa', 'Deportes', 'Hogar'],
            'Cantidad': [2, 1, 3, 1, 2],
            'Precio_Unitario': [50.0, 100.0, 50.0, 200.0, 100.0],
            'Precio_Total': [100.0, 100.0, 150.0, 200.0, 200.0],
            'Genero': ['Masculino', 'Femenino', 'Masculino', 'Masculino', 'Femenino'],
            'Edad': [25, 30, 25, 35, 30]
        }
        return pd.DataFrame(data)
    
    def test_revenue_total(self, df_ventas):
        """
        Test: Calcula el revenue total correctamente
        """
        revenue = df_ventas['Precio_Total'].sum()
        assert revenue == 750.0
    
    def test_ticket_promedio(self, df_ventas):
        """
        Test: Calcula el ticket promedio correctamente
        """
        ticket_promedio = df_ventas['Precio_Total'].mean()
        assert ticket_promedio == 150.0
    
    def test_clientes_unicos(self, df_ventas):
        """
        Test: Cuenta clientes únicos correctamente
        """
        clientes = df_ventas['Cliente_ID'].nunique()
        assert clientes == 3
    
    def test_productos_por_categoria(self, df_ventas):
        """
        Test: Agrupa correctamente por categoría
        """
        por_categoria = df_ventas.groupby('Categoria_Producto')['Cantidad'].sum()
        
        assert por_categoria['Ropa'] == 5
        assert por_categoria['Hogar'] == 3
        assert por_categoria['Deportes'] == 1
    
    def test_revenue_por_categoria(self, df_ventas):
        """
        Test: Calcula revenue por categoría correctamente
        """
        revenue_cat = df_ventas.groupby('Categoria_Producto')['Precio_Total'].sum()
        
        assert revenue_cat['Ropa'] == 250.0
        assert revenue_cat['Hogar'] == 300.0
        assert revenue_cat['Deportes'] == 200.0
    
    def test_transacciones_por_cliente(self, df_ventas):
        """
        Test: Cuenta transacciones por cliente
        """
        trans_cliente = df_ventas.groupby('Cliente_ID').size()
        
        assert trans_cliente[100] == 2
        assert trans_cliente[101] == 2
        assert trans_cliente[102] == 1
    
    def test_gasto_por_cliente(self, df_ventas):
        """
        Test: Calcula gasto total por cliente
        """
        gasto = df_ventas.groupby('Cliente_ID')['Precio_Total'].sum()
        
        assert gasto[100] == 250.0
        assert gasto[101] == 300.0
        assert gasto[102] == 200.0


class TestAnalisisEstadistico:
    """
    Tests para análisis estadístico
    """
    
    def test_estadisticas_descriptivas(self):
        """
        Test: Verifica cálculo de estadísticas básicas
        """
        datos = pd.Series([10, 20, 30, 40, 50])
        
        assert datos.mean() == 30.0
        assert datos.median() == 30.0
        assert datos.std() == pytest.approx(15.81, rel=0.01)
        assert datos.min() == 10
        assert datos.max() == 50
    
    def test_percentiles(self):
        """
        Test: Verifica cálculo de percentiles
        """
        datos = pd.Series(range(1, 101))  # 1 a 100
        
        assert datos.quantile(0.25) == 25.75
        assert datos.quantile(0.50) == 50.5
        assert datos.quantile(0.75) == 75.25
    
    def test_correlacion(self):
        """
        Test: Verifica cálculo de correlación
        """
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 6, 8, 10]  # Correlación perfecta
        })
        
        correlacion = df['x'].corr(df['y'])
        assert correlacion == pytest.approx(1.0, rel=0.01)


class TestSegmentacion:
    """
    Tests para segmentación de clientes
    """
    
    def test_segmentacion_por_valor(self):
        """
        Test: Verifica segmentación por valor de cliente
        """
        valores = pd.Series([100, 200, 300, 400, 500, 600, 700, 800])
        
        # Crear 4 segmentos
        segmentos = pd.qcut(valores, q=4, labels=['Bronce', 'Plata', 'Oro', 'Platino'])
        
        assert len(segmentos.unique()) == 4
        assert 'Platino' in segmentos.values
    
    def test_rangos_edad(self):
        """
        Test: Verifica creación de rangos de edad
        """
        edades = pd.Series([20, 30, 40, 50, 60])
        
        rangos = pd.cut(edades, bins=[0, 25, 35, 50, 100], labels=['18-25', '26-35', '36-50', '51+'])
        
        assert len(rangos) == 5
        assert rangos[0] == '18-25'
        assert rangos[4] == '51+'


class TestAgregaciones:
    """
    Tests para agregaciones y transformaciones
    """
    
    def test_agrupar_y_sumar(self):
        """
        Test: Verifica agrupación y suma
        """
        df = pd.DataFrame({
            'categoria': ['A', 'B', 'A', 'B', 'A'],
            'ventas': [100, 200, 150, 250, 200]
        })
        
        resultado = df.groupby('categoria')['ventas'].sum()
        
        assert resultado['A'] == 450
        assert resultado['B'] == 450
    
    def test_multiples_agregaciones(self):
        """
        Test: Verifica múltiples funciones de agregación
        """
        df = pd.DataFrame({
            'categoria': ['A', 'A', 'B', 'B'],
            'ventas': [100, 200, 150, 250]
        })
        
        resultado = df.groupby('categoria')['ventas'].agg(['sum', 'mean', 'count'])
        
        assert resultado.loc['A', 'sum'] == 300
        assert resultado.loc['A', 'mean'] == 150
        assert resultado.loc['A', 'count'] == 2
    
    def test_pivot_table(self):
        """
        Test: Verifica creación de tabla pivot
        """
        df = pd.DataFrame({
            'categoria': ['A', 'B', 'A', 'B'],
            'mes': [1, 1, 2, 2],
            'ventas': [100, 200, 150, 250]
        })
        
        pivot = df.pivot_table(values='ventas', index='categoria', columns='mes', aggfunc='sum')
        
        assert pivot.loc['A', 1] == 100
        assert pivot.loc['B', 2] == 250


class TestValidacionCalculos:
    """
    Tests para validar que los cálculos sean correctos
    """
    
    def test_precio_total_calculado(self):
        """
        Test: Verifica que Precio_Total = Cantidad * Precio_Unitario
        """
        df = pd.DataFrame({
            'Cantidad': [2, 3, 5],
            'Precio_Unitario': [10.0, 20.0, 30.0]
        })
        
        df['Precio_Total_Calc'] = df['Cantidad'] * df['Precio_Unitario']
        
        assert df['Precio_Total_Calc'][0] == 20.0
        assert df['Precio_Total_Calc'][1] == 60.0
        assert df['Precio_Total_Calc'][2] == 150.0
    
    def test_suma_total_coincide(self):
        """
        Test: Verifica que la suma de partes = total
        """
        df = pd.DataFrame({
            'categoria': ['A', 'B', 'C'],
            'ventas': [100, 200, 300]
        })
        
        total_calculado = df['ventas'].sum()
        total_esperado = 600
        
        assert total_calculado == total_esperado
    
    def test_porcentajes_suman_100(self):
        """
        Test: Verifica que los porcentajes sumen 100%
        """
        df = pd.DataFrame({
            'categoria': ['A', 'B', 'C'],
            'ventas': [100, 200, 300]
        })
        
        df['porcentaje'] = (df['ventas'] / df['ventas'].sum()) * 100
        
        assert df['porcentaje'].sum() == pytest.approx(100.0, rel=0.01)


class TestFechas:
    """
    Tests para manejo de fechas
    """
    
    def test_extraer_año(self):
        """
        Test: Verifica extracción de año de fecha
        """
        fechas = pd.to_datetime(['2023-01-15', '2023-06-20', '2023-12-31'])
        años = fechas.year
        
        assert all(años == 2023)
    
    def test_extraer_mes(self):
        """
        Test: Verifica extracción de mes de fecha
        """
        fechas = pd.to_datetime(['2023-01-15', '2023-06-20', '2023-12-31'])
        meses = fechas.month
        
        assert meses[0] == 1
        assert meses[1] == 6
        assert meses[2] == 12
    
    def test_dia_semana(self):
        """
        Test: Verifica extracción de día de la semana
        """
        fecha = pd.to_datetime('2023-01-01')  # Domingo
        dia = fecha.day_name()
        
        assert dia == 'Sunday'


class TestExportacion:
    """
    Tests para exportación de datos
    """
    
    def test_exportar_csv(self, tmp_path):
        """
        Test: Verifica exportación a CSV
        """
        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        archivo = tmp_path / "test.csv"
        df.to_csv(archivo, index=False)
        
        assert archivo.exists()
        
        # Verificar que se puede leer
        df_leido = pd.read_csv(archivo)
        assert len(df_leido) == 3
    
    def test_redondeo_decimales(self):
        """
        Test: Verifica redondeo de decimales
        """
        df = pd.DataFrame({
            'precio': [10.12345, 20.98765, 30.55555]
        })
        
        df['precio_redondeado'] = df['precio'].round(2)
        
        assert df['precio_redondeado'][0] == 10.12
        assert df['precio_redondeado'][1] == 20.99
        assert df['precio_redondeado'][2] == 30.56


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])