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
    # Kits ludospace
    "kit-mini-pin-sans": "",
    "kit-mini-pin-avec": "",
    "kit-mini-carrossier-sans": "",
    "kit-mini-carrossier-avec": "",
    "kit-mini-hpl-sans": "",
    "kit-mini-hpl-avec": "",
    # Kits van compact
    "kit-moyen-pin-sans": "",
    "kit-moyen-pin-avec": "",
    "kit-moyen-carrossier-sans": "",
    "kit-moyen-carrossier-avec": "",
    "kit-moyen-hpl-sans": "",
    "kit-moyen-hpl-avec": "",
    # Accessoires
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
FICHES = [
    {
        "slug": "dacia-jogger-lodgy",
        "ancien": "/fr/kit-camperizacion/dacia-jogger-lodgy/",
        "nom": "Dacia Jogger et Lodgy",
        "court": "Jogger",
        "categorie": "mini",
        "image": ("/img/kit-carrossier-lit.webp", "Kit camper amovible en phénolique carrossier, lit déplié dans un ludospace", 900, 900),
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
]

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
        <a class="link" href="/boutique/">Boutique</a>
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
    if(!c||c==='grand'){return;}
    var fin=val('fin'),mat=val('mat');
    var total=D.prix[c][fin]+(mat==='avec'?D.matelas:0);
    cat.textContent='Kit '+D.cat[c].toLowerCase()+' · '+o.text;
    sum.textContent=fmt(total)+' TTC';
    ship.textContent='Retrait gratuit au showroom de Nîmes ou livraison montée en France dès '+D.livraison[c]+' €, à choisir au paiement.';
    var link=D.liens['kit-'+c+'-'+fin+'-'+mat];
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
    <p class="lead">Choisissez votre véhicule, la finition et le matelas. Paiement sécurisé par carte, fabrication en 3 semaines environ.</p>
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
        <div class="total" aria-live="polite">
          <p class="r-cat" id="r-cat"></p>
          <p class="sum" id="sum"></p>
          <p class="ship" id="ship"></p>
          <a class="btn btn-primary" id="pay" href="{TALLY}">Commander</a>
          <a class="btn btn-line" href="{TALLY}" target="_blank" rel="noopener">Une question avant de commander ?</a>
          <div class="opts">Options à ajouter sur la page de paiement :<ul>{options}</ul></div>
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
      <p>Livrés avec votre kit ou à retirer au showroom.</p>
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
def fiche(m):
    url = f"{SITE}/kit-amenagement/{m['slug']}/"
    cat = m["categorie"]
    c = CATEGORIES[cat]
    bas, haut = prix(cat, "pin", False), prix(cat, "hpl", True)
    titre = f"Kit aménagement {m['nom']} amovible | Camperizate"
    desc = (f"Kit camper amovible pour {m['nom']} : lit, cuisine et rangements posés en 5 min, "
            f"sans perçage ni VASP. Dès {bas} € TTC, showroom à Nîmes.")
    img, alt, w, h = m["image"]
    faq = m["faq"] + FAQ_COMMUNE
    commande = f"/boutique/?modele={m['slug']}#commande"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": f"Kit d'aménagement amovible {m['nom']}", "description": desc, "image": SITE + img,
         "brand": {"@type": "Brand", "name": "Camperizate"},
         "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": str(bas), "highPrice": str(haut),
                    "offerCount": str(len(FINITIONS) * 2), "availability": "https://schema.org/InStock"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": c["pluriel"], "item": SITE + "/#kits"},
            {"@type": "ListItem", "position": 3, "name": m["nom"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    mesures = "\n".join(f'          <tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in m["mesures"])
    inclus = "\n".join(
        f'        <li><svg class="ico" aria-hidden="true"><use href="#{i}"/></svg><span><b>{e(t)}</b>{e(d)}</span></li>'
        for i, t, d in m["inclus"])
    lignes = "\n".join(
        f"          <tr><td>{e(n)}<small>{e(d)}</small></td><td><b>{p[cat]} €</b></td><td><b>{p[cat] + MATELAS} €</b></td></tr>"
        for _, n, d, p in FINITIONS)
    videos = "\n".join(
        f'      <button type="button" class="yt" data-id="{v}" aria-label="Lire la vidéo : {e(t)}">'
        f'<img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy">'
        f'<span>▶ {e(t)}</span></button>' for v, t in m["videos"])
    faq_html = "\n".join(
        f'      <details><summary>{e(q)}<svg class="ico" aria-hidden="true"><use href="#i-down"/></svg></summary>'
        f'<div class="a"><p>{e(a)}</p></div></details>' for q, a in faq)
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
    body = f"""
<main id="top">
<nav class="crumbs wrap" aria-label="Fil d'Ariane">
  <ol><li><a href="/">Accueil</a></li><li><a href="/#kits">{e(c['pluriel'])}</a></li><li aria-current="page">{e(m['nom'])}</li></ol>
</nav>

<section class="fiche-hero" aria-labelledby="h1">
  <div class="wrap fiche-grid">
    <div class="pic"><img src="{img}" alt="{e(alt)}" width="{w}" height="{h}" fetchpriority="high"></div>
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
</section>

<section id="prix" class="kits" aria-labelledby="h-prix">
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
</section>

<section aria-labelledby="h-videos">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">En vidéo</span><h2 id="h-videos">Le kit {e(m['court'])} en situation</h2></div>
    <div class="videos">
{videos}
    </div>
  </div>
</section>

<section class="showroom" aria-labelledby="h-showroom">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Showroom</span><h2 id="h-showroom">Venez voir le kit à Nîmes</h2></div>
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
</main>
"""
    return head(titre, desc, url, ld, og_type="product") + header("#prix", "Voir les prix") + body + footer(script)


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
    <p class="lead">Votre paiement est confirmé et vous allez recevoir un reçu par e-mail. Nous vous contactons sous 48 h pour vérifier les mesures de votre véhicule et fixer la livraison ou le retrait à Nîmes.</p>
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


def sitemap():
    today = date.today().isoformat()
    urls = ["/", "/boutique/"] + [f"/kit-amenagement/{m['slug']}/" for m in FICHES]
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
    table = {m["ancien"]: f"{SITE}/kit-amenagement/{m['slug']}/" for m in FICHES}
    (ROOT / "tools" / "redirections.json").write_text(json.dumps(table, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    vides = [k for k, v in STRIPE.items() if not v]
    print(f"liens Stripe manquants : {len(vides)}/{len(STRIPE)}")


if __name__ == "__main__":
    main()
