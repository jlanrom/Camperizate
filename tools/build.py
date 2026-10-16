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
    # Kits grand fourgon
    "kit-grand-pin-sans-retrait": "https://buy.stripe.com/aFa3cuagK3wB3nB2dV6EU0y",
    "kit-grand-pin-avec-retrait": "https://buy.stripe.com/aFa9AS0Ga9UZ8HVf0H6EU0z",
    "kit-grand-carrossier-sans-retrait": "https://buy.stripe.com/4gMeVc4WqaZ31ft2dV6EU0A",
    "kit-grand-carrossier-avec-retrait": "https://buy.stripe.com/00w6oGfB41ot2jxaKr6EU0B",
    "kit-grand-hpl-sans-retrait": "https://buy.stripe.com/8x214m0Ga1ot2jx7yf6EU0C",
    "kit-grand-hpl-avec-retrait": "https://buy.stripe.com/9B66oGcoSd7bbU705N6EU0D",
    "kit-grand-pin-sans-livraison": "https://buy.stripe.com/6oU4gy60ud7bf6j6ub6EU0E",
    "kit-grand-pin-avec-livraison": "https://buy.stripe.com/00w8wOdsWaZ32jxcSz6EU0F",
    "kit-grand-carrossier-sans-livraison": "https://buy.stripe.com/8x25kC74y2sx9LZ6ub6EU0G",
    "kit-grand-carrossier-avec-livraison": "https://buy.stripe.com/7sY28q60ugjnaQ3g4L6EU0H",
    "kit-grand-hpl-sans-livraison": "https://buy.stripe.com/8x2cN4bkO7MR2jx6ub6EU0I",
    "kit-grand-hpl-avec-livraison": "https://buy.stripe.com/3cIdR84Wq3wB4rF8Cj6EU0J",
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
# 2. CATALOGUE : données dans tools/catalogue.py (prix et véhicules du formulaire Tally)
# ---------------------------------------------------------------------------
from catalogue import (ACCESSOIRES, CATEGORIES, CONTENU, FINITIONS, FIXATION, FIXATION_GRAND, GROUPES,  # noqa: E402
                       IMAGE_HPL_ANTHRACITE, INCLUS, MATELAS, MODELES, OPTIONS, REDIRECTIONS, REDIRECTIONS_PREFIXES)

# Liste des véhicules de la boutique et de la landing : (catégorie de prix, valeur, libellé, fiche)
VEHICULES = [(cat, valeur, libelle, m["slug"]) for m in MODELES for valeur, libelle, cat in m["variantes"]]

# Photos par modèle : générées par tools/photos.py (voir docs/PHOTOS.md)
PHOTOS_JSON = ROOT / "tools" / "photos.json"
PHOTOS = json.loads(PHOTOS_JSON.read_text(encoding="utf-8")) if PHOTOS_JSON.exists() else {}


def construire_fiches():
    fiches = []
    for m in MODELES:
        c = CONTENU[m["groupe"]]
        photos = PHOTOS.get(m["slug"], [])
        if photos:
            ph = photos[0]
            image = (f"/img/modeles/{m['slug']}/{ph['fichier']}", ph["alt"], ph["w"], ph["h"])
        else:
            image = c["image"]
        fiches.append({
            "slug": m["slug"], "nom": m["nom"], "court": m["court"], "categorie": m["cat"], "groupe": m["groupe"],
            "anciens": m["anciens"], "titre": m.get("titre") or m["nom"], "image": image, "galerie": photos[1:],
            "intro": m.get("intro") or c["intro"].format(nom=m["nom"]),
            "inclus": m.get("inclus") or c["inclus"],
            "fixation": m.get("fixation") or (FIXATION_GRAND if m["cat"] == "grand" else FIXATION),
            "mesures": m.get("mesures", []), "videos": m.get("videos", []),
            "faq": m.get("faq") or c["faq"], "versions": m.get("versions", ""), "variantes": m["variantes"],
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
.price-table td img{float:left;width:44px;height:44px;object-fit:cover;border-radius:var(--r);margin:0 10px 0 0}
.versions{margin-top:24px}
.versions h3{margin-bottom:8px}
.versions p{color:var(--brown-70)}
.versions a{justify-content:space-between;gap:12px}
.versions b{color:var(--orange);white-space:nowrap}
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
.order.is-devis .step-fin,.order.is-devis .step-mat,.order.is-devis .total{display:none}
.order.is-devis .devis{display:block}
.choice.with-img{justify-content:flex-start}
.choice.with-img img{width:56px;height:56px;object-fit:cover;border-radius:var(--r);flex:none}
.choice.with-img span{flex:1}
.opts ul{list-style:none;padding:0;display:grid;gap:6px}
.opts li{display:flex;align-items:center;gap:10px}
.opts li img{width:40px;height:40px;object-fit:cover;border-radius:var(--r)}
.acc-img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--r);background:var(--sand)}
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
.info p+p{margin-top:10px}
.info-list{margin:0 0 20px;padding-left:1.2em;display:grid;gap:6px}
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
    <nav class="nav" id="menu" aria-label="Menu principal">
      <a href="/kit-amenagement/">Modèles</a>
      <a href="/accessoires/">Accessoires</a>
      <a href="/guide-kit-meubles-camper/">Guide</a>
      <a href="/contact/">Contact</a>
    </nav>
    <a href="{lien}" class="btn btn-line head-btn">{texte}</a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="menu" aria-label="Menu"><span></span></button>
  </div>
