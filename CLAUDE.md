# Web de Lifes Campers (camperizacionmalaga.com)

Web estática generada con `python3 src/build.py` (necesita `pillow` y `markdown`). La salida `web/` se publica en Cloudflare Workers al unir cambios a la rama principal del repo. Detalles en `LEEME.md`.

## Publicar artículos del blog desde Notion
Cuando el usuario pida publicar el blog:
1. Consulta la base de datos de Notion «Artículos» (data source `collection://796174e5-dc3b-4cb3-a5a0-1bf204976bd0`, dentro de la página «Blog · Lifes Campers (camperizacionmalaga.com)») y toma las filas con Estado = «Listo para publicar».
2. Por cada una: lee la página, conviértela a `src/blog/<slug>.md` siguiendo `src/blog/_plantilla.md` (slug corto con la palabra clave, sin tildes). Cabecera: titulo, descripcion (columna Descripción), fecha (Fecha de publicación o la de hoy), imagen e imagen_alt.
3. Descarga la foto de portada y las fotos del texto a `src/blog/fotos/` con nombres descriptivos y escribe textos alternativos que describan lo que se ve. Si no hay portada, usa una foto adecuada de `src/fotos/`.
4. Mantén el texto del autor: corrige solo erratas y formato. Si ves datos dudosos (precios, normativa, homologación), pregunta antes de publicar.
5. Ejecuta `python3 src/build.py`, revisa la página en el navegador (escritorio y móvil) y abre un PR hacia la rama principal.
6. Tras el merge, pon el Estado en «Publicado» y rellena «URL en la web» con `https://camperizacionmalaga.com/blog/<slug>/`.
