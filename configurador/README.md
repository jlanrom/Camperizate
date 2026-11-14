# Configurador Lifes Campers (beta)

El cliente diseña su camper en 5 pasos y el dibujo de la furgo cambia con cada elección:

1. **Furgoneta**: si ya la tiene o no, marca, año, color, longitud L1–L4 y altura H1–H3.
2. **Distribución**: plazas (2 o 4), cama (posición y tipo), baño y ducha, cocina, nevera, altillos y armario, más un campo libre de prioridades.
3. **Acabados**: estilo de partida y, por separado, suelo, paredes, techo, estructura de los muebles, puertas y encimera.
4. **Electricidad**: pack estándar y extras.
5. **Resumen y datos de facturación**.

El dibujo tiene tres vistas: exterior (cambia con L/H y color), planta (dónde va cada mueble) e interior (paredes, techo, suelo y muebles con sus colores). Si algo no cabe en la medida elegida, avisa y recomienda la medida que sí vale.

Al enviar, se crea una ficha en Notion → **Configuraciones de clientes · Málaga**, en estado «Nueva».

## Archivos

- `app.html`: la página entera (HTML, CSS y JS). **El catálogo está arriba del `<script>`**: `MEDIDAS`, `MATERIALES`, `ESTILOS`, `PACK_ESTANDAR`, `EXTRAS`. Para cambiar maderas, colores u opciones, editad ahí.
- `python3 build.py`: genera `public/index.html` a partir de `app.html`. Ejecutadlo tras cada cambio.
- `src/index.js`: Worker de Cloudflare que sirve la web y guarda la configuración en Notion.

## Ponerlo en marcha (una vez)

1. **Notion**: Configuración → Conexiones → Desarrollar integraciones → Nueva integración interna «Configurador». Copiad su token (`ntn_…`).
2. Abrid la base «Configuraciones de clientes · Málaga» → `•••` → Conexiones → añadir «Configurador».
3. **Cloudflare**: Workers → Crear → Importar repositorio `jlanrom/Camperizate`, directorio raíz `configurador`.
4. En el Worker: Settings → Variables and Secrets → Secret `NOTION_TOKEN` con el token del paso 1.
5. Opcional: dominio propio, por ejemplo `configura.camperizacionmalaga.com`.

Mientras no esté conectado, el último paso muestra el resumen para copiarlo y mandarlo por WhatsApp.

## Pendiente para la versión 1

- Fotos de las muestras dentro del configurador (ahora son colores aproximados).
- Confirmar: color del suelo Zaragoza y otros suelos, HPL arena, proveedor de los frentes verde salvia y roble.
- Pack eléctrico estándar y extras confirmados, con precio.
- Medidas reales de los módulos (cocina, baño, cama…) del taller para que el aviso de «no cabe» sea exacto.
- Lista de compra automática desde la ficha congelada.