</header>
<script>(function(){{var h=document.querySelector('.site-head'),b=h&&h.querySelector('.nav-toggle');if(!b)return;b.addEventListener('click',function(){{b.setAttribute('aria-expanded',h.classList.toggle('open'))}});h.querySelectorAll('.nav a').forEach(function(a){{a.addEventListener('click',function(){{h.classList.remove('open');b.setAttribute('aria-expanded','false')}})}})}})();</script>
"""


def footer(script=""):
    return f"""
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img src="/img/camperizate-logo-white.svg" alt="Camperizate" width="160" height="21" loading="lazy">
        <p>Kits camper amovibles pour ludospaces, vans et fourgons, fabriqués dans notre atelier.</p>
        <a class="link" href="/kit-amenagement/">Tous les modèles</a> · <a class="link" href="/boutique/">Boutique</a> · <a class="link" href="/accessoires/">Accessoires</a> · <a class="link" href="/guide-kit-meubles-camper/">Guide</a> · <a class="link" href="/contact/">Contact</a>
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
    desc = ("Commandez votre kit d'aménagement amovible pour ludospace, van ou fourgon : choisissez votre véhicule, "
            "la finition et le matelas, et payez en ligne. Dès 500 € TTC.")
    groupes = []
    for cat in ("mini", "moyen", "grand"):
        opts = "".join(f'<option value="{v}" data-cat="{c}" data-fiche="{f}">{e(n)}</option>'
                       for c, v, n, f in sorted((x for x in VEHICULES if x[0] == cat), key=lambda x: x[2]))
        groupes.append(f'<optgroup label="{e(CATEGORIES[cat]["pluriel"])}">{opts}</optgroup>')
    groupes.append('<optgroup label="Autre"><option value="autre" data-cat="autre">Autre modèle</option></optgroup>')
    finitions = "\n".join(
        f'<label class="choice with-img"><input type="radio" name="fin" value="{k}"{" checked" if k == "carrossier" else ""}>'
        f'<img src="{img}" alt="" width="64" height="64" loading="lazy">'
        f'<span>{e(n)}<small>{e(d)}</small></span><b data-fin="{k}"></b></label>'
        for k, n, d, _, img in FINITIONS)
    options = "".join(f'<li><img src="{img}" alt="" width="40" height="40" loading="lazy">{e(n)} <b>+ {p} €</b></li>'
                      for _, n, _d, p, img in OPTIONS)
    def bouton_acc(k):
        if STRIPE.get(k):
            return f'<a class="btn btn-primary" href="{e(STRIPE[k])}">Acheter</a>'
        return f'<a class="btn btn-line" href="{TALLY}" target="_blank" rel="noopener">Commander par message</a>'

    acc = "\n".join(
        f'<li id="{ancre}"><img class="acc-img" src="{img}" alt="{e(n)}" width="400" height="300" loading="lazy">'
        f'<div class="row"><div><h3>{e(n)}</h3>{"<small>" + e(d) + "</small>" if d else ""}</div><b>{p} €</b></div>'
        f'{bouton_acc(k)}</li>'
        for k, ancre, n, d, p, img in ACCESSOIRES)
    data = {
        "liens": {k: v for k, v in STRIPE.items() if k.startswith("kit-")},
        "prix": {c: {f[0]: f[3][c] for f in FINITIONS} for c in ("mini", "moyen", "grand")},
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
        {"@type": "Product", "name": "Kit d'aménagement camper amovible pour grand fourgon",
         "image": SITE + "/img/hero-van-amenage-800.webp", "brand": {"@type": "Brand", "name": "Camperizate"},
         "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": str(prix("grand", "pin", False)),
                    "highPrice": str(prix("grand", "hpl", True)), "offerCount": "6", "availability": "https://schema.org/InStock"}},
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
    f.classList.toggle('is-devis',c==='autre');
    var k=D.prix[c]?c:'mini';
    document.querySelectorAll('[data-fin]').forEach(function(b){b.textContent='dès '+fmt(D.prix[k][b.dataset.fin]);});
    document.getElementById('mat-prix').textContent='+ '+fmt(D.matelas);
    document.getElementById('liv-prix').textContent='+ '+fmt(D.livraison[k]);
    if(!c||c==='autre'){return;}
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
        <p class="help">Modèle absent ? Choisissez « Autre modèle » ou <a href="{TALLY}" target="_blank" rel="noopener">écrivez-nous</a>. <a href="/kit-amenagement/">Voir les fiches des modèles</a>.</p>
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
          <p class="help">Kit fabriqué sur mesure : pas de droit de rétractation. Voir les <a href="/conditions-generales-de-vente/">CGV</a>.</p>
          <div class="opts">Options à ajouter sur la page de paiement (<a href="/accessoires/#options">voir en détail</a>) :<ul>{options}</ul></div>
        </div>
        <div class="devis">
          <h3>Votre véhicule n'est pas dans la liste ?</h3>
          <p>Nous fabriquons des kits pour beaucoup d'autres modèles. Dites-nous la marque, le modèle et l'année : nous vous répondons avec le prix, sans engagement.</p>
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
    <p class="note">Les kits, matelas et occultants sont fabriqués sur mesure pour votre véhicule : ils ne peuvent pas faire l'objet d'un droit de rétractation (art. L221-28, 3° du Code de la consommation). En commandant, vous acceptez nos <a href="/conditions-generales-de-vente/">conditions générales de vente</a>.</p>
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
    bas = prix(m["categorie"], "pin", False)
    return (f"Kit camper amovible pour {m['nom']} : lit, cuisine et rangements posés en quelques minutes, "
            f"sans perçage ni VASP. Dès {bas} € TTC, showroom à Nîmes.")


