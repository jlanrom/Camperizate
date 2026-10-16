#!/usr/bin/env python3
"""Traite en masse les photos des fiches modèle.

Usage :
    python3 tools/photos.py DOSSIER [--ratio 4:3] [--luminosite 1.0] [--contraste 1.0] [--remplacer]

DOSSIER contient les photos brutes, rangées au choix :
    DOSSIER/berlingo/IMG_1234.jpg      (un sous-dossier par modèle)
    DOSSIER/berlingo-1.jpg             (le modèle en début de nom de fichier)
Le nom du modèle peut être le slug (« renault-kangoo ») ou le nom court (« Kangoo »), accents et
majuscules ignorés. Formats : jpg, jpeg, png, webp (heic si pillow-heif est installé).

Pour chaque photo : rotation selon l'EXIF, recadrage centré optionnel (--ratio), réglage
luminosité/contraste optionnel, redimensionnement à 1600 px de large, export WebP qualité 80
(+ une version 800 px), métadonnées supprimées (GPS compris).
Sortie : public/img/modeles/<slug>/<n>.webp et <n>-800.webp, ordre alphabétique des fichiers sources.
La 1re photo devient l'image principale de la fiche, les suivantes la galerie.

tools/photos.json garde la liste des photos et leur texte alternatif (alt), modifiable à la main.
Par défaut les photos s'ajoutent à celles déjà présentes ; --remplacer efface d'abord les photos
des modèles traités. Relancer ensuite : python3 tools/build.py
"""
import argparse
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}
except ImportError:
    EXTS = {".jpg", ".jpeg", ".png", ".webp"}

ROOT = build.ROOT
SORTIE = build.PUBLIC / "img" / "modeles"
MANIFESTE = build.PHOTOS_JSON
LARGEURS = (1600, 800)


def norm(txt):
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", txt).strip("-")


def index_modeles():
    idx = {}
    for m in build.MODELES:
        cles = [m["slug"], norm(m["court"]), norm(m["nom"])] + [v for v, _l, _c in m["variantes"]]
        for cle in cles:
            idx[cle] = m["slug"]
    return idx


def trouver_modele(nom, idx):
    n = norm(nom)
    if n in idx:
        return idx[n]
    # le plus long préfixe connu (« renault-kangoo-3 » -> renault-kangoo)
    for cle in sorted(idx, key=len, reverse=True):
        if n.startswith(cle + "-") or n == cle:
            return idx[cle]
    return None


def collecter(dossier, idx):
    par_modele, inconnus = {}, []
    for f in sorted(dossier.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in EXTS or f.name.startswith("."):
            continue
        rel = f.relative_to(dossier)
        cle = rel.parts[0] if len(rel.parts) > 1 else f.stem
        slug = trouver_modele(cle, idx)
        if slug:
            par_modele.setdefault(slug, []).append(f)
        else:
            inconnus.append(str(rel))
    return par_modele, inconnus


def recadrer(img, ratio):
    if not ratio:
        return img
    a, b = (float(x) for x in ratio.split(":"))
    cible = a / b
    w, h = img.size
    if w / h > cible:
        nw = int(h * cible)
        return img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = int(w / cible)
    return img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))


def traiter(src, dest_base, args):
    img = Image.open(src)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img = recadrer(img, args.ratio)
    if args.luminosite != 1.0:
        img = ImageEnhance.Brightness(img).enhance(args.luminosite)
    if args.contraste != 1.0:
        img = ImageEnhance.Contrast(img).enhance(args.contraste)
    tailles = {}
    for i, largeur in enumerate(LARGEURS):
        out = img if img.width <= largeur else img.resize((largeur, round(img.height * largeur / img.width)), Image.LANCZOS)
        nom = f"{dest_base.name}.webp" if i == 0 else f"{dest_base.name}-{largeur}.webp"
        out.save(dest_base.parent / nom, "WEBP", quality=80, method=6)
        tailles[largeur] = out.size
    return tailles[LARGEURS[0]]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dossier", type=Path)
    ap.add_argument("--ratio", help="recadrage centré, ex. 4:3 ou 1:1")
    ap.add_argument("--luminosite", type=float, default=1.0, help="ex. 1.1 = +10 %%")
    ap.add_argument("--contraste", type=float, default=1.0, help="ex. 1.05 = +5 %%")
    ap.add_argument("--remplacer", action="store_true", help="efface les photos existantes des modèles traités")
    args = ap.parse_args()

    idx = index_modeles()
    par_modele, inconnus = collecter(args.dossier, idx)
    manifeste = json.loads(MANIFESTE.read_text(encoding="utf-8")) if MANIFESTE.exists() else {}
    noms = {m["slug"]: m["nom"] for m in build.MODELES}

    for slug, fichiers in sorted(par_modele.items()):
        dest = SORTIE / slug
        if args.remplacer and dest.exists():
            shutil.rmtree(dest)
            manifeste[slug] = []
        dest.mkdir(parents=True, exist_ok=True)
        liste = manifeste.setdefault(slug, [])
        n = max([int(p["fichier"].split(".")[0]) for p in liste] + [0])
        for f in fichiers:
            n += 1
            w, h = traiter(f, dest / str(n), args)
            liste.append({"fichier": f"{n}.webp", "alt": f"Kit d'aménagement amovible {noms[slug]}, photo {n}",
                          "w": w, "h": h, "source": f.name})
        print(f"{slug:24} {len(fichiers):3} photo(s) -> public/img/modeles/{slug}/")

    MANIFESTE.write_text(json.dumps(manifeste, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if inconnus:
        print("\nModèle non reconnu (renommer le fichier ou le dossier) :")
        for x in inconnus:
            print("  ", x)
        print("Noms acceptés :", ", ".join(sorted(m["slug"] for m in build.MODELES)))
    print(f"\n{sum(len(v) for v in par_modele.values())} photo(s) traitée(s). Lancer ensuite : python3 tools/build.py")


if __name__ == "__main__":
    main()
