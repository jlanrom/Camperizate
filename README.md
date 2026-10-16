# kitamenagement.fr

Landing page (FR, mobile-first) pour les kits d'aménagement camper amovibles, sans VASP.
Fichier unique `public/index.html` (HTML + CSS + JS inline, aucune dépendance), images WebP dans `public/img/`.

## Déploiement Cloudflare

Worker Cloudflare : `fr-camperizate` · branche de production : `kitamenagement`
(chaque push sur cette branche redéploie automatiquement le site).

Option A — Worker (static assets), depuis la racine de cette branche :

    npx wrangler deploy

Puis Workers & Pages → kitamenagement → Settings → Domains & Routes → ajouter `kitamenagement.fr`.

Option B — Cloudflare Pages : créer un projet relié au repo, *production branch* `kitamenagement`, *root directory* vide,
*build command* vide, *output directory* `public`.

## Pages

- `/` — landing page (écrite à la main)
- `/boutique/` — boutique, paiement par liens Stripe (générée)
- `/kit-amenagement/` — catalogue des modèles (généré)
- `/accessoires/`, `/occultants-isolants/`, `/matelas-camper/` — options et accessoires (générés)
- `/guide-kit-meubles-camper/` — guide (généré, remplace /fr/kitmueblescamper/)
- `/contact/` — showroom de Nîmes et atelier (généré)
- `/kit-amenagement/<modèle>/` — fiches modèle (générées, une par modèle de `MODELES`)
- `/merci/` — retour après paiement, noindex (générée)
- `/conditions-generales-de-vente/` — CGV
- `/mentions-legales/` — mentions légales (Camperizate Todo en 1, S.L.U.)
- `/politique-de-confidentialite/` — politique de confidentialité / cookies (aucun cookie déposé)

## Liens

- Produits : les boutons « Commander » de la landing et des fiches mènent à `/boutique/`
  avec le modèle et la finition présélectionnés (`?modele=…&finition=…`).
- Contact (« Écrivez-nous ») : formulaire `https://tally.so/r/OD6BOp`, le même que le bouton WhatsApp
  de camperizatetodoen1.com.

## Pages générées

`python3 tools/build.py` génère la boutique, les fiches modèle, la page merci, `public/sitemap.xml`
et `tools/redirections.json` (ancienne URL camperizatetodoen1.com/fr/… → nouvelle fiche, pour le
futur script de redirection côté Webnode). Ne pas modifier ces pages à la main : modifier le script
puis le relancer.

- Liens de paiement : dictionnaire `STRIPE` en haut du script. Guide de création : `docs/STRIPE.md`.
- Données (modèles, prix, options, accessoires, redirections) : `tools/catalogue.py`, repris du formulaire Tally
  « Configura tu mueble ». Ajouter un modèle = ajouter une entrée à `MODELES`.
- Redirections : `tools/redirections.json` (table) et `docs/redirection-webnode.html` (script à coller dans
  l'en-tête de Webnode le jour de la bascule ; voir docs/REDIRECTION.md).
- La landing est écrite à la main ; le script ne remplace que le bloc entre `<!-- MODELES:debut -->` et `<!-- MODELES:fin -->` et la liste `var FICHES=[…]`.
- Photos des fiches : `python3 tools/photos.py <dossier>` puis `python3 tools/build.py` (voir `docs/PHOTOS.md`).
