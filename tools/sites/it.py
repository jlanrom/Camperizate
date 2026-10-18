"""Site italien : kitcampermodulare.it (dossier public-it/).

Les pages sont les mêmes que celles du site français (mêmes gabarits, même catalogue, mêmes prix de kit),
générées avec les réglages ci-dessous puis traduites avec tools/sites/it_textes.py.
Pages légales : écrites à la main dans tools/sites/it_pages/.
"""
CODE = "it"
LANG = "it"
LOCALE = "it_IT"          # og:locale
LOCALE_JS = "it-IT"       # format des prix dans les scripts (1.000 €)
SITE = "https://kitcampermodulare.it"
SORTIE = "public-it"
# Spedizione per categoria di kit (IVA inclusa)
LIVRAISON = {"mini": 250, "moyen": 300, "grand": 300}

# Chemins : URL française -> URL italienne (les fiches gardent leur slug : /kit-camper/berlingo/)
CHEMINS = {
    "/kit-amenagement/": "/kit-camper/",
    "/boutique/": "/negozio/",
    "/accessoires/": "/accessori/",
    "/occultants-isolants/": "/oscuranti-isolanti/",
    "/matelas-camper/": "/materasso-camper/",
    "/guide-kit-meubles-camper/": "/guida-kit-mobili-camper/",
    "/contact/": "/contatti/",
    "/merci/": "/grazie/",
    "/conditions-generales-de-vente/": "/condizioni-generali-di-vendita/",
    "/mentions-legales/": "/note-legali/",
    "/politique-de-confidentialite/": "/privacy/",
}

# Link di pagamento Stripe (Payment Links) per l'Italia. Stesse chiavi della Francia (vedi docs/STRIPE.md).
STRIPE = {
    "kit-mini-pin-sans-retrait": "https://buy.stripe.com/7sY3cuex07MR0bp6ub6EU0K",
    "kit-mini-pin-avec-retrait": "https://buy.stripe.com/8x2eVc74y5EJ8HV9Gn6EU0L",
    "kit-mini-carrossier-sans-retrait": "https://buy.stripe.com/6oUbJ074y0kpgan5q76EU0M",
    "kit-mini-carrossier-avec-retrait": "https://buy.stripe.com/6oU4gy1KegjncYb3hZ6EU0N",
    "kit-mini-hpl-sans-retrait": "https://buy.stripe.com/4gM28qfB47MRaQ3cSz6EU0O",
    "kit-mini-hpl-avec-retrait": "https://buy.stripe.com/5kQ9AS0Ga3wB9LZ9Gn6EU0P",
    "kit-moyen-pin-sans-retrait": "https://buy.stripe.com/aFaaEW74y9UZ6zNdWD6EU0Q",
    "kit-moyen-pin-avec-retrait": "https://buy.stripe.com/14A9AS9cG8QV7DRaKr6EU0R",
    "kit-moyen-carrossier-sans-retrait": "https://buy.stripe.com/dRm7sK1KeffjbU77yf6EU0S",
    "kit-moyen-carrossier-avec-retrait": "https://buy.stripe.com/6oU28qgF88QV4rF7yf6EU0T",
    "kit-moyen-hpl-sans-retrait": "https://buy.stripe.com/7sY3cu88C5EJ9LZcSz6EU0U",
    "kit-moyen-hpl-avec-retrait": "https://buy.stripe.com/eVqdR888Cebf2jx4m36EU0V",
    "kit-mini-pin-sans-livraison": "https://buy.stripe.com/4gMfZgfB49UZbU74m36EU12",
    "kit-mini-pin-avec-livraison": "https://buy.stripe.com/7sYaEWfB4aZ3aQ3aKr6EU13",
    "kit-mini-carrossier-sans-livraison": "https://buy.stripe.com/aFa00i4Wq9UZgancSz6EU14",
    "kit-mini-carrossier-avec-livraison": "https://buy.stripe.com/7sY28qdsWaZ3aQ32dV6EU15",
    "kit-mini-hpl-sans-livraison": "https://buy.stripe.com/28E00i3Smd7b2jx8Cj6EU16",
    "kit-mini-hpl-avec-livraison": "https://buy.stripe.com/eVq5kCbkOebf7DRaKr6EU17",
    "kit-moyen-pin-sans-livraison": "https://buy.stripe.com/eVq6oGfB43wB7DR6ub6EU18",
    "kit-moyen-pin-avec-livraison": "https://buy.stripe.com/aFaaEWfB4ebfgan4m36EU19",
    "kit-moyen-carrossier-sans-livraison": "https://buy.stripe.com/dRmfZg74ygjnbU7bOv6EU1a",
    "kit-moyen-carrossier-avec-livraison": "https://buy.stripe.com/aFabJ060ugjn5vJ3hZ6EU1b",
    "kit-moyen-hpl-sans-livraison": "https://buy.stripe.com/eVq9ASfB44AFf6jdWD6EU1c",
    "kit-moyen-hpl-avec-livraison": "https://buy.stripe.com/00w14magK8QV4rF4m36EU1d",
    "kit-grand-pin-sans-retrait": "https://buy.stripe.com/bJeaEW4Wq9UZaQ3bOv6EU0W",
    "kit-grand-pin-avec-retrait": "https://buy.stripe.com/28E8wOdsWebfbU719R6EU0X",
    "kit-grand-carrossier-sans-retrait": "https://buy.stripe.com/3cIfZg1Ke3wBf6j5q76EU0Y",
    "kit-grand-carrossier-avec-retrait": "https://buy.stripe.com/dRmfZgdsW5EJ2jx4m36EU0Z",
    "kit-grand-hpl-sans-retrait": "https://buy.stripe.com/aFa9AS60u6IN0bpbOv6EU10",
    "kit-grand-hpl-avec-retrait": "https://buy.stripe.com/3cIbJ088C8QV0bp6ub6EU11",
    "kit-grand-pin-sans-livraison": "https://buy.stripe.com/7sY14m2Oi3wB3nB19R6EU1e",
    "kit-grand-pin-avec-livraison": "https://buy.stripe.com/8x214magKd7b0bpdWD6EU1f",
    "kit-grand-carrossier-sans-livraison": "https://buy.stripe.com/aFa7sK4Wqgjn1ft5q76EU1g",
    "kit-grand-carrossier-avec-livraison": "https://buy.stripe.com/dRm3cu1Ke7MRcYbbOv6EU1h",
    "kit-grand-hpl-sans-livraison": "https://buy.stripe.com/6oUeVc1Ke5EJaQ33hZ6EU1i",
    "kit-grand-hpl-avec-livraison": "https://buy.stripe.com/3cI7sKdsWgjnbU73hZ6EU1j",
    "occultants": "https://buy.stripe.com/7sY3cufB40kp4rF19R6EU1k",
    "frigo-15": "https://buy.stripe.com/aFabJ02Oi5EJ0bp2dV6EU1l",
    "frigo-35": "https://buy.stripe.com/4gM6oGfB4gjn7DR6ub6EU1m",
    "batterie": "https://buy.stripe.com/6oU7sKex06INe2fbOv6EU1n",
    "batterie-onduleur": "https://buy.stripe.com/14A14magKebf8HV4m36EU1o",
    "rechaud": "https://buy.stripe.com/fZuaEWcoS7MR2jx9Gn6EU1p",
    "rechaud-cartouches": "https://buy.stripe.com/aFaeVcagK0kp1ft8Cj6EU1q",
    "toilettes": "https://buy.stripe.com/cNifZg1Keebf7DRg4L6EU1r",
    "douche": "https://buy.stripe.com/aFa14m3Sm7MRganf0H6EU1s",
}

