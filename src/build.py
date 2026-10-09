"""Genera la web estática de Lifes Campers en ../web.

Uso:  python3 src/build.py
Todo el contenido está en este archivo y en src/content_furgonetas.py.
Las fotos originales están en src/fotos/ (nombre del archivo = nombre en la web).
"""
import html
import json
import os
import shutil
from datetime import date

from PIL import Image

from content_furgonetas import FURGONETAS

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(ROOT), "web")
SITE = "https://camperizacionmalaga.com"
BRAND = "Lifes Campers"
TEL1, TEL2 = "637 37 22 96", "637 31 32 52"
WA_NUM = "34637372296"
EMAIL = "info@lifescampers.com"
ADDRESS = "Carril de la Serrería, 7 · 29004 San Julián, Málaga"
INSTAGRAM = "https://www.instagram.com/malagalifescampers/"
FACEBOOK = "https://www.facebook.com/p/Lifes-Campers-M%C3%A1laga-100063913059162/"
MAPS = "https://www.google.com/maps/search/?api=1&query=Lifes+Campers+M%C3%A1laga"
WEB3FORMS_KEY = "71767edc-8025-4398-8918-90c888817feb"
PRICE = "24.900 €"
TODAY = date.today().isoformat()

esc = html.escape


def wa(text="Hola, me gustaría información sobre una camperización."):
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUM}?text={quote(text)}"


# --------------------------------------------------------------------------- fotos
ALT = {
    "furgoneta-camper-playa": "Furgoneta camper de Lifes Campers aparcada en una playa de Málaga",
    "desayuno-camper-mar": "Desayuno sobre la tabla de cortar de una camper con vistas al mar",
    "interior-camper-cama-cocina-azulejo-verde": "Interior de camper con cama trasera, cocina con azulejo verde y techo de madera",
    "cocina-camper-azulejo-escamas": "Cocina de camper con azulejo de escamas verde, encimera de madera y nevera",
    "cocina-camper-horno-vistas-mar": "Cocina de camper con horno y fogón junto a la puerta abierta al mar",
    "dinette-camper-madera-macrame": "Dinette de camper con mesa de madera, armarios blancos y detalles de macramé",
    "ducha-camper-azulejo-blanco": "Ducha de camper con azulejo blanco y grifería negra",
    "encimera-madera-camper-taza": "Encimera de madera barnizada con azulejo verde y taza de Lifes Campers",
    "encimera-barnizada-camper": "Encimera de madera barnizada de una camper vista desde la cabina",
    "camper-puerta-lateral-dinette": "Camper vista desde la puerta lateral con dinette, mesa y cocina",
    "interior-camper-madera-clara": "Interior de camper en madera clara con armarios altos y ventanas",
    "salon-camper-sofa-claraboya": "Salón de camper con sofá, claraboya y luces en el techo",
    "cocina-camper-fogon-gas": "Cocina de camper con fogón de gas, fregadero y mesa abatible",
    "camper-puertas-traseras-cama": "Camper abierta por las puertas traseras con la cama y el interior iluminado",
    "cocina-camper-fregadero-nevera": "Cocina de camper con fregadero, fogón y nevera de compresor",
    "camper-cama-trasera-garaje": "Puertas traseras de camper con cama elevada y garaje debajo",
    "camper-puerta-lateral-mesa": "Camper con la puerta lateral abierta y mesa exterior",
    "camper-literas-dinette": "Camper con cama elevable sobre la dinette y asientos tapizados",
    "cocina-camper-horno-madera": "Cocina de camper con horno, encimera de madera y suelo de madera",
    "cocina-camper-grifo-industrial": "Cocina de camper con fregadero, fogón y grifo de muelle",
    "camper-cama-elevable-dinette": "Cama elevable sobre la dinette de una camper con techo de madera",
    "cocina-camper-encimera-placa": "Cocina de camper con encimera de madera y placa vitrocerámica",
    "bano-camper-ducha-wc": "Baño de camper con ducha y WC",
    "dinette-camper-tapizado-claro": "Dinette de camper con dos bancos tapizados y mesa central",
    "cocina-camper-azulejo-armarios": "Cocina de camper con azulejo de escamas, cajones y mesa abatible",
    "camper-techo-elevable": "Furgoneta camper con techo elevable abierto",
    "interior-camper-gris-claraboya": "Interior de camper en gris con claraboya y suelo vinílico",
    "cocina-camper-tapa-madera": "Mueble de cocina de camper con tapa de madera",
    "cocina-camper-fogon-dos-fuegos": "Fogón de dos fuegos en la cocina de una camper",
    "camper-ruedas-todoterreno": "Furgoneta camper con ruedas todoterreno",
    "peugeot-boxer-camper-frontal": "Peugeot Boxer camperizada vista de frente",
    "peugeot-boxer-camper-trasera": "Peugeot Boxer camperizada vista desde atrás",
    "camper-cama-matrimonio-boxer": "Cama de matrimonio transversal en una Peugeot Boxer camperizada",
    "cocina-camper-boxer-azulejo": "Cocina de una Peugeot Boxer camperizada con azulejo y televisión",
    "camper-boxer-vista-interior": "Vista interior de una Peugeot Boxer camperizada desde la cama",
    "camper-boxer-sofa-mesa": "Sofá y mesa auxiliar en una Peugeot Boxer camperizada",
    "camper-boxer-suelo-madera": "Suelo y mobiliario de madera en una Peugeot Boxer camperizada",
    "camper-boxer-claraboya-tv": "Claraboya con luz LED y televisión en una Peugeot Boxer camperizada",
    "interior-camper-madera-oscura": "Interior de camper con encimera de madera oscura y azulejo decorativo",
    "interior-camper-cocina-madera-dinette": "Interior de camper con cocina de madera, dinette y cama al fondo",
    "salon-camper-mesa-asientos-azules": "Salón de camper con asientos azules y mesa",
    "cocina-camper-madera-tapa-abierta": "Cocina de camper con tapa de madera abierta, fogón y fregadero",
    "cama-camper-transversal": "Cama transversal de matrimonio en una camper con claraboya",
    "camper-salon-cama-claraboyas": "Salón y cama de una camper con dos claraboyas",
    "cocina-camper-horno-encimera-nogal": "Cocina de camper con horno y encimera de madera oscura",
    "iveco-daily-camper-negra": "Iveco Daily negra camperizada a la salida del taller",
    "iveco-daily-camper-puerta-lateral": "Iveco Daily camperizada con la puerta lateral abierta",
    "iveco-daily-camper-cama-trasera": "Cama trasera y garaje de una Iveco Daily camperizada",
    "iveco-daily-camper-cocina-induccion": "Cocina con placa de inducción en una Iveco Daily camperizada",
    "iveco-daily-camper-interior-cocina": "Interior de una Iveco Daily camperizada con cocina y armario",
    "iveco-daily-camper-dinette": "Dinette con mesa y cortinas en una Iveco Daily camperizada",
    "iveco-daily-camper-salon-mesa": "Salón con mesa junto a la cabina en una Iveco Daily camperizada",
    "pedro-y-jose-lifes-campers": "Pedro y José, fundadores de Lifes Campers, en el taller de Málaga",
    "taller-lifes-campers-malaga": "Fachada del taller de Lifes Campers en San Julián, Málaga, con furgonetas camper",
    "taller-lifes-campers-fachada": "Furgoneta camper frente al taller de Lifes Campers en Málaga",
    "entrega-camper-clientes": "Entrega de una camper a sus clientes en el taller de Lifes Campers",
    "entrega-iveco-daily-clientes": "Entrega de una Iveco Daily camperizada a sus clientes",
}

