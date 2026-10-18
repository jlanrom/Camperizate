"""Site français : kitamenagement.fr (dossier public/).

Ce qui est propre à la France. Le reste (catalogue, prix des kits, gabarits, styles) est commun : tools/catalogue.py
et tools/build.py. Les textes français sont la langue source, écrits directement dans tools/build.py.
"""
CODE = "fr"
SITE = "https://kitamenagement.fr"
SORTIE = "public"
# Livraison par catégorie de kit (TTC)
LIVRAISON = {"mini": 200, "moyen": 250, "grand": 250}

# Liens de paiement Stripe (Payment Links), voir docs/STRIPE.md
STRIPE = {
    # Kits : kit-<catégorie>-<finition>-<matelas sans|avec>-<retrait|livraison>
    "kit-mini-pin-sans-retrait": "https://buy.stripe.com/8x2aEW88C5EJ5vJdWD6EU01",
    "kit-mini-pin-avec-retrait": "https://buy.stripe.com/4gMdR8agKc37ganbOv6EU02",
    "kit-mini-carrossier-sans-retrait": "https://buy.stripe.com/9B6fZg9cG8QVaQ3dWD6EU03",
    "kit-mini-carrossier-avec-retrait": "https://buy.stripe.com/aFa28q9cG0kp0bpaKr6EU04",
    "kit-mini-hpl-sans-retrait": "https://buy.stripe.com/eVq9ASbkOaZ38HV8Cj6EU05",
    "kit-mini-hpl-avec-retrait": "https://buy.stripe.com/eVqbJ0ex0ebfaQ3f0H6EU06",
    "kit-moyen-pin-sans-retrait": "https://buy.stripe.com/6oU8wO88Cc376zNf0H6EU07",
    "kit-moyen-pin-avec-retrait": "https://buy.stripe.com/eVq5kCfB44AF4rF19R6EU08",
    "kit-moyen-carrossier-sans-retrait": "https://buy.stripe.com/4gM9AS1Ke6IN7DRaKr6EU09",
    "kit-moyen-carrossier-avec-retrait": "https://buy.stripe.com/8x228q2Oi3wBcYbdWD6EU0a",
    "kit-moyen-hpl-sans-retrait": "https://buy.stripe.com/fZu28q9cG5EJ5vJg4L6EU0b",
    "kit-moyen-hpl-avec-retrait": "https://buy.stripe.com/cNidR89cG7MR0bpdWD6EU0c",
    "kit-mini-pin-sans-livraison": "https://buy.stripe.com/00w7sKdsWebf1ft9Gn6EU0d",
    "kit-mini-pin-avec-livraison": "https://buy.stripe.com/fZufZg88C1ot3nB19R6EU0e",
    "kit-mini-carrossier-sans-livraison": "https://buy.stripe.com/aFaaEWbkOc37bU7dWD6EU0f",
    "kit-mini-carrossier-avec-livraison": "https://buy.stripe.com/dRm00ifB44AFgan19R6EU0g",
    "kit-mini-hpl-sans-livraison": "https://buy.stripe.com/9B69ASgF84AFaQ35q76EU0h",
    "kit-mini-hpl-avec-livraison": "https://buy.stripe.com/6oU14mfB43wB6zNcSz6EU0i",
    "kit-moyen-pin-sans-livraison": "https://buy.stripe.com/14A3cu2Oi0kp8HV8Cj6EU0j",
    "kit-moyen-pin-avec-livraison": "https://buy.stripe.com/4gM6oG0Ga8QV2jx19R6EU0k",
    "kit-moyen-carrossier-sans-livraison": "https://buy.stripe.com/cNiaEW1Ke3wB9LZcSz6EU0l",
    "kit-moyen-carrossier-avec-livraison": "https://buy.stripe.com/aFa4gygF88QV4rF8Cj6EU0m",
    "kit-moyen-hpl-sans-livraison": "https://buy.stripe.com/dRm4gyfB4c377DRdWD6EU0n",
    "kit-moyen-hpl-avec-livraison": "https://buy.stripe.com/3cI9ASagK8QVf6jbOv6EU0o",
    # Kits grand fourgon
    "kit-grand-pin-sans-retrait": "https://buy.stripe.com/aFa3cuagK3wB3nB2dV6EU0y",
    "kit-grand-pin-avec-retrait": "https://buy.stripe.com/aFa9AS0Ga9UZ8HVf0H6EU0z",
    "kit-grand-carrossier-sans-retrait": "https://buy.stripe.com/4gMeVc4WqaZ31ft2dV6EU0A",
    "kit-grand-carrossier-avec-retrait": "https://buy.stripe.com/00w6oGfB41ot2jxaKr6EU0B",
    "kit-grand-hpl-sans-retrait": "https://buy.stripe.com/8x214m0Ga1ot2jx7yf6EU0C",
    "kit-grand-hpl-avec-retrait": "https://buy.stripe.com/9B66oGcoSd7bbU705N6EU0D",
    "kit-grand-pin-sans-livraison": "https://buy.stripe.com/6oU4gy60ud7bf6j6ub6EU0E",
    "kit-grand-pin-avec-livraison": "https://buy.stripe.com/00w8wOdsWaZ32jxcSz6EU0F",
    "kit-grand-carrossier-sans-livraison": "https://buy.stripe.com/8x25kC74y2sx9LZ6ub6EU0G",
    "kit-grand-carrossier-avec-livraison": "https://buy.stripe.com/7sY28q60ugjnaQ3g4L6EU0H",
    "kit-grand-hpl-sans-livraison": "https://buy.stripe.com/8x2cN4bkO7MR2jx6ub6EU0I",
    "kit-grand-hpl-avec-livraison": "https://buy.stripe.com/3cIdR84Wq3wB4rF8Cj6EU0J",
    # Accessoires
    "occultants": "https://buy.stripe.com/bJe3cufB40kp8HV3hZ6EU0p",
    "frigo-15": "https://buy.stripe.com/8x24gy60u0kp9LZbOv6EU0q",
    "frigo-35": "https://buy.stripe.com/00waEWfB43wB8HVcSz6EU0r",
    "batterie": "https://buy.stripe.com/5kQeVc9cG7MR0bp8Cj6EU0s",
    "batterie-onduleur": "https://buy.stripe.com/00w14mex0c378HVg4L6EU0t",
    "rechaud": "https://buy.stripe.com/5kQbJ04Wq3wBbU7dWD6EU0u",
    "rechaud-cartouches": "https://buy.stripe.com/cNi3cu3Sm4AF9LZ19R6EU0v",
    "toilettes": "https://buy.stripe.com/6oU14m1Ke0kp5vJaKr6EU0w",
    "douche": "https://buy.stripe.com/3cIeVcbkO4AF1ft19R6EU0x",
}

