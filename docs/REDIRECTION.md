# Redirigir camperizatetodoen1.com/fr/ a kitamenagement.fr

**Todavía no está activado.** Este documento explica cómo hacerlo cuando se decida.

## Qué hay preparado

- `tools/redirections.json`: las 54 URL antiguas de `/fr/` con su página nueva. Incluye todas las que traen
  tráfico según Search Console (fichas de modelo, catálogo, guía, contacto, tienda, occultants, colchones…).
- `docs/redirection-webnode.html`: el script listo para pegar. Se genera solo con `python3 tools/build.py`.
  - Solo actúa en las páginas que empiezan por `/fr/`: la web española, italiana, etc. no se tocan.
  - Primero busca la URL exacta; si no está, aplica una regla general
    (`/fr/tienda/…` → tienda, `/fr/kit-camperizacion/…` → catálogo, cualquier otra `/fr/…` → portada).

## Cómo activarlo

1. Webnode → Ajustes → **Encabezado HTML** (código en el `<head>` de todas las páginas).
2. Pegar el contenido de `docs/redirection-webnode.html` y publicar.
3. Probar 3 o 4 URL antiguas (por ejemplo `/fr/kit-camperizacion/berlingo/`): deben abrir la ficha nueva.
4. Search Console: dar de alta `kitamenagement.fr` y enviar `https://kitamenagement.fr/sitemap.xml`.

## Cómo desactivarlo

Borrar el script del encabezado de Webnode y publicar. Todo vuelve a estar como antes.

## Antes de activarlo

- Las fichas deberían tener sus fotos (ver `docs/PHOTOS.md`): Google compara la página antigua con la nueva.
- Si se añade o se cambia una página, ejecutar `python3 tools/build.py` y volver a pegar el script.
