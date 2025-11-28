# Data Cleaning Project - Pipeline de Limpieza de Datos

Proyecto completo de extracción, limpieza y procesamiento automatizado de datos usando Python, Pandas y SQL.

## Descripción

Este proyecto implementa un pipeline completo de procesamiento de datos que simula un flujo de trabajo real de Data Engineering/Data Science. Desde la generación de datos con problemas comunes hasta su carga en una base de datos SQL, pasando por limpieza exhaustiva y análisis exploratorio.

## Resultados del Pipeline

**Dataset Procesado:**
- Registros iniciales: 1,040
- Registros finales limpios: 990
- Reducción: 3.2%
- Clientes únicos: 286
- Revenue total: $1,264,588.41

**Problemas de Datos Resueltos:**
- 23 registros duplicados eliminados
- 733 valores nulos manejados
- 15 precios negativos corregidos
- 10 registros inválidos eliminados
- Normalización de 6 categorías de productos

## Tecnologías Utilizadas

- **Python 3.x** - Lenguaje principal
- **Pandas** - Manipulación y limpieza de datos
- **NumPy** - Operaciones numéricas
- **SQLAlchemy** - ORM y conexión a bases de datos
- **SQLite** - Base de datos relacional
- **Matplotlib/Seaborn** - Visualización de datos
- **Jupyter Notebook** - Análisis exploratorio interactivo

## Estructura del Proyecto

```
DATA_CLEANING/
├── data/
│   └── retail_sales.db                # Base de datos SQLite (120 KB)
│
├── data-cleaning-project/
│   ├── data/
│   │   ├── processed/                 # Datos limpios
│   │   │   └── retail_sales_clean.csv (990 registros)
│   │   └── raw/                       # Datos originales sin procesar
│   │       └── retail_sales_raw.csv   (1,040 registros)
│   │
│   ├── docs/
│   │   └── imagenes/                  # Gráficos generados
│   │       ├── distribucion_edad.png
│   │       ├── revenue_por_categoria.png
│   │       └── tendencia_ventas.png
│   │
│   ├── notebooks/                     # Análisis exploratorio
│   │   └── exploracion_inicial.ipynb  # Notebook con visualizaciones
│   │
│   ├── sql/                           # Scripts SQL
│   │   └── consultas.sql              # Consultas útiles
│   │
│   ├── src/                           # Código fuente
│   │   ├── __init__.py
│   │   ├── 01_download_data.py        # Generación del dataset
│   │   ├── 02_limpieza.py             # Limpieza con Pandas
│   │   ├── 03_procesamiento.py        # Análisis y métricas
│   │   └── 04_conexion_sql.py         # Carga a base de datos
│   │
│   ├── tests/                         # Tests (para futuras pruebas)
│   │
│   ├── .gitignore                     # Archivos ignorados por Git
│   ├── README.md                      # Este archivo
│   └── requirements.txt               # Dependencias Python
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/data-cleaning-project.git
cd data-cleaning-project
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar el Pipeline Completo

```bash
# Paso 1: Generar dataset con problemas
python src/01_download_data.py

# Paso 2: Limpiar datos
python src/02_limpieza.py

# Paso 3: Procesar y analizar
python src/03_procesamiento.py

# Paso 4: Cargar a base de datos
python src/04_conexion_sql.py
```

### Explorar con Jupyter Notebook

```bash
jupyter notebook notebooks/exploracion_inicial.ipynb
```

### Consultar la Base de Datos

```bash
# Abrir SQLite
sqlite3 data/retail_sales.db

