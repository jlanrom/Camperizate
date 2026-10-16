# Redirigir camperizatetodoen1.com/fr/ a kitamenagement.fr

**Todavía no está activado.** Este documento explica cómo hacerlo cuando se decida.

## Qué hay preparado

- `tools/redirections.json`: las 54 URL antiguas de `/fr/` con su página nueva. Incluye todas las que traen
  tráfico según Search Console (fichas de modelo, catálogo, guía, contacto, tienda, occultants, colchones…).
- `docs/redirection-webnode-prueba.html`: **versión de prueba**. Solo redirige si la URL lleva `?prueba-redireccion`;
  los visitantes normales no notan nada.
- `docs/redirection-webnode.html`: **versión definitiva**. Redirige a todo el mundo.
- Los dos se generan solos con `python3 tools/build.py`.
  - Solo actúa en las páginas que empiezan por `/fr/`: la web española, italiana, etc. no se tocan.
  - Primero busca la URL exacta; si no está, aplica una regla general
    (`/fr/tienda/…` → tienda, `/fr/kit-camperizacion/…` → catálogo, cualquier otra `/fr/…` → portada).

## Paso 1: probar sin afectar a nadie

1. Webnode → Ajustes → **Encabezado HTML** (código en el `<head>` de todas las páginas).
2. Pegar el contenido de `docs/redirection-webnode-prueba.html` (debajo de lo que ya haya) y publicar.
3. Abrir, por ejemplo:
   - `https://www.camperizatetodoen1.com/fr/kit-camperizacion/berlingo/?prueba-redireccion` → ficha Berlingo nueva
   - `https://www.camperizatetodoen1.com/fr/kitmueblescamper/?prueba-redireccion` → guía nueva
   - `https://www.camperizatetodoen1.com/fr/?prueba-redireccion` → portada nueva
   - `https://www.camperizatetodoen1.com/fr/kit-camperizacion/berlingo/` (sin el añadido) → sigue en Webnode
   - `https://www.camperizatetodoen1.com/` → sigue en la web española

## Paso 2: activarlo de verdad

1. En el mismo sitio de Webnode, **sustituir** el script de prueba por el de `docs/redirection-webnode.html` y publicar.
2. Repetir las pruebas sin el añadido: ahora todas las URL en francés deben llevar a kitamenagement.fr.
3. Search Console: dar de alta `kitamenagement.fr` y enviar `https://kitamenagement.fr/sitemap.xml`.

## Cómo desactivarlo

Borrar el script del encabezado de Webnode y publicar. Todo vuelve a estar como antes.

## Antes de activarlo

- Las fichas deberían tener sus fotos (ver `docs/PHOTOS.md`): Google compara la página antigua con la nueva.
- Si se añade o se cambia una página, ejecutar `python3 tools/build.py` y volver a pegar el script.
