#!/usr/bin/env python3
"""Génère les pages dynamiques de kitamenagement.fr.

Usage :  python3 tools/build.py

Écrit :
- public/boutique/index.html              la boutique (paiement par liens Stripe)
- public/kit-amenagement/<slug>/index.html une fiche par modèle de FICHES
- public/merci/index.html                 page de retour après paiement
- public/sitemap.xml
- tools/redirections.json                 ancienne URL Webnode → nouvelle fiche

Le CSS est repris de public/index.html (une seule source de style).
Ne pas modifier les pages générées à la main : modifier ce script puis le relancer.

LIENS DE PAIEMENT : coller chaque URL de Payment Link Stripe dans STRIPE ci-dessous.
Tant qu'un lien est vide, le bouton correspondant propose de commander par message.
La liste des liens à créer et leur réglage sont dans docs/STRIPE.md.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SITE = "https://kitamenagement.fr"
TALLY = "https://tally.so/r/OD6BOp"

# ---------------------------------------------------------------------------
# 1. LIENS STRIPE (Payment Links) — à remplir, voir docs/STRIPE.md
# ---------------------------------------------------------------------------
STRIPE = {
    # Kits : kit-<catégorie>-<finition>-<matelas sans|avec>-<retrait|livraison>
    "kit-mini-pin-sans-retrait": "https://buy.stripe.com/8x2aEW88C5EJ5vJdWD6EU01",
    "kit-mini-pin-avec-retrait": "https://buy.stripe.com/4gMdR8agKc37ganbOv6EU02",
    "kit-mini-carrossier-sans-retrait": "https://buy.stripe.com/9B6fZg9cG8QVaQ3dWD6EU03",
    "kit-mini-carrossier-avec-retrait": "https://buy.stripe.com/aFa28q9cG0kp0bpaKr6EU04",
    "kit-mini-hpl-sans-retrait": "https://buy.stripe.com/eVq9ASbkOaZ38HV8Cj6EU05",
    "kit-mini-hpl-avec-retrait": "https://buy.stripe.com/eVqbJ0ex0ebfaQ3f0H6EU06",
    "kit-moyen-pin-sans-retrait": "https://buy.stripe.com/6oU8wO88Cc376zNf0H6EU07",
    "kit-moyen-pin-avec-retrait": "https://buy.stripe.com/eVq5kCfB44AF4rF19R6EU08",
    "kit-moyen-carrossier-sans-retrait": "https://buy.stripe.com/4gM9AS1Ke6IN7DRaKr6EU09",
    "kit-moyen-carrossier-avec-retrait": "https://buy.stripe.com/8x228q2Oi3wBcYbdWD6EU0a",
    "kit-moyen-hpl-sans-retrait": "https://buy.stripe.com/fZu28q9cG5EJ5vJg4L6EU0b",
    "kit-moyen-hpl-avec-retrait": "https://buy.stripe.com/cNidR89cG7MR0bpdWD6EU0c",
    "kit-mini-pin-sans-livraison": "https://buy.stripe.com/00w7sKdsWebf1ft9Gn6EU0d",
    "kit-mini-pin-avec-livraison": "https://buy.stripe.com/fZufZg88C1ot3nB19R6EU0e",
    "kit-mini-carrossier-sans-livraison": "https://buy.stripe.com/aFaaEWbkOc37bU7dWD6EU0f",
    "kit-mini-carrossier-avec-livraison": "https://buy.stripe.com/dRm00ifB44AFgan19R6EU0g",
    "kit-mini-hpl-sans-livraison": "https://buy.stripe.com/9B69ASgF84AFaQ35q76EU0h",
    "kit-mini-hpl-avec-livraison": "https://buy.stripe.com/6oU14mfB43wB6zNcSz6EU0i",
    "kit-moyen-pin-sans-livraison": "https://buy.stripe.com/14A3cu2Oi0kp8HV8Cj6EU0j",
    "kit-moyen-pin-avec-livraison": "https://buy.stripe.com/4gM6oG0Ga8QV2jx19R6EU0k",
    "kit-moyen-carrossier-sans-livraison": "https://buy.stripe.com/cNiaEW1Ke3wB9LZcSz6EU0l",
    "kit-moyen-carrossier-avec-livraison": "https://buy.stripe.com/aFa4gygF88QV4rF8Cj6EU0m",
    "kit-moyen-hpl-sans-livraison": "https://buy.stripe.com/dRm4gyfB4c377DRdWD6EU0n",
    "kit-moyen-hpl-avec-livraison": "https://buy.stripe.com/3cI9ASagK8QVf6jbOv6EU0o",
    # Accessoires
    "occultants": "https://buy.stripe.com/bJe3cufB40kp8HV3hZ6EU0p",
    "frigo-15": "https://buy.stripe.com/8x24gy60u0kp9LZbOv6EU0q",
    "frigo-35": "https://buy.stripe.com/00waEWfB43wB8HVcSz6EU0r",
    "batterie": "https://buy.stripe.com/5kQeVc9cG7MR0bp8Cj6EU0s",
    "batterie-onduleur": "https://buy.stripe.com/00w14mex0c378HVg4L6EU0t",
    "rechaud": "https://buy.stripe.com/5kQbJ04Wq3wBbU7dWD6EU0u",
    "rechaud-cartouches": "https://buy.stripe.com/cNi3cu3Sm4AF9LZ19R6EU0v",
    "toilettes": "https://buy.stripe.com/6oU14m1Ke0kp5vJaKr6EU0w",
    "douche": "https://buy.stripe.com/3cIeVcbkO4AF1ft19R6EU0x",
}

# ---------------------------------------------------------------------------
# 2. CATALOGUE
# ---------------------------------------------------------------------------
FINITIONS = [  # clé, nom, description, prix (mini, moyen) sans matelas
    ("pin", "Phénolique pin", "Bois naturel, chaleureux, vernissable.", {"mini": 500, "moyen": 700}),
    ("carrossier", "Phénolique carrossier", "Noir, repousse l'eau et les taches. Le plus vendu.", {"mini": 550, "moyen": 750}),
    ("hpl", "HPL de peuplier", "Léger, ultra-résistant. Blanc ou anthracite.", {"mini": 800, "moyen": 1000}),
]
MATELAS = 150  # supplément matelas sur mesure
CATEGORIES = {
    "mini": {"nom": "Ludospace", "pluriel": "Kits ludospace", "livraison": 200},
    "moyen": {"nom": "Van compact", "pluriel": "Kits van compact", "livraison": 250},
    "grand": {"nom": "Grand fourgon", "pluriel": "Grands fourgons", "livraison": None},
}
# slug = dernier segment de l'ancienne URL camperizatetodoen1.com/fr/…
VEHICULES = [
    ("mini", "berlingo", "Citroën Berlingo"),
    ("mini", "partner", "Peugeot Partner"),
    ("mini", "rifter", "Peugeot Rifter"),
    ("mini", "renault-kangoo", "Renault Kangoo"),
    ("mini", "caddy", "Volkswagen Caddy"),
    ("mini", "opel-combo-life", "Opel Combo Life"),
    ("mini", "fiat-doblo", "Fiat Doblo"),
    ("mini", "proace-city", "Toyota Proace City"),
    ("mini", "nissan-townstar", "Nissan Townstar"),
    ("mini", "mercedes-citan", "Mercedes Citan / Classe T"),
    ("mini", "tourneo-transit", "Ford Tourneo / Transit Connect"),
    ("mini", "ford-courier", "Ford Tourneo / Transit Courier"),
    ("mini", "dokker", "Dacia Dokker"),
    ("mini", "dacia-jogger-lodgy", "Dacia Jogger / Lodgy"),
    ("moyen", "trafic", "Renault Trafic"),
    ("moyen", "transporter-t4-t5-t6", "Volkswagen Transporter T4 / T5 / T6"),
    ("moyen", "caravelle-t4-t5-t6", "Volkswagen Caravelle / Multivan"),
    ("moyen", "vito-viano", "Mercedes Vito / Viano"),
    ("moyen", "expert", "Peugeot Expert"),
    ("moyen", "traveller", "Peugeot Traveller"),
    ("moyen", "jumpy", "Citroën Jumpy"),
    ("moyen", "space-tourer", "Citroën SpaceTourer"),
    ("moyen", "fiat-scudo", "Fiat Scudo"),
    ("moyen", "talento", "Fiat Talento"),
    ("moyen", "opel-vivaro", "Opel Vivaro / Zafira Life"),
    ("moyen", "toyota-proace", "Toyota Proace"),
    ("moyen", "ford-transit-custom", "Ford Transit / Tourneo Custom"),
    ("moyen", "nv200", "Nissan NV200"),
    ("moyen", "nv300", "Nissan NV300 / Primastar"),
    ("moyen", "hyundai-h1", "Hyundai H1"),
    ("grand", "jumper-boxer-transit", "Fiat Ducato / Citroën Jumper / Peugeot Boxer"),
    ("grand", "ford-transit", "Ford Transit"),
    ("grand", "autre", "Autre modèle"),
]
OPTIONS = [  # proposées comme « articles facultatifs » sur la page de paiement Stripe
    ("Équerre rabattable", "+ 25 €"),
    ("Plateau frigo", "+ 25 €"),
    ("Tiroir frigo coulissant", "+ 50 €"),
    ("Égouttoir", "+ 35 €"),
    ("Version 2+1", "+ 100 €"),
]
ACCESSOIRES = [  # clé Stripe, nom, détail, prix
    ("occultants", "Occultants isolants", "9 couches, sur mesure pour votre modèle", 149),
    ("frigo-15", "Frigo à compresseur 15 L", "Pour ludospace", 220),
    ("frigo-35", "Frigo à compresseur 35 L", "Pour van compact", 300),
    ("batterie", "Batterie lithium", "Sans onduleur", 750),
    ("batterie-onduleur", "Batterie lithium + onduleur", "Prises 230 V à bord", 975),
    ("rechaud", "Réchaud", "Réchaud seul", 29),
    ("rechaud-cartouches", "Réchaud + 3 cartouches", "Prêt à cuisiner", 35),
    ("toilettes", "Toilettes portables", "", 110),
    ("douche", "Douche portable", "", 75),
]

# ---------------------------------------------------------------------------
# 3. FICHES MODÈLE
# ---------------------------------------------------------------------------
# Une fiche par modèle : (slug, nom complet, nom court, catégorie, anciennes URL Webnode, titre court optionnel)
# Le slug reprend le dernier segment de l'ancienne URL camperizatetodoen1.com/fr/… pour faciliter la redirection.
W = "/fr/kit-camperizacion/"
MODELES = [
    ("berlingo", "Citroën Berlingo", "Berlingo", "mini", [W + "berlingo/"], None),
    ("partner", "Peugeot Partner et Partner Tepee", "Partner", "mini", [W + "partner/"], "Peugeot Partner et Tepee"),
    ("rifter", "Peugeot Rifter", "Rifter", "mini", [W + "rifter/"], None),
    ("renault-kangoo", "Renault Kangoo", "Kangoo", "mini", [W + "renault-kangoo/"], None),
    ("caddy", "Volkswagen Caddy", "Caddy", "mini", [W + "caddy/"], "VW Caddy"),
    ("opel-combo-life", "Opel Combo Life", "Combo Life", "mini", [W + "opel-combo-life/"], None),
    ("fiat-doblo", "Fiat Doblò", "Doblò", "mini", [W + "fiat-doblo/"], None),
    ("proace-city", "Toyota Proace City", "Proace City", "mini", [W + "proace-city/"], None),
    ("nissan-townstar", "Nissan Townstar", "Townstar", "mini", [W + "nissan-townstar/"], None),
    ("mercedes-citan", "Mercedes Citan et Classe T", "Citan", "mini", [W + "mercedes-citan/"], None),
    ("tourneo-transit", "Ford Tourneo Connect et Transit Connect", "Tourneo Connect", "mini", [W + "tourneo-transit/"], "Ford Tourneo Connect"),
    ("ford-courier", "Ford Tourneo Courier et Transit Courier", "Courier", "mini", [W + "ford-courier/"], "Ford Tourneo Courier"),
    ("dokker", "Dacia Dokker", "Dokker", "mini", [W + "dokker/"], None),
    ("dacia-jogger-lodgy", "Dacia Jogger et Lodgy", "Jogger", "mini", [W + "dacia-jogger-lodgy/"], None),
    ("trafic", "Renault Trafic", "Trafic", "moyen", [W + "trafic/"], None),
    ("transporter-t4-t5-t6", "Volkswagen Transporter T4, T5 et T6", "Transporter", "moyen", [W + "transporter-t4-t5-t6/"], "VW Transporter T4, T5, T6"),
    ("caravelle-t4-t5-t6", "Volkswagen Caravelle et Multivan", "Caravelle", "moyen", [W + "caravelle-t4-t5-t6/"], "VW Caravelle et Multivan"),
    ("vito-viano", "Mercedes Vito et Viano", "Vito", "moyen", [W + "vito-viano/"], None),
    ("expert", "Peugeot Expert", "Expert", "moyen", ["/fr/expert/", W + "expert/"], None),
    ("traveller", "Peugeot Traveller", "Traveller", "moyen", ["/fr/traveller/", W + "traveller/"], None),
    ("jumpy", "Citroën Jumpy", "Jumpy", "moyen", ["/fr/jumpy/", W + "jumpy/"], None),
    ("space-tourer", "Citroën SpaceTourer", "SpaceTourer", "moyen", ["/fr/space-tourer/", W + "space-tourer/"], None),
    ("fiat-scudo", "Fiat Scudo", "Scudo", "moyen", [W + "fiat-scudo/"], None),
    ("talento", "Fiat Talento", "Talento", "moyen", [W + "talento/"], None),
    ("opel-vivaro", "Opel Vivaro et Zafira Life", "Vivaro", "moyen", [W + "opel-vivaro/"], None),
    ("toyota-proace", "Toyota Proace", "Proace", "moyen", ["/fr/toyota-proace/", W + "toyota-proace/"], None),
    ("ford-transit-custom", "Ford Transit Custom et Tourneo Custom", "Transit Custom", "moyen", [W + "ford-transit-custom/"], "Ford Transit Custom"),
    ("nv200", "Nissan NV200", "NV200", "moyen", [W + "nv200/"], None),
    ("nv300", "Nissan NV300 et Primastar", "NV300", "moyen", [W + "nv300/"], None),
    ("hyundai-h1", "Hyundai H1", "H1", "moyen", [W + "hyundai-h1/"], None),
    ("jumper-boxer-transit", "Fiat Ducato, Citroën Jumper et Peugeot Boxer", "Ducato", "grand", [W + "jumper-boxer-transit/"], "Ducato, Jumper, Boxer"),
]

# Contenu par catégorie (repris de la landing ; à enrichir modèle par modèle)
CONTENU = {
    "mini": {
        "intro": "Votre {nom} devient mini camping-car en quelques minutes, puis redevient un véhicule de tous les jours. "
                 "Le kit se pose dans le coffre sans perçage : pas de VASP, carte grise inchangée, et vous gardez vos 5 places.",
        "inclus": [
            ("i-bed", "Lit pliant", "187 cm, jusqu'à 220 cm en version XL."),
            ("i-cook", "Cuisine", "Tiroir extractible pour le réchaud et la vaisselle."),
            ("i-box", "Rangement", "Coffre et logement pour un frigo de 15 L."),
            ("i-table", "Table", "À l'intérieur ou à l'extérieur, 3 hauteurs."),
        ],
        "faq": [("Garde-t-on les 5 places ?", "Oui. Sur ludospace, le kit se pose dans le coffre et vous gardez vos 5 places.")],
        "image": ("/img/kit-carrossier-lit.webp", "Kit camper amovible en phénolique carrossier, lit déplié dans un ludospace", 900, 900),
    },
    "moyen": {
        "intro": "Votre {nom} devient van aménagé en quelques minutes : lit, cuisine et rangements, à retirer quand vous voulez. "
                 "Le kit s'adapte à vos sièges et se pose sans perçage : pas de VASP, carte grise inchangée.",
        "inclus": [
            ("i-bed", "Lit pliant", "Matelas sur mesure en option."),
            ("i-cook", "Cuisine", "Tiroir extractible pour le réchaud et la vaisselle."),
            ("i-box", "Rangement", "Logement pour un frigo jusqu'à 35 L."),
            ("i-table", "Hauteur adaptée", "36,5 à 56,5 cm selon vos sièges."),
        ],
        "faq": [("Puis-je garder mes sièges arrière ?",
                 "Oui. Le kit mesure 56,5 cm de haut avec la 2e rangée de sièges, 44,5 ou 36,5 cm sans sièges.")],
        "image": ("/img/kit-hpl-anthracite.webp", "Kit camper amovible HPL gris anthracite en mode salon dans un van", 900, 822),
    },
    "grand": {
        "intro": "Pour votre {nom}, nous concevons un kit amovible sur mesure : lit, cuisine et rangements, "
                 "toujours sans perçage ni VASP. Le devis est gratuit.",
        "inclus": [
            ("i-bed", "Lit", "Conçu pour la largeur de votre fourgon."),
            ("i-cook", "Cuisine", "Tiroir extractible, réchaud, vaisselle."),
            ("i-box", "Rangement", "Coffres et logement frigo selon votre projet."),
            ("i-shield", "Sans VASP", "Chargement amovible, rien n'est vissé."),
        ],
        "faq": [("Combien coûte un kit pour grand fourgon ?",
                 "Chaque kit est conçu pour votre fourgon et votre usage : nous vous envoyons un devis gratuit après un premier échange.")],
        "image": ("/img/hero-van-amenage-800.webp", "Véhicule aménagé avec un kit camper en bois, hayon ouvert", 800, 400),
    },
}
FIXATION = ("Le kit se pose dans le coffre, repose sur 3 points d'appui contrôlés et se sangle aux anneaux "
            "d'arrimage d'origine. Aucun perçage, rien n'est vissé.")

# Données détaillées déjà vérifiées (prioritaires sur le contenu par catégorie)
DETAILS = {
    "dacia-jogger-lodgy": {
        "intro": "Le Jogger devient mini camping-car en quelques minutes, puis redevient une voiture familiale pour la semaine. "
                 "Le kit se pose dans le coffre sans perçage : pas de VASP, carte grise inchangée.",
        "mesures": [
            ("Lit déplié", "187 cm de long"),
            ("Largeur du kit", "99 cm"),
            ("Largeur du matelas", "125 cm"),
            ("Hauteur", "36 cm"),
            ("Profondeur, kit replié", "environ 95 cm"),
            ("Places assises", "les 5 places restent utilisables"),
        ],
        "inclus": [
            ("i-cook", "Tiroir cuisine", "Extractible, sur glissières renforcées (30 à 40 kg), pour le réchaud et la vaisselle."),
            ("i-table", "Table extérieure", "Le couvercle du compartiment arrière se retire et sert de table."),
            ("i-box", "Grand coffre", "À gauche, ouverture par le dessus et par l'avant."),
            ("i-bed", "Lit dépliable", "En deux parties. Matelas sur mesure en option."),
        ],
        "fixation": "Le kit repose sur trois appuis : le plancher du coffre, un premier panneau dépliable posé sur les sièges rabattus "
                    "et un second sur pieds escamotables. Le poids est réparti, rien n'est vissé.",
        "videos": [("kUtbMAAaMW8", "Le kit Dacia Jogger en vidéo"), ("bdcMn_dis2A", "Montage du kit dans le coffre")],
        "faq": [
            ("Le même kit va-t-il dans un Lodgy et dans un Jogger ?",
             "Oui. Le Lodgy (2012-2022) et le Jogger (depuis 2022) ont les mêmes mesures intérieures : c'est le même kit."),
            ("Garde-t-on les 5 places ?",
             "Oui. Kit replié dans le coffre, les 5 places restent utilisables."),
        ],
    },
}

# Photos par modèle : générées par tools/photos.py (voir docs/PHOTOS.md)
PHOTOS_JSON = ROOT / "tools" / "photos.json"
PHOTOS = json.loads(PHOTOS_JSON.read_text(encoding="utf-8")) if PHOTOS_JSON.exists() else {}


def construire_fiches():
    fiches = []
    for slug, nom, court, cat, anciens, titre in MODELES:
        c = CONTENU[cat]
        d = DETAILS.get(slug, {})
        photos = PHOTOS.get(slug, [])
        if photos:
            ph = photos[0]
            image = (f"/img/modeles/{slug}/{ph['fichier']}", ph["alt"], ph["w"], ph["h"])
        else:
            image = c["image"]
        fiches.append({
            "slug": slug, "nom": nom, "court": court, "categorie": cat, "anciens": anciens,
            "titre": titre or nom, "image": image, "galerie": photos[1:],
            "intro": d.get("intro", c["intro"].format(nom=nom)),
            "inclus": d.get("inclus", c["inclus"]),
            "fixation": d.get("fixation", FIXATION),
            "mesures": d.get("mesures", []),
            "videos": d.get("videos", []),
            "faq": d.get("faq", c["faq"]),
        })
    return fiches


FICHES = construire_fiches()

FAQ_COMMUNE = [
    ("Faut-il une homologation VASP ?",
     "Non. Le kit n'est ni vissé ni percé : c'est un chargement amovible. Pas de VASP, pas de DREAL, carte grise inchangée."),
    ("Quel est le délai ?",
     "Environ 3 semaines de fabrication, plus rapide si votre modèle est en stock."),
]

# ---------------------------------------------------------------------------
# Gabarit commun
# ---------------------------------------------------------------------------
EXTRA_CSS = """
.crumbs{font-size:14px;color:var(--brown-70);padding-top:14px}
.crumbs ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.crumbs li+li::before{content:"›";margin-right:6px}
.crumbs a{text-decoration:none}.crumbs a:hover{color:var(--orange)}
.ctas{display:grid;gap:12px}
.fiche-hero{padding:20px 0 44px}
.fiche-hero .pic{aspect-ratio:4/3;background:var(--sand);border-radius:var(--r);overflow:hidden}
.fiche-hero .pic img{width:100%;height:100%;object-fit:cover}
.fiche-hero .kicker{margin-top:18px}
.fiche-hero h1{margin:0 0 12px}
.fiche-hero .lead{font-size:18px;color:var(--brown-70);margin-bottom:18px}
.specs{width:100%;border-collapse:collapse;background:var(--white);border-radius:var(--r);overflow:hidden}
.specs th,.specs td{text-align:left;padding:12px 16px;border-bottom:1px solid var(--line);font-size:16px;vertical-align:top}
.specs tr:last-child th,.specs tr:last-child td{border-bottom:0}
.specs th{font-weight:600;width:45%}
.price-table{width:100%;border-collapse:collapse;background:var(--white);border-radius:var(--r);overflow:hidden}
.price-table th,.price-table td{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left;font-size:15px}
.price-table thead th{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--brown-70);font-weight:600}
.price-table td b{font:800 20px/1 var(--head);color:var(--orange);white-space:nowrap}
.price-table small{display:block;color:var(--brown-70);font-size:13px}
.price-table tr:last-child td{border-bottom:0}
.fix{max-width:720px;margin-top:20px}
.videos{display:grid;gap:12px}
.yt{position:relative;display:block;width:100%;aspect-ratio:16/9;border:0;padding:0;border-radius:var(--r);overflow:hidden;background:var(--brown);cursor:pointer}
.yt img{width:100%;height:100%;object-fit:cover;opacity:.85}
.yt span{position:absolute;left:12px;bottom:12px;background:var(--white);color:var(--brown);font:600 14px/1.2 var(--body);padding:8px 10px;border-radius:var(--r)}
.yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.showroom{background:var(--blue)}
.showroom address{font-style:normal;font-size:18px;margin-bottom:18px}
/* Boutique */
.shop-hero{padding:28px 0 8px}
.shop-hero .lead{font-size:18px;color:var(--brown-70);max-width:640px;margin-top:12px}
.order{background:var(--white);border-radius:var(--r);padding:20px;display:grid;gap:24px}
.step h3{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.step h3 i{font-style:normal;display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--brown);color:var(--white);font:700 14px/1 var(--body)}
.choices{display:grid;gap:10px}
.choice{position:relative;display:flex;justify-content:space-between;align-items:center;gap:12px;min-height:60px;padding:12px 16px;border:1px solid var(--line);border-radius:var(--r);cursor:pointer}
.choice input{position:absolute;opacity:0;pointer-events:none}
.choice:has(input:checked){border:2px solid var(--brown);padding:11px 15px}
.choice:has(input:focus-visible){outline:2px solid var(--orange);outline-offset:2px}
.choice small{display:block;color:var(--brown-70);font-size:14px;font-weight:400}
.choice span{font-weight:600}
.choice b{font:800 20px/1 var(--head);color:var(--orange);white-space:nowrap}
.total{border-top:1px solid var(--line);padding-top:20px}
.total .r-cat{font:700 13px/1.3 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--brown-70);margin-bottom:6px}
.total .sum{font:800 34px/1.1 var(--head);color:var(--orange);margin-bottom:6px}
.total .ship{font-size:15px;color:var(--brown-70);margin-bottom:16px}
.total .btn+.btn{margin-top:12px}
.devis{display:none}
.order.is-grand .step-fin,.order.is-grand .step-mat,.order.is-grand .total{display:none}
.order.is-grand .devis{display:block}
.opts{margin-top:14px;font-size:15px;color:var(--brown-70)}
.opts ul{margin:6px 0 0;padding-left:1.2em}
.acc{display:grid;gap:10px;list-style:none;margin:0;padding:0}
.acc li{background:var(--white);border:1px solid var(--line);border-radius:var(--r);padding:16px;display:grid;gap:10px}
.acc .row{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.acc h3{font-size:17px}
.acc small{display:block;color:var(--brown-70);font-size:14px;margin-top:4px}
.acc b{font:800 22px/1 var(--head);color:var(--orange);white-space:nowrap}
.acc .btn{min-height:44px;font-size:15px}
.info{display:grid;gap:10px;list-style:none;margin:0;padding:0}
.info li{display:flex;gap:12px;align-items:flex-start}
.info p{margin:0;color:var(--brown-70);font-size:15px}
.model-links{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr;gap:8px}
.model-links a{display:flex;align-items:center;min-height:48px;padding:10px 14px;background:var(--white);border:1px solid var(--line);border-radius:var(--r);text-decoration:none;font-weight:600}
.model-links a:hover{border-color:var(--brown);color:var(--orange)}
.cat-block+.cat-block{margin-top:36px}
.steps-merci{margin:20px 0 0;padding-left:1.3em;display:grid;gap:10px;max-width:640px}
.cat-block h2{margin-bottom:4px}
.cat-block .help{margin:0 0 14px}
@media (min-width:640px){.model-links{grid-template-columns:repeat(2,1fr)}}
@media (min-width:960px){.model-links{grid-template-columns:repeat(3,1fr)}}
@media (min-width:640px){.videos{grid-template-columns:1fr 1fr}.acc{grid-template-columns:repeat(2,1fr)}.choices.three{grid-template-columns:repeat(3,1fr)}.choices.three .choice{flex-direction:column;align-items:flex-start}}
@media (min-width:960px){
  .fiche-grid{display:grid;grid-template-columns:1fr 1.15fr;gap:48px;align-items:start}
  .fiche-grid .pic{order:2}
  .fiche-hero .kicker{margin-top:0}
  .ctas{display:flex;flex-wrap:wrap}
  .ctas .btn{width:auto;min-width:220px}
  .two{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
  .order{padding:32px;grid-template-columns:1fr 1fr;column-gap:48px}
  .order .step-veh{grid-column:1/-1}
  .acc{grid-template-columns:repeat(3,1fr)}
  .info{grid-template-columns:repeat(3,1fr);gap:24px}
}
"""

e = html.escape
INDEX = (PUBLIC / "index.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", INDEX, re.S).group(1)
ICONES = re.search(r'(<svg width="0" height="0".*?</svg>)', INDEX, re.S).group(1)
FAVICON = re.search(r'<link rel="icon"[^>]*>', INDEX).group(0)


def head(titre, desc, url, ld=None, robots=None, og_type="website"):
    ld_html = f'<script type="application/ld+json">\n{json.dumps(ld, ensure_ascii=False, indent=1)}\n</script>\n' if ld else ""
    robots_html = f'<meta name="robots" content="{robots}">\n' if robots else ""
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titre)}</title>
<meta name="description" content="{e(desc)}">
{robots_html}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#513524">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Camperizate">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(titre)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}/img/og-kitamenagement.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/fonts/bricolage-grotesque-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
{FAVICON}
<style>{CSS}{EXTRA_CSS}</style>
{ld_html}</head>
<body>

{ICONES}
"""


def header(lien, texte):
    return f"""
<header class="site-head">
  <div class="wrap">
    <a href="/" class="brand" aria-label="Camperizate, accueil"><img src="/img/camperizate-logo.svg" alt="Camperizate" width="172" height="23"></a>
    <a href="{lien}" class="btn btn-line head-btn">{texte}</a>
  </div>
</header>
"""


def footer(script=""):
    return f"""
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img src="/img/camperizate-logo-white.svg" alt="Camperizate" width="160" height="21" loading="lazy">
        <p>Kits camper amovibles pour ludospaces et vans, fabriqués dans notre atelier.</p>
        <a class="link" href="/kit-amenagement/">Tous les modèles</a> · <a class="link" href="/boutique/">Boutique</a>
      </div>
      <div>
        <h3>Showroom en France</h3>
        <address>Local n° 112<br>866 avenue du Maréchal Juin<br>30900 Nîmes</address>
      </div>
      <div>
        <h3>Contact</h3>
        <ul class="contact-list">
          <li><a href="{TALLY}" target="_blank" rel="noopener"><svg class="ico" aria-hidden="true"><use href="#i-msg"/></svg>Écrivez-nous</a></li>
          <li><a href="tel:+34665319287"><svg class="ico" aria-hidden="true"><use href="#i-phone"/></svg>+34 665 319 287</a></li>
          <li><a href="mailto:info@camperizatetodoen1.com"><svg class="ico" aria-hidden="true"><use href="#i-mail"/></svg>info@camperizatetodoen1.com</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <p>© 2026 Camperizate Todo en 1, S.L.U. Prix TTC. Les photos peuvent présenter des options.</p>
      <a href="/conditions-generales-de-vente/">CGV</a><a href="/mentions-legales/">Mentions légales</a><a href="/politique-de-confidentialite/">Politique de confidentialité</a>
    </div>
  </div>
</footer>
{script}
</body>
</html>
"""


def prix(cat, fin, avec):
    base = dict((f[0], f[3]) for f in FINITIONS)[fin][cat]
    return base + (MATELAS if avec else 0)


# ---------------------------------------------------------------------------
# Boutique
# ---------------------------------------------------------------------------
def boutique():
    url = f"{SITE}/boutique/"
    titre = "Boutique : kit camper amovible sans VASP | Camperizate"
    desc = ("Commandez votre kit d'aménagement amovible pour ludospace ou van : choisissez votre véhicule, "
            "la finition et le matelas, et payez en ligne. Dès 500 € TTC.")
    groupes = []
    for cat in ("mini", "moyen", "grand"):
        opts = "".join(f'<option value="{s}" data-cat="{c}">{e(n)}</option>' for c, s, n in VEHICULES if c == cat)
        groupes.append(f'<optgroup label="{e(CATEGORIES[cat]["pluriel"])}">{opts}</optgroup>')
    finitions = "\n".join(
        f'<label class="choice"><input type="radio" name="fin" value="{k}"{" checked" if k == "carrossier" else ""}>'
        f'<span>{e(n)}<small>{e(d)}</small></span><b data-fin="{k}"></b></label>'
        for k, n, d, _ in FINITIONS)
    options = "".join(f"<li>{e(n)} {e(p)}</li>" for n, p in OPTIONS)
    def bouton_acc(k):
        if STRIPE.get(k):
            return f'<a class="btn btn-primary" href="{e(STRIPE[k])}">Acheter</a>'
        return f'<a class="btn btn-line" href="{TALLY}" target="_blank" rel="noopener">Commander par message</a>'

    acc = "\n".join(
        f'<li><div class="row"><div><h3>{e(n)}</h3>{"<small>" + e(d) + "</small>" if d else ""}</div><b>{p} €</b></div>'
        f'{bouton_acc(k)}</li>'
        for k, n, d, p in ACCESSOIRES)
    data = {
        "liens": {k: v for k, v in STRIPE.items() if k.startswith("kit-")},
        "prix": {c: {f[0]: f[3][c] for f in FINITIONS} for c in ("mini", "moyen")},
        "matelas": MATELAS,
        "cat": {k: v["nom"] for k, v in CATEGORIES.items()},
        "livraison": {k: v["livraison"] for k, v in CATEGORIES.items()},
        "tally": TALLY,
    }
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": "Kit d'aménagement camper amovible pour ludospace",
         "image": SITE + "/img/kit-carrossier-lit.webp", "brand": {"@type": "Brand", "name": "Camperizate"},
         "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": str(prix("mini", "pin", False)),
                    "highPrice": str(prix("mini", "hpl", True)), "offerCount": "6", "availability": "https://schema.org/InStock"}},
        {"@type": "Product", "name": "Kit d'aménagement camper amovible pour van compact",
         "image": SITE + "/img/kit-hpl-anthracite.webp", "brand": {"@type": "Brand", "name": "Camperizate"},
         "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": str(prix("moyen", "pin", False)),
                    "highPrice": str(prix("moyen", "hpl", True)), "offerCount": "6", "availability": "https://schema.org/InStock"}},
    ]}
    script = """<script>
(function(){
  var D=%s;
  var f=document.getElementById('commande'),sel=document.getElementById('vehicule');
  var pay=document.getElementById('pay'),sum=document.getElementById('sum'),cat=document.getElementById('r-cat'),ship=document.getElementById('ship');
  function val(n){var x=f.querySelector('input[name='+n+']:checked');return x?x.value:null;}
  function fmt(n){return n.toLocaleString('fr-FR')+' €';}
  function render(){
    var o=sel.options[sel.selectedIndex],c=o?o.dataset.cat:null;
    f.classList.toggle('is-grand',c==='grand');
    var k=c==='moyen'?'moyen':'mini';
    document.querySelectorAll('[data-fin]').forEach(function(b){b.textContent='dès '+fmt(D.prix[k][b.dataset.fin]);});
    document.getElementById('mat-prix').textContent='+ '+fmt(D.matelas);
    document.getElementById('liv-prix').textContent='+ '+fmt(D.livraison[k]);
    if(!c||c==='grand'){return;}
    var fin=val('fin'),mat=val('mat'),mode=val('mode');
    var total=D.prix[c][fin]+(mat==='avec'?D.matelas:0)+(mode==='livraison'?D.livraison[c]:0);
    cat.textContent='Kit '+D.cat[c].toLowerCase()+' · '+o.text;
    sum.textContent=fmt(total)+' TTC';
    ship.textContent=mode==='livraison'?'Livraison comprise. Options à ajouter sur la page de paiement.':'Retrait gratuit à Nîmes. Options à ajouter sur la page de paiement.';
    var link=D.liens['kit-'+c+'-'+fin+'-'+mat+'-'+mode];
    if(link){pay.href=link+(link.indexOf('?')<0?'?':'&')+'client_reference_id='+encodeURIComponent(sel.value);pay.textContent='Payer '+fmt(total)+' en ligne';pay.removeAttribute('target');pay.className='btn btn-primary';}
    else{pay.href=D.tally;pay.target='_blank';pay.textContent='Commander par message';pay.className='btn btn-primary';}
  }
  var q=new URLSearchParams(location.search);
  if(q.get('modele')){for(var i=0;i<sel.options.length;i++){if(sel.options[i].value===q.get('modele')){sel.selectedIndex=i;}}}
  else if(q.get('cat')){for(var j=0;j<sel.options.length;j++){if(sel.options[j].dataset.cat===q.get('cat')){sel.selectedIndex=j;break;}}}
  if(q.get('finition')){var r=f.querySelector('input[name=fin][value="'+q.get('finition')+'"]');if(r)r.checked=true;}
  f.addEventListener('change',render);render();
})();
</script>""" % json.dumps(data, ensure_ascii=False)

    body = f"""
<main id="top">
<nav class="crumbs wrap" aria-label="Fil d'Ariane"><ol><li><a href="/">Accueil</a></li><li aria-current="page">Boutique</li></ol></nav>

<section class="shop-hero" aria-labelledby="h1">
  <div class="wrap">
    <span class="kicker">Boutique</span>
    <h1 id="h1">Commander votre kit camper</h1>
    <p class="lead">Choisissez votre véhicule, la finition, le matelas et la réception. Paiement sécurisé par carte, fabrication en 3 semaines environ.</p>
  </div>
</section>

<section class="kits" aria-label="Configurer votre kit">
  <div class="wrap">
    <form class="order" id="commande" onsubmit="return false">
      <div class="step step-veh">
        <h3><i>1</i><label for="vehicule">Votre véhicule</label></h3>
        <div class="select">
          <select id="vehicule" name="vehicule">{''.join(groupes)}</select>
          <svg class="ico" aria-hidden="true"><use href="#i-down"/></svg>
        </div>
        <p class="help">Modèle absent ? Choisissez « Autre modèle » ou <a href="{TALLY}" target="_blank" rel="noopener">écrivez-nous</a>.</p>
      </div>
      <fieldset class="step step-fin" style="border:0;margin:0;padding:0">
        <h3><i>2</i>Finition</h3>
        <div class="choices">
{finitions}
        </div>
      </fieldset>
      <div>
        <fieldset class="step step-mat" style="border:0;margin:0;padding:0">
          <h3><i>3</i>Matelas</h3>
          <div class="choices">
            <label class="choice"><input type="radio" name="mat" value="avec" checked><span>Avec matelas sur mesure<small>Mousse coupée pour votre modèle</small></span><b id="mat-prix"></b></label>
            <label class="choice"><input type="radio" name="mat" value="sans"><span>Sans matelas<small>Vous avez déjà le vôtre</small></span></label>
          </div>
        </fieldset>
        <fieldset class="step step-mat" style="border:0;margin:24px 0 0;padding:0">
          <h3><i>4</i>Réception</h3>
          <div class="choices">
            <label class="choice"><input type="radio" name="mode" value="retrait" checked><span>Retrait au showroom de Nîmes<small>866 avenue du Maréchal Juin, sur rendez-vous</small></span><b>0 €</b></label>
            <label class="choice"><input type="radio" name="mode" value="livraison"><span>Livraison à domicile<small>Kit monté, sur palette, France métropolitaine</small></span><b id="liv-prix"></b></label>
          </div>
        </fieldset>
        <div class="total" aria-live="polite">
          <p class="r-cat" id="r-cat"></p>
          <p class="sum" id="sum"></p>
          <p class="ship" id="ship"></p>
          <a class="btn btn-primary" id="pay" href="{TALLY}">Commander</a>
          <a class="btn btn-line" href="{TALLY}" target="_blank" rel="noopener">Une question avant de commander ?</a>
          <div class="opts">Options disponibles sur la page de paiement :<ul>{options}</ul></div>
        </div>
        <div class="devis">
          <h3>Grand fourgon : kit sur devis</h3>
          <p>Ducato, Jumper, Boxer, Transit, Master, Sprinter… Chaque kit est conçu pour votre fourgon, toujours sans VASP. Le devis est gratuit.</p>
          <a class="btn btn-primary" href="{TALLY}" target="_blank" rel="noopener">Demander mon devis</a>
        </div>
      </div>
    </form>
  </div>
</section>

<section id="accessoires" aria-labelledby="h-acc">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Accessoires</span>
      <h2 id="h-acc">Pour partir équipé</h2>
      <p>Livrés avec votre kit ou à retirer au showroom de Nîmes.</p>
    </div>
    <ul class="acc">
{acc}
    </ul>
  </div>
</section>

<section class="showroom" aria-labelledby="h-info">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Bon à savoir</span>
      <h2 id="h-info">Paiement, fabrication, livraison</h2>
    </div>
    <ul class="info">
      <li><svg class="ico" aria-hidden="true"><use href="#i-shield"/></svg><div><h3>Paiement sécurisé</h3><p>Par carte bancaire via Stripe. Nous ne voyons jamais vos données de carte.</p></div></li>
      <li><svg class="ico" aria-hidden="true"><use href="#i-factory"/></svg><div><h3>3 semaines environ</h3><p>Fabrication dans notre atelier, plus rapide si votre modèle est en stock.</p></div></li>
      <li><svg class="ico" aria-hidden="true"><use href="#i-truck"/></svg><div><h3>Livré monté</h3><p>Sur palette partout en France, ou retrait gratuit à Nîmes, 866 avenue du Maréchal Juin.</p></div></li>
    </ul>
    <p class="note">En commandant, vous acceptez nos <a href="/conditions-generales-de-vente/">conditions générales de vente</a>.</p>
  </div>
</section>
</main>
"""
    return head(titre, desc, url, ld) + header("#commande", "Commander") + body + footer(script)


