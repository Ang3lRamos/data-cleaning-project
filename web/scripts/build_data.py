"""Calcula desde los CSV reales lo que muestra la interfaz y lo guarda en web/src/metrics/summary.json.

Uso (desde la raíz del repo): python web/scripts/build_data.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
raw = pd.read_csv(ROOT / "data/raw/retail_sales_raw.csv")
clean = pd.read_csv(ROOT / "data/processed/retail_sales_clean.csv")
monthly = pd.read_csv(ROOT / "data/processed/ventas_mensuales.csv")
by_cat = pd.read_csv(ROOT / "data/processed/analisis_categoria.csv")

COLS = ["Genero", "Edad", "Categoria_Producto", "Precio_Total", "Metodo_Pago"]


def counts(series: pd.Series) -> list[dict]:
    """Valores tal como vienen (con espacios y mayúsculas), para mostrar el desorden original."""
    return [{"value": "(vacío)" if pd.isna(v) else repr(v)[1:-1], "n": int(n)} for v, n in series.value_counts(dropna=False).items()]


# Filas de ejemplo con problemas típicos, y cómo quedaron (o si se eliminaron).
def sample(ids: list[int]) -> list[dict]:
    out = []
    for tid in ids:
        before = raw[raw.Transaction_ID == tid].iloc[0]
        after = clean[clean.Transaction_ID == tid]
        row = lambda r, cols: {c: (None if pd.isna(r[c]) else (r[c].item() if hasattr(r[c], "item") else r[c])) for c in cols}
        base = ["Transaction_ID", "Genero", "Edad", "Categoria_Producto", "Cantidad", "Precio_Unitario", "Precio_Total", "Metodo_Pago"]
        out.append({"before": row(before, base), "after": row(after.iloc[0], base) if len(after) else None})
    return out


def pick(mask, n=1):
    return raw[mask].Transaction_ID.head(n).tolist()


ids = (pick(raw.Genero.isna() & raw.Metodo_Pago.isna()) + pick(raw.Precio_Unitario < 0) + pick(raw.Categoria_Producto == "  HOGAR  ")
       + pick(raw.Categoria_Producto == "Electronica") + pick(raw.Cantidad == 0) + pick(raw.Edad.isna()) + pick(raw.Categoria_Producto == "    "))

summary = {
    "raw": {
        "rows": len(raw),
        "duplicateRows": int(raw.duplicated().sum()),
        "duplicateIds": int(raw.duplicated("Transaction_ID").sum()),
        "nulls": {c: int(raw[c].isna().sum()) for c in COLS},
        "negativePrices": int((raw.Precio_Unitario < 0).sum()),
        "zeroQuantity": int((raw.Cantidad == 0).sum()),
        "categories": counts(raw.Categoria_Producto),
        "genders": counts(raw.Genero),
    },
    "clean": {
        "rows": len(clean),
        "nulls": {c: int(clean[c].isna().sum()) for c in COLS},
        "categories": clean.Categoria_Producto.fillna("(vacío)").value_counts().to_dict(),
        "genders": clean.Genero.value_counts().to_dict(),
        "ageRanges": clean.Rango_Edad.value_counts().reindex(["18-25", "26-35", "36-50", "51+"]).fillna(0).astype(int).to_dict(),
        "payments": clean.Metodo_Pago.value_counts().to_dict(),
        "revenue": round(float(clean.Precio_Total.sum()), 2),
        "customers": int(clean.Cliente_ID.nunique()),
        "avgTicket": round(float(clean.Precio_Total.mean()), 2),
    },
    "monthly": monthly.rename(columns={"Año_Mes": "month", "Revenue": "revenue", "Num_Transacciones": "transactions"}).to_dict("records"),
    "byCategory": by_cat.rename(columns={"Categoria_Producto": "category", "Revenue_Total": "revenue", "Ticket_Promedio": "ticket",
                                         "Num_Transacciones": "transactions", "Unidades_Vendidas": "units"}).to_dict("records"),
    "samples": sample(ids),
}

out = ROOT / "web" / "src" / "metrics" / "summary.json"
out.write_text(json.dumps(summary, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print(f"{out.relative_to(ROOT)}: {len(raw)} -> {len(clean)} filas, {len(summary['samples'])} ejemplos")