PROJECTS = [
    ("Iveco Daily negra", "Camperización integral sobre Iveco Daily: cama trasera con garaje, cocina con inducción, dinette y armario.",
     ["iveco-daily-camper-negra", "iveco-daily-camper-puerta-lateral", "iveco-daily-camper-salon-mesa", "iveco-daily-camper-interior-cocina",
      "iveco-daily-camper-cocina-induccion", "iveco-daily-camper-dinette", "iveco-daily-camper-cama-trasera", "entrega-iveco-daily-clientes"]),
    ("Madera oscura y cama transversal", "Encimeras de madera oscura, horno, salón con asientos azules y cama transversal bajo dos claraboyas.",
     ["interior-camper-cocina-madera-dinette", "salon-camper-mesa-asientos-azules", "cocina-camper-madera-tapa-abierta", "cama-camper-transversal",
      "camper-salon-cama-claraboyas", "cocina-camper-horno-encimera-nogal", "interior-camper-madera-oscura", "entrega-camper-clientes"]),
    ("Peugeot Boxer 2023", "Boxer con cama de matrimonio transversal, cocina con azulejo, sofá, claraboya y suelo de madera.",
     ["peugeot-boxer-camper-frontal", "peugeot-boxer-camper-trasera", "camper-cama-matrimonio-boxer", "cocina-camper-boxer-azulejo",
      "camper-boxer-vista-interior", "camper-boxer-sofa-mesa", "camper-boxer-claraboya-tv", "camper-boxer-suelo-madera"]),
    ("Azulejo verde y madera natural", "Cocina con azulejo de escamas, horno, ducha, dinette y techo de madera.",
     ["interior-camper-cama-cocina-azulejo-verde", "cocina-camper-azulejo-escamas", "cocina-camper-horno-vistas-mar", "dinette-camper-madera-macrame",
      "ducha-camper-azulejo-blanco", "encimera-madera-camper-taza", "encimera-barnizada-camper", "desayuno-camper-mar"]),
    ("Madera clara y salón amplio", "Interior luminoso en madera clara, salón con sofá y cocina completa.",
     ["camper-puerta-lateral-dinette", "interior-camper-madera-clara", "salon-camper-sofa-claraboya", "cocina-camper-fogon-gas",
      "camper-puertas-traseras-cama", "cocina-camper-fregadero-nevera", "furgoneta-camper-playa", "taller-lifes-campers-fachada"]),
    ("Cama elevable y dinette para cuatro", "Cama elevable sobre la dinette, garaje trasero y cocina con horno.",
     ["camper-cama-trasera-garaje", "camper-puerta-lateral-mesa", "camper-literas-dinette", "camper-cama-elevable-dinette",
      "cocina-camper-horno-madera", "cocina-camper-grifo-industrial"]),
    ("Baño completo y cocina con vitrocerámica", "Baño con ducha y WC, dinette tapizada y cocina con azulejo.",
     ["cocina-camper-encimera-placa", "bano-camper-ducha-wc", "dinette-camper-tapizado-claro", "cocina-camper-azulejo-armarios"]),
    ("Techo elevable y equipamiento off-road", "Camper con techo elevable, interior en gris y ruedas todoterreno.",
     ["camper-techo-elevable", "camper-ruedas-todoterreno", "interior-camper-gris-claraboya", "cocina-camper-tapa-madera", "cocina-camper-fogon-dos-fuegos"]),
]


