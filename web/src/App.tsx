import Analysis from './components/Analysis';
import BeforeAfter from './components/BeforeAfter';
import Diagnosis from './components/Diagnosis';
import Mess from './components/Mess';
import Pipeline from './components/Pipeline';
import Quality from './components/Quality';
import { n, S } from './data';

const REPO = 'https://github.com/Ang3lRamos/data-cleaning-project';

export default function App() {
  const nulls = Object.values(S.raw.nulls).reduce((a, b) => a + b, 0);
  return (
    <>
      <header className="topbar">
        <div className="topbar-inner">
          <a href="#inicio" className="brand">
            <span className="brand-mark" aria-hidden>
              <svg width="16" height="16" viewBox="0 0 32 32"><path d="M7 9h18M10 16h12M13 23h6" stroke="#93c5fd" strokeWidth="4" strokeLinecap="round" /></svg>
            </span>
            data-cleaning
          </a>
          <nav className="nav" aria-label="Secciones">
            <a href="#diagnostico">Diagnóstico</a>
            <a href="#antes-despues">Antes y después</a>
            <a href="#pipeline">Pipeline</a>
            <a href="#analisis">Análisis</a>
            <a href="#calidad">Calidad</a>
          </nav>
          <a className="gh" href={REPO} target="_blank" rel="noreferrer">Código</a>
        </div>
      </header>

      <main className="shell" id="inicio">
        <section className="hero">
          <p className="eyebrow">Python · Pandas · SQL · pytest</p>
          <h1>De {n(S.raw.rows)} ventas sucias a {n(S.clean.rows)} confiables.</h1>
          <p className="lead">
            Un dataset de ventas minoristas con duplicados, nulos, precios negativos y la misma categoría en 23 variantes distintas.
            El pipeline lo limpia paso a paso, lo valida con tests y lo deja listo para SQL y análisis.
          </p>
          <div className="grid-4 kpis">
            <Kpi value={String(S.raw.duplicateRows)} label="filas duplicadas eliminadas" />
            <Kpi value={n(nulls)} label="valores nulos en el origen" />
            <Kpi value={String(S.raw.negativePrices)} label="precios negativos corregidos" />
            <Kpi value={String(S.raw.categories.length)} label="variantes para 6 categorías" />
          </div>
        </section>

        <Diagnosis />
        <Mess />
        <BeforeAfter />
        <Pipeline />
        <Analysis />
        <Quality />
      </main>

      <footer className="footer">
        <div className="shell">Proyecto de Angel Ramos. Datos sintéticos de ventas generados por el propio pipeline (src/01_download_data.py).</div>
      </footer>
    </>
  );
}

function Kpi({ value, label }: { value: string; label: string }) {
  return (
    <div className="card kpi">
      <span className="kpi-value mono">{value}</span>
      <span className="kpi-label">{label}</span>
    </div>
  );
}
