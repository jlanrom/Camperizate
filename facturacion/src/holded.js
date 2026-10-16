// Client minimal de l'API Holded v2 (https://api.holded.com/api/v2, en-tête Authorization: Bearer <clé>).
const BASE = "https://api.holded.com/api/v2";

export function clientHolded(apiKey, fetchFn = fetch) {
  async function appel(methode, chemin, corps) {
    if (!apiKey) throw new Error("HOLDED_API_KEY manquante (Cloudflare > Variables and Secrets, type Secret)");
    const r = await fetchFn(BASE + chemin, {
      method: methode,
      headers: { Authorization: `Bearer ${apiKey}`, Accept: "application/json", "Content-Type": "application/json" },
      body: corps ? JSON.stringify(corps) : undefined,
    });
    const texte = await r.text();
    let json = {};
    try { json = texte ? JSON.parse(texte) : {}; } catch { json = { brut: texte }; }
    if (!r.ok || json.status === 0) throw new Error(`Holded ${methode} ${chemin} : ${r.status} ${texte.slice(0, 300)}`);
    return json;
  }
  const liste = (j) => (Array.isArray(j) ? j : j.items || j.data || j.contacts || []);

  return {
    /** Cherche un contact par e-mail exact. Le filtre est vérifié côté worker : on ne réutilise que l'e-mail identique. */
    async contactParEmail(email) {
      if (!email) return null;
      const essais = [`/contacts?email=${encodeURIComponent(email)}`, `/contacts/search?query=${encodeURIComponent(email)}`];
      for (const chemin of essais) {
        try {
          const c = liste(await appel("GET", chemin)).find((x) => (x.email || "").trim().toLowerCase() === email);
          if (c?.id) return c;
        } catch (e) {
          if (/ 401 | 403 /.test(e.message)) throw e; // clé invalide : inutile de continuer
        }
      }
      return null;
    },
    creerContact: (contact) => appel("POST", "/contacts", contact),
    creerCommande: (doc) => appel("POST", "/sales-orders", doc),
    lireCommande: (id) => appel("GET", `/sales-orders/${id}`),
    envoyerCommande: (id, envoi) => appel("POST", `/sales-orders/${id}/send`, envoi),
    creerFacture: (doc) => appel("POST", "/invoices", doc),
    approuverFacture: (id) => appel("POST", `/invoices/${id}/approve`, {}),
    envoyerFacture: (id, envoi) => appel("POST", `/invoices/${id}/send`, envoi),
    payerFacture: (id, paiement) => appel("POST", `/invoices/${id}/payments`, paiement),
  };
}
