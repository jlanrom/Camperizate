"""Envuelve app.html en un documento completo para la web (public/index.html).
app.html es la fuente: editadla a ella y volved a ejecutar  python3 build.py"""
from pathlib import Path
here = Path(__file__).parent
app = (here / "app.html").read_text(encoding="utf-8")
head = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="robots" content="noindex">\n')
# título y estilos al <head>, resto al <body>
i = app.index("</style>") + len("</style>")
html = head + app[:i] + "\n</head>\n<body>\n" + app[i:] + "\n</body>\n</html>\n"
(here / "public" / "index.html").write_text(html, encoding="utf-8")
print("public/index.html generado")
