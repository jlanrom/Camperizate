// Worker « facturation » : Stripe (Payment Links) -> Holded (contact, bon de commande, facture) + e-mail client.
//
// Étapes, chacune mémorisée dans les métadonnées du paiement Stripe (PaymentIntent), ce qui rend
// le traitement idempotent : si Stripe renvoie l'événement, les étapes déjà faites sont sautées.
//   holded_contact  -> holded_commande -> holded_mail -> holded_facture -> holded_paiement

import { verifierSignature, clientStripe } from "./stripe.js";
import { clientHolded } from "./holded.js";
import { lireCommande, contactHolded, documentHolded, emailCommande, lignesHolded, totalRecalcule } from "./commande.js";

const EVENEMENTS = new Set(["checkout.session.completed", "checkout.session.async_payment_succeeded"]);

export async function traiterSession(sessionId, env, deps = {}) {
  const stripe = deps.stripe || clientStripe(env.STRIPE_SECRET_KEY);
  const holded = deps.holded || clientHolded(env.HOLDED_API_KEY);
  const journal = [];
  const log = (m) => { journal.push(m); console.log(m); };

  const session = await stripe.session(sessionId);
  if (env.SITE_METADATA && session.metadata?.site !== env.SITE_METADATA) {
    log(`ignoré : session ${sessionId} hors ${env.SITE_METADATA}`);
    return { ignore: true, journal };
  }
  if (session.payment_status !== "paid") {
    log(`ignoré : session ${sessionId} non payée (${session.payment_status})`);
    return { ignore: true, journal };
  }
  const commande = lireCommande(session);
  const fait = { ...commande.metadataPaiement };
  const dry = env.DRY_RUN === "true";
  const memoriser = async (cle, valeur) => {
    fait[cle] = valeur;
    if (!dry && commande.paymentIntentId) await stripe.majMetadataPaiement(commande.paymentIntentId, { [cle]: valeur });
  };

  const items = lignesHolded(commande, env);
  const recalcule = totalRecalcule(items);
  if (Math.abs(recalcule - commande.totalTTC) > 0.01) {
    log(`attention : total Holded recalculé ${recalcule} ≠ Stripe ${commande.totalTTC} (arrondi)`);
  }

  if (dry) {
    log(`DRY_RUN : contact ${JSON.stringify(contactHolded(commande))}`);
    log(`DRY_RUN : commande ${JSON.stringify(documentHolded(commande, "<contact>", env, { type: "salesorder" }))}`);
    log(`DRY_RUN : facture ${JSON.stringify(documentHolded(commande, "<contact>", env, { type: "invoice" }))}`);
    log(`DRY_RUN : e-mail à ${commande.email}\n${JSON.stringify(emailCommande(commande, "SO-XXXX"))}`);
    return { dry: true, commande, journal };
  }

  // 1. Contact (recherché par CustomId = stripe:<email>, sinon créé)
  if (!fait.holded_contact) {
    const trouves = await holded.contactsParCustomId(`stripe:${commande.email}`);
    const id = Array.isArray(trouves) && trouves[0]?.id ? trouves[0].id : (await holded.creerContact(contactHolded(commande))).id;
    await memoriser("holded_contact", id);
    log(`contact ${id}`);
  }

  // 2. Bon de commande
  let numero = fait.holded_commande_num || "";
  if (!fait.holded_commande) {
    const r = await holded.creerDocument("salesorder", documentHolded(commande, fait.holded_contact, env, { type: "salesorder" }));
    await memoriser("holded_commande", r.id);
    try {
      const doc = await holded.lireDocument("salesorder", r.id);
      numero = doc.docNumber || doc.number || "";
      if (numero) await memoriser("holded_commande_num", numero);
    } catch (e) { log(`numéro de commande non lu : ${e.message}`); }
    log(`bon de commande ${r.id} ${numero}`);
  }

  // 3. E-mail de confirmation au client (bon de commande en PDF + texte : récapitulatif, délais, CGV)
  if (!fait.holded_mail && commande.email) {
    const { subject, message } = emailCommande(commande, numero);
    await holded.envoyerDocument("salesorder", fait.holded_commande, { emails: commande.email, subject, message });
    await memoriser("holded_mail", "envoye");
    log(`e-mail envoyé à ${commande.email}`);
  }

  // 4. Facture (brouillon par défaut, approuvée si APPROVE_INVOICE=true)
  if (!fait.holded_facture) {
    const r = await holded.creerDocument("invoice", documentHolded(commande, fait.holded_contact, env, { type: "invoice" }));
    await memoriser("holded_facture", r.id);
    log(`facture ${r.id}`);
    if (env.APPROVE_INVOICE === "true" && env.SEND_INVOICE === "true" && commande.email) {
      await holded.envoyerDocument("invoice", r.id, {
        emails: commande.email,
        subject: "Votre facture Camperizate",
        message: "Bonjour, vous trouverez ci-joint la facture de votre commande. Merci pour votre confiance ! L'équipe Camperizate",
      });
      log("facture envoyée");
    }
  }

  // 5. Paiement enregistré sur la facture (si une trésorerie Holded est configurée)
  if (!fait.holded_paiement && env.HOLDED_TREASURY_ID) {
    await holded.payerDocument("invoice", fait.holded_facture, {
      date: commande.date,
      amount: commande.totalTTC,
      treasury: env.HOLDED_TREASURY_ID,
      desc: `Stripe ${commande.paymentIntentId || commande.sessionId}`,
    });
    await memoriser("holded_paiement", "ok");
    log("paiement enregistré");
  }

  return { ok: true, fait, journal };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/") {
      return new Response("Facturation Stripe → Holded : en service.", { status: 200 });
    }
    if (request.method !== "POST" || url.pathname !== "/stripe") {
      return new Response("Not found", { status: 404 });
    }
    const corps = await request.text();
    try {
      await verifierSignature(corps, request.headers.get("stripe-signature"), env.STRIPE_WEBHOOK_SECRET);
    } catch (e) {
      return new Response(`Signature refusée : ${e.message}`, { status: 400 });
    }
    const evt = JSON.parse(corps);
    if (!EVENEMENTS.has(evt.type)) return new Response(`ignoré : ${evt.type}`, { status: 200 });
    try {
      const r = await traiterSession(evt.data.object.id, env);
      return new Response(JSON.stringify({ ok: true, journal: r.journal }), { status: 200, headers: { "Content-Type": "application/json" } });
    } catch (e) {
      // 500 => Stripe réessaiera ; les étapes déjà faites ne seront pas refaites.
      console.error(e);
      return new Response(`Erreur : ${e.message}`, { status: 500 });
    }
  },
};