def build_images():
    src = os.path.join(ROOT, "fotos")
    dst = os.path.join(OUT, "img")
    os.makedirs(dst, exist_ok=True)
    for f in sorted(os.listdir(src)):
        slug = f.rsplit(".", 1)[0]
        assert slug in ALT, f"Falta el texto alternativo (ALT) de {f}"
        im = Image.open(os.path.join(src, f))
        im.load()
        for w in (1200, 600):
            out = os.path.join(dst, f"{slug}-{w}.webp")
            if os.path.exists(out):
                continue
            c = im.copy()
            c.thumbnail((w, w), Image.LANCZOS)
            c.save(out, "WEBP", quality=78, method=6)
    # logo y favicons
    logo = Image.open(os.path.join(ROOT, "assets", "logo-src.webp")).convert("RGBA")
    for s in (88, 180, 32):
        c = logo.copy()
        c.thumbnail((s, s), Image.LANCZOS)
        if s == 180:
            bg = Image.new("RGBA", c.size, (255, 253, 249, 255))
            bg.alpha_composite(c)
            bg.convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"))
        elif s == 32:
            c.save(os.path.join(OUT, "favicon.png"))
        else:
            c.save(os.path.join(dst, "logo-lifes-campers.png"), optimize=True)
    # imagen para compartir en redes (1200x630)
    og = Image.open(os.path.join(src, "interior-camper-cocina-madera-dinette.webp")).convert("RGB")
    w, h = og.size
    og = og.crop((0, (h - int(w * 630 / 1200)) // 2, w, (h + int(w * 630 / 1200)) // 2)).resize((1200, 630), Image.LANCZOS)
    og.save(os.path.join(dst, "og-lifes-campers.jpg"), quality=82)


def pic(slug, cls="", sizes="(max-width: 760px) 100vw, 50vw", eager=False):
    a = esc(ALT[slug])
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img src="/img/{slug}-1200.webp" srcset="/img/{slug}-600.webp 600w, /img/{slug}-1200.webp 1200w" '
            f'sizes="{sizes}" width="1200" height="1200" alt="{a}" {load}{c}>')


def thumb_link(slug, group, cls=""):
    a = esc(ALT[slug])
    c = f' class="{cls}"' if cls else ""
    return (f'<a href="/img/{slug}-1200.webp" data-lb="{group}"{c}><img src="/img/{slug}-600.webp" width="600" height="600" '
            f'alt="{a}" loading="lazy" decoding="async"></a>')


# --------------------------------------------------------------------------- layout
WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4C2.7 15.6 2.2 13.8 2.2 12 2.2 6.6 6.6 2.2 12 2.2c2.6 0 5.1 1 6.9 2.9 1.8 1.8 2.9 4.3 2.9 6.9 0 5.4-4.4 9.8-9.8 9.8zm8.4-18.2C18.1 1.3 15.2.1 12 .1 5.5.1.1 5.4.1 12c0 2.1.5 4.1 1.6 5.9L0 24l6.3-1.7c1.7.9 3.7 1.4 5.7 1.4 6.6 0 11.9-5.3 11.9-11.9 0-3.2-1.2-6.2-3.5-8.4z"/></svg>')

NAV = [("/camperizacion-integral/", "Camperización integral"), ("/furgonetas/", "Furgonetas"),
       ("/trabajos/", "Trabajos"), ("/contacto/", "Contacto")]

BUSINESS = {
    "@type": "AutomotiveBusiness",
    "@id": SITE + "/#negocio",
    "name": BRAND,
    "description": "Taller de camperización integral de furgonetas grandes en Málaga: diseño a medida, mobiliario, electricidad solar, agua, homologación y garantía.",
    "url": SITE + "/",
    "logo": SITE + "/img/logo-lifes-campers.png",
    "image": SITE + "/img/og-lifes-campers.jpg",
    "telephone": "+34 637 37 22 96",
    "email": EMAIL,
    "priceRange": "€€€",
    "address": {"@type": "PostalAddress", "streetAddress": "Carril de la Serrería, 7", "addressLocality": "Málaga",
                "postalCode": "29004", "addressRegion": "Málaga", "addressCountry": "ES"},
    "areaServed": [{"@type": "State", "name": "Andalucía"}, {"@type": "Country", "name": "España"}],
    "sameAs": [INSTAGRAM, FACEBOOK],
}


def layout(path, title, desc, body, schema=None, active=None, og_img=None):
    url = SITE + path
    nav = "".join(
        f'<a href="{h}"{" aria-current=page" if active == h else ""}>{esc(t)}</a>' for h, t in NAV)
    graph = [BUSINESS, {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc,
                        "inLanguage": "es-ES", "isPartOf": {"@type": "WebSite", "url": SITE + "/", "name": BRAND},
                        "about": {"@id": SITE + "/#negocio"}}]
    graph += schema or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    og = og_img or SITE + "/img/og-lifes-campers.jpg"
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#fffdf9">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/spectral-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/hanken-grotesk-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="{BRAND}, inicio"><img src="/img/logo-lifes-campers.png" width="44" height="44" alt=""><span>Lifes Campers</span></a>
    <button class="menu-btn" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
    <nav class="nav" id="nav" aria-label="Principal">{nav}<a class="btn btn-wa" href="{wa()}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <p style="font-family:var(--serif);font-size:1.5rem;color:#fff;margin:0 0 8px">Lifes Campers</p>
        <p>Camperizaciones integrales a medida en Málaga. Furgonetas grandes, materiales que duran, homologación y garantía.</p>
      </div>
      <div>
        <h4>Contacto</h4>
        <ul>
          <li><a href="tel:+34637372296">{TEL1}</a></li>
          <li><a href="tel:+34637313252">{TEL2}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{MAPS}" target="_blank" rel="noopener">{esc(ADDRESS)}</a></li>
        </ul>
      </div>
      <div>
        <h4>Furgonetas</h4>
        <ul>{"".join(f'<li><a href="/furgonetas/{v["slug"]}/">{esc(v["name"])}</a></li>' for v in FURGONETAS)}</ul>
      </div>
      <div>
        <h4>Síguenos</h4>
        <ul>
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a></li>
        </ul>
        <h4 style="margin-top:24px">Legal</h4>
        <ul>
          <li><a href="/aviso-legal/">Aviso legal</a></li>
          <li><a href="/politica-de-privacidad/">Privacidad</a></li>
          <li><a href="/politica-de-cookies/">Cookies</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom"><span>© {date.today().year} Lifes Campers · CROSSCAMPERS, S.L.</span><span>Camperización de furgonetas en Málaga</span></div>
  </div>
</footer>
<a class="wa-float" href="{wa()}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{WA_SVG}</a>
<script src="/assets/main.js" defer></script>
</body>
</html>
"""


def crumbs(items):
    """items: [(nombre, ruta)] sin incluir Inicio. Devuelve (html, schema)."""
    full = [("Inicio", "/")] + items
    h = " / ".join(f'<a href="{p}">{esc(n)}</a>' if i < len(full) - 1 else esc(n) for i, (n, p) in enumerate(full))
    sc = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(full)]}
    return f'<nav class="crumbs" aria-label="Migas de pan">{h}</nav>', sc


def faq_block(faqs):
    h = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in faqs)
    sc = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    return f'<div class="faq">{h}</div>', sc


def cta(title="¿Damos el siguiente paso?",
        text="Cuéntanos qué furgoneta tienes (o cuál buscas) y cómo viajas. Te respondemos por WhatsApp y diseñamos tu camper contigo."):
    return f"""<section class="section"><div class="wrap"><div class="cta">
<div><h2>{esc(title)}</h2><p>{esc(text)}</p></div>
<a class="btn btn-wa" href="{wa()}" target="_blank" rel="noopener">{WA_SVG}Escríbenos por WhatsApp</a>
</div></div></section>"""


# --------------------------------------------------------------------------- contenido común
SPECS = [
    ("Aislamiento y panelado", ["Doble aislamiento de la furgoneta completa: Kaiflex de 20 mm en paneles y 10 mm en los nervios.",
                                "Panelado de friso blanco en techos y paredes; puertas en friso de pino.",
                                "Suelo de tablero de chopo marino de 15 mm con parquet AC5."]),
    ("Mobiliario", ["Mobiliario completo en HPL marino, resistente a la humedad y al uso diario.",
                    "Mesa con fijación a la pared, mesa exterior y mesa pequeña abatible."]),
    ("Energía y electricidad", ["2 baterías de litio de 100 Ah cada una (200 Ah de autonomía total).",
                                "Placa solar de perfil alto de 400 W NDS con regulador MPPT.",
                                "Inversor + cargador de 1000 W de onda pura.",
                                "Centralita de control CBE PC180.",
                                "Varios enchufes de 12 V, toma exterior de 230 V y múltiples puntos de iluminación."]),
    ("Agua", ["Depósito de aguas limpias de 200 l con bomba a presión Shurflo.",
              "Termo de gas para agua caliente Whale / Webasto.",
              "Ducha exterior con agua caliente y fría."]),
    ("Cocina", ["Bloque de cocina con fregadero y hornilla de 2 fuegos Dometic.",
                "Nevera de compresor Webasto Isotherm de 115 l."]),
    ("Baño", ["Cabina de baño con puerta de carpintería, plato de ducha y grifo.",
              "Claraboya de ventilación Turbovent en el baño."]),
    ("Ventilación, luz y ventanas", ["2 claraboyas Dometic: una en el salón y otra en el dormitorio.",
                                     "2 ventanas de cristal con apertura corredera, oscurecedores y cortinas."]),
    ("Descanso y climatización", ["1 o 2 camas de matrimonio completas de 135 × 185 cm.",
                                  "Calefacción estacionaria de gasoil Planar."]),
    ("Seguridad y exterior", ["Cámara trasera de aparcamiento.", "Luz exterior y toma exterior de 230 V."]),
    ("Homologación", ["Plazas traseras homologadas para viajar en regla.",
                      "Proyecto de homologación completa, gestionado por nosotros."]),
]

REVIEWS = [
    ("Encantado con el trabajo realizado. El resultado final ha sido excelente, con una terminación de gran calidad y detalles exclusivos que marcan la diferencia. Incluso después de la entrega han estado siempre dispuestos a atender cualquier ajuste.", "Juan Sánchez"),
    ("Los mejores, cumplieron un sueño que tenía desde hace muchos años. Encantado con el trabajo que me hicieron; tanto José como Pedro, súper atentos a todo el proceso.", "Raúl Hijano"),
    ("Muy buenos profesionales todo el equipo. Tanto José como Pedro muy atentos a todas nuestras necesidades y orientándonos en lo mejor. Justos en cuanto a calidad-precio.", "Pepa Puchero"),
]


def reviews_html():
    items = "".join(f'<figure class="review"><div class="stars" aria-label="5 estrellas">★★★★★</div><blockquote>“{esc(t)}”</blockquote>'
                    f'<figcaption>{esc(n)} · reseña en Google</figcaption></figure>' for t, n in REVIEWS)
    return f"""<section class="section"><div class="wrap">
<div class="section-head"><p class="label">Lo que dicen nuestros clientes</p><h2>Opiniones de quienes ya viajan en su Lifes Campers</h2></div>
<div class="reviews">{items}</div>
<p style="margin-top:22px"><a href="{MAPS}" target="_blank" rel="noopener">Ver todas las reseñas en Google →</a></p>
</div></section>"""


def vans_grid():
    cards = "".join(f'<a class="van" href="/furgonetas/{v["slug"]}/"><div><p class="label">{esc(v["brand"])}</p>'
                    f'<h3>{esc(v["model"])}</h3><p>{esc(v["card"])}</p></div><span class="more">Ver camperización →</span></a>'
                    for v in FURGONETAS)
    return f'<div class="vans">{cards}</div>'


# --------------------------------------------------------------------------- páginas
def page_home():
    mosaic_slugs = ["interior-camper-cocina-madera-dinette", "cocina-camper-azulejo-escamas", "cama-camper-transversal",
                    "iveco-daily-camper-negra", "bano-camper-ducha-wc", "camper-salon-cama-claraboyas",
                    "cocina-camper-horno-vistas-mar", "camper-cama-matrimonio-boxer", "iveco-daily-camper-cocina-induccion"]
    mosaic = "".join(thumb_link(s, "home", "big" if i == 0 else "") for i, s in enumerate(mosaic_slugs))
    body = f"""
<section class="hero"><div class="wrap">
  <div>
    <p class="kicker">Camperización integral a medida en Málaga</p>
    <h1>Tu casa sobre ruedas, hecha a mano de principio a fin.</h1>
    <p class="lead">Camperizamos furgonetas grandes —Ducato, Boxer, Jumper, Movano, Crafter, Sprinter y similares— con todo incluido: aislamiento, mobiliario, energía solar, agua, cocina, baño y descanso. Con homologación y garantía, para que invertir sea una alegría y no un riesgo.</p>
    <div class="actions">
      <a class="btn btn-wa" href="{wa()}" target="_blank" rel="noopener">{WA_SVG}Escríbenos por WhatsApp</a>
      <a class="btn btn-line" href="/trabajos/">Ver trabajos</a>
    </div>
    <ul class="trust"><li>Homologación incluida</li><li>Plazas legales</li><li>Garantía</li><li>Entrega en 3 meses</li></ul>
  </div>
  <div class="hero-img">{pic("interior-camper-cama-cocina-azulejo-verde", eager=True)}</div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="trio">
    <div><p class="label">01</p><h3>A medida, de verdad</h3><p>Diseñamos la distribución contigo y la ejecutamos pieza a pieza en nuestro taller de Málaga.</p></div>
    <div><p class="label">02</p><h3>Materiales que duran</h3><p>HPL marino, suelos marinos y un aislamiento serio. Para años de uso real, no para la foto.</p></div>
    <div><p class="label">03</p><h3>Legal y con garantía</h3><p>Homologación completa y plazas traseras homologadas. Gestionamos todo el papeleo por ti.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><p class="label">Nuestro trabajo</p><h2>Camperizaciones hechas en Málaga</h2>
  <p class="lead">Cada camper es distinta. Lo que no cambia es el cuidado en los acabados: juntas, cantos, cableado y anclajes pensados para durar.</p></div>
  <div class="mosaic">{mosaic}</div>
  <div class="actions"><a class="btn btn-dark" href="/trabajos/">Ver todos los trabajos</a></div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="price">
    <div>
      <p class="label">Equipamiento completo</p>
      <p class="amount">{PRICE}</p>
      <p class="note">Homologación y garantía incluidas · Entrega en 3 meses</p>
      <p>Camperización integral sobre tu furgoneta tipo Ducato, Boxer, Jumper, Sprinter, Crafter o Transit. ¿Aún no la tienes? Te ayudamos a encontrarla.</p>
      <div class="actions"><a class="btn btn-dark" href="/camperizacion-integral/">Ver todo lo que incluye</a></div>
    </div>
    <div class="price-card"><ul>
      <li>Doble aislamiento Kaiflex y panelado de friso</li>
      <li>Mobiliario completo en HPL marino</li>
      <li>200 Ah de litio, placa solar de 400 W e inversor de 1000 W</li>
      <li>Depósito de 200 l, agua caliente y ducha exterior</li>
      <li>Cocina Dometic y nevera de compresor de 115 l</li>
      <li>Baño con ducha, 2 claraboyas y calefacción Planar</li>
      <li>Proyecto de homologación y plazas traseras homologadas</li>
    </ul></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><p class="label">Furgonetas grandes, desde L2H2</p><h2>Elige tu furgoneta</h2>
  <p class="lead">Nos especializamos en furgonetas grandes porque son las que permiten una casa de verdad: cama fija, cocina completa, baño y altura para estar de pie.</p></div>
  {vans_grid()}
</div></section>

<section class="section alt"><div class="wrap split">
  <div>{pic("pedro-y-jose-lifes-campers")}</div>
  <div>
    <p class="label">Quiénes somos</p>
    <h2>No sueñes tu vida, vive tus sueños</h2>
    <p>Somos Pedro y José, dos amigos que coincidimos en un mismo sueño y decidimos hacerlo realidad. Hoy, junto a nuestro equipo, camperizamos furgonetas en nuestro taller de San Julián, en Málaga.</p>
    <p>Nos gusta hacer las cosas bien y con trato cercano: te acompañamos desde el diseño hasta la entrega, y seguimos ahí después para cualquier ajuste.</p>
    <p>¿Quieres ver cómo trabajamos? Ven a visitarnos al taller.</p>
    <div class="actions"><a class="btn btn-line" href="/contacto/">Cómo llegar</a></div>
  </div>
</div></section>

{reviews_html()}
{cta()}
"""
    return layout("/", "Camperización de furgonetas en Málaga | Lifes Campers",
                  "Camperización integral de furgonetas grandes en Málaga: Ducato, Boxer, Jumper, Sprinter, Crafter… Equipamiento completo por 24.900 € con homologación y garantía.",
                  body)


def page_integral():
    specs = "".join(f'<div class="spec"><div><span class="n">{i + 1:02d}</span><h3>{esc(t)}</h3></div>'
                    f'<ul>{"".join(f"<li>{esc(x)}</li>" for x in items)}</ul></div>' for i, (t, items) in enumerate(SPECS))
    faqs = [
        ("¿El precio incluye la furgoneta?", "No. Los 24.900 € son la camperización integral completa sobre tu furgoneta. Si todavía no la tienes, te ayudamos a encontrar la base adecuada."),
        ("¿En qué furgonetas trabajáis?", "Nos centramos en furgonetas grandes desde L2H2: Fiat Ducato, Peugeot Boxer, Citroën Jumper, Opel Movano, Renault Master, Volkswagen Crafter, Mercedes Sprinter, Ford Transit e Iveco Daily."),
        ("¿Cuánto se tarda?", "Unos 3 meses desde la reserva hasta la entrega de tu camper, lista y homologada."),
        ("¿Está incluida la homologación?", "Sí. Preparamos y gestionamos el proyecto de homologación completo, incluidas las plazas traseras homologadas para viajar en regla."),
        ("¿Se puede personalizar el equipamiento?", "Sí. El equipamiento es orientativo y se adapta a tu furgoneta y a cómo viajas. El precio final depende de la configuración que acordemos."),
        ("¿Cómo se paga?", "Una reserva de 1.000 € para bloquear tu hueco de producción, un 40 % al comenzar, un 40 % con el grueso del trabajo avanzado y el 20 % restante a la entrega."),
    ]
    faq_h, faq_sc = faq_block(faqs)
    cr, cr_sc = crumbs([("Camperización integral", "/camperizacion-integral/")])
    service = {"@type": "Service", "name": "Camperización integral de furgoneta", "serviceType": "Camperización de furgonetas",
               "provider": {"@id": SITE + "/#negocio"}, "areaServed": "España",
               "offers": {"@type": "Offer", "price": "24900", "priceCurrency": "EUR",
                          "description": "Equipamiento completo, homologación y garantía incluidas. Precio de la camperización, sin la furgoneta."}}
    body = f"""
<section class="hero"><div class="wrap">
  <div>
    {cr}
    <p class="kicker">Qué incluye la camperización</p>
    <h1>Camperización integral de furgonetas</h1>
    <p class="lead">Todo lo que necesitas para viajar con autonomía y comodidad, montado y homologado en nuestro taller de Málaga. Este es nuestro equipamiento de serie, área por área.</p>
    <ul class="trust"><li>Homologación incluida</li><li>Plazas legales</li><li>Garantía</li><li>Entrega en 3 meses</li></ul>
  </div>
  <div class="hero-img">{pic("interior-camper-cocina-madera-dinette", eager=True)}</div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="section-head"><p class="label">Equipamiento de serie</p><h2>Detalle por áreas</h2></div>
  <div class="specs">{specs}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="price">
    <div>
      <p class="label">La inversión</p>
      <p class="amount">{PRICE}</p>
      <p>Camperización integral con todo el equipamiento de esta página, sobre tu furgoneta o te ayudamos a encontrarla.</p>
      <p class="note">3 meses de plazo, de la reserva a la entrega de tu camper.</p>
    </div>
    <div>{pic("cama-camper-transversal")}</div>
  </div>
  <h2 style="margin-top:56px">Plan de pago</h2>
  <div class="steps">
    <div class="step"><p class="label">Paso 01</p><h3>Reserva</h3><strong>1.000 €</strong><p>Bloqueamos tu hueco de producción.</p></div>
    <div class="step"><p class="label">Paso 02</p><h3>Al comenzar</h3><strong>40 %</strong><p>Arranca el montaje de tu camper.</p></div>
    <div class="step"><p class="label">Paso 03</p><h3>Durante el proceso</h3><strong>40 %</strong><p>Con el grueso del trabajo avanzado.</p></div>
    <div class="step"><p class="label">Paso 04</p><h3>A la entrega</h3><strong>20 %</strong><p>Recoges tu camper, lista y homologada.</p></div>
  </div>
  <p class="muted" style="margin-top:18px;font-size:.92rem">Equipamiento orientativo de la camperización integral; puede adaptarse según la furgoneta y las necesidades de cada proyecto. Precio y plan de pago sujetos a la configuración final acordada.</p>
</div></section>

<section class="section alt"><div class="wrap narrow">
  <p class="label">Preguntas frecuentes</p><h2>Lo que más nos preguntáis</h2>
  {faq_h}
</div></section>
{cta()}
"""
    return layout("/camperizacion-integral/", "Camperización integral de furgonetas: qué incluye y precio | Lifes Campers",
                  "Camperización integral por 24.900 €: aislamiento Kaiflex, mobiliario HPL marino, 200 Ah de litio, solar 400 W, agua, cocina, baño, calefacción y homologación. Taller en Málaga.",
                  body, [cr_sc, faq_sc, service], active="/camperizacion-integral/")


def page_furgonetas():
    cr, cr_sc = crumbs([("Furgonetas", "/furgonetas/")])
    body = f"""
<section class="section"><div class="wrap">
  {cr}
  <div class="section-head">
    <p class="kicker">Furgonetas grandes, desde L2H2</p>
    <h1>¿Qué furgoneta camperizar?</h1>
    <p class="lead">Trabajamos con las furgonetas grandes del mercado. Todas permiten una camper completa, pero cada una tiene sus puntos fuertes: anchura, tracción, altura o capacidad de carga. Elige la tuya y te contamos cómo la camperizamos.</p>
  </div>
  {vans_grid()}
</div></section>

<section class="section alt"><div class="wrap narrow prose">
  <p class="label">Antes de elegir</p>
  <h2>Por qué recomendamos furgonetas desde L2H2</h2>
  <p>En las furgonetas grandes la letra <strong>L</strong> indica la longitud y la <strong>H</strong> la altura del techo. Una <strong>L2H2</strong> (media longitud, techo alto) es el punto de partida que recomendamos: con un techo H2 puedes estar de pie dentro, y con una L2 caben cama de matrimonio, cocina completa, baño y una dinette con plazas homologadas.</p>
  <p>Si viajáis más de dos personas o queréis un baño más amplio o un garaje trasero grande, una <strong>L3</strong> o <strong>L4</strong> da mucho juego. Eso sí, ten en cuenta el aparcamiento en ciudad y el peso total.</p>
  <h2>El peso: la clave que casi nadie mira</h2>
  <p>Con el carné B puedes conducir vehículos de hasta <strong>3.500 kg de masa máxima autorizada</strong>. Una camperización completa suma peso (muebles, agua, baterías…), por eso diseñamos cada camper pensando en el peso final: baterías de litio, tableros ligeros y depósitos bien colocados para que viajes cargado y dentro de la ley.</p>
  <h2>¿Aún no tienes furgoneta?</h2>
  <p>Escríbenos antes de comprarla. Te ayudamos a elegir modelo, versión y año según tu presupuesto y cómo vas a viajar, y te decimos qué revisar en una de segunda mano.</p>
  <div class="actions"><a class="btn btn-wa" href="{wa("Hola, estoy buscando furgoneta para camperizar y me gustaría consejo.")}" target="_blank" rel="noopener">{WA_SVG}Pídenos consejo</a></div>
</div></section>
{cta()}
"""
    return layout("/furgonetas/", "Furgonetas para camperizar: Ducato, Boxer, Sprinter, Crafter… | Lifes Campers",
                  "Qué furgoneta camperizar: Fiat Ducato, Peugeot Boxer, Citroën Jumper, Opel Movano, Renault Master, VW Crafter, Mercedes Sprinter, Ford Transit e Iveco Daily. Camperización integral en Málaga.",
                  body, [cr_sc], active="/furgonetas/")


def page_van(v):
    cr, cr_sc = crumbs([("Furgonetas", "/furgonetas/"), (v["name"], f'/furgonetas/{v["slug"]}/')])
    faq_h, faq_sc = faq_block(v["faq"])
    facts = "".join(f"<tr><th>{esc(k)}</th><td>{esc(x)}</td></tr>" for k, x in v["facts"])
    gallery = "".join(thumb_link(s, "van") for s in v["photos"])
    others = "".join(f'<li><a href="/furgonetas/{o["slug"]}/">Camperizar {esc(o["name"])}</a></li>' for o in FURGONETAS if o is not v)
    body = f"""
<section class="hero"><div class="wrap">
  <div>
    {cr}
    <p class="kicker">Camperización integral · {esc(v["brand"])}</p>
    <h1>Camperizar una {esc(v["name"])}</h1>
    <p class="lead">{v["intro"]}</p>
    <div class="actions">
      <a class="btn btn-wa" href="{wa(f'Hola, quiero camperizar una {v["name"]}.')}" target="_blank" rel="noopener">{WA_SVG}Pide información</a>
      <a class="btn btn-line" href="/camperizacion-integral/">Qué incluye</a>
    </div>
  </div>
  <div class="hero-img">{pic(v["hero"], eager=True)}</div>
</div></section>

<section class="section alt"><div class="wrap narrow prose">
  {v["body"]}
  <h2>Datos útiles de la {esc(v["name"])}</h2>
  <table class="facts">{facts}</table>
  <p class="muted" style="font-size:.9rem">Medidas y versiones orientativas: varían según el año y el carrozado. Te confirmamos los datos de tu furgoneta antes de diseñar.</p>
</div></section>

<section class="section"><div class="wrap">
  <div class="price">
    <div>
      <p class="label">Camperización integral sobre {esc(v["name"])}</p>
      <p class="amount">{PRICE}</p>
      <p class="note">Homologación y garantía incluidas · Entrega en 3 meses</p>
      <p>Aislamiento, mobiliario en HPL marino, 200 Ah de litio con solar de 400 W, agua con 200 l, cocina, baño, calefacción y homologación. Precio de la camperización, sin la furgoneta.</p>
      <div class="actions"><a class="btn btn-dark" href="/camperizacion-integral/">Ver el equipamiento completo</a></div>
    </div>
    <div class="grid" style="grid-template-columns:repeat(2,1fr);margin:0">{gallery}</div>
  </div>
</div></section>

<section class="section alt"><div class="wrap narrow">
  <p class="label">Preguntas frecuentes</p><h2>Dudas sobre camperizar una {esc(v["name"])}</h2>
  {faq_h}
  <h3 style="margin-top:40px">Otras furgonetas que camperizamos</h3>
  <ul>{others}</ul>
</div></section>
{cta(f"¿Tienes una {v['name']}?", "Cuéntanos versión y año y te proponemos una distribución a medida. Respondemos por WhatsApp.")}
"""
    return layout(f'/furgonetas/{v["slug"]}/', v["title"], v["desc"], body, [cr_sc, faq_sc], active="/furgonetas/")


def page_trabajos():
    cr, cr_sc = crumbs([("Trabajos", "/trabajos/")])
    blocks = ""
    for i, (title, text, slugs) in enumerate(PROJECTS):
        grid = "".join(thumb_link(s, f"p{i}") for s in slugs)
        blocks += f'<article class="project"><h2>{esc(title)}</h2><p>{esc(text)}</p><div class="grid">{grid}</div></article>'
    body = f"""
<section class="section"><div class="wrap">
  {cr}
  <div class="section-head">
    <p class="kicker">Galería</p>
    <h1>Nuestros trabajos de camperización</h1>
    <p class="lead">Furgonetas que han salido de nuestro taller de Málaga. Pulsa en cualquier foto para verla en grande.</p>
  </div>
  {blocks}
  <div class="split" style="margin-top:24px">
    <div>{pic("taller-lifes-campers-malaga")}</div>
    <div><p class="label">Ven a verlas en persona</p><h2>Visítanos en el taller</h2>
    <p>Las fotos están bien, pero los acabados se aprecian de cerca. Escríbenos y quedamos en el taller de San Julián, Málaga, para que veas cómo trabajamos.</p>
    <div class="actions"><a class="btn btn-wa" href="{wa("Hola, me gustaría visitar el taller.")}" target="_blank" rel="noopener">{WA_SVG}Concertar visita</a></div></div>
  </div>
</div></section>
{cta()}
"""
    return layout("/trabajos/", "Trabajos de camperización de furgonetas en Málaga | Lifes Campers",
                  "Galería de camperizaciones integrales hechas en Málaga: Iveco Daily, Peugeot Boxer y más. Cocinas, baños, camas y acabados en madera.",
                  body, [cr_sc], active="/trabajos/")


def page_contacto():
    cr, cr_sc = crumbs([("Contacto", "/contacto/")])
    options = "".join(f"<option>{esc(v['name'])}</option>" for v in FURGONETAS)
    body = f"""
<section class="section"><div class="wrap">
  {cr}
  <div class="section-head"><p class="kicker">Hablemos</p><h1>Contacto</h1>
  <p class="lead">La forma más rápida es WhatsApp. También puedes llamarnos, escribirnos o venir al taller.</p></div>
  <div class="contact">
    <div>
      <div class="actions" style="margin-top:0">
        <a class="btn btn-wa" href="{wa()}" target="_blank" rel="noopener">{WA_SVG}WhatsApp {TEL1}</a>
        <a class="btn btn-wa" href="https://wa.me/34637313252" target="_blank" rel="noopener">{WA_SVG}WhatsApp {TEL2}</a>
      </div>
      <dl>
        <dt>Teléfonos</dt><dd><a href="tel:+34637372296">{TEL1}</a> · <a href="tel:+34637313252">{TEL2}</a></dd>
        <dt>Atención telefónica</dt><dd>Lunes a viernes, de 8:00 a 14:00</dd>
        <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
        <dt>Taller</dt><dd>{esc(ADDRESS)}<br><a href="{MAPS}" target="_blank" rel="noopener">Abrir en Google Maps →</a></dd>
      </dl>
      <div style="margin-top:28px">{pic("taller-lifes-campers-fachada")}</div>
    </div>
    <form class="form" id="contact-form">
      <h2 style="font-size:1.6rem">Cuéntanos tu proyecto</h2>
      <input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
      <input type="hidden" name="subject" value="Nuevo mensaje desde camperizacionmalaga.com">
      <input type="hidden" name="from_name" value="Web Lifes Campers">
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">
      <div class="row">
        <div><label for="f-name">Nombre</label><input id="f-name" name="name" required autocomplete="name"></div>
        <div><label for="f-phone">Teléfono</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      </div>
      <label for="f-email">Email</label><input id="f-email" name="email" type="email" required autocomplete="email">
      <label for="f-van">Furgoneta</label>
      <select id="f-van" name="furgoneta"><option>Aún no tengo furgoneta</option>{options}<option>Otra</option></select>
      <label for="f-msg">Mensaje</label><textarea id="f-msg" name="message" required placeholder="Versión y año de la furgoneta, cuántas personas viajáis, qué necesitáis…"></textarea>
      <label class="check"><input type="checkbox" required> He leído y acepto la <a href="/politica-de-privacidad/">política de privacidad</a>.</label>
      <button class="btn btn-dark" type="submit">Enviar mensaje</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</div></section>
"""
    return layout("/contacto/", "Contacto | Lifes Campers, camperización en Málaga",
                  "Contacta con Lifes Campers: WhatsApp 637 37 22 96 · 637 31 32 52. Taller de camperización de furgonetas en San Julián, Málaga.",
                  body, [cr_sc], active="/contacto/")


LEGAL_HOLDER = f"""<table class="facts">
<tr><th>Titular</th><td>CROSSCAMPERS, S.L.</td></tr>
<tr><th>Nombre comercial</th><td>Lifes Campers</td></tr>
<tr><th>CIF</th><td>B93729606</td></tr>
<tr><th>Domicilio social</th><td>C/ Pascal, 14 · 29004 Málaga</td></tr>
<tr><th>Taller</th><td>{esc(ADDRESS)}</td></tr>
<tr><th>Teléfono</th><td>{TEL1} · {TEL2}</td></tr>
<tr><th>Email</th><td>{EMAIL}</td></tr>
<tr><th>Sitio web</th><td>camperizacionmalaga.com</td></tr>
</table>"""


def page_legal(path, title, h1, content):
    cr, cr_sc = crumbs([(h1, path)])
    body = f'<section class="section"><div class="wrap narrow prose">{cr}<h1>{esc(h1)}</h1>{content}<p class="muted">Última actualización: {TODAY}.</p></div></section>'
    return layout(path, title, f"{h1} de camperizacionmalaga.com, web de Lifes Campers (CROSSCAMPERS, S.L.).", body, [cr_sc])


AVISO = f"""
<h2>1. Datos identificativos</h2>
<p>En cumplimiento del artículo 10 de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:</p>
{LEGAL_HOLDER}
<h2>2. Objeto y condiciones de uso</h2>
<p>Este sitio web ofrece información sobre los servicios de camperización de Lifes Campers. El acceso es gratuito y no requiere registro. El uso del sitio implica la aceptación de este aviso legal. El usuario se compromete a hacer un uso adecuado de los contenidos y a no emplearlos para actividades ilícitas o contrarias a la buena fe.</p>
<h2>3. Precios e información comercial</h2>
<p>Los precios y el equipamiento publicados son orientativos, incluyen las condiciones indicadas en cada caso y pueden variar según la furgoneta y la configuración final acordada por escrito con cada cliente.</p>
<h2>4. Propiedad intelectual e industrial</h2>
<p>Los textos, fotografías, logotipos y diseño de este sitio son propiedad de CROSSCAMPERS, S.L. o se utilizan con autorización. Queda prohibida su reproducción, distribución o transformación sin autorización previa y por escrito.</p>
<h2>5. Responsabilidad</h2>
<p>CROSSCAMPERS, S.L. procura que la información de esta web sea correcta y esté actualizada, pero no se hace responsable de errores u omisiones, ni de los daños derivados del uso de la web o de enlaces a sitios de terceros, cuyos contenidos no controla.</p>
<h2>6. Protección de datos y cookies</h2>
<p>El tratamiento de datos personales se explica en la <a href="/politica-de-privacidad/">política de privacidad</a> y el uso de cookies en la <a href="/politica-de-cookies/">política de cookies</a>.</p>
<h2>7. Legislación aplicable</h2>
<p>Este aviso legal se rige por la legislación española. Para cualquier controversia, las partes se someten a los juzgados y tribunales que correspondan conforme a la normativa vigente.</p>
"""

PRIVACIDAD = f"""
<h2>1. Responsable del tratamiento</h2>
{LEGAL_HOLDER}
<h2>2. Qué datos tratamos y para qué</h2>
<p>Tratamos los datos que nos facilitas al escribirnos por el formulario de contacto, por WhatsApp, por teléfono o por email (nombre, email, teléfono y la información de tu consulta) con la única finalidad de <strong>responder a tu solicitud</strong> y, si nos contratas, de gestionar la relación comercial y la facturación.</p>
<h2>3. Base legal</h2>
<p>El consentimiento que nos das al enviar la consulta (art. 6.1.a RGPD) y, en su caso, la ejecución de un contrato o de medidas precontractuales a petición tuya (art. 6.1.b RGPD), así como el cumplimiento de obligaciones legales, como las fiscales (art. 6.1.c RGPD).</p>
<h2>4. Conservación</h2>
<p>Conservamos los datos de las consultas el tiempo necesario para atenderlas y, como máximo, un año si no llegas a ser cliente. Los datos de clientes se conservan durante la relación comercial y los plazos legales posteriores.</p>
<h2>5. Destinatarios</h2>
<p>No cedemos tus datos a terceros salvo obligación legal. Para prestar el servicio utilizamos proveedores que actúan como encargados del tratamiento: Web3Forms, que recibe los mensajes del formulario y nos los reenvía por email, y Cloudflare, que aloja esta web. Algunos de estos proveedores pueden tratar datos fuera del Espacio Económico Europeo con las garantías previstas en el RGPD (cláusulas contractuales tipo o marcos de adecuación).</p>
<h2>6. Tus derechos</h2>
<p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a <a href="mailto:{EMAIL}">{EMAIL}</a> o por correo postal a C/ Pascal, 14 · 29004 Málaga, indicando qué derecho ejerces. Si consideras que no hemos atendido correctamente tu solicitud, puedes reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es" target="_blank" rel="noopener">www.aepd.es</a>).</p>
"""

COOKIES = """
<h2>¿Qué son las cookies?</h2>
<p>Las cookies son pequeños archivos que algunas webs guardan en tu navegador para recordar información sobre tu visita.</p>
<h2>Cookies que usa esta web</h2>
<p>Esta web <strong>no utiliza cookies de análisis, de publicidad ni de seguimiento</strong>, y no incluye vídeos, mapas ni botones sociales de terceros que las instalen. Por eso no te mostramos ningún aviso para aceptarlas.</p>
<p>Nuestro proveedor de alojamiento, Cloudflare, puede usar cookies técnicas estrictamente necesarias para la seguridad del sitio (por ejemplo, para filtrar tráfico malicioso). Estas cookies no requieren consentimiento según el artículo 22.2 de la LSSI-CE.</p>
<p>Los enlaces a WhatsApp, Instagram, Facebook o Google Maps te llevan a esas plataformas, que aplican sus propias políticas de cookies.</p>
<h2>Cómo gestionar las cookies</h2>
<p>Puedes ver y borrar las cookies desde la configuración de tu navegador (Chrome, Safari, Firefox, Edge…).</p>
<h2>Cambios</h2>
<p>Si en el futuro añadimos herramientas que utilicen cookies no técnicas, actualizaremos esta política y te pediremos el consentimiento antes de instalarlas.</p>
"""


def page_404():
    body = f"""<section class="section"><div class="wrap narrow"><p class="kicker">Error 404</p><h1>Esta página no existe</h1>
<p class="lead">Puede que el enlace sea antiguo o que la hayamos movido.</p>
<div class="actions"><a class="btn btn-dark" href="/">Ir al inicio</a><a class="btn btn-line" href="/trabajos/">Ver trabajos</a></div></div></section>"""
    return layout("/404.html", "Página no encontrada | Lifes Campers", "La página que buscas no existe.", body)


# --------------------------------------------------------------------------- escritura
def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    if full.endswith("/"):
        full += "index.html"
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    # Conserva las imágenes ya generadas (img/) para no recomprimirlas en cada build.
    if os.path.isdir(OUT):
        for name in os.listdir(OUT):
            if name == "img":
                continue
            p = os.path.join(OUT, name)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(OUT, exist_ok=True)
    build_images()
    shutil.copytree(os.path.join(ROOT, "fonts"), os.path.join(OUT, "fonts"))
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    for f in ("style.css", "main.js"):
        shutil.copy(os.path.join(ROOT, "assets", f), os.path.join(OUT, "assets", f))

    pages = {
        "/": page_home(),
        "/camperizacion-integral/": page_integral(),
        "/furgonetas/": page_furgonetas(),
        "/trabajos/": page_trabajos(),
        "/contacto/": page_contacto(),
        "/aviso-legal/": page_legal("/aviso-legal/", "Aviso legal | Lifes Campers", "Aviso legal", AVISO),
        "/politica-de-privacidad/": page_legal("/politica-de-privacidad/", "Política de privacidad | Lifes Campers", "Política de privacidad", PRIVACIDAD),
        "/politica-de-cookies/": page_legal("/politica-de-cookies/", "Política de cookies | Lifes Campers", "Política de cookies", COOKIES),
    }
    for v in FURGONETAS:
        pages[f'/furgonetas/{v["slug"]}/'] = page_van(v)
    for path, content in pages.items():
        write(path, content)
    write("/404.html", page_404())

    prio = {"/": "1.0", "/camperizacion-integral/": "0.9", "/furgonetas/": "0.8", "/trabajos/": "0.8", "/contacto/": "0.7"}
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(p, '0.6' if 'furgonetas' in p else '0.3')}</priority></url>"
                   for p in pages)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    # URLs de la web antigua (WordPress) que redirigen a su equivalente nuevo
    write("/_redirects", "\n".join([
        "/galeria/ /trabajos/ 301",
        "/galeria /trabajos/ 301",
        "/venta/ / 301",
        "/venta / 301",
        "/camperizaciones-malaga/ / 301",
        "/camperizaciones-malaga / 301",
        "/informacion-cookies/ /politica-de-cookies/ 301",
        "/informacion-cookies /politica-de-cookies/ 301",
    ]) + "\n")
    write("/_headers", "/img/*\n  Cache-Control: public, max-age=2592000\n/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n")
    print(f"{len(pages)} páginas generadas en {OUT}")


if __name__ == "__main__":
    main()
