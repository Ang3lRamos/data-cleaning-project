// Los pasos de LimpiadorDatos (src/limpieza.py), en el orden en que se ejecutan.
const STEPS = [
  ['Duplicados', 'Quita filas idénticas y después IDs de transacción repetidos.', 'eliminar_duplicados'],
  ['Espacios', 'Recorta espacios al inicio y al final de cada texto.', 'limpiar_espacios'],
  ['Categorías', 'Unifica mayúsculas, tildes y sinónimos: “electronica”, “ELECTRÓNICOS” → Electrónicos.', 'normalizar_categorias'],
  ['Negativos', 'Pasa a positivo los precios unitarios negativos.', 'corregir_valores_negativos'],
  ['Nulos', 'Edad con la mediana, total recalculado y textos vacíos como “Desconocido”.', 'manejar_valores_nulos'],
  ['Inválidos', 'Descarta ventas con cantidad o precio en cero.', 'eliminar_registros_invalidos'],
  ['Tipos', 'Fechas como fecha, edades y cantidades como enteros, precios con 2 decimales.', 'convertir_tipos_datos'],
  ['Columnas nuevas', 'Año, mes, día de la semana y rango de edad para el análisis.', 'agregar_columnas_derivadas'],
];

export default function Pipeline() {
  return (
    <section id="pipeline">
      <div className="section-head">
        <p className="eyebrow">04 · Pipeline</p>
        <h2>Ocho pasos, siempre en el mismo orden</h2>
        <p>Cada paso es un método de <code className="mono">LimpiadorDatos</code> con su propio test. Al final los datos se cargan en SQLite para consultarlos con SQL.</p>
      </div>
      <ol className="pipeline">
        {STEPS.map(([title, text, fn], i) => (
          <li key={fn} className="card step">
            <span className="step-n mono">{String(i + 1).padStart(2, '0')}</span>
            <h3 className="h3">{title}</h3>
            <p>{text}</p>
            <code className="fn mono">{fn}()</code>
          </li>
        ))}
      </ol>
    </section>
  );
}
