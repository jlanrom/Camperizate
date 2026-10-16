"""Traduction d'une page générée en français vers une autre langue (aujourd'hui : l'italien).

Principe : les gabarits de build.py écrivent en français ; pour l'Italie on génère les mêmes pages avec les
réglages italiens (domaine, livraison, liens Stripe), puis ce module :
  1. remplace chaque texte visible par sa traduction (tools/sites/it_textes.py : TEXTES exacts, puis MOTIFS) ;
  2. traduit les attributs lisibles (alt, title, aria-label, label, placeholder, meta description/og) et le JSON-LD ;
  3. applique SCRIPTS (remplacements dans le JavaScript) ;
  4. remplace les chemins français par les chemins italiens (CHEMINS) et le domaine.
Un texte sans traduction reste en français et est listé dans tools/sites/it_a_traduire.txt : le build échoue
pour qu'on ne publie pas une page à moitié traduite.
"""
import html
import json
import re

TOKENS = re.compile(r"(<!--.*?-->|<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>)", re.S)
LETTRES = re.compile(r"[A-Za-zÀ-ÿ]{2}")
ATTRS = re.compile(r'\b(alt|title|aria-label|label|placeholder)="([^"]*)"')
META = re.compile(r'(<meta\s+(?:name="description"|property="og:(?:title|description)")\s+content=")([^"]*)(")')
CLES_JSON = {"name", "description", "text", "headline"}


def _motif(cle):
    parties = cle.split("{}")
    return re.compile("^" + "(.+?)".join(re.escape(p) for p in parties) + "$", re.S)


class Localiseur:
    def __init__(self, cfg, site_source, noms=()):
        self.cfg = cfg
        self.noms = set(noms) | set(getattr(cfg, "NOMS", ()))  # noms propres (modèles) : ne se traduisent pas
        self.site_source = site_source
        self.textes = cfg.TEXTES
        self.motifs = sorted(((_motif(k), v) for k, v in cfg.MOTIFS.items()), key=lambda m: -len(m[0].pattern))
        self.scripts = cfg.SCRIPTS
        self.chemins = sorted(cfg.CHEMINS.items(), key=lambda kv: -len(kv[0]))
        self.manquants = {}
        self.utilises = set()
        self.page_courante = ""

    # --- textes -------------------------------------------------------------------------------
    def traduire(self, texte):
        """Traduction d'un texte (sans balises), ou None."""
        if not LETTRES.search(texte):
            return texte
        if texte in self.textes:
            self.utilises.add(texte)
            return self.textes[texte]
        for rx, rempl in self.motifs:
            m = rx.match(texte)
            if m:
                morceaux = [self.traduire(g) for g in m.groups()]
                if all(x is not None for x in morceaux):
                    return rempl.format(*morceaux)
        if texte in self.noms:
            return texte
        return None

    def _ou_signaler(self, texte):
        t = self.traduire(texte)
        if t is None:
            self.manquants.setdefault(texte, self.page_courante)
            return texte
        return t

    def _texte_brut(self, brut):
        source = html.unescape(brut)
        coeur = source.strip()
        if not coeur or not LETTRES.search(coeur):
            return brut
        debut = source[: len(source) - len(source.lstrip())]
        fin = source[len(source.rstrip()):]
        return debut + html.escape(self._ou_signaler(coeur), quote=False) + fin

    def _attr(self, m):
        valeur = html.unescape(m.group(2)).strip()
        if not LETTRES.search(valeur) or valeur.startswith(("http", "/", "#")):
            return m.group(0)
        return f'{m.group(1)}="{html.escape(self._ou_signaler(valeur))}"'

    def _json(self, x):
        if isinstance(x, dict):
            return {k: (self._ou_signaler(v) if k in CLES_JSON and isinstance(v, str) else self._json(v)) for k, v in x.items()}
        if isinstance(x, list):
            return [self._json(v) for v in x]
        return x

    def _balise(self, b):
        if b.startswith("<script"):
            if 'type="application/ld+json"' in b:
                debut, corps, fin = re.match(r"(<script[^>]*>)(.*)(</script>)", b, re.S).groups()
                data = self._json(json.loads(corps))
                return f"{debut}\n{json.dumps(data, ensure_ascii=False, indent=1)}\n{fin}"
            for fr, it in self.scripts:
                if fr in b:
                    self.utilises.add(("script", fr))
                    b = b.replace(fr, it)
            return b
        if b.startswith(("<style", "<!--")):
            return b
        if b.startswith("<html"):
            return b.replace('lang="fr"', f'lang="{self.cfg.LANG}"')
        if b.startswith("<meta") and 'property="og:locale"' in b:
            return b.replace("fr_FR", self.cfg.LOCALE)
        b = META.sub(lambda m: m.group(1) + html.escape(self._ou_signaler(html.unescape(m.group(2)).strip())) + m.group(3), b)
        return ATTRS.sub(self._attr, b)

    # --- chemins ------------------------------------------------------------------------------
    def chemin(self, texte):
        """Remplace le domaine et les chemins français dans tout le document."""
        texte = texte.replace(self.site_source, self.cfg.SITE)
        for fr, it in self.chemins:
            texte = re.sub(r"""(?:(?<=["'(=\s])|(?<=\.it)|(?<=\.fr))""" + re.escape(fr), it, texte)
        return texte

    def chemin_fichier(self, chemin):
        """kit-amenagement/berlingo/index.html -> kit-camper/berlingo/index.html"""
        for fr, it in self.chemins:
            if ("/" + chemin).startswith(fr):
                return it[1:] + chemin[len(fr) - 1:]
        return chemin

    # --- page ---------------------------------------------------------------------------------
    def page(self, doc, xml=False):
        if not xml:
            m = re.search(r"<title>(.*?)</title>", doc, re.S)
            self.page_courante = html.unescape(m.group(1)) if m else ""
            parties = TOKENS.split(doc)
            doc = "".join(self._balise(p) if p.startswith("<") else self._texte_brut(p) for p in parties if p)
        return self.chemin(doc)

    def rapport(self, fichier):
        """Écrit la liste des textes sans traduction. Renvoie True si tout est traduit."""
        inutiles = [k for k in self.textes if k not in self.utilises]
        lignes = [f"# Textes sans traduction : {len(self.manquants)}. Les ajouter dans tools/sites/it_textes.py.", ""]
        lignes += [f"{json.dumps(k, ensure_ascii=False)}: \"\",  # {p}" for k, p in sorted(self.manquants.items())]
        lignes += ["", f"# Traductions jamais utilisées (texte français modifié ou supprimé ?) : {len(inutiles)}", ""]
        lignes += [json.dumps(k, ensure_ascii=False) for k in sorted(inutiles)]
        scripts_inutiles = [fr for fr, _ in self.scripts if ("script", fr) not in self.utilises]
        lignes += ["", f"# Remplacements SCRIPTS jamais utilisés : {len(scripts_inutiles)}", ""]
        lignes += [json.dumps(k, ensure_ascii=False) for k in scripts_inutiles]
        fichier.write_text("\n".join(lignes) + "\n", encoding="utf-8")
        print(f"Italie : {len(self.manquants)} textes sans traduction, {len(inutiles)} traductions inutilisées "
              f"({fichier.name})")
        return not self.manquants and not scripts_inutiles