# Avis Google (fiche Camperizate de La Garriga). Note et nombre : à mettre à jour de temps en temps.
AVIS_GOOGLE = {"note": 4.5, "nombre": 255, "url": "https://www.google.com/maps?cid=12150316368005830472"}
# Avis affichés sur le site (vrais avis Google). traduit = texte traduit par nous depuis la langue indiquée.
AVIS = [
    dict(nom="Zoé B.", date="2026-09", note=5, vehicule="Peugeot Expert",
         texte="Nous avons commandé un kit d'aménagement pour notre Peugeot Expert et nous en sommes vraiment très contents. "
               "Le kit est pratique, bien pensé et surtout très confortable. Le matelas est vraiment top, le frigo aussi, et les "
               "occultants sont parfaitement adaptés à notre véhicule. Nous avons pu profiter pleinement de l'ensemble lors d'un "
               "road trip de plusieurs milliers de kilomètres."),
    dict(nom="Eric H.", date="", note=5, vehicule="Citroën Jumpy", traduit="espagnol",
         texte="Le kit est génial, facile à installer dans le Jumpy. Nous venons de le recevoir et nous allons faire un petit "
               "essai ce week-end. Merci et bonne chance à cette entreprise !"),
    dict(nom="Ysf K.", date="2026-06", note=5, vehicule="",
         texte="Très satisfait par la qualité du produit : tout a été réalisé avec précision et une finition irréprochable ! "
               "En arrivant à leur atelier de Barcelone, j'ai été extrêmement bien accueilli. Je recommande vivement cet atelier."),
    dict(nom="Van' Bou", date="2025-10", note=5, vehicule="",
         texte="Merci à l'équipe pour sa fiabilité, son savoir-faire, sa communication personnalisée, sa réactivité, sa rapidité. "
               "Le kit est vraiment parfait. Une expérience client 5 étoiles !"),
]
# Note et avis aussi dans les données structurées (aggregateRating, review) des produits.
AVIS_DONNEES = True
