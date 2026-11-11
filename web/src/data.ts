import summary from './metrics/summary.json';

export type Row = {
  Transaction_ID: number; Genero: string | null; Edad: number | null; Categoria_Producto: string | null;
  Cantidad: number; Precio_Unitario: number; Precio_Total: number | null; Metodo_Pago: string | null;
};

export const S = summary as unknown as {
  raw: {
    rows: number; duplicateRows: number; duplicateIds: number; nulls: Record<string, number>;
    negativePrices: number; zeroQuantity: number;
    categories: { value: string; n: number }[]; genders: { value: string; n: number }[];
  };
  clean: {
    rows: number; nulls: Record<string, number>; categories: Record<string, number>; genders: Record<string, number>;
    ageRanges: Record<string, number>; payments: Record<string, number>; revenue: number; customers: number; avgTicket: number;
  };
  monthly: { month: string; revenue: number; transactions: number }[];
  byCategory: { category: string; revenue: number; ticket: number; transactions: number; units: number }[];
  samples: { before: Row; after: Row | null }[];
};

export const COLUMN_LABEL: Record<string, string> = {
  Genero: 'Género', Edad: 'Edad', Categoria_Producto: 'Categoría', Precio_Total: 'Precio total', Metodo_Pago: 'Método de pago',
};

export const n = (v: number, d = 0) => v.toLocaleString('es', { minimumFractionDigits: d, maximumFractionDigits: d });
export const usd = (v: number) => `$${n(v, 0)}`;
