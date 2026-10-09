# kitamenagement.fr

Landing page (FR, mobile-first) pour les kits d'aménagement camper amovibles, sans VASP.
Fichier unique `public/index.html` (HTML + CSS + JS inline, aucune dépendance), images WebP dans `public/img/`.

## Déploiement Cloudflare

Option A — Worker (static assets), depuis ce dossier :

    npx wrangler deploy

Puis Workers & Pages → kitamenagement → Settings → Domains & Routes → ajouter `kitamenagement.fr`.

Option B — Cloudflare Pages : créer un projet relié au repo, *root directory* `kitamenagement`,
*build command* vide, *output directory* `public`.

## Pages

- `/` — landing page
- `/mentions-legales/` — mentions légales (Camperizate Todo en 1, S.L.U.)
- `/politique-de-confidentialite/` — politique de confidentialité / cookies (aucun cookie déposé)

## Liens

- Produits : pages françaises de la boutique `https://www.camperizatetodoen1.com/fr/kit-camperizacion/<modèle>/`
  (avec paramètres UTM). Le sélecteur de véhicule met à jour les boutons des fiches vers le modèle choisi.
- Contact (« Écrivez-nous ») : formulaire `https://tally.so/r/OD6BOp`, le même que le bouton WhatsApp
  de camperizatetodoen1.com.
