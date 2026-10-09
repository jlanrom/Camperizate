# kitamenagement.fr

Landing page (FR, mobile-first) pour les kits d'aménagement camper amovibles, sans VASP.
Fichier unique `public/index.html` (HTML + CSS + JS inline, aucune dépendance), images WebP dans `public/img/`.

## Déploiement Cloudflare

Option A — Worker (static assets), depuis ce dossier :

    npx wrangler deploy

Puis Workers & Pages → kitamenagement → Settings → Domains & Routes → ajouter `kitamenagement.fr`.

Option B — Cloudflare Pages : créer un projet relié au repo, *root directory* `kitamenagement`,
*build command* vide, *output directory* `public`.

## À compléter avant mise en ligne

- Liens boutique : tous les boutons « Commander » pointent vers `https://camperizatetodoen1.com/`
  (+ UTM). Pour des liens produit précis, modifier `SHOP` / la fonction `utm()` en bas du fichier.
- Mentions légales / politique de confidentialité (obligatoires en France) : pages non incluses.
