# Visibilité des produits : Google, Gemini, Bing/Copilot, Perplexity, ChatGPT

Ce que le site fournit (généré par `python3 tools/build.py`, pour la France et l'Italie) :

| Fichier | France | Italie | Sert à |
|---|---|---|---|
| Flux produits (format Google Shopping) | https://kitamenagement.fr/feeds/produits.xml | https://kitcampermodulare.it/feeds/produits.xml | Google Merchant Center, Microsoft Merchant Center, Perplexity |
| Données structurées `ProductGroup` + `Offer` sur chaque fiche | /kit-amenagement/<modèle>/ | /kit-camper/<modello>/ | Google (fiches marchandes), ChatGPT, Perplexity, Copilot, Claude (lecture des pages) |
| `llms.txt` | /llms.txt | /llms.txt | Résumé du catalogue pour les assistants IA |
| `robots.txt` | /robots.txt | /robots.txt | Autorise moteurs et assistants IA |

Flux : 264 offres par pays (44 véhicules × 3 finitions × avec/sans matelas), prix TTC, livraison du pays,
délai de fabrication 5 à 15 jours ouvrés, `identifier_exists = no` (produit fabriqué sur mesure, marque Camperizate).
Les liens mènent à la fiche du modèle (prix affichés dans le tableau) ou à la boutique présélectionnée.

## À faire une fois (comptes, par pays)

1. **Google Merchant Center** (Google Search, Shopping, Images, Maps, AI Mode, Gemini) — gratuit
   - merchants.google.com → créer un compte par site (FR, IT), pays de vente France / Italie, langue FR / IT.
   - Valider le domaine (le plus simple : avec la Search Console du domaine).
   - Produits → Sources de données → Ajouter → « Fichier » → **Récupération planifiée** (fetch) avec l'URL du flux, tous les jours.
   - Activer les **fiches gratuites** (free listings) dans « Canaux / Applications ».
   - Livraison : laisser celle du flux, ou recopier : FR 200 € ludospace, 250 € van/fourgon ; IT 250 € / 300 €.
   - Retours : kits, matelas, occultants sans retour (fabriqués sur mesure).
2. **Microsoft Merchant Center** (Bing Shopping, Copilot) — gratuit
   - ads.microsoft.com → Outils → Microsoft Merchant Center → créer une boutique, valider le domaine.
   - Flux : « Importer depuis Google Merchant Center » ou URL du flux en récupération planifiée.
3. **Perplexity** — perplexity.ai/merchants : candidature gratuite, donner l'URL du flux (format Google accepté).
4. **ChatGPT** — le flux marchand d'OpenAI est aujourd'hui limité aux États-Unis, au Canada et au Mexique. En France
   et en Italie, ChatGPT trouve les produits en lisant les pages (OAI-SearchBot) : les fiches et les données structurées
   suffisent. Candidature pour plus tard : chatgpt.com/merchants.
5. **Cloudflare** — vérifier que les robots IA ne sont pas bloqués par le tableau de bord (les nouveaux domaines bloquent
   parfois les robots IA par défaut) : Security / AI Crawl Control → autoriser OAI-SearchBot, ChatGPT-User, PerplexityBot,
   Claude-SearchBot, Bingbot ; désactiver « Block AI bots » et la « Managed robots.txt » qui ajoute des interdictions.
6. **Search Console / Bing Webmaster Tools** — soumettre le sitemap des deux sites.
