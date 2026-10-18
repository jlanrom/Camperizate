# Mantenimiento de kitamenagement.fr y kitcampermodulare.it

Qué cambiar, dónde y cómo publicarlo. Las dos webs salen del mismo código: **lo común se cambia una vez y vale para las dos**.

## Cómo se publica cualquier cambio
1. Cambiar el archivo indicado abajo (o pedírselo a Claude: «cambia X en la web francesa / italiana / en las dos»).
2. Ejecutar `python3 tools/build.py`. Regenera `public/` (Francia) y `public-it/` (Italia).
   - Si un texto francés cambia y falta su traducción, el build se para y la lista en `tools/sites/it_a_traduire.txt`.
3. Commit en una rama, PR a `kitamenagement` y fusionar. Cloudflare publica solo: Worker de la .fr, Worker
   `kitcampermodulare` de la .it y Worker de facturación (`facturacion/`).

## Dónde está cada cosa

| Qué | Archivo | Afecta a |
| --- | --- | --- |
| **Nota y nº de reseñas Google** | `AVIS_GOOGLE` en `tools/sites/fr.py` y `tools/sites/it.py` | Bloque de reseñas y datos para Google |
| **Reseñas mostradas** (4 por web) | `AVIS` en `tools/sites/fr.py` (en francés) y `tools/sites/it.py` (en italiano) | Portada, tienda y fichas |
| Reseñas en los datos para Google (sí/no) | `AVIS_DONNEES` en los mismos archivos | Quitar si Search Console muestra una acción manual |
| Precios de los kits, colchón, opciones, accesorios | `tools/catalogue.py` (`FINITIONS`, `MATELAS`, `OPTIONS`, `ACCESSOIRES`) | Las dos webs. **Ojo:** también hay que cambiar el precio en Stripe |
| Precio de envío | `LIVRAISON` en `tools/sites/fr.py` / `it.py` | Cada web. También en Stripe y en los textos que lo citan |
| Modelos de vehículo, medidas, textos de las fichas | `MODELES` en `tools/catalogue.py` | Las dos webs (la .it pide la traducción de los textos nuevos) |
| Vídeos de las fichas | `tools/videos.csv` (ver `docs/VIDEOS.md`) | Las dos webs |
| Fotos de las fichas | `tools/photos.py` (ver `docs/PHOTOS.md`) | Las dos webs |
| Enlaces de pago Stripe | `STRIPE` en `tools/sites/fr.py` / `it.py` (ver `docs/STRIPE.md`) | Cada web |
| Textos de la web italiana | `tools/sites/it_textes.py` (francés → italiano) | Solo .it |
| Páginas legales italianas | `tools/sites/it_pages/` | Solo .it |
| Páginas legales francesas | `public/conditions-generales-de-vente/`, `mentions-legales/`, `politique-de-confidentialite/` | Solo .fr |
| Portada (textos fijos) | `public/index.html` (la .it la traduce sola) | Las dos |
| Diseño y estilos | `<style>` de `public/index.html` + `EXTRA_CSS` en `tools/build.py` | Las dos |
| Menú, pie de página, plantillas de página | `tools/build.py` | Las dos |
| Redirecciones desde Webnode | `REDIRECTIONS` en `tools/catalogue.py` (/fr/) y en `tools/sites/it.py` (/it/). Después pegar `docs/redirection-webnode.html` en el encabezado de Webnode | camperizatetodoen1.com |
| Facturación Stripe → Holded, e-mail al cliente | `facturacion/src/commande.js`, ajustes en `facturacion/wrangler.jsonc` | Pedidos de las dos webs |

## Tareas periódicas
- **Cada mes:** actualizar la nota y el nº de reseñas Google (`AVIS_GOOGLE`). Cambiar alguna reseña por otra más reciente.
- **Si cambia un precio:** catálogo + Stripe (precio nuevo en el producto y en los enlaces) + textos que lo mencionen.
- **Si se añade un modelo:** `MODELES` + traducción italiana + fotos/vídeos + redirección si tenía URL antigua.
- **Cada trimestre:** revisar `docs/redirection-webnode.html` en Webnode (sigue pegado y funcionando).