def nom_groupe(groupe):
    return next(n for g, n, _ in GROUPES if g == groupe)


def section_videos(videos, court):
    if not videos:
        return "", ""
    boutons = "\n".join(
        f'      <button type="button" class="yt" data-id="{v}" aria-label="Lire la vidéo : {e(t)}">'
        f'<img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy">'
        f'<span>▶ {e(t)}</span></button>' for v, t in videos)
    html_ = f"""
<section aria-labelledby="h-videos">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">En vidéo</span><h2 id="h-videos">{e(court)} en situation</h2></div>
    <div class="videos">
{boutons}
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
    return html_, script


def faq_html(faq):
    return "\n".join(
        f'      <details><summary>{e(q)}<svg class="ico" aria-hidden="true"><use href="#i-down"/></svg></summary>'
        f'<div class="a"><p>{e(a)}</p></div></details>' for q, a in faq)


def fiche(m):
    url = f"{SITE}/kit-amenagement/{m['slug']}/"
    cat = m["categorie"]
    c = CATEGORIES[cat]
    titre, desc = titre_fiche(m), desc_fiche(m)
    img, alt, w, h = m["image"]
    srcset = (f' srcset="{img[:-5]}-800.webp 800w, {img} 1600w" sizes="(min-width:960px) 50vw, 100vw"'
              if img.startswith("/img/modeles/") else "")
    faq = m["faq"] + FAQ_COMMUNE
    commande = f"/boutique/?modele={m['slug']}#commande"
    bas, haut = prix(cat, "pin", False), prix(cat, "hpl", True)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": f"Kit d'aménagement amovible {m['nom']}", "description": desc, "image": SITE + img,
         "brand": {"@type": "Brand", "name": "Camperizate"},
         "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": str(bas), "highPrice": str(haut),
                    "offerCount": str(len(FINITIONS) * 2), "availability": "https://schema.org/InStock"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Kits par modèle", "item": SITE + "/kit-amenagement/"},
            {"@type": "ListItem", "position": 3, "name": m["nom"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}

    inclus = "\n".join(
        f'        <li><svg class="ico" aria-hidden="true"><use href="#{i}"/></svg><span><b>{e(t)}</b>{e(d)}</span></li>'
        for i, t, d in m["inclus"])

    # Versions (Berlingo M / XL…) : une ligne par variante, avec son prix
    versions = ""
    if len(m["variantes"]) > 1 or m["versions"]:
        lignes_v = "".join(
            f'<li><a href="/boutique/?modele={v}#commande"><span>{e(lib)}</span>'
            f'<b>dès {prix(vc, "pin", False)} €</b></a></li>' for v, lib, vc in m["variantes"]) if len(m["variantes"]) > 1 else ""
        versions = f"""
    <div class="versions">
      <h3>Versions</h3>
      {f'<p>{e(m["versions"])}</p>' if m["versions"] else ""}
      {f'<ul class="model-links">{lignes_v}</ul>' if lignes_v else ""}
    </div>"""

    lignes = "\n".join(
        f'          <tr><td><img src="{im}" alt="" width="48" height="48" loading="lazy">{e(n)}<small>{e(d)}</small></td>'
        f'<td><b>{p[cat]} €</b></td><td><b>{p[cat] + MATELAS} €</b></td></tr>'
        for _, n, d, p, im in FINITIONS)

    section_mesures = ""
    if m["mesures"]:
        mesures = "\n".join(f'          <tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in m["mesures"])
        section_mesures = f"""
