"""
01_download_data.py
===================
Script para generar el dataset de ventas retail.

Autor: Angel Ramos
Fecha: 2025-11-28
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def crear_dataset_retail():
    """
    Genera un dataset realista de ventas retail con problemas comunes:
    - Valores nulos
    - Duplicados
    - Inconsistencias en formato
    - Valores negativos (errores)
    - Espacios en blanco
    """
    
    print("Generando dataset de ventas retail")
    print("="*60)
    
    np.random.seed(42)
    
    # Configuración
    n_records = 1000
    
    # Generar fechas aleatorias en 2023
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=np.random.randint(0, 365)) 
             for _ in range(n_records)]
    
    # Categorías con inconsistencias intencionales
    categorias = [
        'Electrónicos', 'Ropa', 'Alimentos', 'Hogar', 'Deportes',
        'Electronica', 'ROPA', 'alimentos', 'HOGAR', 'deportes',
        None, '', '  Electrónicos  '
    ]
    
    # Géneros con variaciones
    generos = [
        'Masculino', 'Femenino', 'M', 'F', 
        'Hombre', 'Mujer', 'masculino', 'femenino',
        None, ''
    ]
    
    # Métodos de pago
    metodos_pago = ['Efectivo', 'Tarjeta', 'Transferencia', 'Debito', None, '']
    
    # Crear dataset base
    data = {
        'Transaction_ID': range(1, n_records + 1),
        'Fecha': dates,
        'Cliente_ID': np.random.randint(1, 300, n_records),
        'Genero': np.random.choice(generos, n_records),
        'Edad': np.random.randint(18, 80, n_records),
        'Categoria_Producto': np.random.choice(categorias, n_records),
        'Cantidad': np.random.randint(1, 10, n_records),
        'Precio_Unitario': np.round(np.random.uniform(5, 500, n_records), 2),
        'Precio_Total': None,
        'Metodo_Pago': np.random.choice(metodos_pago, n_records)
    }
    
    df = pd.DataFrame(data)
    
    print(f"Dataset base creado: {len(df)} registros")
    
    # INTRODUCIR PROBLEMAS COMUNES
    print("\nIntroduciendo problemas comunes en los datos")
    
    # 1. Valores nulos en Edad
    indices_nulos = np.random.choice(df.index, 50, replace=False)
    df.loc[indices_nulos, 'Edad'] = None
    print(f"Agregados 50 valores nulos en 'Edad'")
    
    # 2. Precios negativos (errores de entrada)
    indices_negativos = np.random.choice(df.index, 15, replace=False)
    df.loc[indices_negativos, 'Precio_Unitario'] = -abs(df.loc[indices_negativos, 'Precio_Unitario'])
    print(f"Agregados 15 precios negativos")
    
    # 3. Calcular precio total (con algunos errores)
    df['Precio_Total'] = df['Cantidad'] * df['Precio_Unitario']
    indices_error_total = np.random.choice(df.index, 25, replace=False)
    df.loc[indices_error_total, 'Precio_Total'] = None
    print(f"Agregados 25 valores nulos en 'Precio_Total'")
    
    # 4. Duplicar registros
    duplicados = df.sample(40)
    df = pd.concat([df, duplicados], ignore_index=True)
    print(f"Agregados 40 registros duplicados")
    
    # 5. Espacios en blanco en categorías
    mask = df['Categoria_Producto'].notna()
    df.loc[mask, 'Categoria_Producto'] = df.loc[mask, 'Categoria_Producto'].apply(
        lambda x: f'  {x}  ' if np.random.random() > 0.7 else x
    )
    print(f"Agregados espacios en blanco en categorías")
    
    # 6. Algunas cantidades = 0 o negativas
    indices_cantidad = np.random.choice(df.index, 10, replace=False)
    df.loc[indices_cantidad, 'Cantidad'] = 0
    print(f"Agregadas 10 cantidades = 0")
    
    return df

def guardar_dataset(df, carpeta='data/raw', nombre='retail_sales_raw.csv'):
    """
    Guarda el dataset en la carpeta especificada
    """
    
    # Crear carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)
    
    # Ruta completa
    ruta_completa = os.path.join(carpeta, nombre)
    
    # Guardar
    df.to_csv(ruta_completa, index=False)
    
    return ruta_completa

def mostrar_resumen(df, ruta_archivo):
    """
    Muestra un resumen del dataset generado
    """
    
    print("\n" + "="*60)
    print("RESUMEN DEL DATASET GENERADO")
    print("="*60)
    
    print(f"\nArchivo guardado en: {ruta_archivo}")
    print(f"Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
    print(f"Tamaño del archivo: {os.path.getsize(ruta_archivo) / 1024:.2f} KB")
    
    print("\nColumnas:")
    for i, col in enumerate(df.columns, 1):
        tipo = df[col].dtype
        print(f"   {i}. {col:<20} [{tipo}]")
    
    print("\n🔍 Primeras 3 filas:")
    print(df.head(3).to_string())
    
    print("\nPROBLEMAS DETECTADOS:")
    print(f"   • Valores nulos:")
    nulos = df.isnull().sum()
    for col, num in nulos[nulos > 0].items():
        porcentaje = (num / len(df)) * 100
        print(f"     - {col}: {num} ({porcentaje:.1f}%)")
    
    print(f"\n   • Duplicados: {df.duplicated().sum()} registros")
    
    print(f"\n   • Valores negativos en Precio_Unitario: {(df['Precio_Unitario'] < 0).sum()}")
    
    print(f"\n   • Cantidades = 0: {(df['Cantidad'] == 0).sum()}")
    
    print("\nDataset listo para limpieza!")
    print("Siguiente paso: ejecutar limpieza.py")

def main():
    """
    Función principal
    """
    
    print("\n" + "GENERACIÓN DE DATASET" + "\n")
    
    # Generar dataset
    df = crear_dataset_retail()
    
    # Guardar
    ruta = guardar_dataset(df)
    
    # Mostrar resumen
    mostrar_resumen(df, ruta)
    
    print("\n" + "="*60)
    print("Proceso completado exitosamente!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()