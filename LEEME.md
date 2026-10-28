# camperizacionmalaga.com · Lifes Campers

Web estática de Lifes Campers, publicada en Cloudflare Workers. Cada cambio que se une a la rama principal se publica solo.

## Estructura
- `src/build.py`: genera toda la web en `web/` (páginas, textos, SEO, sitemap…).
- `src/content_furgonetas.py`: textos de las páginas de cada furgoneta.
- `src/fotos/`: fotos originales. El nombre del archivo es el nombre con el que sale en la web (bueno para SEO).
- `src/assets/`: estilos (`style.css`) y JavaScript (menú, visor de fotos y formulario).
- `web/`: la web generada. **No se edita a mano**: se regenera con `python3 src/build.py`.
- `wrangler.jsonc`: configuración de Cloudflare (sirve la carpeta `web/`).

## Páginas
- `/`: inicio (Málaga).
- `/camperizacion-integral/`: equipamiento, precio, plan de pago y preguntas frecuentes.
- `/furgonetas/` y una página por modelo: Ducato, Boxer, Jumper, Movano, Master, Crafter, Sprinter, Transit y Daily.
- `/trabajos/`: galería por proyectos.
- `/contacto/`: WhatsApp, teléfonos, taller y formulario.
- Aviso legal, privacidad y cookies.

## Cómo hacer cambios habituales
- **Añadir fotos**: copia la foto (en .webp o .jpg convertida a .webp) en `src/fotos/` con un nombre descriptivo, por ejemplo `cocina-camper-ducato-encimera-roble.webp`. Añade su texto alternativo en `ALT` y colócala en un proyecto de `PROJECTS` (ambos en `build.py`).
- **Añadir una furgoneta**: copia un bloque de `content_furgonetas.py` y adáptalo.
- **Formulario**: los mensajes llegan por email vía Web3Forms (clave `WEB3FORMS_KEY` en `build.py`).

## Blog
- Los artículos se escriben en Notion, en la base de datos **Artículos** de la página «Blog · Lifes Campers (camperizacionmalaga.com)».
- Al marcar un artículo como **Listo para publicar**, se le pide a Claude «publica los artículos del blog» (instrucciones completas en `CLAUDE.md`).
- En la web, cada artículo es un archivo `src/blog/<slug>.md` (ver `src/blog/_plantilla.md`) y sus fotos van en `src/blog/fotos/`. Se publica en `https://camperizacionmalaga.com/<slug>/` y aparece en el listado `/blog/`.
- **Artículos programados**: si la fecha es futura, el artículo no sale hasta ese día. Cada mañana, la tarea de GitHub Actions «Publicar artículos programados (Lifes Campers)» regenera la web de esta rama y, si toca publicar algo, hace commit y Cloudflare lo publica. La tarea está en la rama principal del repo (`kitamenagement`), en `.github/workflows/publicar-programados-lifes.yml`, porque GitHub solo ejecuta tareas programadas desde la rama principal. También se puede lanzar a mano desde GitHub → Actions → Run workflow.
- El build comprueba que los enlaces internos de los artículos existen y genera los datos de preguntas frecuentes para Google.
- El enlace «Blog» del menú aparece solo cuando hay algún artículo publicado.
- Para generar la web hace falta Python con `pillow` y `markdown` (`pip install pillow markdown`).

## Pendiente / ideas
- Páginas por ciudad (Granada, Almería, Córdoba, Sevilla…) con contenido propio de cada una.
- Redirigir `www.camperizacionmalaga.com` a `camperizacionmalaga.com` (regla de redirección en Cloudflare).
- Email con el dominio nuevo.
