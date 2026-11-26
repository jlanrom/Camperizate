// Configurador Lifes Campers: sirve la web (public/) y guarda cada configuración en Notion.
// POST /api/configuracion  → crea una ficha en la base «Configuraciones de clientes · Málaga».
// Secretos del Worker: NOTION_TOKEN. Variable: NOTION_DATABASE_ID.

const MAX = 1900; // Notion admite 2000 caracteres por bloque de texto

const txt = (s) => [{ type: "text", text: { content: String(s ?? "").slice(0, MAX) } }];
const lista = (arr) => (Array.isArray(arr) ? arr : []).map(String).join("\n");
const sel = (v, permitidos) => (permitidos.includes(v) ? { select: { name: v } } : undefined);

function propiedades(p) {
  const c = p.cliente || {};
  const f = p.furgoneta || {};
  const props = {
    Ficha: { title: txt(`${c.nombre || "Sin nombre"} · ${f.longitud || ""}${f.altura || ""}`) },
    Referencia: { rich_text: txt(p.referencia) },
    Estado: { select: { name: "Nueva" } },
    Cliente: { rich_text: txt(c.nombre) },
    NIF: { rich_text: txt(c.nif) },
    "Dirección de facturación": { rich_text: txt(c.direccion) },
    "Tiene furgoneta": { checkbox: !!f.tiene },
    Furgoneta: { rich_text: txt(f.texto) },
    Distribución: { rich_text: txt(lista(p.distribucion)) },
    Acabados: { rich_text: txt(lista(p.acabados)) },
    Eléctrico: { rich_text: txt(lista(p.electrico)) },
    "Prioridades del cliente": { rich_text: txt(p.prioridades) },
    "Avisos de espacio": { rich_text: txt(lista(p.avisos)) },
    Recibida: { date: { start: new Date().toISOString() } },
  };
  if (c.email) props.Email = { email: String(c.email).slice(0, 200) };
  if (c.telefono) props["Teléfono"] = { phone_number: String(c.telefono).slice(0, 40) };
  const tipo = sel(c.tipo, ["Particular", "Empresa"]); if (tipo) props["Tipo de cliente"] = tipo;
  const lo = sel(f.longitud, ["L1", "L2", "L3", "L4", "Aconsejadme"]); if (lo) props.Longitud = lo;
  const al = sel(f.altura, ["H1", "H2", "H3", "Aconsejadme"]); if (al) props.Altura = al;
  const pl = sel(String(p.plazas), ["2", "4"]); if (pl) props.Plazas = pl;
  return props;
}

function cuerpo(p) {
  const h2 = (t) => ({ object: "block", type: "heading_2", heading_2: { rich_text: txt(t) } });
  const h3 = (t) => ({ object: "block", type: "heading_3", heading_3: { rich_text: txt(t) } });
  const li = (t) => ({ object: "block", type: "bulleted_list_item", bulleted_list_item: { rich_text: txt(t) } });
  const todo = (t) => ({ object: "block", type: "to_do", to_do: { rich_text: txt(t), checked: false } });
  const nota = (t) => ({ object: "block", type: "callout", callout: { rich_text: txt(t), icon: { type: "emoji", emoji: "🛠️" } } });
  const bloques = [];
  // Hoja de trabajo: lo elegido por el cliente en lista; lo que hay que confirmar o definir, como casilla
  if (Array.isArray(p.hoja) && p.hoja.length) {
    bloques.push(h2("Hoja de trabajo"));
    bloques.push(nota("Las casillas son lo que el encargado debe confirmar o definir antes de comprar material. Márcalas al cerrarlas."));
    for (const s of p.hoja) {
      bloques.push(h3(s.t));
      for (const [etiqueta, valor, estado] of s.rows || []) {
        if (estado === "taller") bloques.push(todo(`${etiqueta}: POR DEFINIR`));
        else if (estado === "defecto") bloques.push(todo(`${etiqueta}: ${valor} (por defecto, confirmar)`));
        else bloques.push(li(`${etiqueta}: ${valor}`));
      }
    }
  }
  // Lista de compra estimada como tabla
  if (Array.isArray(p.compra) && p.compra.length) {
    const celda = (s) => txt(s);
    const fila = (cells) => ({ type: "table_row", table_row: { cells: cells.map(celda) } });
    bloques.push(h2("Lista de compra (estimada)"));
    bloques.push(nota("Cantidades calculadas con las medidas del modelo. Revísalas con el despiece antes de pedir."));
    bloques.push({ object: "block", type: "table", table: { table_width: 4, has_column_header: true, has_row_header: false,
      children: [fila(["Partida", "Material", "Cantidad", "Nota"])].concat(p.compra.slice(0, 99).map(([pa, m, q, u, n]) => fila([pa, m, q === "" ? "—" : `${String(q).replace(".", ",")} ${u}`, n || ""]))) } });
  }
  if (p.promptFoto) {
    bloques.push(h2("Descripción para generar la foto"));
    bloques.push({ object: "block", type: "paragraph", paragraph: { rich_text: txt(p.promptFoto) } });
  }
  bloques.push(h2("Lo que eligió el cliente"));
  bloques.push(h3("Furgoneta"), li(p.furgoneta?.texto));
  for (const [titulo, lista] of [["Distribución", p.distribucion], ["Acabados", p.acabados], ["Extras", p.electrico], ["Avisos del configurador", p.avisos]]) {
    if ((lista || []).length) bloques.push(h3(titulo), ...lista.map(li));
  }
  return bloques.slice(0, 100); // límite de Notion por petición
}

async function guardar(req, env) {
  let p;
  try { p = await req.json(); } catch { return json({ ok: false, error: "json" }, 400); }
  if (!p?.cliente?.nombre || !(p.cliente.email || p.cliente.telefono)) return json({ ok: false, error: "faltan datos" }, 400);
  if (!env.NOTION_TOKEN || !env.NOTION_DATABASE_ID) return json({ ok: false, error: "sin configurar" }, 503);
  const r = await fetch("https://api.notion.com/v1/pages", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.NOTION_TOKEN}`, "Notion-Version": "2022-06-28", "Content-Type": "application/json" },
    body: JSON.stringify({ parent: { database_id: env.NOTION_DATABASE_ID }, properties: propiedades(p), children: cuerpo(p) }),
  });
  if (!r.ok) { console.error("Notion", r.status, await r.text()); return json({ ok: false, error: "notion" }, 502); }
  return json({ ok: true, referencia: p.referencia });
}

const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { "Content-Type": "application/json" } });

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname === "/api/configuracion") {
      if (req.method !== "POST") return json({ ok: false }, 405);
      return guardar(req, env);
    }
    return env.ASSETS.fetch(req);
  },
};

export { propiedades, cuerpo };
