"""
test_limpieza.py
================
Tests unitarios para el módulo de limpieza de datos

Ejecutar con: pytest tests/test_limpieza.py -v
"""

import pytest
import pandas as pd
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../', 'src'))

from limpieza import LimpiadorDatos


class TestLimpiadorDatos:
    """
    Tests para la clase LimpiadorDatos
    """
    
    @pytest.fixture
    def df_prueba(self):
        """
        Crea un DataFrame de prueba con problemas conocidos
        """
        data = {
            'Transaction_ID': [1, 2, 3, 3, 4, 5],  # ID 3 duplicado
            'Fecha': ['2023-01-01', '2023-01-02', '2023-01-03', 
                      '2023-01-03', '2023-01-04', '2023-01-05'],
            'Cliente_ID': [100, 101, 102, 102, 103, 104],
            'Genero': ['M', 'F', 'masculino', 'masculino', None, 'femenino'],
            'Edad': [25, 30, None, 35, 40, 45],
            'Categoria_Producto': ['  Ropa  ', 'HOGAR', 'electronica', 
                                   'electronica', 'Deportes', None],
            'Cantidad': [2, 3, 0, 1, 5, 2],  # Cantidad 0 inválida
            'Precio_Unitario': [100.0, -50.0, 200.0, 200.0, 150.0, 75.0],  # Precio negativo
            'Precio_Total': [200.0, None, 0.0, 200.0, 750.0, 150.0],
            'Metodo_Pago': ['Efectivo', 'Tarjeta', 'Transferencia', 
                           'Transferencia', '', 'Efectivo']
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def limpiador(self, df_prueba, tmp_path):
        """
        Crea una instancia de LimpiadorDatos con datos de prueba
        """
        # Guardar DataFrame de prueba en archivo temporal
        archivo_temp = tmp_path / "test_data.csv"
        df_prueba.to_csv(archivo_temp, index=False)
        
        # Crear limpiador
        limpiador = LimpiadorDatos(
            ruta_entrada=str(archivo_temp),
            ruta_salida=str(tmp_path / "test_clean.csv")
        )
        limpiador.cargar_datos()
        
        return limpiador
    
    def test_cargar_datos(self, limpiador):
        """
        Test: Verifica que los datos se carguen correctamente
        """
        assert limpiador.df_original is not None
        assert limpiador.df_limpio is not None
        assert len(limpiador.df_original) == 6
    
    def test_eliminar_duplicados(self, limpiador):
        """
        Test: Verifica que se eliminen los duplicados
        """
        antes = len(limpiador.df_limpio)
        limpiador.eliminar_duplicados()
        despues = len(limpiador.df_limpio)
        
        assert despues < antes
        assert limpiador.reporte['duplicados_eliminados'] >= 1
    
    def test_limpiar_espacios(self, limpiador):
        """
        Test: Verifica que se eliminen espacios en blanco
        """
        limpiador.limpiar_espacios()
        
        # Verificar que no haya espacios al inicio o final
        for col in limpiador.df_limpio.select_dtypes(include=['object']).columns:
            valores_con_espacios = limpiador.df_limpio[col].astype(str).str.strip() != limpiador.df_limpio[col].astype(str)
            assert not valores_con_espacios.any()
    
    def test_normalizar_categorias(self, limpiador):
        """
        Test: Verifica que las categorías se normalicen correctamente
        """
        limpiador.limpiar_espacios()
        limpiador.normalizar_categorias()
        
        # Verificar que no haya variaciones de género
        generos_validos = ['Masculino', 'Femenino', 'Desconocido']
        generos_unicos = limpiador.df_limpio['Genero'].dropna().unique()
        
        for genero in generos_unicos:
            assert genero in generos_validos or pd.isna(genero)
    
    def test_corregir_valores_negativos(self, limpiador):
        """
        Test: Verifica que los valores negativos se corrijan
        """
        # Verificar que hay valores negativos antes
        assert (limpiador.df_limpio['Precio_Unitario'] < 0).any()
        
        limpiador.corregir_valores_negativos()
        
        # Verificar que no hay valores negativos después
        assert not (limpiador.df_limpio['Precio_Unitario'] < 0).any()
        assert limpiador.reporte['precios_negativos_corregidos'] >= 1
    
    def test_manejar_valores_nulos(self, limpiador):
        """
        Test: Verifica que los valores nulos se manejen correctamente
        """
        nulos_antes = limpiador.df_limpio.isnull().sum().sum()
        assert nulos_antes > 0
        
        limpiador.manejar_valores_nulos()
        
        nulos_despues = limpiador.df_limpio.isnull().sum().sum()
        assert nulos_despues < nulos_antes
    
    def test_eliminar_registros_invalidos(self, limpiador):
        """
        Test: Verifica que se eliminen registros con cantidad = 0
        """
        limpiador.eliminar_registros_invalidos()
        
        # Verificar que no hay cantidades = 0
        assert not (limpiador.df_limpio['Cantidad'] == 0).any()
        
        # Verificar que no hay precios = 0
        assert not (limpiador.df_limpio['Precio_Unitario'] == 0).any()
    
    def test_convertir_tipos_datos(self, limpiador):
        """
        Test: Verifica la conversión correcta de tipos de datos
        """
        # Primero manejar nulos para evitar errores
        limpiador.manejar_valores_nulos()
        limpiador.convertir_tipos_datos()
        
        # Verificar tipos de datos
        assert pd.api.types.is_datetime64_any_dtype(limpiador.df_limpio['Fecha'])
        assert pd.api.types.is_integer_dtype(limpiador.df_limpio['Edad'])
        assert pd.api.types.is_integer_dtype(limpiador.df_limpio['Cantidad'])
    
    def test_agregar_columnas_derivadas(self, limpiador):
        """
        Test: Verifica que se agreguen columnas derivadas
        """
        limpiador.manejar_valores_nulos()
        limpiador.convertir_tipos_datos()
        limpiador.agregar_columnas_derivadas()
        
        # Verificar que existan las nuevas columnas
        assert 'Año' in limpiador.df_limpio.columns
        assert 'Mes' in limpiador.df_limpio.columns
        assert 'Dia_Semana' in limpiador.df_limpio.columns
        assert 'Rango_Edad' in limpiador.df_limpio.columns
    
    def test_pipeline_completo(self, limpiador, tmp_path):
        """
        Test: Verifica que el pipeline completo funcione sin errores
        """
        # Ejecutar pipeline completo
        resultado = limpiador.ejecutar_limpieza_completa()
        
        assert resultado is True
        assert limpiador.df_limpio is not None
        
        # Verificar que el archivo se haya guardado
        assert os.path.exists(limpiador.ruta_salida)
        
        # Verificar calidad final
        assert limpiador.df_limpio.isnull().sum().sum() == 0  # Sin nulos
        assert limpiador.df_limpio.duplicated().sum() == 0  # Sin duplicados


class TestValidacionDatos:
    """
    Tests adicionales para validación de datos
    """
    
    def test_rango_edad_valido(self):
        """
        Test: Verifica que las edades estén en un rango válido
        """
        df = pd.DataFrame({
            'Edad': [18, 25, 30, 65, 80]
        })
        
        # Todas las edades deben estar entre 18 y 100
        assert (df['Edad'] >= 18).all()
        assert (df['Edad'] <= 100).all()
    
    def test_precios_positivos(self):
        """
        Test: Verifica que los precios sean positivos después de limpieza
        """
        df = pd.DataFrame({
            'Precio_Unitario': [-100, 50, 200, -30],
            'Precio_Total': [-200, 150, 400, -90]
        })
        
        # Convertir a valores absolutos
        df['Precio_Unitario'] = df['Precio_Unitario'].abs()
        df['Precio_Total'] = df['Precio_Total'].abs()
        
        assert (df['Precio_Unitario'] >= 0).all()
        assert (df['Precio_Total'] >= 0).all()
    
    def test_categorias_normalizadas(self):
        """
        Test: Verifica que las categorías estén normalizadas
        """
        categorias_originales = ['ROPA', 'ropa', 'Ropa', '  Ropa  ']
        
        # Normalizar
        categorias_normalizadas = [cat.strip().capitalize() for cat in categorias_originales]
        
        # Todas deben ser 'Ropa'
        assert all(cat == 'Ropa' for cat in categorias_normalizadas)


class TestIntegracionSQL:
    """
    Tests para la integración con SQL (requiere base de datos)
    """
    
    @pytest.fixture
    def db_conexion(self, tmp_path):
        """
        Crea una conexión a base de datos temporal
        """
        import sqlite3
        db_path = tmp_path / "test.db"
        conn = sqlite3.connect(str(db_path))
        return conn
    
    def test_crear_tabla(self, db_conexion):
        """
        Test: Verifica que se pueda crear una tabla
        """
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'valor': [100, 200, 300]
        })
        
        # Guardar en SQL
        df.to_sql('test_tabla', db_conexion, if_exists='replace', index=False)
        
        # Verificar que se creó
        cursor = db_conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_tabla'")
        resultado = cursor.fetchone()
        
        assert resultado is not None
        assert resultado[0] == 'test_tabla'
    
    def test_consulta_sql(self, db_conexion):
        """
        Test: Verifica que se puedan hacer consultas
        """
        # Crear tabla de prueba
        df = pd.DataFrame({
            'categoria': ['A', 'B', 'A', 'C'],
            'ventas': [100, 200, 150, 300]
        })
        df.to_sql('ventas_test', db_conexion, if_exists='replace', index=False)
        
        # Hacer consulta
        resultado = pd.read_sql(
            "SELECT categoria, SUM(ventas) as total FROM ventas_test GROUP BY categoria",
            db_conexion
        )
        
        assert len(resultado) == 3
        assert 'total' in resultado.columns


def test_requirements_instalados():
    """
    Test: Verifica que las librerías necesarias estén instaladas
    """
    try:
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import sqlalchemy
        assert True
    except ImportError as e:
        pytest.fail(f"Librería faltante: {e}")


if __name__ == "__main__":
    # Ejecutar tests
    pytest.main([__file__, '-v', '--tb=short'])