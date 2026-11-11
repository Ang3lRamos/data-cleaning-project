import { n, S } from '../data';

/** Muestra los espacios invisibles como puntos, para que el desorden se vea. */
const visible = (v: string) => v.replace(/ /g, '·');

function Variants({ title, before, after }: { title: string; before: { value: string; n: number }[]; after: Record<string, number> }) {
  return (
    <div className="card">
      <h3 className="h3">{title}</h3>
      <div className="mess">
        <div>
          <p className="mess-label">Antes · {before.length} variantes</p>
          <ul className="chips">
            {before.map((v) => (
              <li key={v.value} className={`chip ${v.value === '(vacío)' || v.value.trim() === '' ? 'bad' : ''}`}>
                <span className="mono">{v.value === '(vacío)' ? '∅ vacío' : `"${visible(v.value)}"`}</span> <b className="mono">{n(v.n)}</b>
              </li>
            ))}
          </ul>
        </div>
        <span className="arrow" aria-hidden>→</span>
        <div>
          <p className="mess-label">Después · {Object.keys(after).length} valores</p>
          <ul className="chips">
            {Object.entries(after).map(([k, c]) => (
              <li key={k} className={`chip ${k === '(vacío)' ? 'bad' : 'good'}`}>
                {k === '(vacío)' ? '∅ vacío' : k} <b className="mono">{n(c)}</b>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default function Mess() {
  return (
    <section id="normalizacion">
      <div className="section-head">
        <p className="eyebrow">02 · Normalización</p>
        <h2>Seis categorías, 23 variantes</h2>
        <p>Espacios al inicio y al final, mayúsculas, tildes y sinónimos. Los puntos (·) son espacios que en el archivo no se ven.</p>
      </div>
      <div className="stack">
        <Variants title="Categoría de producto" before={S.raw.categories} after={S.clean.categories} />
        <Variants title="Género" before={S.raw.genders} after={S.clean.genders} />
      </div>
    </section>
  );
}
