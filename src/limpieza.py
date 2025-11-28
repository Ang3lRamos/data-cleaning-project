"""
02_limpieza.py
==============
Script para limpiar y normalizar el dataset de ventas retail.

Autor: Angel Ramos
Fecha: 2025-11-28
"""

import pandas as pd
import os
from datetime import datetime

class LimpiadorDatos:
    """
    Clase para encapsular todas las operaciones de limpieza
    """
    
    def __init__(self, ruta_entrada, ruta_salida='data/processed/retail_sales_clean.csv'):
        """
        Inicializa el limpiador con las rutas de archivos
        """
        self.ruta_entrada = ruta_entrada
        self.ruta_salida = ruta_salida
        self.df_original = None
        self.df_limpio = None
        self.reporte = {}
        
    def cargar_datos(self):
        """
        Carga el dataset desde el archivo CSV
        """
        print("Cargando datos")
        try:
            self.df_original = pd.read_csv(self.ruta_entrada)
            print(f"Datos cargados: {self.df_original.shape[0]} filas, {self.df_original.shape[1]} columnas")
            self.df_limpio = self.df_original.copy()
            return True
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.ruta_entrada}")
            return False
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return False
    
    def mostrar_info_inicial(self):
        """
        Muestra información del dataset antes de limpiar
        """
        print("\n" + "="*60)
        print("INFORMACIÓN INICIAL DEL DATASET")
        print("="*60)
        
        print(f"\nDimensiones: {self.df_limpio.shape}")
        print(f"\nColumnas: {list(self.df_limpio.columns)}")
        
        print("\nPROBLEMAS DETECTADOS:")
        
        # Valores nulos
        nulos = self.df_limpio.isnull().sum()
        if nulos.sum() > 0:
            print(f"\nValores nulos:")
            for col, num in nulos[nulos > 0].items():
                porcentaje = (num / len(self.df_limpio)) * 100
                print(f"{col}: {num} ({porcentaje:.1f}%)")
        
        # Duplicados
        duplicados = self.df_limpio.duplicated().sum()
        print(f"\nRegistros duplicados: {duplicados}")
        
        # Valores negativos
        if 'Precio_Unitario' in self.df_limpio.columns:
            negativos = (self.df_limpio['Precio_Unitario'] < 0).sum()
            print(f"Precios negativos: {negativos}")
        
        # Cantidades cero
        if 'Cantidad' in self.df_limpio.columns:
            ceros = (self.df_limpio['Cantidad'] == 0).sum()
            print(f"Cantidades = 0: {ceros}")
    
    def eliminar_duplicados(self):
        """
        Elimina registros duplicados
        """
        print("\nPaso 1: Eliminando duplicados")
        
        antes = len(self.df_limpio)
        
        # Eliminar duplicados completos primero
        self.df_limpio = self.df_limpio.drop_duplicates()
        
        # Eliminar duplicados basados en Transaction_ID 
        if 'Transaction_ID' in self.df_limpio.columns:
            self.df_limpio = self.df_limpio.drop_duplicates(subset=['Transaction_ID'], keep='first')
        
        despues = len(self.df_limpio)
        eliminados = antes - despues
        self.reporte['duplicados_eliminados'] = eliminados
        
        print(f"Eliminados {eliminados} registros duplicados")
        print(f"Registros restantes: {despues}")
    
    def limpiar_espacios(self):
        """
        Elimina espacios en blanco innecesarios en columnas de texto
        """
        print("\nPaso 2: Limpiando espacios en blanco")
        
        columnas_texto = self.df_limpio.select_dtypes(include=['object']).columns
        
        for col in columnas_texto:
            # Eliminar espacios al inicio y final
            self.df_limpio[col] = self.df_limpio[col].str.strip()
        
        print(f"Espacios eliminados en {len(columnas_texto)} columnas de texto")
    
    def normalizar_categorias(self):
        """
        Normaliza las categorías de productos y géneros
        """
        print("\nPaso 3: Normalizando categorías...")
        
        # Normalizar Categoría de Producto
        if 'Categoria_Producto' in self.df_limpio.columns:
            # Mapeo de categorías
            mapeo_categorias = {
                'electronica': 'Electrónicos',
                'electrónicos': 'Electrónicos',
                'electronico': 'Electrónicos',
                'ropa': 'Ropa',
                'alimentos': 'Alimentos',
                'hogar': 'Hogar',
                'deportes': 'Deportes'
            }
            
            # Convertir a minúsculas para comparar
            self.df_limpio['Categoria_Producto'] = self.df_limpio['Categoria_Producto'].str.lower()
            
            # Aplicar mapeo
            self.df_limpio['Categoria_Producto'] = self.df_limpio['Categoria_Producto'].replace(mapeo_categorias)
            
            # Capitalizar primera letra
            self.df_limpio['Categoria_Producto'] = self.df_limpio['Categoria_Producto'].str.capitalize()
            
            print(f"Categorías normalizadas")
            print(f"Categorías únicas: {self.df_limpio['Categoria_Producto'].nunique()}")
        
        # Normalizar Género
        if 'Genero' in self.df_limpio.columns:
            mapeo_generos = {
                'm': 'Masculino',
                'masculino': 'Masculino',
                'hombre': 'Masculino',
                'f': 'Femenino',
                'femenino': 'Femenino',
                'mujer': 'Femenino'
            }
            
            self.df_limpio['Genero'] = self.df_limpio['Genero'].str.lower()
            self.df_limpio['Genero'] = self.df_limpio['Genero'].replace(mapeo_generos)
            self.df_limpio['Genero'] = self.df_limpio['Genero'].str.capitalize()
            
            print(f"Géneros normalizados")
    
    def corregir_valores_negativos(self):
        """
        Corrige valores negativos en precios (convirtiéndolos a positivos)
        """
        print("\nPaso 4: Corrigiendo valores negativos...")
        
        if 'Precio_Unitario' in self.df_limpio.columns:
            negativos_antes = (self.df_limpio['Precio_Unitario'] < 0).sum()
            
            # Convertir a valor absoluto
            self.df_limpio['Precio_Unitario'] = self.df_limpio['Precio_Unitario'].abs()
            
            print(f"Corregidos {negativos_antes} precios negativos")
            self.reporte['precios_negativos_corregidos'] = negativos_antes
    
    def manejar_valores_nulos(self):
        """
        Maneja valores nulos según la columna
        """
        print("\nPaso 5: Manejando valores nulos...")
        
        nulos_inicial = self.df_limpio.isnull().sum().sum()
        
        # Edad: rellenar con la mediana
        if 'Edad' in self.df_limpio.columns:
            nulos_edad = self.df_limpio['Edad'].isnull().sum()
            if nulos_edad > 0:
                mediana_edad = self.df_limpio['Edad'].median()
                self.df_limpio['Edad'].fillna(mediana_edad, inplace=True)
                print(f"Edad: {nulos_edad} nulos rellenados con mediana ({mediana_edad:.0f})")
        
        # Precio_Total: recalcular
        if 'Precio_Total' in self.df_limpio.columns:
            nulos_precio = self.df_limpio['Precio_Total'].isnull().sum()
            if nulos_precio > 0:
                self.df_limpio['Precio_Total'] = self.df_limpio['Cantidad'] * self.df_limpio['Precio_Unitario']
                print(f"Precio_Total: {nulos_precio} nulos recalculados")
        
        # Categoría y Género: rellenar con 'Desconocido'
        for col in ['Categoria_Producto', 'Genero', 'Metodo_Pago']:
            if col in self.df_limpio.columns:
                nulos_col = self.df_limpio[col].isnull().sum()
                if nulos_col > 0:
                    self.df_limpio[col].fillna('Desconocido', inplace=True)
                    print(f"{col}: {nulos_col} nulos rellenados con 'Desconocido'")
        
        nulos_final = self.df_limpio.isnull().sum().sum()
        self.reporte['nulos_manejados'] = nulos_inicial - nulos_final
    
    def eliminar_registros_invalidos(self):
        """
        Elimina registros con datos inválidos (ej: cantidad = 0)
        """
        print("\nPaso 6: Eliminando registros inválidos")
        
        antes = len(self.df_limpio)
        
        # Eliminar cantidades = 0
        if 'Cantidad' in self.df_limpio.columns:
            self.df_limpio = self.df_limpio[self.df_limpio['Cantidad'] > 0]
        
        # Eliminar precios = 0
        if 'Precio_Unitario' in self.df_limpio.columns:
            self.df_limpio = self.df_limpio[self.df_limpio['Precio_Unitario'] > 0]
        
        despues = len(self.df_limpio)
        eliminados = antes - despues
        
        print(f"Eliminados {eliminados} registros inválidos")
        self.reporte['registros_invalidos'] = eliminados
    
    def convertir_tipos_datos(self):
        """
        Convierte columnas a los tipos de datos apropiados
        """
        print("\nPaso 7: Convirtiendo tipos de datos")
        
        # Fecha a datetime
        if 'Fecha' in self.df_limpio.columns:
            self.df_limpio['Fecha'] = pd.to_datetime(self.df_limpio['Fecha'])
            print(f"'Fecha' convertida a datetime")
        
        # Edad a entero
        if 'Edad' in self.df_limpio.columns:
            self.df_limpio['Edad'] = self.df_limpio['Edad'].astype(int)
            print(f"'Edad' convertida a int")
        
        # Cantidad a entero
        if 'Cantidad' in self.df_limpio.columns:
            self.df_limpio['Cantidad'] = self.df_limpio['Cantidad'].astype(int)
            print(f"'Cantidad' convertida a int")
        
        # Precios a float con 2 decimales
        for col in ['Precio_Unitario', 'Precio_Total']:
            if col in self.df_limpio.columns:
                self.df_limpio[col] = self.df_limpio[col].round(2)
                print(f"'{col}' redondeado a 2 decimales")
    
    def agregar_columnas_derivadas(self):
        """
        Agrega columnas útiles derivadas de los datos existentes
        """
        print("\nPaso 8: Agregando columnas derivadas...")
        
        if 'Fecha' in self.df_limpio.columns:
            # Extraer año, mes, día
            self.df_limpio['Año'] = self.df_limpio['Fecha'].dt.year
            self.df_limpio['Mes'] = self.df_limpio['Fecha'].dt.month
            self.df_limpio['Dia_Semana'] = self.df_limpio['Fecha'].dt.day_name()
            print(f"Agregadas: Año, Mes, Dia_Semana")
        
        # Rango de edad
        if 'Edad' in self.df_limpio.columns:
            self.df_limpio['Rango_Edad'] = pd.cut(
                self.df_limpio['Edad'],
                bins=[0, 25, 35, 50, 100],
                labels=['18-25', '26-35', '36-50', '51+']
            )
            print(f"Agregada: Rango_Edad")
    
    def guardar_datos_limpios(self):
        """
        Guarda el dataset limpio
        """
        print("\nGuardando datos limpios...")
        
        # Crear carpeta si no existe
        carpeta = os.path.dirname(self.ruta_salida)
        os.makedirs(carpeta, exist_ok=True)
        
        # Guardar
        self.df_limpio.to_csv(self.ruta_salida, index=False)
        
        print(f"Datos guardados en: {self.ruta_salida}")
        print(f"Registros finales: {len(self.df_limpio)}")
        print(f"Tamaño: {os.path.getsize(self.ruta_salida) / 1024:.2f} KB")
    
    def generar_reporte_final(self):
        """
        Genera un reporte completo de la limpieza
        """
        print("\n" + "="*60)
        print("REPORTE FINAL DE LIMPIEZA")
        print("="*60)
        
        print(f"\nESTADÍSTICAS:")
        print(f"• Registros iniciales: {len(self.df_original)}")
        print(f"• Registros finales: {len(self.df_limpio)}")
        print(f"• Reducción: {len(self.df_original) - len(self.df_limpio)} ({((len(self.df_original) - len(self.df_limpio)) / len(self.df_original) * 100):.1f}%)")
        
        print(f"\nOPERACIONES REALIZADAS:")
        print(f"• Duplicados eliminados: {self.reporte.get('duplicados_eliminados', 0)}")
        print(f"• Precios negativos corregidos: {self.reporte.get('precios_negativos_corregidos', 0)}")
        print(f"• Valores nulos manejados: {self.reporte.get('nulos_manejados', 0)}")
        print(f"• Registros inválidos eliminados: {self.reporte.get('registros_invalidos', 0)}")
        
        print(f"\nCALIDAD DEL DATASET LIMPIO:")
        print(f"• Valores nulos: {self.df_limpio.isnull().sum().sum()}")
        print(f"• Duplicados: {self.df_limpio.duplicated().sum()}")
        print(f"• Columnas: {len(self.df_limpio.columns)}")
        
        print("\nPRIMERAS 5 FILAS DEL DATASET LIMPIO:")
        print(self.df_limpio.head().to_string())
        
        print("\n" + "="*60)
        print("Limpieza completada exitosamente!")
        print("="*60)
    
    def ejecutar_limpieza_completa(self):
        """
        Ejecuta todo el proceso de limpieza
        """
        print("\nINICIANDO PROCESO DE LIMPIEZA DE DATOS\n")
        
        # Cargar datos
        if not self.cargar_datos():
            return False
        
        # Mostrar info inicial
        self.mostrar_info_inicial()
        
        # Ejecutar limpieza paso a paso
        self.eliminar_duplicados()
        self.limpiar_espacios()
        self.normalizar_categorias()
        self.corregir_valores_negativos()
        self.manejar_valores_nulos()
        self.eliminar_registros_invalidos()
        self.convertir_tipos_datos()
        self.agregar_columnas_derivadas()
        
        # Guardar
        self.guardar_datos_limpios()
        
        # Reporte final
        self.generar_reporte_final()
        
        return True

def main():
    """
    Función principal
    """
    
    # Crear instancia del limpiador
    limpiador = LimpiadorDatos(
        ruta_entrada='data-cleaning-project/data/raw/retail_sales_raw.csv',
        ruta_salida='data-cleaning-project/data/processed/retail_sales_clean.csv'
    )
    
    # Ejecutar limpieza
    limpiador.ejecutar_limpieza_completa()
    
    print("\nSiguiente paso: ejecutar 03_procesamiento.py")

if __name__ == "__main__":
    main()