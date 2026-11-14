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
  const h = (t) => ({ object: "block", type: "heading_3", heading_3: { rich_text: txt(t) } });
  const li = (t) => ({ object: "block", type: "bulleted_list_item", bulleted_list_item: { rich_text: txt(t) } });
  const bloques = [h("Furgoneta"), li(p.furgoneta?.texto)];
  bloques.push(h("Distribución"), ...(p.distribucion || []).map(li));
  if (p.prioridades) bloques.push(li("Prioridades: " + p.prioridades));
  bloques.push(h("Acabados"), ...(p.acabados || []).map(li));
  bloques.push(h("Electricidad"), ...(p.electrico || []).map(li));
  if ((p.avisos || []).length) bloques.push(h("Avisos del configurador"), ...p.avisos.map(li));
  return bloques.slice(0, 90);
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
