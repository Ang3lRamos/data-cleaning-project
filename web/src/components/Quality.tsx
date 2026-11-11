import { S } from '../data';

// Tests de tests/test_limpieza.py y tests/test_procesamiento.py, agrupados.
const GROUPS = [
  ['Limpieza', ['Carga de datos', 'Duplicados', 'Espacios', 'Categorías', 'Precios negativos', 'Nulos', 'Registros inválidos', 'Tipos de datos', 'Columnas derivadas', 'Pipeline completo']],
  ['Validación', ['Edades en rango', 'Precios positivos', 'Categorías normalizadas']],
  ['Métricas', ['Ingresos totales', 'Ticket promedio', 'Clientes únicos', 'Productos por categoría', 'Ingresos por categoría', 'Transacciones por cliente', 'Gasto por cliente']],
  ['SQL y estadística', ['Crear tabla', 'Consultas SQL', 'Estadísticas descriptivas', 'Percentiles']],
] as const;

export default function Quality() {
  const blank = S.clean.categories['(vacío)'] ?? 0;
  return (
    <section id="calidad">
      <div className="section-head">
        <p className="eyebrow">06 · Calidad</p>
        <h2>Probado con pytest</h2>
        <p>Cada paso de la limpieza y cada métrica tiene su test, incluida la carga en SQLite.</p>
      </div>
      <div className="grid-2">
        {GROUPS.map(([title, tests]) => (
          <div key={title} className="card">
            <h3 className="h3">{title} <span className="muted mono">· {tests.length}</span></h3>
            <ul className="tests">
              {tests.map((t) => <li key={t}><span className="check" aria-hidden>✓</span> {t}</li>)}
            </ul>
          </div>
        ))}
      </div>
      {blank > 0 && (
        <div className="card pending">
          <h3 className="h3">Pendiente detectado</h3>
          <p>
            {blank} ventas tenían como categoría solo espacios. Al recortarlos quedan vacías en lugar de pasar a “Desconocido”, así que el
            archivo limpio todavía tiene {blank} categorías en blanco. La corrección: tratar el texto vacío como nulo antes de rellenar.
          </p>
        </div>
      )}
    </section>
  );
}
