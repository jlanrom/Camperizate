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
    "kit-mini-pin-sans-livraison": "",
    "kit-mini-pin-avec-livraison": "",
    "kit-mini-carrossier-sans-livraison": "",
    "kit-mini-carrossier-avec-livraison": "",
    "kit-mini-hpl-sans-livraison": "",
    "kit-mini-hpl-avec-livraison": "",
    "kit-moyen-pin-sans-livraison": "",
    "kit-moyen-pin-avec-livraison": "",
    "kit-moyen-carrossier-sans-livraison": "",
    "kit-moyen-carrossier-avec-livraison": "",
    "kit-moyen-hpl-sans-livraison": "",
    "kit-moyen-hpl-avec-livraison": "",
    "kit-grand-pin-sans-retrait": "https://buy.stripe.com/bJeaEW4Wq9UZaQ3bOv6EU0W",
    "kit-grand-pin-avec-retrait": "",
    "kit-grand-carrossier-sans-retrait": "",
    "kit-grand-carrossier-avec-retrait": "",
    "kit-grand-hpl-sans-retrait": "",
    "kit-grand-hpl-avec-retrait": "",
    "kit-grand-pin-sans-livraison": "",
    "kit-grand-pin-avec-livraison": "",
    "kit-grand-carrossier-sans-livraison": "",
    "kit-grand-carrossier-avec-livraison": "",
    "kit-grand-hpl-sans-livraison": "",
    "kit-grand-hpl-avec-livraison": "",
    "occultants": "",
    "frigo-15": "",
    "frigo-35": "",
    "batterie": "",
    "batterie-onduleur": "",
    "rechaud": "",
    "rechaud-cartouches": "",
    "toilettes": "",
    "douche": "",
}

# Mettere True solo quando kitcampermodulare.it è online: allora il build aggiunge le pagine /it/ allo script per Webnode.
REDIRECTION_ACTIVE = False

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