<section aria-labelledby="h-mesures">
  <div class="wrap two">
    <div class="sec-head">
      <span class="kicker">Mesures</span>
      <h2 id="h-mesures">Dimensions du kit {e(m['court'])}</h2>
      <p>Chaque kit est ajusté à votre véhicule : nous vérifions les mesures avec vous avant la fabrication. Une question ? <a href="{TALLY}" target="_blank" rel="noopener">Écrivez-nous</a>.</p>
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

    videos_html, script = section_videos(m["videos"], f"Le kit {m['court']}")

    autres = [x for x in FICHES if x["groupe"] == m["groupe"] and x["slug"] != m["slug"]]
    liens_autres = "".join(f'<li><a href="/kit-amenagement/{x["slug"]}/">{e(x["nom"])}</a></li>' for x in autres)
    section_autres = f"""
<section aria-labelledby="h-autres">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">{e(nom_groupe(m['groupe']))}</span><h2 id="h-autres">Autres modèles compatibles</h2></div>
    <ul class="model-links">{liens_autres}</ul>
    <p class="help"><a href="/kit-amenagement/">Voir tous les modèles</a> · <a href="/accessoires/">Options et accessoires</a> · <a href="/guide-kit-meubles-camper/">Le guide du kit camper</a></p>
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
      <p class="price-line"><b>Dès {bas} €</b><span>TTC, direct atelier</span></p>
      <div class="ctas">
        <a href="{commande}" class="btn btn-primary">Commander ce kit <svg class="ico" aria-hidden="true"><use href="#i-right"/></svg></a>
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

<section id="prix" class="{'kits' if m['mesures'] else ''}" aria-labelledby="h-prix">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Prix</span>
      <h2 id="h-prix">Trois finitions, un prix atelier</h2>
      <p>Prix TTC du kit {e(c['nom'].lower())}, hors livraison (dès {c['livraison']} € en France, retrait gratuit à Nîmes).</p>
    </div>
    <table class="price-table">
      <thead><tr><th>Finition</th><th>Sans matelas</th><th>Avec matelas</th></tr></thead>
      <tbody>
{lignes}
      </tbody>
    </table>
    {versions}
    <p class="help">Options (tiroirs, égouttoir, version 2+1…) et accessoires (occultants, frigo, batterie…) : <a href="/accessoires/">voir en détail</a>.</p>
    <a href="{commande}" class="btn btn-primary" style="margin-top:20px;max-width:420px">Commander ce kit <svg class="ico" aria-hidden="true"><use href="#i-right"/></svg></a>
  </div>
</section>
{section_galerie}
{videos_html}

<section class="showroom" aria-labelledby="h-showroom">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Showroom</span><h2 id="h-showroom">Venez voir nos kits à Nîmes</h2></div>
    <address>Local n° 112, 866 avenue du Maréchal Juin<br>30900 Nîmes</address>
    <a href="/contact/" class="btn btn-line" style="max-width:420px">Préparer ma visite</a>
  </div>
</section>

<section class="faq" aria-labelledby="h-faq">
  <div class="wrap faq-wrap">
    <div class="sec-head"><span class="kicker">Questions fréquentes</span><h2 id="h-faq">Kit {e(m['court'])} : en bref</h2></div>
    <div class="faq-list">
{faq_html(faq)}
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
def liste_modeles(groupe):
    return "".join(f'<li><a href="/kit-amenagement/{m["slug"]}/">{e(m["nom"])}</a></li>'
                   for m in FICHES if m["groupe"] == groupe)


SOUS_TITRES = {
    "ludospace": "dès 500 € TTC · vous gardez vos 5 places",
    "monospace": "dès 500 € TTC · couchage pour 1 ou 2 personnes",
    "van": "dès 700 € TTC · hauteur adaptée à vos sièges · versions XL et Maxi des ludospaces",
    "fourgon": "dès 800 € TTC · lit 180 à 190 cm",
}
ANCRES = {"ludospace": "ludospaces", "monospace": "monospaces", "van": "vans", "fourgon": "fourgons"}


def catalogue():
    url = f"{SITE}/kit-amenagement/"
    titre = "Kit aménagement par modèle : ludospace, van, fourgon | Camperizate"
    desc = ("Trouvez le kit camper amovible de votre véhicule : Berlingo, Kangoo, Partner, Trafic, Transporter, Vito, "
            "Ducato… Sans perçage ni VASP, dès 500 € TTC.")
    blocs = []
    for groupe, nom, _ in GROUPES:
        blocs.append(f"""
    <div class="cat-block" id="{ANCRES[groupe]}">
      <h2>{e(nom)}</h2>
      <p class="help">{e(SOUS_TITRES[groupe])}</p>
      <ul class="model-links">{liste_modeles(groupe)}</ul>
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
# Pages de contenu : accessoires, occultants, matelas, guide, contact
# ---------------------------------------------------------------------------
def page_simple(chemin, titre, desc, kicker, h1, lead, contenu, ld=None, script="", cta=("/boutique/", "Boutique"), crumb=None):
    url = f"{SITE}{chemin}"
    fil = crumb or h1
    body = f"""
<main id="top">
<nav class="crumbs wrap" aria-label="Fil d'Ariane"><ol><li><a href="/">Accueil</a></li><li aria-current="page">{e(fil)}</li></ol></nav>
<section class="shop-hero" aria-labelledby="h1">
  <div class="wrap">
    <span class="kicker">{e(kicker)}</span>
    <h1 id="h1">{e(h1)}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
{contenu}
</main>
"""
    return head(titre, desc, url, ld) + header(*cta) + body + footer(script)


def bouton_stripe(cle, texte="Acheter"):
    if STRIPE.get(cle):
        return f'<a class="btn btn-primary" href="{e(STRIPE[cle])}">{texte}</a>'
    return f'<a class="btn btn-line" href="{TALLY}" target="_blank" rel="noopener">Commander par message</a>'


def accessoires():
    inclus = "\n".join(
        f'<li><img class="acc-img" src="{img}" alt="{e(n)}" width="400" height="300" loading="lazy">'
        f'<div class="row"><div><h3>{e(n)}</h3><small>{e(d)}</small></div><b>Inclus</b></div></li>'
        for n, d, img in INCLUS)
    options = "\n".join(
        f'<li id="{ancre}"><img class="acc-img" src="{img}" alt="{e(n)}" width="400" height="300" loading="lazy">'
        f'<div class="row"><div><h3>{e(n)}</h3><small>{e(d)}</small></div><b>+ {p} €</b></div></li>'
        for ancre, n, d, p, img in OPTIONS)
    acc = "\n".join(
        f'<li id="{ancre}"><img class="acc-img" src="{img}" alt="{e(n)}" width="400" height="300" loading="lazy">'
        f'<div class="row"><div><h3>{e(n)}</h3><small>{e(d)}</small></div><b>{p} €</b></div>{bouton_stripe(k)}</li>'
        for k, ancre, n, d, p, img in ACCESSOIRES)
    contenu = f"""
<section class="kits" aria-labelledby="h-inclus">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">De série</span><h2 id="h-inclus">Inclus dans chaque kit</h2>
      <p>Lit, table, tiroir cuisine à droite et coffre à gauche. Les options ci-dessous remplacent ou complètent ces éléments.</p></div>
    <ul class="acc">
{inclus}
    </ul>
  </div>
</section>
<section id="options" aria-labelledby="h-options">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Options du kit</span><h2 id="h-options">Adaptez le kit à votre façon de voyager</h2>
      <p>Toutes les options sont facultatives. Vous les ajoutez sur la page de paiement de votre kit, après l'avoir choisi dans la <a href="/boutique/">boutique</a>.</p></div>
    <ul class="acc">
{options}
    </ul>
    <a class="btn btn-primary" href="/boutique/#commande" style="margin-top:20px;max-width:420px">Configurer mon kit</a>
  </div>
</section>
<section id="accessoires-seuls" class="kits" aria-labelledby="h-acc">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Accessoires</span><h2 id="h-acc">Pour partir équipé</h2>
      <p>Livrés avec votre kit ou à retirer au showroom de Nîmes. Les occultants sont faits sur mesure : indiquez votre modèle au paiement.</p></div>
    <ul class="acc">
{acc}
    </ul>
  </div>
</section>"""
    return page_simple("/accessoires/", "Options et accessoires pour kit camper amovible | Camperizate",
                       "Options du kit camper (tiroirs, équerre, égouttoir, version 2+1) et accessoires : occultants isolants, "
                       "frigo à compresseur, batterie lithium, réchaud, douche et toilettes portables. Prix TTC.",
                       "Options et accessoires", "Options et accessoires du kit camper",
                       "Tout ce qui complète votre kit : les options à choisir à la commande et les accessoires pour partir équipé.",
                       contenu)


