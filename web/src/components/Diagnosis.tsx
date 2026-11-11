import { COLUMN_LABEL, n, S } from '../data';

/** Nulos por columna antes y después: la barra gris es el origen, la azul lo que quedó. */
export default function Diagnosis() {
  const cols = Object.keys(S.raw.nulls);
  const max = Math.max(...cols.map((c) => S.raw.nulls[c]));
  return (
    <section id="diagnostico">
      <div className="section-head">
        <p className="eyebrow">01 · Diagnóstico</p>
        <h2>Qué estaba mal en los datos</h2>
        <p>Antes de tocar nada, el pipeline mide cada problema. Estos son los números reales del archivo de origen.</p>
      </div>
      <div className="grid-2">
        <div className="card">
          <h3 className="h3">Valores nulos por columna</h3>
          <ul className="bars">
            {cols.map((c) => (
              <li key={c}>
                <span className="bar-label">{COLUMN_LABEL[c] ?? c}</span>
                <span className="bar-track">
                  <span className="bar raw" style={{ width: `${(S.raw.nulls[c] / max) * 100}%` }} />
                  <span className="bar fixed" style={{ width: `${(S.clean.nulls[c] / max) * 100}%` }} />
                </span>
                <span className="bar-value mono">{n(S.raw.nulls[c])} → {n(S.clean.nulls[c])}</span>
              </li>
            ))}
          </ul>
          <p className="note"><span className="key raw" /> origen <span className="key fixed" /> después de limpiar</p>
        </div>
        <div className="card">
          <h3 className="h3">Otros problemas</h3>
          <dl className="calc">
            <dt>Filas idénticas repetidas</dt><dd className="mono">{S.raw.duplicateRows}</dd>
            <dt>IDs de transacción repetidos</dt><dd className="mono">{S.raw.duplicateIds}</dd>
            <dt>Precios unitarios negativos</dt><dd className="mono">{S.raw.negativePrices}</dd>
            <dt>Ventas con cantidad 0</dt><dd className="mono">{S.raw.zeroQuantity}</dd>
            <dt>Variantes de categoría</dt><dd className="mono">{S.raw.categories.length}</dd>
            <dt>Variantes de género</dt><dd className="mono">{S.raw.genders.length}</dd>
          </dl>
        </div>
      </div>
    </section>
  );
}
