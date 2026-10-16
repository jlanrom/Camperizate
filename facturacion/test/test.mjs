// Tests sans réseau : node facturacion/test/test.mjs
import assert from "node:assert/strict";
import worker, { traiterSession } from "../src/index.js";
import { signer, verifierSignature } from "../src/stripe.js";
import { lignesHolded, totalRecalcule, lireCommande, emailCommande } from "../src/commande.js";

const ENV = {
  DRY_RUN: "false", SITE_METADATA: "kitamenagement.fr", TAX_KEY: "s_iva_21", TAX_RATE: "21", TAX_BY_COUNTRY: "{}",
  HOLDED_SALES_ACCOUNT_ID: "67d01537b71b6257a30c39cb", HOLDED_PAYMENT_METHOD_ID: "6a591285b8a9e7007a0e35e2",
  HOLDED_ORDER_SERIES_ID: "67d01533b71b6257a30c391c", HOLDED_INVOICE_SERIES_ID: "", HOLDED_TREASURY_ID: "tresorerie1",
  APPROVE_INVOICE: "false", SEND_INVOICE: "false", STRIPE_WEBHOOK_SECRET: "whsec_test",
};

const ligne = (nom, cle, total, q = 1) => ({ description: nom, quantity: q, amount_total: total, price: { product: { name: nom, metadata: { cle } } } });
function session(extra = {}) {
  return {
    id: "cs_test_1", created: 1792150000, payment_status: "paid", amount_total: 90000, metadata: { site: "kitamenagement.fr" },
    client_reference_id: "dacia-jogger-lodgy",
    customer_details: { email: "Marie.Dupont@example.fr", name: "Marie Dupont", phone: "+33612345678",
      address: { line1: "12 rue des Arènes", city: "Nîmes", postal_code: "30000", country: "FR" } },
    collected_information: { shipping_details: { name: "Marie Dupont", address: { line1: "12 rue des Arènes", city: "Nîmes", postal_code: "30000", country: "FR" } } },
    custom_fields: [{ key: "modele", text: { value: "Dacia Jogger 2023" } }],
    line_items: { data: [
      ligne("Kit camper ludospace – Phénolique carrossier", "kit-mini-carrossier", 55000),
      ligne("Matelas sur mesure", "matelas", 15000),
      ligne("Livraison – kit ludospace (France métropolitaine)", "livraison-mini", 20000),
    ] },
    payment_intent: { id: "pi_1", metadata: {} },
    ...extra,
  };
}

function faux() {
  const appels = [];
  const metaPI = {};
  const stripe = {
    session: async () => { const s = session(); s.payment_intent.metadata = { ...metaPI }; return s; },
    majMetadataPaiement: async (id, m) => { appels.push(["stripe.meta", m]); Object.assign(metaPI, m); },
  };
  const holded = {
    contactsParCustomId: async (c) => { appels.push(["contacts?", c]); return []; },
    creerContact: async (c) => { appels.push(["creerContact", c]); return { status: 1, id: "c1" }; },
    creerDocument: async (t, d) => { appels.push(["creer", t, d]); return { status: 1, id: t === "invoice" ? "f1" : "so1" }; },
    lireDocument: async () => ({ docNumber: "SO260001" }),
    envoyerDocument: async (t, id, e) => { appels.push(["envoyer", t, id, e]); return { status: 1 }; },
    payerDocument: async (t, id, p) => { appels.push(["payer", t, id, p]); return { status: 1 }; },
  };
  return { stripe, holded, appels, metaPI };
}

// 1. Signature
const corps = JSON.stringify({ type: "checkout.session.completed", data: { object: { id: "cs_test_1" } } });
const sig = await signer(corps, "whsec_test");
assert.equal(await verifierSignature(corps, sig, "whsec_test"), true);
await assert.rejects(() => verifierSignature(corps, sig, "autre_secret"), /invalide/);
await assert.rejects(() => verifierSignature(corps, sig, "whsec_test", Date.now() / 1000 + 3600), /expirée/);
const rep = await worker.fetch(new Request("https://x/stripe", { method: "POST", body: corps, headers: { "stripe-signature": "t=1,v1=00" } }), ENV);
assert.equal(rep.status, 400);
console.log("✓ signature Stripe (valide, fausse, expirée, refus HTTP 400)");

// 2. Lignes et TVA incluse
const cmd = lireCommande(session());
const items = lignesHolded(cmd, ENV);
assert.equal(items.length, 3);
assert.equal(items[0].subtotal, 454.5455);
assert.equal(totalRecalcule(items), 900);
assert.equal(cmd.email, "marie.dupont@example.fr");
assert.equal(cmd.livraison, true);
console.log("✓ lignes HT/TTC : 900,00 € Stripe = 900,00 € recalculé dans Holded");
for (const total of [50000, 65000, 70000, 95000, 115000, 2900, 3500, 14900, 97500]) {
  const t = totalRecalcule(lignesHolded({ lignes: [{ nom: "x", cle: "x", quantite: 1, totalTTC: total / 100 }], adresse: {} }, ENV));
  assert.equal(t, total / 100, `arrondi ${total}`);
}
console.log("✓ aucun écart d'arrondi sur les prix du catalogue");

// 3. Traitement complet
const f = faux();
const r = await traiterSession("cs_test_1", ENV, f);
assert.equal(r.ok, true);
const etapes = f.appels.map((a) => a[0] + (a[1] && typeof a[1] === "string" ? ":" + a[1] : ""));
console.log("  appels :", etapes.join(" → "));
const so = f.appels.find((a) => a[0] === "creer" && a[1] === "salesorder")[2];
assert.equal(so.contactId, "c1");
assert.equal(so.numSerieId, "67d01533b71b6257a30c391c");
assert.equal(so.shippingCity, "Nîmes");
const fac = f.appels.find((a) => a[0] === "creer" && a[1] === "invoice")[2];
assert.equal(fac.approveDoc, false);
assert.equal(fac.paymentMethodId, "6a591285b8a9e7007a0e35e2");
const mail = f.appels.find((a) => a[0] === "envoyer")[3];
assert.equal(mail.emails, "marie.dupont@example.fr");
assert.match(mail.subject, /SO260001/);
assert.ok(mail.subject.length >= 10 && mail.message.length >= 20);
const pay = f.appels.find((a) => a[0] === "payer")[3];
assert.equal(pay.amount, 900);
console.log("✓ contact → bon de commande → e-mail → facture brouillon → paiement");

// 4. Idempotence : Stripe renvoie le même événement
const avant = f.appels.length;
await traiterSession("cs_test_1", ENV, f);
assert.equal(f.appels.filter((a, i) => i >= avant && a[0] !== "stripe.meta").length, 0);
console.log("✓ renvoi du même paiement : rien n'est créé ni envoyé deux fois");

// 5. Paiement d'une autre source (ex. Webnode) ignoré
const g = faux();
g.stripe.session = async () => session({ metadata: {} });
const ig = await traiterSession("cs_x", ENV, g);
assert.equal(ig.ignore, true);
assert.equal(g.appels.length, 0);
console.log("✓ paiement hors kitamenagement.fr ignoré");

// 6. DRY_RUN : rien n'est écrit
const h = faux();
const d = await traiterSession("cs_test_1", { ...ENV, DRY_RUN: "true" }, h);
assert.equal(d.dry, true);
assert.equal(h.appels.length, 0);
console.log("✓ DRY_RUN n'écrit rien");

// 7. Aperçu de l'e-mail
console.log("\n--- Aperçu de l'e-mail ---");
const e = emailCommande(cmd, "SO260001");
console.log("Objet :", e.subject);
console.log(e.message);
