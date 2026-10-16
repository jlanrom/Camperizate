# Fotos de las fichas de modelo

## Cómo pasarme las fotos

1. Crea una carpeta en tu ordenador, por ejemplo `fotos-fr`.
2. Dentro, **una subcarpeta por modelo** con el nombre del modelo: `Berlingo`, `Kangoo`, `Transporter`…
   También vale poner el modelo al principio del nombre del archivo: `berlingo-salon.jpg`, `kangoo-1.jpg`.
3. Ordena las fotos por nombre: **la primera será la foto principal** de la ficha y las demás irán a la galería.
4. Pásamelas: adjúntalas en el chat (sueltas o en un .zip) o dame acceso a la carpeta de tu ordenador.

Valen fotos directas del móvil (jpg, png; heic si se puede convertir). No hace falta reducirlas.

## Qué hago con ellas (todas de golpe)

`python3 tools/photos.py <carpeta> [opciones]`:

- Endereza según la orientación del móvil y **borra los metadatos** (incluida la ubicación GPS).
- Recorta todas al mismo formato si se pide: `--ratio 4:3` (recomendado para la ficha) o `--ratio 1:1`.
- Ajusta luz y contraste en bloque si se pide: `--luminosite 1.1` (+10 %), `--contraste 1.05`.
- Las reduce a 1600 px y 800 px y las convierte a WebP (pesan unas 10 veces menos).
- Las guarda en `public/img/modeles/<modelo>/1.webp, 2.webp…` y las apunta en `tools/photos.json`.
- Si no reconoce un modelo, lo dice y no lo procesa.

Por defecto **añade** las fotos a las que ya hay. Con `--remplacer` sustituye las del modelo.
Después, `python3 tools/build.py` regenera las fichas con las fotos nuevas.

## Textos alternativos (alt)

Cada foto recibe un texto alternativo por defecto («Kit d'aménagement amovible Citroën Berlingo, photo 1»).
Se cambia en `tools/photos.json`; lo ideal es describir lo que se ve («Kit Berlingo en mode lit, matelas gris»).
Puedo escribirlos yo viendo las fotos.

## Nombres de modelo que reconoce

Nombre corto o nombre de la carpeta (mayúsculas y acentos dan igual):

| Ludospace | Van compacto | Gran furgón |
| --- | --- | --- |
| Berlingo · Partner · Rifter · Kangoo · Caddy · Combo Life · Doblo · Proace City · Townstar · Citan · Tourneo Connect · Courier · Dokker · Jogger | Trafic · Transporter · Caravelle · Vito · Expert · Traveller · Jumpy · SpaceTourer · Scudo · Talento · Vivaro · Proace · Transit Custom · NV200 · NV300 · H1 | Ducato |

También vale el nombre técnico (slug) de cada ficha: `renault-kangoo`, `transporter-t4-t5-t6`, `jumper-boxer-transit`…
