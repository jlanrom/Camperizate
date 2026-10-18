// Transforme une Checkout Session Stripe en commande, lignes Holded et e-mail client.

const CGV = "https://kitamenagement.fr/conditions-generales-de-vente/";
const SHOWROOM = "Local n° 112, 866 avenue du Maréchal Juin, 30900 Nîmes";
const ATELIER = "Carrer de Vulcà 1B, 08530 La Garriga (Barcellona), Spagna";

/** Réglages par site (métadonnée « site » des Payment Links). */
export const SITES = {
  "kitamenagement.fr": { langue: "fr", tag: "web-fr", cgv: CGV },
  "kitcampermodulare.it": { langue: "it", tag: "web-it", cgv: "https://kitcampermodulare.it/condizioni-generali-di-vendita/" },
};
const RITIRO = { lagarriga: "La Garriga (atelier)", nimes: "Nîmes (showroom)" };
const CONTACT = "WhatsApp +34 665 319 287 · info@camperizatetodoen1.com";

const arrondi = (n, d = 2) => Math.round((n + Number.EPSILON) * 10 ** d) / 10 ** d;
const euros = (n) => `${n.toFixed(2).replace(".", ",")} €`;

/** Taxe à appliquer : par pays si configuré (ex. OSS), sinon taxe par défaut. */
export function taxePour(pays, config) {
  const parPays = JSON.parse(config.TAX_BY_COUNTRY || "{}");
  if (pays && parPays[pays]) return { cle: parPays[pays].key, taux: Number(parPays[pays].rate) };
  return { cle: config.TAX_KEY || "s_iva_21", taux: Number(config.TAX_RATE ?? 21) };
}

export function lireCommande(session) {
  const client = session.customer_details || {};
  const livraisonInfo = session.collected_information?.shipping_details || session.shipping_details || null;
  const champs = Object.fromEntries((session.custom_fields || []).map((c) => [c.key, c.text?.value || c.dropdown?.value || c.numeric?.value || ""]));
  const lignes = (session.line_items?.data || []).map((li) => {
    const produit = li.price?.product || {};
    const quantite = li.quantity || 1;
    return {
      nom: produit.name || li.description,
      description: produit.description || "",
      cle: produit.metadata?.cle || "",
      quantite,
      totalTTC: (li.amount_total ?? li.amount_subtotal) / 100,
    };
  });
  const livraison = lignes.some((l) => l.cle.startsWith("livraison"));
  const estKit = lignes.some((l) => l.cle.startsWith("kit-"));
  return {
    sessionId: session.id,
    paymentIntentId: typeof session.payment_intent === "string" ? session.payment_intent : session.payment_intent?.id,
    metadataPaiement: typeof session.payment_intent === "object" ? session.payment_intent?.metadata || {} : {},
    date: session.created,
    email: (client.email || "").trim().toLowerCase(),
    nom: client.name || livraisonInfo?.name || client.email,
    telephone: client.phone || "",
    adresse: client.address || {},
    livraisonAdresse: livraisonInfo?.address || null,
    vehicule: champs.modele || "",
    ritiro: champs.ritiro || "",
    site: SITES[session.metadata?.site] ? session.metadata.site : "kitamenagement.fr",
    modeleSite: session.client_reference_id || "",
    lignes,
    totalTTC: session.amount_total / 100,
    livraison,
    estKit,
    langue: (SITES[session.metadata?.site] || SITES["kitamenagement.fr"]).langue,
  };
}

/** Lignes au format Holded v2 : prix unitaire HT (price), clé de taxe. Le taux sert au contrôle du total. */
export function lignesHolded(commande, config) {
  const { cle, taux } = taxePour(commande.adresse?.country, config);
  return commande.lignes.map((l) => {
    const unitTTC = l.totalTTC / l.quantite;
    const item = {
      name: l.nom,
      description: l.description || null,
      units: l.quantite,
      price: arrondi(unitTTC / (1 + taux / 100), 4),
      taxes: [cle],
      sku: l.cle || null,
      type: "product",
    };
    if (config.HOLDED_SALES_ACCOUNT_ID) item.account = config.HOLDED_SALES_ACCOUNT_ID;
    Object.defineProperty(item, "taux", { value: taux, enumerable: false });
    return item;
  });
}

