# camperizacionmalaga.com

Copia estática de lifescampers.com (WordPress + Divi), lista para alojar sin servidor ni base de datos.

## Páginas
Inicio, Camperizaciones Málaga, Venta, Galería, Contacto, Aviso legal, Política de privacidad e Información de cookies.

## Cambios respecto al original
- Enlaces absolutos a `lifescampers.com` cambiados a `camperizacionmalaga.com`.
- Eliminados los restos de WordPress que necesitan servidor (feeds, wp-json, xmlrpc y estadísticas Burst).
- Vídeos recomprimidos para que ninguno pase de 25 MB (límite de Cloudflare Pages).
- El formulario de contacto envía los mensajes con Web3Forms (gratis).

## Activar el formulario de contacto
1. Entra en https://web3forms.com, escribe el email donde quieres recibir los mensajes y pulsa **Create Access Key**.
2. Busca `TU_ACCESS_KEY` en `index.html`, `contacto/index.html` y `camperizaciones-malaga/index.html`, y sustitúyelo por tu clave.

## Publicar en Cloudflare Pages (gratis)
1. Crea una cuenta en https://dash.cloudflare.com y ve a **Workers & Pages → Create → Pages → Connect to Git**.
2. Elige el repositorio `jlanrom/camperizate` y la rama donde esté esta carpeta.
3. Framework preset: **None**. Build command: vacío. Build output directory: `web`.
4. Pulsa **Save and Deploy**.
5. En **Custom domains**, añade `camperizacionmalaga.com` y sigue los pasos para apuntar el DNS.
