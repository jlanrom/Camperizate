# Cambiar los vídeos de las fichas

Los vídeos de cada modelo están en **`tools/videos.csv`**, una fila por vídeo:

| modele | url | titre |
| --- | --- | --- |
| berlingo | https://www.youtube.com/watch?v=fuLKMpnw2x8 | Le kit Berlingo en vidéo |

- `modele`: el slug de la ficha (la parte final de la URL: `kitamenagement.fr/kit-amenagement/berlingo/` → `berlingo`).
- `url`: cualquier enlace de YouTube (`youtube.com/watch?v=…`, `youtu.be/…`, `/shorts/…`) o solo el código.
- `titre`: el texto que sale sobre la miniatura (en francés).
- El orden de las filas es el orden en la página. Para quitar un vídeo, borra su fila.

## Formas de editarlo

1. **En GitHub**: abre `tools/videos.csv` en la rama `kitamenagement`, pulsa el lápiz, cambia las filas y guarda
   («Create a new branch and start a pull request»). Pídele a Claude que regenere las páginas en ese PR.
2. **Con Claude**: pásale las URL («Berlingo: estos dos vídeos…») o el CSV editado en Excel/Sheets; actualiza el CSV,
   ejecuta `python3 tools/build.py` y abre el PR.

Si un modelo no está en el CSV, se usan los vídeos por defecto de `tools/catalogue.py`.