# Ejemplo de consulta
SELECT * FROM ventas_por_categoria ORDER BY Revenue_Total DESC;
```

## Pipeline de Limpieza

El script `02_limpieza.py` realiza las siguientes operaciones:

1. **Eliminación de duplicados** - Identifica y elimina registros repetidos
2. **Limpieza de espacios** - Elimina espacios en blanco innecesarios
3. **Normalización de categorías** - Unifica variaciones (ej: "ROPA" → "Ropa")
4. **Corrección de valores negativos** - Convierte precios negativos a positivos
5. **Manejo de valores nulos**:
   - Edad: rellena con mediana
   - Precio_Total: recalcula a partir de cantidad × precio
   - Categorías: marca como "Desconocido"
6. **Eliminación de registros inválidos** - Elimina cantidades = 0
7. **Conversión de tipos de datos** - Asegura tipos correctos (datetime, int, float)
8. **Columnas derivadas** - Agrega Año, Mes, Día de semana, Rango de edad

## Métricas Clave

### Ventas por Categoría

| Categoría     | Revenue Total | Transacciones | Ticket Promedio |
|---------------|---------------|---------------|-----------------|
| Electrónicos  | $328,813.01   | 260           | $1,264.67       |
| Hogar         | $200,644.18   | 149           | $1,346.61       |
| Deportes      | $192,948.92   | 144           | $1,339.92       |
| Alimentos     | $176,582.27   | 149           | $1,185.12       |

### Top 5 Clientes

| Cliente ID | Total Gastado | Num Compras | Ticket Promedio |
|------------|---------------|-------------|-----------------|
| 293        | $14,460.67    | 11          | $1,314.61       |
| 59         | $14,001.65    | 7           | $2,000.24       |
| 9          | $13,682.54    | 6           | $2,280.42       |
| 89         | $12,544.55    | 6           | $2,090.76       |
| 199        | $12,461.07    | 4           | $3,115.27       |

## Base de Datos SQL

El proyecto incluye una base de datos SQLite con 3 tablas:

1. **ventas** (990 registros) - Tabla principal con todas las transacciones
2. **ventas_por_categoria** (6 registros) - Agregación por categoría de producto
3. **resumen_clientes** (286 registros) - Métricas por cliente

### Ejemplos de Consultas

```sql
-- Top 5 categorías por revenue
SELECT Categoria_Producto, Revenue_Total, Num_Transacciones
FROM ventas_por_categoria
ORDER BY Revenue_Total DESC
LIMIT 5;

-- Clientes con más de 5 compras
SELECT Cliente_ID, Num_Compras, Total_Gastado
FROM resumen_clientes
WHERE Num_Compras > 5
ORDER BY Total_Gastado DESC;

-- Revenue mensual
SELECT strftime('%Y-%m', Fecha) as Mes, 
       COUNT(*) as Transacciones,
       SUM(Precio_Total) as Revenue
FROM ventas
GROUP BY Mes
ORDER BY Mes;
```

## Visualizaciones

El proyecto genera visualizaciones automáticamente en `docs/imagenes/`:

- **revenue_por_categoria.png** - Comparación de ingresos por categoría
- **distribucion_edad.png** - Histograma de edades de clientes
- **tendencia_ventas.png** - Evolución mensual de ventas

## Aprendizajes y Buenas Prácticas

Este proyecto demuestra:

- **Arquitectura orientada a objetos** para scripts reutilizables
- **Manejo robusto de errores** y validaciones
- **Documentación clara** en código y README
- **Reportes detallados** de cada etapa del proceso
- **Separación de responsabilidades** (limpieza, procesamiento, carga)
- **Versionamiento de datos** (raw vs processed)
- **Automatización** del pipeline completo

## Próximos Pasos

- [ ] Implementar análisis predictivo (forecasting de ventas)
- [ ] Crear dashboard interactivo con Streamlit o Dash
- [ ] Implementar CI/CD con GitHub Actions
- [ ] Conectar a base de datos PostgreSQL en la nube
- [ ] Añadir clustering de clientes (segmentación avanzada)

## Autor

**Angel Ramos**

- GitHub: [@Ang3lRamos](https://github.com/Ang3lRamos)
- LinkedIn: [Angel Ramos](www.linkedin.com/in/angel-ramos-528974231)
- Email: angelf.ramosc@unac.edu.co

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Agradecimientos

- Dataset inspirado en problemas reales de datos
- Comunidad de Python y Pandas por las excelentes herramientas
- Recursos de aprendizaje de Data Science

---

**Nota:** Este es un proyecto educativo de portafolio que demuestra habilidades en limpieza y procesamiento de datos.