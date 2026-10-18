// Worker « facturation » : Stripe (Payment Links) -> Holded (contact, bon de commande, facture) + e-mail client.
//
// Étapes, chacune mémorisée dans les métadonnées du paiement Stripe (PaymentIntent), ce qui rend
// le traitement idempotent : si Stripe renvoie l'événement, les étapes déjà faites sont sautées.
//   holded_contact  -> holded_commande -> holded_mail -> holded_facture -> holded_paiement

import { verifierSignature, clientStripe } from "./stripe.js";
import { clientHolded } from "./holded.js";
import { lireCommande, contactHolded, documentHolded, emailCommande, lignesHolded, totalRecalcule, dateISO } from "./commande.js";

const EVENEMENTS = new Set(["checkout.session.completed", "checkout.session.async_payment_succeeded"]);

export async function traiterSession(sessionId, env, deps = {}) {
  const stripe = deps.stripe || clientStripe(env.STRIPE_SECRET_KEY);
  const holded = deps.holded || clientHolded(env.HOLDED_API_KEY);
  const journal = [];
  const log = (m) => { journal.push(m); console.log(m); };

  const session = await stripe.session(sessionId);
  const sites = (env.SITE_METADATA || "").split(",").map((x) => x.trim()).filter(Boolean);
  if (sites.length && !sites.includes(session.metadata?.site)) {
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

  // 1. Contact (recherché par e-mail exact, sinon créé)
  if (!fait.holded_contact) {
    const existant = await holded.contactParEmail(commande.email);
    const id = existant?.id || (await holded.creerContact(contactHolded(commande))).id;
    await memoriser("holded_contact", id);
    log(`contact ${id}${existant ? " (existant)" : " (créé)"}`);
  }

  // 2. Bon de commande
  let numero = fait.holded_commande_num || "";
  if (!fait.holded_commande) {
    const r = await holded.creerCommande(documentHolded(commande, fait.holded_contact, env, { type: "salesorder" }));
    await memoriser("holded_commande", r.id);
    try {
      const doc = await holded.lireCommande(r.id);
      numero = doc.number || doc.document_number || doc.doc_number || doc.docNumber || "";
      if (numero) await memoriser("holded_commande_num", numero);
    } catch (e) { log(`numéro de commande non lu : ${e.message}`); }
    log(`bon de commande ${r.id} ${numero}`);
  }

  // 3. E-mail de confirmation au client (bon de commande en PDF + texte : récapitulatif, délais, CGV)
  if (!fait.holded_mail && commande.email) {
    const { subject, message } = emailCommande(commande, numero);
    await holded.envoyerCommande(fait.holded_commande, { emails: [commande.email], subject, message });
    await memoriser("holded_mail", "envoye");
    log(`e-mail envoyé à ${commande.email}`);
  }

  // 4. Facture (brouillon par défaut ; approuvée si APPROVE_INVOICE=true)
  if (!fait.holded_facture) {
    const r = await holded.creerFacture(documentHolded(commande, fait.holded_contact, env, { type: "invoice" }));
    await memoriser("holded_facture", r.id);
    log(`facture ${r.id}`);
  }
  if (env.APPROVE_INVOICE === "true" && !fait.holded_facture_ok) {
    await holded.approuverFacture(fait.holded_facture);
    await memoriser("holded_facture_ok", "approuvee");
    log("facture approuvée");
    if (env.SEND_INVOICE === "true" && commande.email) {
      await holded.envoyerFacture(fait.holded_facture, {
        emails: [commande.email],
        ...(commande.langue === "it"
          ? { subject: "La tua fattura Camperizate", message: "Ciao, in allegato trovi la fattura del tuo ordine. Grazie per la fiducia! Il team Camperizate" }
          : { subject: "Votre facture Camperizate", message: "Bonjour, vous trouverez ci-joint la facture de votre commande. Merci pour votre confiance ! L'équipe Camperizate" }),
      });
      log("facture envoyée");
    }
  }

  // 5. Paiement enregistré sur la facture (si une trésorerie Holded est configurée)
  if (!fait.holded_paiement && env.HOLDED_TREASURY_ID) {
    await holded.payerFacture(fait.holded_facture, {
      date: dateISO(commande.date),
      amount: commande.totalTTC,
      treasury_id: env.HOLDED_TREASURY_ID,
      description: `Stripe ${commande.paymentIntentId || commande.sessionId}`,
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