/** Total TTC que Holded recalculera à partir des lignes (pour détecter un écart d'arrondi). */
export function totalRecalcule(items) {
  return arrondi(items.reduce((s, i) => s + arrondi(i.price * i.units * (1 + i.taux / 100), 2), 0), 2);
}

function adresseTexte(a) {
  if (!a) return "";
  return [a.line1, a.line2, `${a.postal_code || ""} ${a.city || ""}`.trim(), a.country].filter(Boolean).join(", ");
}

export const dateISO = (unix) => new Date(unix * 1000).toISOString().slice(0, 10);

export function contactHolded(commande) {
  const a = commande.adresse || {};
  return {
    name: commande.nom,
    email: commande.email,
    mobile: commande.telephone || null,
    type: "client",
    is_person: true,
    tags: [(SITES[commande.site] || SITES["kitamenagement.fr"]).tag, "stripe"],
    bill_address: {
      address: [a.line1, a.line2].filter(Boolean).join(", "),
      city: a.city || "",
      postal_code: a.postal_code || "",
      province: a.state || "",
      country_code: a.country || "",
    },
  };
}

export function documentHolded(commande, contactId, config, { type }) {
  const doc = {
    contact_id: contactId,
    date: dateISO(commande.date),
    description: `Commande web ${commande.site || "kitamenagement.fr"}${commande.vehicule ? ` – ${commande.vehicule}` : ""}`,
    notes: [
      `Stripe : ${commande.sessionId}`,
      commande.vehicule && `Véhicule : ${commande.vehicule}`,
      commande.modeleSite && `Modèle choisi sur le site : ${commande.modeleSite}`,
      commande.livraison ? `Livraison : ${adresseTexte(commande.livraisonAdresse)}`
        : `Retrait : ${RITIRO[commande.ritiro] || "showroom de Nîmes"}`,
      commande.telephone && `Tél. : ${commande.telephone}`,
    ].filter(Boolean).join("\n"),
    items: lignesHolded(commande, config),
    language: commande.langue,
    currency: "EUR",
  };
  if (type === "salesorder" && config.HOLDED_ORDER_SERIES_ID) doc.number_line_id = config.HOLDED_ORDER_SERIES_ID;
  if (type === "invoice") {
    if (config.HOLDED_INVOICE_SERIES_ID) doc.number_line_id = config.HOLDED_INVOICE_SERIES_ID;
    if (config.HOLDED_PAYMENT_METHOD_ID) doc.payment_method_id = config.HOLDED_PAYMENT_METHOD_ID;
  }
  return doc;
}

/** E-mail de confirmation de commande (texte), envoyé via Holded avec le bon de commande en PDF. */
export function emailCommande(commande, numero) {
  if (commande.langue === "it") return emailCommandeIT(commande, numero);
  const prenom = (commande.nom || "").split(" ")[0];
  const lignes = commande.lignes.map((l) => `• ${l.quantite > 1 ? `${l.quantite} × ` : ""}${l.nom} : ${euros(l.totalTTC)}`).join("\n");
  const reception = commande.livraison
    ? `Livraison du kit monté, sur palette, à l'adresse : ${adresseTexte(commande.livraisonAdresse)}.`
    : `Retrait gratuit au showroom : ${SHOWROOM}.`;
  const etapes = commande.estKit
    ? [
        "1. Sous 48 h ouvrées, nous vous contactons pour vérifier les mesures de votre véhicule.",
        "2. Fabrication dans notre atelier : environ 3 semaines (plus rapide si votre modèle est en stock).",
        commande.livraison
          ? "3. Livraison : le transporteur vous appelle pour fixer le jour. À la réception, vérifiez le colis et notez toute réserve auprès du transporteur."
          : "3. Retrait : nous convenons ensemble du jour où vous passez au showroom de Nîmes.",
      ]
    : [
        "1. Nous préparons votre commande et vous contactons pour convenir du retrait ou de l'envoi avec votre kit.",
      ];
  const texte = [
    `Bonjour ${prenom},`,
    "",
    `Merci pour votre commande${numero ? ` n° ${numero}` : ""} ! Votre paiement est confirmé. Vous trouverez le bon de commande en pièce jointe.`,
    "",
    "Votre commande",
    lignes,
    `Total payé : ${euros(commande.totalTTC)} TTC`,
    commande.vehicule ? `Véhicule : ${commande.vehicule}` : "",
    reception,
    "",
    "Et maintenant ?",
    ...etapes,
    "",
    "Bon à savoir",
    commande.estKit || commande.lignes.some((l) => ["matelas", "occultants"].includes(l.cle))
      ? "• Votre kit est fabriqué sur mesure pour votre véhicule : il n'est donc pas soumis au droit de rétractation (art. L221-28, 3° du Code de la consommation)."
      : "• Accessoires standard : vous disposez de 14 jours après la réception pour vous rétracter.",
    "• Tous nos produits bénéficient de la garantie légale de conformité de 2 ans.",
    `• Nos conditions générales de vente : ${CGV}`,
    "",
    `Une question ? Écrivez-nous : ${CONTACT}.`,
    "",
    "À très bientôt sur la route,",
    "L'équipe Camperizate",
  ].filter((l, i, arr) => !(l === "" && arr[i - 1] === "")).join("\n");
  return {
    subject: `Votre commande Camperizate${numero ? ` n° ${numero}` : ""} est confirmée`,
    message: texte,
  };
}

