# Web italiana kitcampermodulare.it (beta)

## Cómo está montado
- **Común a Francia e Italia**: `tools/build.py` (plantillas), `tools/catalogue.py` (modelos, precios de kit, opciones),
  `tools/videos.csv`, fotos, CSS de `public/index.html`, imágenes y fuentes.
- **Solo Italia**: `tools/sites/it.py` (dominio, envío 250/300 €, enlaces Stripe, URL italianas, redirecciones /it/),
  `tools/sites/it_textes.py` (traducción francés → italiano), `tools/sites/it_pages/` (páginas legales en italiano).
- `python3 tools/build.py` genera las dos webs: `public/` (Francia) y `public-it/` (Italia).
  Si un texto francés cambia y no tiene traducción, el build falla y lo lista en `tools/sites/it_a_traduire.txt`.
- Publicación: Worker de Cloudflare propio con `wrangler.it.jsonc` (carpeta `public-it/`), misma rama `kitamenagement`.

## Estado (18/10/2026)
- Web online en https://kitcampermodulare.it/ (Worker `kitcampermodulare`).
- **Stripe: 45/45 enlaces creados** (`STRIPE` en `tools/sites/it.py`), metadata `site=kitcampermodulare.it`.
  - Recogida: kit (+ materasso) + 6 optional; campos «Modello e anno del veicolo» y «Punto di ritiro» (La Garriga / Nîmes).
  - Envío: + spedizione (250/300 €), dirección de envío solo IT.
  - Accesorios: cantidad 1-5; oscuranti con campo de modelo.
- **Facturación Stripe → Holded**: acepta `kitamenagement.fr` y `kitcampermodulare.it` (`SITE_METADATA` en
  `facturacion/wrangler.jsonc`). Pedidos italianos: contacto con etiqueta `web-it`, documento en italiano,
  nota con el punto de recogida, e-mail de confirmación en italiano.
- **Redirecciones /it/ activadas** en `docs/redirection-webnode.html` (43 URL + reglas generales): hay que pegar el
  script nuevo en el encabezado de Webnode (sustituye al anterior, sirve para /fr/ y /it/).

## Pendiente
- Pegar el script nuevo de redirección en Webnode y comprobar 2-3 URL /it/.
- Search Console: dar de alta kitcampermodulare.it y enviar `sitemap.xml`.
- Compra de prueba (fornello 29 €) y reembolso, para ver el flujo completo hasta Holded.
- IVA de las ventas a Italia (OSS) con el gestor: hoy se factura con IVA español 21 %, igual que Francia.
- Revisar con el gestor/abogado las condiciones de venta italianas (`tools/sites/it_pages/`).
- Confirmar envío a islas (la web dice «in Italia»), formulario de contacto en italiano (hoy es el Tally francés),
  imagen para compartir (`og-kitamenagement.jpg`) en italiano.
