# Web de Lifes Campers (camperizacionmalaga.com)

Web estática generada con `python3 src/build.py` (necesita `pillow` y `markdown`). La salida `web/` se publica en Cloudflare Workers al unir cambios a la rama principal del repo. Detalles en `LEEME.md`.

Regla de marca: aquí solo van contenidos de Lifes Campers (camperización integral en Málaga). Nada de kits Camperízate ni de kitamenagement.fr / kitcampermodulare.it.

## Publicar artículos del blog desde Notion
Cuando el usuario pida publicar el blog:
1. Consulta la base de datos de Notion «Artículos» (data source `collection://796174e5-dc3b-4cb3-a5a0-1bf204976bd0`, dentro de la página «Blog · Lifes Campers (camperizacionmalaga.com)»). Publica solo los artículos que el usuario nombre; si no nombra ninguno, los que estén en «Listo para publicar». Nunca publiques un «Borrador» sin que el usuario lo pida expresamente.
2. Antes de publicar cada uno, comprueba y, si falla algo, no lo publiques y avisa:
   - No queda ningún texto en rojo con «[VERIFICAR …]».
   - Tiene «Foto de portada». Si está vacía, no uses fotos de banco ni inventes: avisa.
3. Lee el recuadro gris «Nota interna (borrar antes de publicar)»: usa el slug que indica (sin barras) y sigue sus instrucciones de enlaces. El recuadro no se publica.
4. Convierte la página a `src/blog/<slug>.md` siguiendo `src/blog/_plantilla.md`. El artículo queda en `https://camperizacionmalaga.com/<slug>/`.
   - Cabecera: titulo = propiedad Título; descripcion = propiedad Descripción; fecha = «Fecha de publicación» (o hoy si está vacía); imagen e imagen_alt.
   - El cuerpo empieza en el primer párrafo (el título no se repite como H1).
   - Mantén el texto del autor: corrige solo erratas y formato. Si ves datos dudosos (precios, normativa, homologación), pregunta antes.
5. Descarga la portada y las fotos del texto a `src/blog/fotos/` con nombres descriptivos y escribe textos alternativos que describan lo que se ve.
6. El build hace solo estas comprobaciones:
   - Genera el schema FAQPage a partir de la sección «Preguntas frecuentes» (H2 con preguntas en H3).
   - Para un error si un enlace interno apunta a una página que no existe.
   - Con fecha futura, el artículo queda programado: lo publica `.github/workflows/publicar-programados.yml` la mañana de su fecha. Hasta entonces, los enlaces que apunten a él se muestran como texto normal.
7. Serie «Reparación de campers»: al publicar o programar una guía, enlázala desde su H3 en `src/blog/reparacion-camper-andalucia.md` (por ejemplo `### [Claraboyas y ventanas](/reparar-claraboya-ventana-camper/)`).
8. Ejecuta `python3 src/build.py`, revisa la página en el navegador (escritorio y móvil) y abre un PR hacia la rama principal.
9. Tras el merge, pon el Estado en «Publicado» y rellena «URL en la web». Para los programados, indica en la respuesta la fecha en que saldrán.