# ---------------------------------------------------------------------------
# Fiche modèle
# ---------------------------------------------------------------------------
def titre_fiche(m):
    t = f"Kit aménagement {m['titre']} amovible | Camperizate"
    return t if len(t) <= 62 else f"Kit aménagement {m['titre']} | Camperizate"


def desc_fiche(m):
    if m["categorie"] == "grand":
        return (f"Kit camper amovible sur mesure pour {m['nom']} : lit, cuisine et rangements, "
                f"sans perçage ni VASP. Devis gratuit, showroom à Nîmes.")
    bas = prix(m["categorie"], "pin", False)
    return (f"Kit camper amovible pour {m['nom']} : lit, cuisine et rangements posés en 5 min, "
            f"sans perçage ni VASP. Dès {bas} € TTC, showroom à Nîmes.")


def fiche(m):
    url = f"{SITE}/kit-amenagement/{m['slug']}/"
    cat = m["categorie"]
    c = CATEGORIES[cat]
    grand = cat == "grand"
    titre, desc = titre_fiche(m), desc_fiche(m)
    img, alt, w, h = m["image"]
    srcset = (f' srcset="{img[:-5]}-800.webp 800w, {img} 1600w" sizes="(min-width:960px) 50vw, 100vw"'
              if img.startswith("/img/modeles/") else "")
    faq = m["faq"] + FAQ_COMMUNE
    commande = TALLY if grand else f"/boutique/?modele={m['slug']}#commande"
    cible = ' target="_blank" rel="noopener"' if grand else ""
    texte_cta = "Demander mon devis" if grand else "Commander ce kit"
    graphe = []
    if not grand:
        bas, haut = prix(cat, "pin", False), prix(cat, "hpl", True)
        graphe.append({"@type": "Product", "name": f"Kit d'aménagement amovible {m['nom']}", "description": desc,
                       "image": SITE + img, "brand": {"@type": "Brand", "name": "Camperizate"},
                       "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": str(bas),
                                  "highPrice": str(haut), "offerCount": str(len(FINITIONS) * 2),
                                  "availability": "https://schema.org/InStock"}})
    graphe.append({"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Kits par modèle", "item": SITE + "/kit-amenagement/"},
        {"@type": "ListItem", "position": 3, "name": m["nom"], "item": url}]})
    graphe.append({"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    ld = {"@context": "https://schema.org", "@graph": graphe}

    inclus = "\n".join(
        f'        <li><svg class="ico" aria-hidden="true"><use href="#{i}"/></svg><span><b>{e(t)}</b>{e(d)}</span></li>'
        for i, t, d in m["inclus"])
    faq_html = "\n".join(
        f'      <details><summary>{e(q)}<svg class="ico" aria-hidden="true"><use href="#i-down"/></svg></summary>'
        f'<div class="a"><p>{e(a)}</p></div></details>' for q, a in faq)

    if grand:
        prix_ligne = '<p class="price-line"><b>Sur devis</b><span>gratuit, sans engagement</span></p>'
        section_prix = f"""
<section id="prix" class="kits" aria-labelledby="h-prix">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Prix</span>
      <h2 id="h-prix">Un kit conçu pour votre fourgon</h2>
      <p>Dites-nous votre modèle, sa longueur et votre usage : nous vous envoyons un devis gratuit.</p>
    </div>
    <a href="{TALLY}" class="btn btn-primary" style="max-width:420px" target="_blank" rel="noopener">Demander mon devis <svg class="ico" aria-hidden="true"><use href="#i-right"/></svg></a>
  </div>
</section>"""
    else:
        prix_ligne = f'<p class="price-line"><b>Dès {prix(cat, "pin", False)} €</b><span>TTC, direct atelier</span></p>'
        lignes = "\n".join(
            f"          <tr><td>{e(n)}<small>{e(d)}</small></td><td><b>{p[cat]} €</b></td><td><b>{p[cat] + MATELAS} €</b></td></tr>"
            for _, n, d, p in FINITIONS)
        fond = "kits" if m["mesures"] else ""
        section_prix = f"""
<section id="prix" class="{fond}" aria-labelledby="h-prix">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Prix</span>
      <h2 id="h-prix">Trois finitions, un prix atelier</h2>
      <p>Prix TTC, hors livraison (dès {c['livraison']} € en France, retrait gratuit à Nîmes).</p>
    </div>
    <table class="price-table">
      <thead><tr><th>Finition</th><th>Sans matelas</th><th>Avec matelas</th></tr></thead>
      <tbody>
{lignes}
      </tbody>
    </table>
    <p class="help">Options et accessoires (occultants, frigo, batterie, version 2+1…) : <a href="/boutique/#accessoires">voir la boutique</a>.</p>
    <a href="{commande}" class="btn btn-primary" style="margin-top:20px;max-width:420px">Commander ce kit <svg class="ico" aria-hidden="true"><use href="#i-right"/></svg></a>
  </div>
</section>"""

    section_mesures = ""
    if m["mesures"]:
        mesures = "\n".join(f'          <tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in m["mesures"])
        section_mesures = f"""
<section aria-labelledby="h-mesures">
  <div class="wrap two">
    <div class="sec-head">
      <span class="kicker">Mesures</span>
      <h2 id="h-mesures">Dimensions du kit {e(m['court'])}</h2>
      <p>Chaque kit est ajusté au coffre du véhicule. Une question sur une cote ? <a href="{TALLY}" target="_blank" rel="noopener">Écrivez-nous</a>.</p>
    </div>
    <table class="specs"><tbody>
{mesures}
    </tbody></table>
  </div>
</section>"""

    section_galerie = ""
    if m["galerie"]:
        figs = "\n".join(
            f'      <figure><img src="/img/modeles/{m["slug"]}/{ph["fichier"][:-5]}-800.webp" alt="{e(ph["alt"])}" width="{ph["w"]}" height="{ph["h"]}" loading="lazy"></figure>'
            for ph in m["galerie"])
        section_galerie = f"""
<section aria-labelledby="h-photos">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">En images</span><h2 id="h-photos">Le kit {e(m['court'])} en photos</h2></div>
    <div class="gallery">
{figs}
    </div>
  </div>
</section>"""

    section_videos, script = "", ""
    if m["videos"]:
        videos = "\n".join(
            f'      <button type="button" class="yt" data-id="{v}" aria-label="Lire la vidéo : {e(t)}">'
            f'<img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy">'
            f'<span>▶ {e(t)}</span></button>' for v, t in m["videos"])
        section_videos = f"""
<section aria-labelledby="h-videos">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">En vidéo</span><h2 id="h-videos">Le kit {e(m['court'])} en situation</h2></div>
    <div class="videos">
{videos}
    </div>
  </div>
</section>"""
        script = """<script>
document.querySelectorAll('.yt').forEach(function(b){
  b.addEventListener('click',function(){
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.id+'?autoplay=1&rel=0';
    f.title=b.getAttribute('aria-label');f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;
    var d=document.createElement('div');d.className='yt';d.appendChild(f);b.replaceWith(d);
  });
});
</script>"""

    autres = [x for x in FICHES if x["categorie"] == cat and x["slug"] != m["slug"]]
    liens_autres = "".join(f'<li><a href="/kit-amenagement/{x["slug"]}/">{e(x["nom"])}</a></li>' for x in autres)
    section_autres = f"""
<section aria-labelledby="h-autres">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">{e(c['pluriel'])}</span><h2 id="h-autres">Autres modèles compatibles</h2></div>
    <ul class="model-links">{liens_autres}</ul>
    <p class="help"><a href="/kit-amenagement/">Voir tous les modèles</a></p>
  </div>
</section>""" if autres else ""

    body = f"""
<main id="top">
<nav class="crumbs wrap" aria-label="Fil d'Ariane">
  <ol><li><a href="/">Accueil</a></li><li><a href="/kit-amenagement/">Kits par modèle</a></li><li aria-current="page">{e(m['nom'])}</li></ol>
</nav>

<section class="fiche-hero" aria-labelledby="h1">
  <div class="wrap fiche-grid">
    <div class="pic"><img src="{img}"{srcset} alt="{e(alt)}" width="{w}" height="{h}" fetchpriority="high"></div>
    <div>
      <span class="kicker">Kit camper amovible · sans VASP</span>
      <h1 id="h1">Kit d'aménagement amovible pour {e(m['nom'])}</h1>
      <p class="lead">{e(m['intro'])}</p>
      {prix_ligne}
      <div class="ctas">
        <a href="{commande}" class="btn btn-primary"{cible}>{texte_cta} <svg class="ico" aria-hidden="true"><use href="#i-right"/></svg></a>
        <a href="{TALLY}" class="btn btn-line" target="_blank" rel="noopener">Poser une question</a>
      </div>
      <ul class="chips">
        <li><svg class="ico" aria-hidden="true"><use href="#i-shield"/></svg>Sans VASP</li>
        <li><svg class="ico" aria-hidden="true"><use href="#i-timer"/></svg>Sans perçage</li>
        <li><svg class="ico" aria-hidden="true"><use href="#i-truck"/></svg>Livré monté en France</li>
      </ul>
    </div>
  </div>
</section>

<section class="kits" aria-labelledby="h-kit">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Le kit {e(m['court'])}</span><h2 id="h-kit">Ce que comprend le kit</h2></div>
    <ul class="incl">
{inclus}
    </ul>
    <p class="fix">{e(m['fixation'])}</p>
  </div>
</section>
{section_mesures}
{section_prix}
{section_galerie}
{section_videos}

<section class="showroom" aria-labelledby="h-showroom">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Showroom</span><h2 id="h-showroom">Venez voir nos kits à Nîmes</h2></div>
    <address>Local n° 112, 866 avenue du Maréchal Juin<br>30900 Nîmes</address>
    <a href="{TALLY}" class="btn btn-line" style="max-width:420px" target="_blank" rel="noopener">Prévenir de ma visite</a>
  </div>
</section>

<section class="faq" aria-labelledby="h-faq">
  <div class="wrap faq-wrap">
    <div class="sec-head"><span class="kicker">Questions fréquentes</span><h2 id="h-faq">Kit {e(m['court'])} : en bref</h2></div>
    <div class="faq-list">
{faq_html}
    </div>
  </div>
</section>
{section_autres}
</main>
"""
    return head(titre, desc, url, ld, og_type="product") + header("#prix", "Voir les prix") + body + footer(script)


# ---------------------------------------------------------------------------
# Catalogue des modèles
# ---------------------------------------------------------------------------
def liste_modeles(cat):
    return "".join(f'<li><a href="/kit-amenagement/{m["slug"]}/">{e(m["nom"])}</a></li>'
                   for m in FICHES if m["categorie"] == cat)


def catalogue():
    url = f"{SITE}/kit-amenagement/"
    titre = "Kit aménagement par modèle : ludospace et van | Camperizate"
    desc = ("Trouvez le kit camper amovible de votre véhicule : Berlingo, Kangoo, Partner, Trafic, Transporter, Vito… "
            "Sans perçage ni VASP, dès 500 € TTC.")
    blocs = []
    for cat, ancre, sous in (("mini", "ludospaces", "dès 500 € TTC · vous gardez vos 5 places"),
                             ("moyen", "vans", "dès 700 € TTC · hauteur adaptée à vos sièges"),
                             ("grand", "fourgons", "sur devis")):
        blocs.append(f"""
    <div class="cat-block" id="{ancre}">
      <h2>{e(CATEGORIES[cat]['pluriel'])}</h2>
      <p class="help">{e(sous)}</p>
      <ul class="model-links">{liste_modeles(cat)}</ul>
    </div>""")
    ld = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": m["nom"], "url": f"{SITE}/kit-amenagement/{m['slug']}/"}
        for i, m in enumerate(FICHES)]}
    body = f"""
<main id="top">
<nav class="crumbs wrap" aria-label="Fil d'Ariane"><ol><li><a href="/">Accueil</a></li><li aria-current="page">Kits par modèle</li></ol></nav>
<section class="shop-hero" aria-labelledby="h1">
  <div class="wrap">
    <span class="kicker">Kits par modèle</span>
    <h1 id="h1">Le kit d'aménagement de votre véhicule</h1>
    <p class="lead">Chaque kit est fabriqué pour un modèle précis. Choisissez le vôtre pour voir le kit, les prix et les mesures.</p>
  </div>
</section>
<section class="kits" aria-label="Modèles compatibles">
  <div class="wrap">{''.join(blocs)}
    <p class="help" style="margin-top:28px">Modèle absent ? <a href="{TALLY}" target="_blank" rel="noopener">Écrivez-nous</a> : nous avons sûrement déjà un kit pour lui.</p>
  </div>
</section>
</main>
"""
    return head(titre, desc, url, ld) + header("/boutique/", "Boutique") + body + footer()


# ---------------------------------------------------------------------------
# Merci (retour Stripe)
# ---------------------------------------------------------------------------
def merci():
    body = f"""
<main id="top">
<section class="shop-hero">
  <div class="wrap">
    <span class="kicker">Commande reçue</span>
    <h1>Merci pour votre commande !</h1>
    <p class="lead">Votre paiement est confirmé. Vous allez recevoir par e-mail votre bon de commande avec le récapitulatif.</p>
    <ol class="steps-merci">
      <li><b>Sous 48 h ouvrées</b> : nous vous contactons pour vérifier les mesures de votre véhicule.</li>
      <li><b>Environ 3 semaines</b> : fabrication dans notre atelier (plus rapide si votre modèle est en stock).</li>
      <li><b>Livraison ou retrait</b> : kit livré monté sur palette, ou retrait au showroom de Nîmes à la date convenue.</li>
    </ol>
    <p class="help">Rétractation sous 14 jours, garantie légale de 2 ans : voir nos <a href="/conditions-generales-de-vente/">conditions générales de vente</a>.</p>
    <div class="ctas" style="margin-top:20px">
      <a class="btn btn-primary" href="{TALLY}" target="_blank" rel="noopener">Nous écrire</a>
      <a class="btn btn-line" href="/">Retour à l'accueil</a>
    </div>
  </div>
</section>
</main>
"""
    return (head("Merci pour votre commande | Camperizate", "Confirmation de commande.", f"{SITE}/merci/", robots="noindex")
            + header("/", "Accueil") + body + footer())


# ---------------------------------------------------------------------------
# Landing (écrite à la main) : on ne met à jour que la liste des modèles
# ---------------------------------------------------------------------------
def maj_landing():
    chemin = PUBLIC / "index.html"
    src = chemin.read_text(encoding="utf-8")
    cols = "".join(f"""
      <div>
        <h3>{e(CATEGORIES[cat]['pluriel'])}</h3>
        <ul class="all-models">{liste_modeles(cat)}</ul>
      </div>""" for cat in ("mini", "moyen", "grand"))
    bloc = f"""<!-- MODELES:debut -->
<section id="modeles" aria-labelledby="h-modeles">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Modèles compatibles</span>
      <h2 id="h-modeles">Un kit pour chaque véhicule</h2>
    </div>
    <div class="all-models-grid">{cols}
    </div>
    <p class="help"><a href="/kit-amenagement/">Voir tous les kits par modèle</a></p>
  </div>
</section>
<style>
.all-models-grid{{display:grid;gap:24px}}
.all-models-grid h3{{margin-bottom:8px}}
.all-models{{list-style:none;margin:0;padding:0;columns:2;column-gap:16px}}
.all-models li{{break-inside:avoid}}
.all-models a{{display:inline-flex;align-items:center;min-height:40px;font-size:15px;text-underline-offset:3px}}
.all-models a:hover{{color:var(--orange)}}
@media (min-width:960px){{.all-models-grid{{grid-template-columns:1fr 1fr 1fr}}.all-models{{columns:1}}}}
</style>
<!-- MODELES:fin -->"""
    src = re.sub(r"<!-- MODELES:debut -->.*?<!-- MODELES:fin -->", lambda _: bloc, src, flags=re.S)
    slugs = json.dumps([m["slug"] for m in FICHES])
    src = re.sub(r"var FICHES=\[.*?\];", lambda _: f"var FICHES={slugs};", src)
    chemin.write_text(src, encoding="utf-8")
    print("mis à jour public/index.html (liste des modèles)")


def sitemap():
    today = date.today().isoformat()
    urls = ["/", "/kit-amenagement/", "/boutique/"] + [f"/kit-amenagement/{m['slug']}/" for m in FICHES]
    urls += ["/conditions-generales-de-vente/", "/mentions-legales/", "/politique-de-confidentialite/"]
    rows = "\n".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n'


def ecrire(chemin, contenu):
    out = PUBLIC / chemin
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(contenu, encoding="utf-8")
    print("écrit", out.relative_to(ROOT))


def main():
    ecrire("boutique/index.html", boutique())
    ecrire("merci/index.html", merci())
    for m in FICHES:
        ecrire(f"kit-amenagement/{m['slug']}/index.html", fiche(m))
    ecrire("sitemap.xml", sitemap())
    ecrire("kit-amenagement/index.html", catalogue())
    maj_landing()
    table = {"/fr/": f"{SITE}/", "/fr/kit-camperizacion/": f"{SITE}/kit-amenagement/", "/fr/tienda/": f"{SITE}/boutique/"}
    for m in FICHES:
        for ancien in m["anciens"]:
            table[ancien] = f"{SITE}/kit-amenagement/{m['slug']}/"
    (ROOT / "tools" / "redirections.json").write_text(json.dumps(table, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    vides = [k for k, v in STRIPE.items() if not v]
    print(f"liens Stripe manquants : {len(vides)}/{len(STRIPE)}")


if __name__ == "__main__":
    main()