# Mettere True solo quando kitcampermodulare.it è online: allora il build aggiunge le pagine /it/ allo script per Webnode.
REDIRECTION_ACTIVE = True

# Vecchie pagine camperizatetodoen1.com/it/ (Webnode) -> nuove pagine
W = "/it/"
_FICHES = {
    "berlingo": "berlingo", "partner": "partner", "rifter": "rifter", "renault-kangoo": "renault-kangoo",
    "caddy": "caddy", "opel-combo-life": "opel-combo-life", "fiat-doblo": "fiat-doblo", "proace-city": "proace-city",
    "nissan-townstar": "nissan-townstar", "mercedes-citan-classe-t": "mercedes-citan", "tourneo-transit": "tourneo-transit",
    "ford-courier": "ford-courier", "dokker": "dokker", "dacia-jogger-lodgy": "dacia-jogger-lodgy",
    "traffic": "trafic", "transporter-t4-t5-t6": "transporter-t4-t5-t6", "vw-caravelle-t4-t5-t6": "caravelle-t4-t5-t6",
    "vito-viano": "vito-viano", "expert": "expert", "traveller": "traveller", "jumpy": "jumpy",
    "spacetourer": "space-tourer", "toyota-proace": "toyota-proace", "fiat-scudo": "fiat-scudo", "talento": "talento",
    "opel-vivaro": "opel-vivaro", "ford-transit-custom": "ford-transit-custom", "nv200": "nv200", "nv300": "nv300",
    "hyundai-h1": "hyundai-h1", "jumper-boxer-ducato": "jumper-boxer-transit",
}
REDIRECTIONS = {W + ancien + "/": f"/kit-camper/{slug}/" for ancien, slug in _FICHES.items()}
REDIRECTIONS.update({
    "/it/": "/",
    "/it/kit-camperizzazione/": "/kit-camper/",
    "/it/kitsmobilicamper/": "/guida-kit-mobili-camper/",
    "/it/negozio-online/": "/negozio/",
    "/it/2-1/": "/accessori/#version-2-1",
    "/it/batteria/": "/accessori/#batterie",
    "/it/materasso-per-camper/": "/materasso-camper/",
    "/it/contatto/": "/contatti/",
    "/it/sobre-nosotros/": "/contatti/",
    "/it/terminos-y-condiciones/": "/condizioni-generali-di-vendita/",
    "/it/politica-de-privacidad/": "/privacy/",
    "/it/gracias/": "/",
})
REDIRECTIONS_PREFIXES = {
    "/it/negozio-online/": "/negozio/",
    "/it/kit-camperizzazione/": "/kit-camper/",
    "/it/": "/",
}

from sites.it_textes import TEXTES, MOTIFS, SCRIPTS  # noqa: E402,F401
