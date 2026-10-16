// Holded : API « invoicing v1 » (en-tête `key`). https://developers.holded.com/

const BASE = "https://api.holded.com/api/invoicing/v1";

export function clientHolded(apiKey, fetchFn = fetch) {
  async function appel(methode, chemin, corps) {
    const r = await fetchFn(`${BASE}${chemin}`, {
      method: methode,
      headers: { key: apiKey, Accept: "application/json", "Content-Type": "application/json" },
      body: corps ? JSON.stringify(corps) : undefined,
    });
    const texte = await r.text();
    let json;
    try { json = texte ? JSON.parse(texte) : {}; } catch { json = { brut: texte }; }
    if (!r.ok || json?.status === 0) {
      throw new Error(`Holded ${methode} ${chemin} : ${r.status} ${texte.slice(0, 300)}`);
    }
    return json;
  }
  return {
    contactsParCustomId: (customId) => appel("GET", `/contacts?customId=${encodeURIComponent(customId)}`),
    creerContact: (contact) => appel("POST", "/contacts", contact),
    creerDocument: (type, doc) => appel("POST", `/documents/${type}`, doc),
    lireDocument: (type, id) => appel("GET", `/documents/${type}/${id}`),
    payerDocument: (type, id, paiement) => appel("POST", `/documents/${type}/${id}/pay`, paiement),
    envoyerDocument: (type, id, envoi) => appel("POST", `/documents/${type}/${id}/send`, envoi),
  };
}