def occultants():
    k = next(a for a in ACCESSOIRES if a[0] == "occultants")
    faq = [("Les occultants vont-ils sur toutes les vitres ?",
            "Oui. Le jeu couvre toutes les vitres de votre véhicule, découpées sur mesure pour votre modèle."),
           ("Comment se fixent-ils ?", "Avec des ventouses intégrées à l'isolant : ils se posent et se retirent en quelques secondes, sans outil."),
           ("Isolent-ils du froid et du chaud ?", "Oui. Les 9 couches limitent les pertes de chaleur la nuit et coupent le soleil le jour. "
            "Ils occultent aussi totalement : personne ne voit l'intérieur.")]
    videos_html, script = section_videos([("wbGcR5GZ1Fg", "Les occultants en vidéo")], "Les occultants")
    contenu = f"""
<section class="kits" aria-labelledby="h-produit">
  <div class="wrap fiche-grid">
    <div class="pic"><img src="{k[5]}" alt="Occultants isolants posés sur les vitres d'un van" width="800" height="600" loading="lazy" style="border-radius:var(--r);width:100%"></div>
    <div>
      <h2 id="h-produit">Occultants isolants 9 couches</h2>
      <p class="price-line"><b>{k[4]} €</b><span>TTC, le jeu complet</span></p>
      <ul class="info-list">
        <li>Toutes les vitres du véhicule, découpées pour votre modèle</li>
        <li>Isolant 9 couches, finition grise</li>
        <li>Fixation par ventouses, sans perçage ni adhésif</li>
        <li>Nuit noire et intimité totale, même en ville</li>
      </ul>
      <div class="ctas">{bouton_stripe("occultants", "Acheter les occultants")}
        <a class="btn btn-line" href="{TALLY}" target="_blank" rel="noopener">Une question ?</a></div>
      <p class="help">Fabriqués sur mesure : pas de droit de rétractation. Indiquez votre modèle et son année au paiement.</p>
    </div>
  </div>
</section>
{videos_html}
<section class="faq" aria-labelledby="h-faq">
  <div class="wrap faq-wrap">
    <div class="sec-head"><span class="kicker">Questions fréquentes</span><h2 id="h-faq">Occultants : en bref</h2></div>
    <div class="faq-list">
{faq_html(faq)}
    </div>
  </div>
</section>"""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": "Occultants isolants 9 couches", "image": k[5], "brand": {"@type": "Brand", "name": "Camperizate"},
         "offers": {"@type": "Offer", "priceCurrency": "EUR", "price": str(k[4]), "availability": "https://schema.org/InStock",
                    "url": f"{SITE}/occultants-isolants/"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    return page_simple("/occultants-isolants/", "Occultants isolants pour van sur mesure | Camperizate",
                       f"Occultants isotherme 9 couches pour toutes les vitres de votre van ou ludospace, sur mesure, fixation par ventouses. {k[4]} € TTC.",
                       "Accessoire", "Occultants isolants sur mesure pour van",
                       "Noir complet, intimité et isolation : un jeu d'occultants pour toutes les vitres, découpé pour votre modèle.",
                       contenu, ld, script, crumb="Occultants isolants")


def matelas():
    faq = [("Le matelas est-il vendu seul ?", "Non : il est fabriqué avec votre kit, aux mesures du lit. Vous le choisissez à la commande du kit (+ 150 €)."),
           ("Peut-on le replier dans le coffre ?", "Oui. Il est en plusieurs pièces et se range dans le coffre avec le kit replié."),
           ("Quelle épaisseur ?", "8 cm de mousse haute densité D30 (30 kg/m³), ferme et confortable pour dormir plusieurs nuits.")]
    videos_html, script = section_videos([("fRCdNFoSC8M", "Le matelas en vidéo"), ("kUtbMAAaMW8", "Le lit monté")], "Le matelas")
    contenu = f"""
<section class="kits" aria-labelledby="h-produit">
  <div class="wrap two">
    <div>
      <h2 id="h-produit">Un matelas aux mesures de votre lit</h2>
      <p class="price-line"><b>+ {MATELAS} €</b><span>TTC, avec votre kit</span></p>
      <table class="specs"><tbody>
        <tr><th scope="row">Mousse</th><td>haute densité D30 (30 kg/m³)</td></tr>
        <tr><th scope="row">Épaisseur</th><td>8 cm</td></tr>
        <tr><th scope="row">Pièces</th><td>en plusieurs pièces, 3 pièces pour les monospaces</td></tr>
        <tr><th scope="row">Mesures</th><td>découpé pour le lit de votre kit</td></tr>
      </tbody></table>
    </div>
    <div>
      <p>Chaque kit a ses propres mesures : nous coupons le matelas pour qu'il couvre tout le lit, sans trou ni débord. Il se range en pièces dans le coffre avec le kit.</p>
      <div class="ctas"><a class="btn btn-primary" href="/boutique/#commande">Choisir mon kit avec matelas</a></div>
      <p class="help">Fabriqué sur mesure : pas de droit de rétractation.</p>
    </div>
  </div>
</section>
{videos_html}
<section class="faq" aria-labelledby="h-faq">
  <div class="wrap faq-wrap">
    <div class="sec-head"><span class="kicker">Questions fréquentes</span><h2 id="h-faq">Matelas : en bref</h2></div>
    <div class="faq-list">
{faq_html(faq)}
    </div>
  </div>
</section>"""
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return page_simple("/matelas-camper/", "Matelas camper sur mesure pour van | Camperizate",
                       f"Matelas camper sur mesure en mousse D30 de 8 cm, découpé pour le lit de votre kit amovible. + {MATELAS} € avec le kit.",
                       "Matelas", "Matelas camper sur mesure", "Une mousse ferme de 8 cm, découpée pour le lit de votre kit et rangée en pièces dans le coffre.",
                       contenu, ld, script, crumb="Matelas camper")


def guide():
    lignes_prix = "".join(
        f'<tr><td><a href="/kit-amenagement/#{ANCRES[g]}">{e(n)}</a></td>'
        f'<td><b>dès {prix(cat, "pin", False)} €</b></td><td>dès {CATEGORIES[cat]["livraison"]} €</td></tr>'
        for g, n, cat in GROUPES)
    finitions = "".join(
        f'<li><img class="acc-img" src="{img}" alt="{e(n)}" width="400" height="300" loading="lazy">'
        f'<div class="row"><div><h3>{e(n)}</h3><small>{e(d)}</small></div></div></li>' for _, n, d, _p, img in FINITIONS)
    faq = FAQ_COMMUNE + [
        ("Combien de temps pour monter le kit ?", "Quelques minutes. Le kit se pose dans le coffre et le lit se déplie ; pour rouler, tout se replie."),
        ("Le kit passe-t-il le contrôle technique ?", "Oui : c'est un chargement amovible, le véhicule n'est pas modifié. Vous pouvez aussi le retirer avant le contrôle."),
        ("Puis-je voir un kit avant d'acheter ?", "Oui, au showroom de Nîmes, sur rendez-vous."),
    ]
    contenu = f"""
<section class="kits" aria-labelledby="h-principe">
  <div class="wrap two">
    <div class="sec-head"><span class="kicker">1. Le principe</span><h2 id="h-principe">Un kit amovible, pas un aménagement fixe</h2></div>
    <div>
      <p>Le kit réunit le lit, la cuisine et les rangements dans un meuble qui se pose dans le coffre. Il n'est ni vissé ni percé : c'est un chargement, comme une valise.</p>
      <p>Résultat : <b>pas d'homologation VASP</b>, carte grise inchangée, et vous retrouvez votre véhicule normal quand vous retirez le kit. <a href="/#vasp">Pourquoi pas de VASP ?</a></p>
    </div>
  </div>
</section>
<section aria-labelledby="h-vehicule">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">2. Votre véhicule</span><h2 id="h-vehicule">Un kit fabriqué pour votre modèle</h2>
      <p>Le prix dépend de la taille du véhicule. Les versions longues des ludospaces (Berlingo XL, Kangoo Maxi…) prennent le kit van compact.</p></div>
    <table class="price-table">
      <thead><tr><th>Véhicule</th><th>Kit</th><th>Livraison en France</th></tr></thead>
      <tbody>{lignes_prix}</tbody>
    </table>
    <p class="help"><a href="/kit-amenagement/">Trouver la fiche de mon modèle</a></p>
  </div>
</section>
<section class="kits" aria-labelledby="h-finition">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">3. La finition</span><h2 id="h-finition">Pin, carrossier ou HPL</h2>
      <p>Les trois finitions ont la même structure. Elles changent l'aspect, le poids et la résistance aux taches.</p></div>
    <ul class="acc">{finitions}</ul>
  </div>
</section>
<section aria-labelledby="h-confort">
  <div class="wrap two">
    <div class="sec-head"><span class="kicker">4. Le confort</span><h2 id="h-confort">Matelas, options et accessoires</h2></div>
    <div>
      <p>Le <a href="/matelas-camper/">matelas sur mesure</a> (mousse D30, 8 cm) s'ajoute pour {MATELAS} €. À la commande, vous pouvez aussi choisir des
      <a href="/accessoires/#options">options</a> : tiroir à gauche, équerre rabattable, égouttoir, version 2+1 pour un vélo.</p>
      <p>Pour partir équipé : <a href="/occultants-isolants/">occultants isolants</a>, frigo à compresseur, batterie lithium, réchaud, douche et toilettes portables. <a href="/accessoires/">Voir les accessoires</a>.</p>
    </div>
  </div>
</section>
<section class="kits" aria-labelledby="h-montage">
  <div class="wrap two">
    <div class="sec-head"><span class="kicker">5. Le montage</span><h2 id="h-montage">Quelques minutes, sans outil</h2></div>
    <div>
      <p>{e(FIXATION)}</p>
      <p>Pour rouler, le lit se replie et le kit reste dans le coffre ; sur les ludospaces, les 5 places restent utilisables.</p>
    </div>
  </div>
</section>
<section aria-labelledby="h-commande">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">6. La commande</span><h2 id="h-commande">De la commande à la route</h2></div>
    <ol class="steps-merci">
      <li><b>Vous commandez</b> dans la <a href="/boutique/">boutique</a> : véhicule, finition, matelas, livraison ou retrait. Paiement par carte.</li>
      <li><b>Sous 48 h ouvrées</b>, nous vérifions avec vous les mesures de votre véhicule.</li>
      <li><b>Environ 3 semaines</b> de fabrication dans notre atelier, moins si votre modèle est en stock.</li>
      <li><b>Livraison</b> du kit monté sur palette en France, ou <b>retrait gratuit</b> au showroom de Nîmes.</li>
    </ol>
    <div class="ctas" style="margin-top:24px"><a class="btn btn-primary" href="/boutique/#commande">Configurer mon kit</a>
      <a class="btn btn-line" href="/contact/">Visiter le showroom</a></div>
  </div>
</section>
<section class="faq" aria-labelledby="h-faq">
  <div class="wrap faq-wrap">
    <div class="sec-head"><span class="kicker">Questions fréquentes</span><h2 id="h-faq">Kit meubles camper : en bref</h2></div>
    <div class="faq-list">
{faq_html(faq)}
    </div>
  </div>
</section>"""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": "Kit meubles camper : le guide pour aménager son van",
         "author": {"@type": "Organization", "name": "Camperizate"}, "publisher": {"@type": "Organization", "name": "Camperizate"},
         "mainEntityOfPage": f"{SITE}/guide-kit-meubles-camper/", "dateModified": date.today().isoformat()},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    return page_simple("/guide-kit-meubles-camper/", "Kit meubles camper : le guide pour aménager son van | Camperizate",
                       "Comment choisir et installer un kit meubles camper amovible : véhicule, finition, matelas, options, montage, "
                       "commande. Sans VASP, dès 500 € TTC.",
                       "Guide", "Kit meubles camper : le guide pour aménager son van",
                       "Six étapes pour comprendre le kit, choisir le bon pour votre véhicule et partir.", contenu, ld, crumb="Guide du kit camper")


