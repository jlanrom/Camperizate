// Stripe : vérification de signature des webhooks et appels API (sans dépendance).

const enc = new TextEncoder();

function hex(buf) {
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function egal(a, b) {
  if (a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

/** Vérifie l'en-tête Stripe-Signature (schéma v1, tolérance 5 min). Lève une erreur si invalide. */
export async function verifierSignature(corps, entete, secret, maintenant = Date.now() / 1000, tolerance = 300) {
  if (!secret) throw new Error("STRIPE_WEBHOOK_SECRET manquant dans Cloudflare (type Secret)");
  if (!entete) throw new Error("signature absente");
  const parts = Object.fromEntries([]);
  const v1 = [];
  for (const morceau of entete.split(",")) {
    const [k, v] = morceau.split("=");
    if (k === "t") parts.t = v;
    if (k === "v1") v1.push(v);
  }
  if (!parts.t || v1.length === 0) throw new Error("signature mal formée");
  if (Math.abs(maintenant - Number(parts.t)) > tolerance) throw new Error("signature expirée");
  const cle = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const attendu = hex(await crypto.subtle.sign("HMAC", cle, enc.encode(`${parts.t}.${corps}`)));
  if (!v1.some((s) => egal(s, attendu))) throw new Error("signature invalide");
  return true;
}

/** Calcule une signature valide (utile pour les tests). */
export async function signer(corps, secret, t = Math.floor(Date.now() / 1000)) {
  const cle = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return `t=${t},v1=${hex(await crypto.subtle.sign("HMAC", cle, enc.encode(`${t}.${corps}`)))}`;
}

function formulaire(obj, prefixe = "", out = new URLSearchParams()) {
  for (const [k, v] of Object.entries(obj)) {
    const cle = prefixe ? `${prefixe}[${k}]` : k;
    if (v !== null && typeof v === "object") formulaire(v, cle, out);
    else if (v !== undefined) out.append(cle, String(v));
  }
  return out;
}

export function clientStripe(secretKey, fetchFn = fetch) {
  async function appel(methode, chemin, corps) {
    const r = await fetchFn(`https://api.stripe.com/v1${chemin}`, {
      method: methode,
      headers: {
        Authorization: `Bearer ${secretKey}`,
        "Content-Type": "application/x-www-form-urlencoded",
        "Stripe-Version": "2025-09-30.clover",
      },
      body: corps ? formulaire(corps).toString() : undefined,
    });
    const json = await r.json();
    if (!r.ok) throw new Error(`Stripe ${methode} ${chemin} : ${r.status} ${json?.error?.message || ""}`);
    return json;
  }
  return {
    session: (id) =>
      appel("GET", `/checkout/sessions/${id}?expand[]=line_items.data.price.product&expand[]=payment_intent`),
    majMetadataPaiement: (paymentIntentId, metadata) =>
      appel("POST", `/payment_intents/${paymentIntentId}`, { metadata }),
  };
}