/** E-mail de confirmation en italien (site kitcampermodulare.it). */
export function emailCommandeIT(commande, numero) {
  const nome = (commande.nom || "").split(" ")[0];
  const lignes = commande.lignes.map((l) => `• ${l.quantite > 1 ? `${l.quantite} × ` : ""}${l.nom}: ${euros(l.totalTTC)}`).join("\n");
  const luogo = commande.ritiro === "nimes" ? `showroom di Nîmes: ${SHOWROOM}` : `laboratorio di La Garriga: ${ATELIER}`;
  const consegna = commande.livraison
    ? `Consegna del kit montato, su pallet, all'indirizzo: ${adresseTexte(commande.livraisonAdresse)}.`
    : `Ritiro gratuito presso il ${luogo}.`;
  const passi = commande.estKit
    ? [
        "1. Entro 48 ore lavorative ti contattiamo per controllare le misure del tuo veicolo.",
        "2. Fabbricazione nel nostro laboratorio: circa 3 settimane (meno se il tuo modello è disponibile in magazzino).",
        commande.livraison
          ? "3. Consegna: il corriere ti chiama per fissare il giorno. Al ricevimento controlla la merce e annota eventuali riserve al corriere."
          : "3. Ritiro: concordiamo insieme il giorno in cui passi a ritirare il kit.",
      ]
    : ["1. Prepariamo il tuo ordine e ti contattiamo per concordare il ritiro o la spedizione insieme al kit."];
  const testo = [
    `Ciao ${nome},`,
    "",
    `Grazie per il tuo ordine${numero ? ` n. ${numero}` : ""}! Il pagamento è confermato. In allegato trovi la conferma d'ordine.`,
    "",
    "Il tuo ordine",
    lignes,
    `Totale pagato: ${euros(commande.totalTTC)} IVA inclusa`,
    commande.vehicule ? `Veicolo: ${commande.vehicule}` : "",
    consegna,
    "",
    "E adesso?",
    ...passi,
    "",
    "Da sapere",
    commande.estKit || commande.lignes.some((l) => ["matelas", "occultants"].includes(l.cle))
      ? "• Il kit è fabbricato su misura per il tuo veicolo: il diritto di recesso è escluso (art. 59, comma 1, lettera c, del Codice del Consumo)."
      : "• Accessori standard: hai 14 giorni dal ricevimento per recedere.",
    "• Tutti i nostri prodotti hanno la garanzia legale di conformità di 2 anni.",
    `• Le nostre condizioni generali di vendita: ${SITES["kitcampermodulare.it"].cgv}`,
    "",
    `Una domanda? Scrivici: ${CONTACT}.`,
    "",
    "A presto, in viaggio!",
    "Il team Camperizate",
  ].filter((l, i, arr) => !(l === "" && arr[i - 1] === "")).join("\n");
  return {
    subject: `Il tuo ordine Camperizate${numero ? ` n. ${numero}` : ""} è confermato`,
    message: testo,
  };
}