def contact():
    contenu = f"""
<section class="kits" aria-labelledby="h-lieux">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Nous rendre visite</span><h2 id="h-lieux">Showroom en France, atelier en Espagne</h2></div>
    <ul class="info">
      <li><svg class="ico" aria-hidden="true"><use href="#i-pin"/></svg><div><h3>Showroom de Nîmes</h3>
        <p>Local n° 112, 866 avenue du Maréchal Juin, 30900 Nîmes.<br>Sur rendez-vous : voir les kits, essayer un matelas, retirer votre commande.</p>
        <p><a href="https://www.google.com/maps/search/?api=1&amp;query=866+avenue+du+Mar%C3%A9chal+Juin+30900+N%C3%AEmes" target="_blank" rel="noopener">Ouvrir dans Google Maps</a></p></div></li>
      <li><svg class="ico" aria-hidden="true"><use href="#i-factory"/></svg><div><h3>Atelier de fabrication</h3>
        <p>Carrer de Vulcà 1B, 08530 La Garriga (Barcelone), Espagne.<br>Sur rendez-vous.</p>
        <p><a href="https://www.google.com/maps/search/?api=1&amp;query=Carrer+de+Vulc%C3%A0+1B+08530+La+Garriga" target="_blank" rel="noopener">Ouvrir dans Google Maps</a></p></div></li>
      <li><svg class="ico" aria-hidden="true"><use href="#i-msg"/></svg><div><h3>Nous écrire</h3>
        <p>Formulaire : réponse rapide par WhatsApp.<br>Téléphone et WhatsApp : <a href="tel:+34665319287">+34 665 319 287</a><br>
        E-mail : <a href="mailto:info@camperizatetodoen1.com">info@camperizatetodoen1.com</a></p>
        <p><a class="btn btn-primary" href="{TALLY}" target="_blank" rel="noopener">Écrivez-nous</a></p></div></li>
    </ul>
  </div>
</section>"""
    ld = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": f"{SITE}/#atelier", "name": "Camperizate",
          "url": f"{SITE}/contact/", "telephone": "+34665319287", "email": "info@camperizatetodoen1.com",
          "address": {"@type": "PostalAddress", "streetAddress": "866 Avenue du Maréchal Juin, Local n° 112",
                      "postalCode": "30900", "addressLocality": "Nîmes", "addressCountry": "FR"}}
    return page_simple("/contact/", "Contact et showroom à Nîmes | Camperizate",
                       "Venez voir nos kits camper au showroom de Nîmes, 866 avenue du Maréchal Juin, sur rendez-vous, "
                       "ou écrivez-nous : réponse rapide par WhatsApp.",
                       "Contact", "Contact et showroom à Nîmes",
                       "Venez voir et essayer nos kits à Nîmes, ou posez-nous vos questions : nous répondons vite, en français.",
                       contenu, ld, crumb="Contact")


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
    <p class="help">Kit fabriqué sur mesure (sans droit de rétractation), garantie légale de 2 ans : voir nos <a href="/conditions-generales-de-vente/">conditions générales de vente</a>.</p>
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
# Landing (écrite à la main) : on ne met à jour que la liste des modèles et le sélecteur
# ---------------------------------------------------------------------------
def maj_landing():
    chemin = PUBLIC / "index.html"
    src = chemin.read_text(encoding="utf-8")
    cols = "".join(f"""
      <div>
        <h3>{e(nom)}</h3>
        <ul class="all-models">{liste_modeles(groupe)}</ul>
      </div>""" for groupe, nom, _ in GROUPES)
    bloc = f"""<!-- MODELES:debut -->
<section id="modeles" aria-labelledby="h-modeles">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Modèles compatibles</span>
      <h2 id="h-modeles">Un kit pour chaque véhicule</h2>
    </div>
    <div class="all-models-grid">{cols}
    </div>
    <p class="help"><a href="/kit-amenagement/">Voir tous les kits par modèle</a> · <a href="/guide-kit-meubles-camper/">Le guide du kit camper</a></p>
  </div>
</section>
<style>
.all-models-grid{{display:grid;gap:24px}}
.all-models-grid h3{{margin-bottom:8px}}
.all-models{{list-style:none;margin:0;padding:0;columns:2;column-gap:16px}}
.all-models li{{break-inside:avoid}}
.all-models a{{display:inline-flex;align-items:center;min-height:40px;font-size:15px;text-underline-offset:3px}}
.all-models a:hover{{color:var(--orange)}}
@media (min-width:960px){{.all-models-grid{{grid-template-columns:repeat(4,1fr)}}.all-models{{columns:1}}}}
</style>
<!-- MODELES:fin -->"""
    src = re.sub(r"<!-- MODELES:debut -->.*?<!-- MODELES:fin -->", lambda _: bloc, src, flags=re.S)
    opts = ['            <option value="">Choisir mon modèle</option>']
    for cat in ("mini", "moyen", "grand"):
        opts.append(f'            <optgroup label="{e(CATEGORIES[cat]["pluriel"])}">')
        for c, v, n, f in sorted((x for x in VEHICULES if x[0] == cat), key=lambda x: x[2]):
            opts.append(f'              <option value="{c}" data-slug="{v}" data-fiche="{f}">{e(n)}</option>')
        opts.append('            </optgroup>')
    opts.append('            <option value="autre">Autre modèle</option>')
    vehicules = "<!-- VEHICULES:debut -->\n" + "\n".join(opts) + "\n<!-- VEHICULES:fin -->"
    src = re.sub(r"<!-- VEHICULES:debut -->.*?<!-- VEHICULES:fin -->", lambda _: vehicules, src, flags=re.S)
    slugs = json.dumps([m["slug"] for m in FICHES])
    src = re.sub(r"var FICHES=\[.*?\];", lambda _: f"var FICHES={slugs};", src)
    chemin.write_text(src, encoding="utf-8")
    print("mis à jour public/index.html (modèles et sélecteur)")


