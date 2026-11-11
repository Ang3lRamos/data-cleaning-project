import { useState } from 'react';
import { n, S, usd } from '../data';

const MONTHS = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];

export default function Analysis() {
  return (
    <section id="analisis">
      <div className="section-head">
        <p className="eyebrow">05 · Análisis</p>
        <h2>Lo que dicen los datos limpios</h2>
        <p>Con los datos ya confiables, el análisis sale de los archivos procesados: ventas por mes, por categoría y por cliente.</p>
      </div>
      <div className="grid-4 kpis-tight">
        <div className="card kpi"><span className="kpi-value mono">{usd(S.clean.revenue)}</span><span className="kpi-label">ingresos en 2023</span></div>
        <div className="card kpi"><span className="kpi-value mono">{n(S.clean.rows)}</span><span className="kpi-label">ventas</span></div>
        <div className="card kpi"><span className="kpi-value mono">{n(S.clean.customers)}</span><span className="kpi-label">clientes únicos</span></div>
        <div className="card kpi"><span className="kpi-value mono">{usd(S.clean.avgTicket)}</span><span className="kpi-label">ticket promedio</span></div>
      </div>
      <div className="card"><Monthly /></div>
      <div className="grid-2 gap-top">
        <div className="card">
          <h3 className="h3">Ingresos por categoría</h3>
          <HBars rows={S.byCategory.map((c) => ({ label: c.category, value: c.revenue, sub: `${c.transactions} ventas · ticket ${usd(c.ticket)}` }))} format={usd} />
        </div>
        <div className="card">
          <h3 className="h3">Clientes por rango de edad</h3>
          <HBars rows={Object.entries(S.clean.ageRanges).map(([k, v]) => ({ label: `${k} años`, value: v }))} format={(v) => n(v)} />
          <h3 className="h3 gap-top">Método de pago</h3>
          <HBars rows={Object.entries(S.clean.payments).map(([k, v]) => ({ label: k, value: v }))} format={(v) => n(v)} />
        </div>
      </div>
    </section>
  );
}

function HBars({ rows, format }: { rows: { label: string; value: number; sub?: string }[]; format: (v: number) => string }) {
  const max = Math.max(...rows.map((r) => r.value));
  return (
    <ul className="bars">
      {rows.map((r) => (
        <li key={r.label}>
          <span className="bar-label">{r.label}{r.sub && <small className="muted block">{r.sub}</small>}</span>
          <span className="bar-track"><span className="bar fixed" style={{ width: `${(r.value / max) * 100}%` }} /></span>
          <span className="bar-value mono">{format(r.value)}</span>
        </li>
      ))}
    </ul>
  );
}

/** Ingresos por mes en barras; al pasar el cursor se ve el detalle. */
function Monthly() {
  const [active, setActive] = useState<number | null>(null);
  const max = Math.max(...S.monthly.map((m) => m.revenue));
  const best = S.monthly.reduce((b, m) => (m.revenue > b.revenue ? m : b));
  const shown = active == null ? null : S.monthly[active];
  return (
    <figure>
      <div className="chart-head">
        <figcaption className="h3">Ingresos por mes</figcaption>
        <span className="muted mono">
          {shown ? `${MONTHS[Number(shown.month.slice(5)) - 1]} · ${usd(shown.revenue)} · ${shown.transactions} ventas` : `mejor mes: ${MONTHS[Number(best.month.slice(5)) - 1]} · ${usd(best.revenue)}`}
        </span>
      </div>
      <div className="columns" onMouseLeave={() => setActive(null)}>
        {S.monthly.map((m, i) => (
          <button key={m.month} className={`col ${active === i ? 'on' : ''}`} onMouseEnter={() => setActive(i)} onFocus={() => setActive(i)}
            aria-label={`${MONTHS[i]}: ${usd(m.revenue)}`}>
            <span className="col-bar" style={{ height: `${(m.revenue / max) * 100}%` }} />
            <span className="col-label">{MONTHS[Number(m.month.slice(5)) - 1]}</span>
          </button>
        ))}
      </div>
    </figure>
  );
}
