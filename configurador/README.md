# Configurador Lifes Campers (beta)

El cliente diseña su camper en 5 pasos y el dibujo de la furgo cambia con cada elección:

1. **Furgoneta**: si ya la tiene o no, marca, año, color, longitud L1–L4 y altura H1–H3.
2. **Distribución**: plazas (2 o 4), cama (posición y tipo), baño y ducha, cocina, nevera, altillos y armario, más un campo libre de prioridades.
3. **Acabados**: estilo de partida y, por separado, suelo, paredes, techo, estructura de los muebles, puertas y encimera.
4. **Electricidad**: pack estándar y extras.
5. **Resumen y datos de facturación**.

En la vista de planta el cliente puede **arrastrar los muebles** (cocina, baño, nevera, armario, banco, mesa…) al lado y la altura que quiera, y añadir o quitar módulos con los botones de debajo. Si dos muebles se solapan o algo tapa la puerta, salen en rojo. Las posiciones llegan a Notion dentro de «Distribución».

El dibujo tiene tres vistas: exterior (cambia con L/H y color), planta (dónde va cada mueble) e interior (paredes, techo, suelo y muebles con sus colores). Si algo no cabe en la medida elegida, avisa y recomienda la medida que sí vale.

Al enviar, se crea una ficha en Notion → **Configuraciones de clientes · Málaga**, en estado «Nueva».

## Tres versiones (todas salen de `app.html`)

| Página | Para quién | Qué pide |
|---|---|---|
| `index.html` | Clientes | 6 pasos sencillos: furgo, viaje y cama, estilo, cocina, extras y datos. Sin preguntas técnicas. |
| `acabados.html` | Clientes que ya tienen la distribución hablada | Furgo, paredes, suelo, techo, muebles y datos. |
| `taller.html` | El taller, en la reunión con el cliente | Todo: distribución con plano editable, acabados, extras y la hoja de trabajo en pantalla. |

## Hoja de trabajo

Cada envío crea en Notion una ficha con la **hoja de trabajo** para los trabajadores: techo, paredes, puertas de la furgo,
mobiliario (cascos, puertas, cama, tiradores, perfiles de aluminio, canteado, encimera, azulejos), cocina, baño,
electrónica, depósitos, ventanas, claraboyas y extras.

- Lo que eligió el cliente sale como punto normal.
- Lo que pone el taller por defecto (pack eléctrico, depósitos, tiradores…) sale como **casilla «por defecto, confirmar»**.
- Lo que nadie ha decidido (perfiles de aluminio, canteado, marca de nevera, medidas de ventanas…) sale como **casilla «POR DEFINIR»**.

Los valores por defecto del taller están en `TALLER_DEF`, dentro de `app.html`.

## Vista 3D, foto y lista de compra

- **Vista 3D**: perspectiva desde la cabina hacia atrás con los materiales elegidos (pestaña «3D»). Es orientativa, no una foto.
- **Descripción para la foto**: `promptFoto()` redacta el texto para pegarlo en un generador de imágenes (ChatGPT, Gemini…).
  Sale en la versión de taller y en la ficha de Notion. Para que la foto se genere sola hace falta conectar un servicio de
  imágenes con clave propia (coste por imagen); no está hecho.
- **Lista de compra**: `listaCompra()` calcula materiales y cantidades con las medidas del modelo (m² de paredes, techo y
  suelo, tableros HPL, tiradores, bisagras, cierres, encimera, azulejo, electricidad, agua, ventanas, claraboyas y extras).
  Sale en la versión de taller y como tabla en la ficha de Notion. Formatos supuestos (tablero HPL 3,05 × 1,30 m, caja de
  suelo 2,2 m², merma 15 %) en `FORMATOS`.

## Archivos

- `app.html`: la página entera (HTML, CSS y JS). **El catálogo está arriba del `<script>`**: `MODELOS` (medidas por marca), `MATERIALES`, `ESTILOS`, `CAMAS`, `COMEDORES`, `FUEGOS`, `SALPICADERO`, `BANO_*`, `PACK_ESTANDAR`, `EXTRAS`. Para cambiar maderas, colores, fotos u opciones, editad ahí.
- `public/img/op/`: fotos de las opciones, sacadas de camperizacionmalaga.com/opciones-y-acabados (320 px).
- `python3 build.py`: genera a partir de `app.html` las dos versiones:
  - `public/index.html`: configurador completo.
  - `public/acabados.html`: versión corta (furgo, paredes, suelo, techo, muebles y datos). Es el mismo código con `window.MODO_SIMPLE = true`; los pasos están en `STEPS`.
  Ejecutadlo tras cada cambio.
- `src/index.js`: Worker de Cloudflare que sirve la web y guarda la configuración en Notion.

## Ponerlo en marcha (una vez)

1. **Notion**: Configuración → Conexiones → Desarrollar integraciones → Nueva integración interna «Configurador». Copiad su token (`ntn_…`).
2. Abrid la base «Configuraciones de clientes · Málaga» → `•••` → Conexiones → añadir «Configurador».
3. **Cloudflare**: Workers → Crear → Importar repositorio `jlanrom/Camperizate`, directorio raíz `configurador`.
4. En el Worker: Settings → Variables and Secrets → Secret `NOTION_TOKEN` con el token del paso 1.
5. Opcional: dominio propio, por ejemplo `configura.camperizacionmalaga.com`.

Mientras no esté conectado, el último paso muestra el resumen para copiarlo y mandarlo por WhatsApp.

## Pendiente para la versión 1

- Fotos de las muestras de paneles y HPL (ahora son colores aproximados).
- Confirmar medidas de Master, Transit, Sprinter, Crafter y Daily (ahora aproximadas).
- Confirmar: otros suelos además del Zaragoza, HPL arena, proveedor de los frentes verde salvia y roble.
- Pack eléctrico estándar y extras confirmados, con precio.
- Medidas reales de los módulos (cocina, baño, cama…) del taller para que el aviso de «no cabe» sea exacto.
- Lista de compra automática desde la ficha congelada.