# ---------------------------------------------------------------------------
# Redirections : table ancienne URL -> nouvelle, et script à coller dans Webnode
# ---------------------------------------------------------------------------
def table_redirections():
    table = {k: SITE + v for k, v in REDIRECTIONS.items()}
    for m in FICHES:
        for ancien in m["anciens"]:
            table[ancien] = f"{SITE}/kit-amenagement/{m['slug']}/"
    return dict(sorted(table.items()))


def script_webnode(table):
    exact = json.dumps(table, ensure_ascii=False, separators=(",", ":"))
    prefixes = json.dumps([[k, SITE + v] for k, v in REDIRECTIONS_PREFIXES.items()], ensure_ascii=False, separators=(",", ":"))
    return f"""<!-- Redirection camperizatetodoen1.com/fr/ -> kitamenagement.fr (généré par tools/build.py) -->
<script>
(function(){{
  var p=location.pathname;
  if(p.indexOf('/fr/')!==0&&p!=='/fr')return;
  if(p.charAt(p.length-1)!=='/')p+='/';
  var M={exact};
  var P={prefixes};
  var d=M[p];
  if(!d){{for(var i=0;i<P.length;i++){{if(p.indexOf(P[i][0])===0){{d=P[i][1];break;}}}}}}
  if(d)location.replace(d);
}})();
</script>
"""


def sitemap():
    today = date.today().isoformat()
    urls = ["/", "/kit-amenagement/", "/boutique/", "/accessoires/", "/guide-kit-meubles-camper/",
            "/occultants-isolants/", "/matelas-camper/", "/contact/"]
    urls += [f"/kit-amenagement/{m['slug']}/" for m in FICHES]
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
    ecrire("kit-amenagement/index.html", catalogue())
    ecrire("accessoires/index.html", accessoires())
    ecrire("occultants-isolants/index.html", occultants())
    ecrire("matelas-camper/index.html", matelas())
    ecrire("guide-kit-meubles-camper/index.html", guide())
    ecrire("contact/index.html", contact())
    ecrire("sitemap.xml", sitemap())
    maj_landing()
    table = table_redirections()
    (ROOT / "tools" / "redirections.json").write_text(json.dumps(table, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "docs" / "redirection-webnode.html").write_text(script_webnode(table), encoding="utf-8")
    print(f"redirections : {len(table)} URL exactes + {len(REDIRECTIONS_PREFIXES)} préfixes")
    vides = [k for k, v in STRIPE.items() if not v]
    print(f"liens Stripe manquants : {len(vides)}/{len(STRIPE)}")


if __name__ == "__main__":
    main()
