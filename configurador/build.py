"""Genera las versiones del configurador a partir de app.html (la fuente: editad solo app.html).
  public/index.html     configurador para clientes (sencillo, 6 pasos)
  public/taller.html    configurador completo del taller, con plano editable y hoja de trabajo
  public/acabados.html  versión corta: furgo, paredes, suelo, techo, muebles y datos
  taller.html, simple.html  las mismas como fragmento (vista previa en claude.ai; app.html es la de clientes)
Uso:  python3 build.py"""
from pathlib import Path
here = Path(__file__).parent
app = (here / "app.html").read_text(encoding="utf-8")
TITULO = "<title>Configurador Lifes Campers</title>"
assert app.startswith(TITULO)

def modo(titulo, m):
    return app.replace(TITULO, "<title>" + titulo + "</title>\n<script>window.MODO=\"" + m + "\"</script>", 1)

def documento(frag):
    head = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<meta name="robots" content="noindex">\n')
    i = frag.index("</style>") + len("</style>")
    return head + frag[:i] + "\n</head>\n<body>\n" + frag[i:] + "\n</body>\n</html>\n"

taller = modo("Configurador de taller", "taller")
acabados = modo("Acabados Lifes Campers", "acabados")
(here / "taller.html").write_text(taller, encoding="utf-8")
(here / "simple.html").write_text(acabados, encoding="utf-8")
(here / "public" / "index.html").write_text(documento(app), encoding="utf-8")
(here / "public" / "taller.html").write_text(documento(taller), encoding="utf-8")
(here / "public" / "acabados.html").write_text(documento(acabados), encoding="utf-8")
print("public/index.html, public/taller.html, public/acabados.html (+ taller.html, simple.html) generados")
