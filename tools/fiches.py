#!/usr/bin/env python3
"""Génère les fiches modèle de kitamenagement.fr.

Usage :  python3 tools/fiches.py
Écrit public/kit-amenagement/<slug>/index.html pour chaque modèle de MODELES
et régénère public/sitemap.xml. Le CSS est repris de public/index.html pour
garder une seule source de style.

Pour ajouter un modèle : copier un bloc de MODELES, adapter les données,
relancer le script. Chaque fiche correspond à une ancienne page
camperizatetodoen1.com/fr/kit-camperizacion/<ancien>/ (champ "ancien"),
ce qui sert ensuite à la table de redirection.
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
UTM = "utm_source=kitamenagement.fr&utm_medium=fiche&utm_campaign=fr_sans_vasp"

# Prix TTC par catégorie : (finition, description, sans matelas, avec matelas)
PRIX = {
    "ludospace": [
        ("Phénolique pin", "Bois naturel, chaleureux, vernissable.", 500, 650),
        ("Phénolique carrossier", "Noir, repousse l'eau et les taches.", 550, 700),
        ("HPL de peuplier", "Léger, ultra-résistant. Blanc ou anthracite.", 800, 950),
    ],
    "van": [
        ("Phénolique pin", "Bois naturel, chaleureux, vernissable.", 700, 850),
        ("Phénolique carrossier", "Noir, repousse l'eau et les taches.", 750, 900),
        ("HPL de peuplier", "Léger, ultra-résistant. Blanc ou anthracite.", 1000, 1150),
    ],
}
CATEGORIE = {
    "ludospace": ("Kits ludospace", "livraison dès 200 € en France"),
    "van": ("Kits van compact", "livraison dès 250 € en France"),
}

MODELES = [
    {
        "slug": "dacia-jogger-lodgy",
        "ancien": "/fr/kit-camperizacion/dacia-jogger-lodgy/",
        "nom": "Dacia Jogger et Lodgy",
        "court": "Jogger",
        "categorie": "ludospace",
        "commande": "https://www.camperizatetodoen1.com/p/kit-mueble-camper-dacia-jogger-lodgy/",
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

EXTRA_CSS = """
.crumbs{font-size:14px;color:var(--brown-70);padding-top:14px}
.crumbs ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.crumbs li+li::before{content:"›";margin-right:6px}
.crumbs a{text-decoration:none}.crumbs a:hover{color:var(--orange)}
.fiche-hero{padding:20px 0 44px}
.fiche-hero .pic{aspect-ratio:4/3;background:var(--sand);border-radius:var(--r);overflow:hidden}
.fiche-hero .pic img{width:100%;height:100%;object-fit:cover}
.fiche-hero .kicker{margin-top:18px}
.fiche-hero h1{margin:0 0 12px}
.fiche-hero .lead{font-size:18px;color:var(--brown-70);margin-bottom:18px}
.ctas{display:grid;gap:12px}
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
@media (min-width:640px){.videos{grid-template-columns:1fr 1fr}}
@media (min-width:960px){
  .fiche-grid{display:grid;grid-template-columns:1fr 1.15fr;gap:48px;align-items:start}
  .fiche-grid .pic{order:2}
  .fiche-hero .kicker{margin-top:0}
  .ctas{display:flex;flex-wrap:wrap}
  .ctas .btn{width:auto;min-width:220px}
  .two{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
}
"""

e = html.escape


def css_base():
    src = (PUBLIC / "index.html").read_text(encoding="utf-8")
    return re.search(r"<style>(.*?)</style>", src, re.S).group(1)


def icones():
    src = (PUBLIC / "index.html").read_text(encoding="utf-8")
    return re.search(r'(<svg width="0" height="0".*?</svg>)', src, re.S).group(1)


def avec_utm(url):
    return url + ("&" if "?" in url else "?") + UTM


def page(m):
    url = f"{SITE}/kit-amenagement/{m['slug']}/"
    cat_nom, livraison = CATEGORIE[m["categorie"]]
    prix = PRIX[m["categorie"]]
    bas = min(p[2] for p in prix)
    haut = max(p[3] for p in prix)
    titre = f"Kit aménagement {m['nom']} amovible | Camperizate"
    desc = (f"Kit camper amovible pour {m['nom']} : lit, cuisine et rangements posés en 5 min, "
            f"sans perçage ni VASP. Dès {bas} € TTC, showroom à Nîmes.")
    img, alt, w, h = m["image"]
    faq = m["faq"] + FAQ_COMMUNE
    commande = avec_utm(m["commande"])

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Product", "name": f"Kit d'aménagement amovible {m['nom']}",
             "description": desc, "image": SITE + img,
             "brand": {"@type": "Brand", "name": "Camperizate"},
             "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": str(bas),
                        "highPrice": str(haut), "offerCount": str(len(prix) * 2),
                        "availability": "https://schema.org/InStock"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": cat_nom, "item": SITE + "/#kits"},
                {"@type": "ListItem", "position": 3, "name": m["nom"], "item": url}]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        ],
    }

    mesures = "\n".join(f"          <tr><th scope=\"row\">{e(k)}</th><td>{e(v)}</td></tr>" for k, v in m["mesures"])
    inclus = "\n".join(
        f'        <li><svg class="ico" aria-hidden="true"><use href="#{i}"/></svg><span><b>{e(t)}</b>{e(d)}</span></li>'
        for i, t, d in m["inclus"])
    lignes_prix = "\n".join(
        f"          <tr><td>{e(f)}<small>{e(d)}</small></td><td><b>{a} €</b></td><td><b>{b} €</b></td></tr>"
        for f, d, a, b in prix)
    videos = "\n".join(
        f'      <button type="button" class="yt" data-id="{vid}" aria-label="Lire la vidéo : {e(t)}">'
        f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy">'
        f'<span>▶ {e(t)}</span></button>'
        for vid, t in m["videos"])
    faq_html = "\n".join(
        f'      <details><summary>{e(q)}<svg class="ico" aria-hidden="true"><use href="#i-down"/></svg></summary>'
        f'<div class="a"><p>{e(a)}</p></div></details>'
        for q, a in faq)

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titre)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#513524">
<meta property="og:type" content="product">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Camperizate">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(f"Kit aménagement {m['nom']} : sans VASP, dès {bas} €")}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}/img/og-kitamenagement.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/fonts/bricolage-grotesque-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23513524'/%3E%3Cg stroke='%23fff' stroke-width='7' fill='none'%3E%3Cpath d='M32 10v26M14 20l16 16M50 20 34 36'/%3E%3C/g%3E%3Cpath d='M10 46h14a8 8 0 0 1 16 0h14v6H10z' fill='%23fff'/%3E%3C/svg%3E">
<style>{css_base()}{EXTRA_CSS}</style>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>

{icones()}

<header class="site-head">
  <div class="wrap">
    <a href="/" class="brand" aria-label="Camperizate, accueil"><img src="/img/camperizate-logo.svg" alt="Camperizate" width="172" height="23"></a>
    <a href="#prix" class="btn btn-line head-btn">Voir les prix</a>
  </div>
</header>

<main id="top">

<nav class="crumbs wrap" aria-label="Fil d'Ariane">
  <ol><li><a href="/">Accueil</a></li><li><a href="/#kits">{e(cat_nom)}</a></li><li aria-current="page">{e(m['nom'])}</li></ol>
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
        <a href="{e(commande)}" class="btn btn-primary">Commander ce kit <svg class="ico" aria-hidden="true"><use href="#i-right"/></svg></a>
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
    <div class="sec-head">
      <span class="kicker">Le kit {e(m['court'])}</span>
      <h2 id="h-kit">Ce que comprend le kit</h2>
    </div>
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
    <table class="specs">
      <tbody>
{mesures}
      </tbody>
    </table>
  </div>
</section>

<section id="prix" class="kits" aria-labelledby="h-prix">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Prix</span>
      <h2 id="h-prix">Trois finitions, un prix atelier</h2>
      <p>Prix TTC, hors livraison ({e(livraison)}).</p>
    </div>
    <table class="price-table">
      <thead><tr><th>Finition</th><th>Sans matelas</th><th>Avec matelas</th></tr></thead>
      <tbody>
{lignes_prix}
      </tbody>
    </table>
    <p class="help">Options et accessoires (occultants, frigo, batterie, version 2+1…) : <a href="/#kits">voir la liste complète</a>.</p>
    <a href="{e(commande)}" class="btn btn-primary" style="margin-top:20px;max-width:420px">Commander ce kit <svg class="ico" aria-hidden="true"><use href="#i-right"/></svg></a>
  </div>
</section>

<section aria-labelledby="h-videos">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">En vidéo</span>
      <h2 id="h-videos">Le kit {e(m['court'])} en situation</h2>
    </div>
    <div class="videos">
{videos}
    </div>
  </div>
</section>

<section class="showroom" aria-labelledby="h-showroom">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Showroom</span>
      <h2 id="h-showroom">Venez voir le kit à Nîmes</h2>
    </div>
    <address>Local n° 112, 866 avenue du Maréchal Juin<br>30900 Nîmes</address>
    <a href="{TALLY}" class="btn btn-line" style="max-width:420px" target="_blank" rel="noopener">Prévenir de ma visite</a>
  </div>
</section>

<section class="faq" aria-labelledby="h-faq">
  <div class="wrap faq-wrap">
    <div class="sec-head">
      <span class="kicker">Questions fréquentes</span>
      <h2 id="h-faq">Kit {e(m['court'])} : en bref</h2>
    </div>
    <div class="faq-list">
{faq_html}
    </div>
  </div>
</section>

</main>

<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img src="/img/camperizate-logo-white.svg" alt="Camperizate" width="160" height="21" loading="lazy">
        <p>Kits camper amovibles pour ludospaces et vans, fabriqués dans notre atelier.</p>
        <a class="link" href="/">Tous nos kits</a>
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
      <a href="/mentions-legales/">Mentions légales</a><a href="/politique-de-confidentialite/">Politique de confidentialité</a>
    </div>
  </div>
</footer>

<script>
document.querySelectorAll('.yt').forEach(function(b){{
  b.addEventListener('click',function(){{
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.id+'?autoplay=1&rel=0';
    f.title=b.getAttribute('aria-label');
    f.allow='autoplay; encrypted-media; picture-in-picture';
    f.allowFullscreen=true;
    var d=document.createElement('div');d.className='yt';d.appendChild(f);
    b.replaceWith(d);
  }});
}});
</script>
</body>
</html>
"""


def sitemap():
    today = date.today().isoformat()
    urls = ["/", "/mentions-legales/", "/politique-de-confidentialite/"]
    urls += [f"/kit-amenagement/{m['slug']}/" for m in MODELES]
    rows = "\n".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n'


def main():
    for m in MODELES:
        out = PUBLIC / "kit-amenagement" / m["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(m), encoding="utf-8")
        print("écrit", out.relative_to(ROOT))
    (PUBLIC / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("écrit public/sitemap.xml")
    # Table de redirection pour le script Webnode (ancienne URL → nouvelle)
    table = {m["ancien"]: f"{SITE}/kit-amenagement/{m['slug']}/" for m in MODELES}
    (ROOT / "tools" / "redirections.json").write_text(json.dumps(table, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("écrit tools/redirections.json")


if __name__ == "__main__":
    main()
