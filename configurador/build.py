"""Genera las dos versiones del configurador a partir de app.html (la fuente: editad solo app.html).
  public/index.html     configurador completo
  public/acabados.html  versión corta: furgo, paredes, suelo, techo, muebles y datos
  simple.html           versión corta como fragmento (para la vista previa en claude.ai)
Uso:  python3 build.py"""
from pathlib import Path
here = Path(__file__).parent
app = (here / "app.html").read_text(encoding="utf-8")
TITULO = "<title>Configurador Lifes Campers</title>"
assert app.startswith(TITULO)
simple = app.replace(TITULO, "<title>Acabados Lifes Campers</title>\n<script>window.MODO_SIMPLE=true</script>", 1)
(here / "simple.html").write_text(simple, encoding="utf-8")

def documento(frag):
    head = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<meta name="robots" content="noindex">\n')
    i = frag.index("</style>") + len("</style>")
    return head + frag[:i] + "\n</head>\n<body>\n" + frag[i:] + "\n</body>\n</html>\n"

(here / "public" / "index.html").write_text(documento(app), encoding="utf-8")
(here / "public" / "acabados.html").write_text(documento(simple), encoding="utf-8")
print("public/index.html, public/acabados.html y simple.html generados")
