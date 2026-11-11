import { useState } from 'react';
import { Row, S } from '../data';

const COLS: [keyof Row, string][] = [
  ['Transaction_ID', 'ID'], ['Genero', 'Género'], ['Edad', 'Edad'], ['Categoria_Producto', 'Categoría'],
  ['Cantidad', 'Cant.'], ['Precio_Unitario', 'Precio unit.'], ['Precio_Total', 'Total'], ['Metodo_Pago', 'Pago'],
];

// Decimales a 2 cifras: sin eso, ruido como 1779.3600000000001 parecía un cambio.
const show = (v: unknown) =>
  v == null ? '∅' : typeof v === 'string' ? `"${v.replace(/ /g, '·')}"` : Number.isInteger(v) ? String(v) : (v as number).toFixed(2);

export default function BeforeAfter() {
  const [view, setView] = useState<'before' | 'after'>('before');
  return (
    <section id="antes-despues">
      <div className="section-head">
        <p className="eyebrow">03 · Antes y después</p>
        <h2>Fila por fila</h2>
        <p>Siete ventas reales del archivo con algún problema. Cambia entre el origen y el resultado: lo que cambió queda marcado.</p>
      </div>
      <div className="card">
        <div className="segmented" role="tablist" aria-label="Versión de los datos">
          <button role="tab" aria-selected={view === 'before'} onClick={() => setView('before')}>Origen</button>
          <button role="tab" aria-selected={view === 'after'} onClick={() => setView('after')}>Limpio</button>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>{COLS.map(([k, l]) => <th key={k} className={k === 'Transaction_ID' ? '' : 'num'}>{l}</th>)}</tr>
            </thead>
            <tbody>
              {S.samples.map(({ before, after }) => {
                if (view === 'after' && !after) {
                  return (
                    <tr key={before.Transaction_ID} className="removed">
                      <td className="mono">{before.Transaction_ID}</td>
                      <td colSpan={COLS.length - 1}>Eliminada: venta con cantidad 0</td>
                    </tr>
                  );
                }
                const row = view === 'before' ? before : (after as Row);
                return (
                  <tr key={before.Transaction_ID}>
                    {COLS.map(([k]) => {
                      const changed = after && show(before[k]) !== show(after[k]);
                      // Un vacío que sobrevive a la limpieza también es un problema (ver "Pendiente detectado").
                      const bad = row[k] == null || (view === 'before' && ((typeof before[k] === 'number' && (before[k] as number) < 0) || (k === 'Cantidad' && before[k] === 0)));
                      return (
                        <td key={k} className={`mono ${k === 'Transaction_ID' ? '' : 'num'} ${bad ? 'cell-bad' : ''} ${view === 'after' && changed && !bad ? 'cell-fixed' : ''}`}>
                          {show(row[k])}
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <p className="note"><span className="key bad" /> problema en el origen <span className="key fixed" /> valor corregido · ∅ = vacío · · = espacio</p>
      </div>
    </section>
  );
}
