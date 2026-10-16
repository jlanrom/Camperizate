"""Catalogue de kitamenagement.fr : modèles, prix, options, accessoires, images.

Source des prix et de la liste des véhicules : formulaire Tally « Configura tu mueble Camperízate »
(https://tally.so/forms/2EqadL), octobre 2026. Mesures et vidéos : anciennes pages
camperizatetodoen1.com/fr/ de chaque modèle.

Ce fichier ne contient que des données. Les pages sont générées par tools/build.py.
"""

T = "https://storage.tally.so/"  # images du formulaire Tally (hébergées par Tally)

# ---------------------------------------------------------------------------
# Prix (TTC) par catégorie de kit
# ---------------------------------------------------------------------------
FINITIONS = [  # clé, nom, description, prix sans matelas par catégorie, image
    ("pin", "Phénolique pin", "Contreplaqué phénolique de pin, finition bois naturel.",
     {"mini": 500, "moyen": 700, "grand": 800}, T + "b2a97ab2-3782-47d6-8e5d-04b1d5b1281a/materiales-muebles-1-X12.jpg"),
    ("carrossier", "Phénolique carrossier", "Contreplaqué phénolique antidérapant, noir. Le plus vendu.",
     {"mini": 550, "moyen": 750, "grand": 850}, T + "5c1b8d35-41db-43ef-920d-f82a3c309563/materiales-muebles-0-X10.jpg"),
    ("hpl", "HPL de peuplier", "Peuplier phénolique avec HPL, blanc ou anthracite. Notre finition premium.",
     {"mini": 800, "moyen": 1000, "grand": 1100}, T + "306e225d-2e4c-4ff7-875d-a10f4b2fc2aa/materiales-muebles-2-X14.jpg"),
]
IMAGE_HPL_ANTHRACITE = T + "e655e4dd-31c6-47fc-a770-5ca1c2d18f68/materiales-muebles-3-X17.jpg"
MATELAS = 150

CATEGORIES = {
    "mini": {"nom": "Ludospace", "pluriel": "Kits ludospace et monospace", "livraison": 200},
    "moyen": {"nom": "Van compact", "pluriel": "Kits van compact", "livraison": 250},
    "grand": {"nom": "Grand fourgon", "pluriel": "Kits grand fourgon", "livraison": 250},
}

# Groupes d'affichage (catalogue, landing). La catégorie de prix reste celle du modèle.
GROUPES = [
    ("ludospace", "Ludospaces", "mini"),
    ("monospace", "Monospaces et SUV", "mini"),
    ("van", "Vans compacts", "moyen"),
    ("fourgon", "Grands fourgons", "grand"),
]

# ---------------------------------------------------------------------------
# Options du kit (articles facultatifs sur la page de paiement Stripe)
# ---------------------------------------------------------------------------
INCLUS = [  # ce qui est livré de série
    ("Tiroir cuisine", "À droite, extractible, pour le réchaud et la vaisselle.", T + "6cca46a7-750e-424c-9af1-7bd36cc9080e/cajon-nevera.jpg"),
    ("Coffre de gauche", "Ouverture par le dessus et par l'avant.", T + "5841bf53-f090-467d-b59e-3ca5efd799a4/baul-pino-mejorado.png"),
]
OPTIONS = [  # ancre, nom, description, prix, image
    ("equerre", "Équerre rabattable sur le tiroir cuisine", "Un plan de travail qui se déplie au bout du tiroir.", 25,
     T + "af8abc34-4b58-437c-95ea-e1b6df7b584c/configuracion-especial-0-X8.jpg"),
    ("plateau", "Côté gauche : plateau", "Remplace le coffre par un plateau, idéal pour poser un frigo.", 25,
     T + "36fcc932-a705-4779-baec-984c37856438/configuracion-especial-1-X11.jpg"),
    ("tiroir-gauche", "Côté gauche : tiroir coulissant", "Remplace le coffre par un tiroir, sans équerre.", 50,
     T + "8a8ac0f2-1510-482a-9988-bba25b414bc2/configuracion-especial-2-X12.jpg"),
    ("tiroir-equerre", "Côté gauche : tiroir avec équerre rabattable", "Tiroir coulissant avec plan rabattable.", 75,
     T + "5f855939-4067-4701-af5c-e8f30f3f2f69/codex-clipboard-c1a4ac56-971a-4334-9a95-9a2971d8bbdb.png"),
    ("egouttoir", "Égouttoir", "Pour faire la vaisselle dehors.", 35,
     T + "4b38c070-de6d-4a7c-9ae7-06627f7d8531/configuracion-especial-3-X13.jpg"),
    ("version-2-1", "Version 2+1", "Kit en deux parties : un lit simple et un espace libre pour un vélo, une planche ou un kayak, "
     "ou un lit double quand on réunit les deux.", 100, T + "4b072ce3-3b84-485a-b80c-d092ca5b0c1f/configuracion-especial-4-X14.jpg"),
]

# ---------------------------------------------------------------------------
# Accessoires vendus seuls (un lien Stripe chacun)
# ---------------------------------------------------------------------------
ACCESSOIRES = [  # clé Stripe, ancre, nom, détail, prix, image
    ("occultants", "occultants", "Occultants isolants", "9 couches, sur mesure pour votre modèle", 149,
     T + "8d98c10c-92dd-4707-99bb-b8c50b90f0ba/extras-0-X8.jpg"),
    ("frigo-15", "frigo", "Frigo à compresseur 15 L", "Pour ludospace", 220,
     T + "282c1438-82f3-4bc7-978a-e49d2af18236/extras-1-X11.jpg"),
    ("frigo-35", "frigo-35", "Frigo à compresseur 35 L", "Pour van compact et grand fourgon", 300,
     T + "282c1438-82f3-4bc7-978a-e49d2af18236/extras-1-X11.jpg"),
    ("batterie", "batterie", "Batterie lithium", "Sans onduleur", 750,
     T + "015e8874-b0ed-44ce-8637-66dd880395ea/bateria-sin-inversor.png"),
    ("batterie-onduleur", "batterie-onduleur", "Batterie lithium + onduleur", "Prises 230 V à bord", 975,
     T + "ea94b591-c51c-4611-be52-360adab423e9/extras-2-X12.jpg"),
    ("rechaud", "rechaud", "Réchaud", "Réchaud seul", 29,
     T + "243ba676-56cc-4fee-be72-b30aef58c06e/extras-4-X14.jpg"),
    ("rechaud-cartouches", "rechaud-cartouches", "Réchaud + 3 cartouches", "Prêt à cuisiner", 35,
     T + "243ba676-56cc-4fee-be72-b30aef58c06e/extras-4-X14.jpg"),
    ("toilettes", "toilettes", "Toilettes portables", "Format compact, se range dans le coffre", 110,
     T + "cce9dc8f-c7cb-4bf7-8687-c98655bb6908/extras-3-X13.jpg"),
    ("douche", "douche", "Douche portable", "12 V, réservoir de 20 L", 75,
     T + "e9eab5c0-4ff1-4bed-b3d8-e4c29dd6fd6e/extras-5-X15.jpg"),
]

# ---------------------------------------------------------------------------
# Modèles : une fiche par entrée
# ---------------------------------------------------------------------------
# Champs : slug, nom, court, cat (prix), groupe, anciens (URL Webnode), titre (court, optionnel),
#          versions (texte), mesures [(libellé, valeur)], videos [(id, titre)], faq [(q, r)],
#          variantes [(valeur boutique, libellé, cat)] : la 1re = le modèle de base.
W = "/fr/kit-camperizacion/"

V_LUDO = [("bdcMn_dis2A", "Le kit ludospace en vidéo")]
V_VAN = [("nH2jGupoShc", "Le kit van compact en vidéo"), ("B5cHLnJlecc", "Montage du kit")]
V_VAN_L = [("RqTD-6W14Yc", "Le kit en vidéo"), ("Lb4JxWqnmSQ", "Le kit en mode salon")]
V_FOURGON = [("Sr2Taz2WiM0", "Le kit grand fourgon en vidéo"), ("YYaN5GDxf_4", "Le kit grand fourgon monté")]
V_MONO = [("AD8b1E6J4Wk", "Le kit pour monospace en vidéo")]

M_LUDO = [("Lit déplié", "187 cm (jusqu'à 190 cm)"), ("Largeur du kit", "115 cm"),
          ("Largeur avec matelas", "120 cm"), ("Places assises", "les 5 places restent utilisables")]
M_VAN_EXPERT = [("Lit", "185 à 190 × 130 à 135 cm"), ("Matelas", "8 cm, housse lavable"),
                ("Frigo", "logement pour un frigo jusqu'à 35 L"), ("Poids du kit", "35 à 45 kg selon la finition"),
                ("Places assises", "on conseille de garder la 2e rangée ; 3e rangée possible en version longue")]
M_VAN_LARGE = [("Lit", "185 à 190 cm"), ("Largeur du kit", "152 cm (155 cm avec matelas)"), ("Profondeur", "120 cm"),
               ("Hauteur", "environ 55 cm avec sièges, 40 à 44 cm sans sièges"),
               ("Places assises", "5 ou 6 places, ou kit posé sans sièges")]
M_FOURGON = [("Lit", "180 à 190 × 120 cm"), ("Largeur du kit", "environ 170 cm, en 3 parties"),
             ("Hauteur", "40, 44 ou 48 cm selon le montage"), ("Places assises", "5 ou 6 places selon les sièges montés"),
             ("Frigo", "logement pour un frigo à compresseur type Fr40 ou plus")]
M_MONO = [("Couchage", "1 ou 2 personnes"), ("Matelas", "sur mesure, en 3 pièces pour les véhicules bas"),
          ("Hauteur", "kit plus bas que sur un ludospace : l'habitacle est moins haut")]

MODELES = [
    # --- Ludospaces --------------------------------------------------------------------------
    dict(slug="berlingo", nom="Citroën Berlingo", court="Berlingo", cat="mini", groupe="ludospace", anciens=[W + "berlingo/"],
         versions="Berlingo M : kit ludospace. Berlingo XL : meuble 30 cm plus profond et lit jusqu'à 220 cm, au prix van compact.",
         mesures=[("Lit déplié", "187 cm (M), jusqu'à 220 cm (XL)"), ("Largeur du kit", "115 cm"), ("Largeur avec matelas", "120 cm"),
                  ("Générations", "1996-2008, 2008-2018 et depuis 2018"), ("Places assises", "les 5 places restent utilisables")],
         videos=[("fuLKMpnw2x8", "Le kit Berlingo en vidéo"), ("BfS5PiHbbbI", "Le kit monté dans un ludospace")],
         variantes=[("berlingo", "Citroën Berlingo (M)", "mini"), ("berlingo-xl", "Citroën Berlingo XL", "moyen")]),
    dict(slug="partner", nom="Peugeot Partner et Partner Tepee", court="Partner", cat="mini", groupe="ludospace",
         anciens=[W + "partner/"], titre="Peugeot Partner et Tepee",
         mesures=M_LUDO + [("Générations", "1996-2008, 2008-2018 (Partner Tepee) et depuis 2018")],
         videos=V_LUDO, variantes=[("partner", "Peugeot Partner / Partner Tepee", "mini")]),
    dict(slug="rifter", nom="Peugeot Rifter", court="Rifter", cat="mini", groupe="ludospace", anciens=[W + "rifter/"],
         versions="Rifter M : kit ludospace. Rifter XL (Long) : meuble 30 cm plus profond et lit de 220 cm, au prix van compact.",
         mesures=[("Lit déplié", "187 cm (M), 220 cm (XL)"), ("Largeur du kit", "115 cm (120 cm avec matelas)"),
                  ("Profondeur", "84 cm"), ("Hauteur", "35 cm"), ("Places assises", "les 5 places restent utilisables")],
         videos=[("fuLKMpnw2x8", "Le kit Rifter en vidéo"), ("BfS5PiHbbbI", "Le kit monté dans un ludospace")],
         variantes=[("rifter", "Peugeot Rifter (M)", "mini"), ("rifter-xl", "Peugeot Rifter XL", "moyen")]),
    dict(slug="renault-kangoo", nom="Renault Kangoo", court="Kangoo", cat="mini", groupe="ludospace", anciens=[W + "renault-kangoo/"],
         versions="Kangoo : kit ludospace. Kangoo Maxi : kit plus long, au prix van compact.",
         mesures=[("Lit déplié", "187 cm (jusqu'à 190 cm)"), ("Largeur du kit", "111 à 117 cm selon la génération"),
                  ("Largeur avec matelas", "120 cm"), ("Générations", "1997-2008, 2008-2021 et depuis 2021"),
                  ("Places assises", "les 5 places restent utilisables")],
         videos=[("5Finz42pfkI", "Le kit Kangoo en vidéo"), ("JUHMYA8Wyw4", "Le kit Kangoo en détail")],
         variantes=[("renault-kangoo", "Renault Kangoo", "mini"), ("kangoo-maxi", "Renault Kangoo Maxi", "moyen")]),
    dict(slug="caddy", nom="Volkswagen Caddy", court="Caddy", cat="mini", groupe="ludospace", anciens=[W + "caddy/"], titre="VW Caddy",
         versions="Caddy : kit ludospace. Caddy Maxi : kit plus long, au prix van compact.",
         mesures=[("Montage", "moins de 3 minutes"), ("Générations", "2004-2010, 2010-2015, 2015-2020 et depuis 2021"),
                  ("Places assises", "la banquette arrière reste utilisable")],
         videos=[("K3OmeilybmU", "Le kit Caddy en vidéo"), ("Vr_60ZhBFjk", "Le kit Caddy en détail")],
         variantes=[("caddy", "Volkswagen Caddy", "mini"), ("caddy-maxi", "Volkswagen Caddy Maxi", "moyen")]),
    dict(slug="opel-combo-life", nom="Opel Combo et Combo Life", court="Combo", cat="mini", groupe="ludospace",
         anciens=[W + "opel-combo-life/"],
         versions="Combo Life M : kit ludospace. Combo Life XL : meuble 30 cm plus profond et lit de 220 cm, nous consulter.",
         mesures=[("Lit déplié", "187 cm (M), 220 cm (XL)"), ("Largeur du kit", "115 cm (120 cm avec matelas)"),
                  ("Générations", "2001-2012, 2012-2018 et depuis 2018"), ("Places assises", "les 5 places restent utilisables")],
         videos=[("ydV4p_qIKpg", "Le kit Combo Life en vidéo")],
         variantes=[("opel-combo-life", "Opel Combo / Combo Life", "mini")]),
    dict(slug="fiat-doblo", nom="Fiat Doblò", court="Doblò", cat="mini", groupe="ludospace", anciens=[W + "fiat-doblo/"],
         versions="Doblò : kit ludospace. Doblò Maxi : kit plus long, au prix van compact.",
         mesures=M_LUDO + [("Générations", "2000-2009, 2009-2021 et depuis 2022")],
         videos=[("hc7UY43I7XY", "Le kit Doblò en vidéo")],
         variantes=[("fiat-doblo", "Fiat Doblò", "mini"), ("doblo-maxi", "Fiat Doblò Maxi", "moyen")]),
    dict(slug="proace-city", nom="Toyota Proace City", court="Proace City", cat="mini", groupe="ludospace", anciens=[W + "proace-city/"],
         versions="Proace City M : kit ludospace. Proace City L2 : meuble 30 cm plus profond et lit de 220 cm, nous consulter.",
         mesures=[("Lit déplié", "187 cm (M), 220 cm (L2)"), ("Largeur du kit", "115 cm (120 cm avec matelas)"),
                  ("Génération", "depuis 2019"), ("Places assises", "les 5 places restent utilisables")],
         videos=[("ydV4p_qIKpg", "Le kit Proace City en vidéo")],
         variantes=[("proace-city", "Toyota Proace City", "mini")]),
    dict(slug="nissan-townstar", nom="Nissan Townstar", court="Townstar", cat="mini", groupe="ludospace", anciens=[W + "nissan-townstar/"],
         mesures=[("Lit déplié", "187 cm (jusqu'à 190 cm)"), ("Largeur du kit", "117 cm (120 cm avec matelas)"),
                  ("Profondeur", "72,4 cm"), ("Génération", "depuis septembre 2021"), ("Places assises", "les 5 places restent utilisables")],
         videos=[("5Finz42pfkI", "Le kit en vidéo")], variantes=[("nissan-townstar", "Nissan Townstar", "mini")]),
    dict(slug="mercedes-citan", nom="Mercedes Citan et Classe T", court="Citan", cat="mini", groupe="ludospace", anciens=[W + "mercedes-citan/"],
         versions="Même base que le Renault Kangoo. Citan Maxi : nous consulter.",
         mesures=[("Lit déplié", "187 cm (jusqu'à 190 cm)"), ("Largeur du kit", "111 cm (1re génération), 117 cm (2e)"),
                  ("Largeur avec matelas", "120 cm"), ("Générations", "2012-2021 et depuis 2021"),
                  ("Places assises", "les 5 places restent utilisables")],
         videos=[("5Finz42pfkI", "Le kit en vidéo")], variantes=[("mercedes-citan", "Mercedes Citan / Classe T", "mini")]),
    dict(slug="tourneo-transit", nom="Ford Tourneo Connect et Transit Connect", court="Tourneo Connect", cat="mini", groupe="ludospace",
         anciens=[W + "tourneo-transit/"], titre="Ford Tourneo Connect",
         mesures=[("Lit déplié", "187 cm (jusqu'à 190 cm)"), ("Largeur du kit", "117 cm (1re et 2e génération), 115 cm (3e)"),
                  ("Profondeur", "72 cm (1re et 2e génération), 82 cm (3e)"), ("Largeur avec matelas", "120 cm"),
                  ("Générations", "2002-2013, 2013-2021 et depuis 2021 (base VW Caddy)"), ("Places assises", "les 5 places restent utilisables")],
         videos=[("K3OmeilybmU", "Le kit en vidéo"), ("Vr_60ZhBFjk", "Le kit en détail")],
         variantes=[("tourneo-transit", "Ford Transit / Tourneo Connect", "mini")]),
    dict(slug="ford-courier", nom="Ford Tourneo Courier et Transit Courier", court="Courier", cat="mini", groupe="ludospace",
         anciens=[W + "ford-courier/"], titre="Ford Tourneo Courier",
         mesures=[("Largeur du kit", "97 cm (100 à 105 cm avec matelas)"), ("Générations", "2014-2023 et depuis 2023"),
                  ("Places assises", "les 5 places restent utilisables")],
         videos=[("7NPgUG2iTzM", "Le kit Courier en vidéo"), ("hNt-xfPaCDg", "Le kit Courier en détail")],
         variantes=[("ford-courier", "Ford Transit / Tourneo Courier", "mini")]),
    dict(slug="dokker", nom="Dacia Dokker", court="Dokker", cat="mini", groupe="ludospace", anciens=[W + "dokker/"],
         mesures=[("Lit déplié", "187 cm (jusqu'à 190 cm)"), ("Largeur du kit", "114 cm (120 cm avec matelas)"),
                  ("Profondeur, kit replié", "88 cm"), ("Hauteur", "36 cm"), ("Génération", "2012-2021"),
                  ("Places assises", "les 5 places restent utilisables")],
         videos=[("aytApIpSFtY", "Le kit Dokker en vidéo"), ("EOo9NZ71VVk", "Le kit Dokker en détail")],
         variantes=[("dokker", "Dacia Dokker", "mini")]),
    dict(slug="dacia-jogger-lodgy", nom="Dacia Jogger et Lodgy", court="Jogger", cat="mini", groupe="ludospace",
         anciens=[W + "dacia-jogger-lodgy/"],
         intro="Le Jogger devient mini camping-car en quelques minutes, puis redevient une voiture familiale pour la semaine. "
               "Le kit se pose dans le coffre sans perçage : pas de VASP, carte grise inchangée.",
         mesures=[("Lit déplié", "187 cm de long"), ("Largeur du kit", "99 cm"), ("Largeur du matelas", "125 cm"),
                  ("Hauteur", "36 cm"), ("Profondeur, kit replié", "environ 95 cm"), ("Places assises", "les 5 places restent utilisables")],
         inclus=[("i-cook", "Tiroir cuisine", "Extractible, sur glissières renforcées (30 à 40 kg), pour le réchaud et la vaisselle."),
                 ("i-table", "Table extérieure", "Le couvercle du compartiment arrière se retire et sert de table."),
                 ("i-box", "Grand coffre", "À gauche, ouverture par le dessus et par l'avant."),
                 ("i-bed", "Lit dépliable", "En deux parties. Matelas sur mesure en option.")],
         fixation="Le kit repose sur trois appuis : le plancher du coffre, un premier panneau dépliable posé sur les sièges rabattus "
                  "et un second sur pieds escamotables. Le poids est réparti, rien n'est vissé.",
         videos=[("kUtbMAAaMW8", "Le kit Dacia Jogger en vidéo"), ("bdcMn_dis2A", "Montage du kit dans le coffre")],
         faq=[("Le même kit va-t-il dans un Lodgy et dans un Jogger ?",
               "Oui. Le Lodgy (2012-2022) et le Jogger (depuis 2022) ont les mêmes mesures intérieures : c'est le même kit."),
              ("Garde-t-on les 5 places ?", "Oui. Kit replié dans le coffre, les 5 places restent utilisables.")],
         variantes=[("dacia-jogger-lodgy", "Dacia Jogger / Lodgy", "mini")]),
    # --- Monospaces --------------------------------------------------------------------------
    dict(slug="citroen-c8-peugeot-807", nom="Citroën C8 et Peugeot 807", court="C8", cat="mini", groupe="monospace", anciens=[],
         mesures=M_MONO, videos=V_MONO, variantes=[("citroen-c8-peugeot-807", "Citroën C8 / Peugeot 807", "mini")]),
    dict(slug="renault-grand-scenic", nom="Renault Grand Scénic", court="Grand Scénic", cat="mini", groupe="monospace", anciens=[],
         mesures=M_MONO, videos=V_MONO, variantes=[("renault-grand-scenic", "Renault Grand Scénic", "mini")]),
    dict(slug="vw-touran", nom="Volkswagen Touran", court="Touran", cat="mini", groupe="monospace", anciens=[], titre="VW Touran",
         mesures=M_MONO, videos=V_MONO, variantes=[("vw-touran", "Volkswagen Touran", "mini")]),
    dict(slug="nissan-juke", nom="Nissan Juke", court="Juke", cat="mini", groupe="monospace", anciens=[],
         mesures=M_MONO, videos=V_MONO, variantes=[("nissan-juke", "Nissan Juke", "mini")]),
    # --- Vans compacts -------------------------------------------------------------------------
    dict(slug="trafic", nom="Renault Trafic", court="Trafic", cat="moyen", groupe="van", anciens=[W + "trafic/"],
         versions="Un kit pour les versions normale, longue et extra-longue.",
         mesures=M_VAN_LARGE + [("Générations", "2002-2014 et depuis 2014"), ("Frigo", "logement pour un frigo à compresseur type Fr40")],
         videos=V_VAN_L, variantes=[("trafic", "Renault Trafic", "moyen")]),
    dict(slug="transporter-t4-t5-t6", nom="Volkswagen Transporter T4, T5, T6 et T7", court="Transporter", cat="moyen", groupe="van",
         anciens=[W + "transporter-t4-t5-t6/"], titre="VW Transporter T4, T5, T6, T7",
         mesures=[("Lit", "185 à 190 cm"), ("Matelas", "155 × 120 cm"), ("Largeur du kit", "152 cm"),
                  ("Hauteur", "40 à 44 cm sans sièges"), ("Places assises", "5 ou 6 places"),
                  ("Rangement", "3 coffres, dont un pour un frigo type Fr40 et une douche 12 V")],
         videos=[("RqTD-6W14Yc", "Le kit Transporter en vidéo"), ("g4FtCffZYMU", "Le kit en détail")],
         variantes=[("transporter-t4-t5-t6", "Volkswagen Transporter T4 / T5 / T6 / T7", "moyen")]),
    dict(slug="caravelle-t4-t5-t6", nom="Volkswagen Caravelle et Multivan", court="Caravelle", cat="moyen", groupe="van",
         anciens=[W + "caravelle-t4-t5-t6/"], titre="VW Caravelle et Multivan",
         mesures=[("Lit", "185 à 190 cm"), ("Largeur du kit", "120 cm (135 cm avec matelas)"), ("Profondeur", "120 cm"),
                  ("Hauteur", "environ 55 cm avec sièges, 40 à 44 cm sans sièges"), ("Générations", "T4, T5, T6 et T7")],
         videos=[("RqTD-6W14Yc", "Le kit Caravelle en vidéo"), ("g4FtCffZYMU", "Le kit en détail")],
         variantes=[("caravelle-t4-t5-t6", "Volkswagen Caravelle / Multivan", "moyen")]),
    dict(slug="vito-viano", nom="Mercedes Vito et Viano", court="Vito", cat="moyen", groupe="van", anciens=[W + "vito-viano/"],
         mesures=[("Lit", "185 à 190 cm"), ("Largeur du kit", "150 cm (155 cm avec matelas)"), ("Profondeur", "120 cm"),
                  ("Hauteur", "environ 55 cm avec sièges, 40 à 44 cm sans sièges"), ("Frigo", "logement pour un frigo type Fr34 ou Fr40")],
         videos=[("DrW7qT4eyz8", "Le kit Vito en vidéo"), ("RqTD-6W14Yc", "Le kit en mode salon")],
         variantes=[("vito-viano", "Mercedes Vito / Viano", "moyen")]),
    dict(slug="expert", nom="Peugeot Expert", court="Expert", cat="moyen", groupe="van", anciens=["/fr/expert/", W + "expert/"],
         versions="Compact (4,60 m), Standard (4,95 m) et Long (5,30 m).",
         mesures=M_VAN_EXPERT, videos=V_VAN, variantes=[("expert", "Peugeot Expert", "moyen")]),
    dict(slug="traveller", nom="Peugeot Traveller", court="Traveller", cat="moyen", groupe="van", anciens=["/fr/traveller/", W + "traveller/"],
         versions="XS (4,60 m), M (4,95 m) et XL (5,30 m).",
         mesures=M_VAN_EXPERT, videos=V_VAN, variantes=[("traveller", "Peugeot Traveller", "moyen")]),
    dict(slug="jumpy", nom="Citroën Jumpy", court="Jumpy", cat="moyen", groupe="van", anciens=["/fr/jumpy/", W + "jumpy/"],
         versions="M et XL.", mesures=M_VAN_EXPERT,
         videos=[("aOEE7pFiZx8", "Le kit Jumpy en vidéo"), ("B5cHLnJlecc", "Montage du kit")],
         variantes=[("jumpy", "Citroën Jumpy", "moyen")]),
    dict(slug="space-tourer", nom="Citroën SpaceTourer", court="SpaceTourer", cat="moyen", groupe="van",
         anciens=["/fr/space-tourer/", W + "space-tourer/"], versions="XS (4,60 m), M (4,95 m) et XL (5,30 m).",
         mesures=M_VAN_EXPERT, videos=V_VAN, variantes=[("space-tourer", "Citroën SpaceTourer", "moyen")]),
    dict(slug="toyota-proace", nom="Toyota Proace et Proace Verso", court="Proace", cat="moyen", groupe="van",
         anciens=["/fr/toyota-proace/", W + "toyota-proace/"], versions="Compact (4,60 m), Medium (4,95 m) et Long (5,30 m).",
         mesures=M_VAN_EXPERT, videos=V_VAN, variantes=[("toyota-proace", "Toyota Proace / Proace Verso", "moyen")]),
    dict(slug="fiat-scudo", nom="Fiat Scudo", court="Scudo", cat="moyen", groupe="van", anciens=[W + "fiat-scudo/"],
         versions="Versions courte et longue : même kit.",
         mesures=[("Lit", "185 à 190 cm"), ("Largeur du kit", "115 à 120 cm"), ("Profondeur", "120 cm"),
                  ("Hauteur", "environ 50,5 cm avec sièges, 40 à 44 cm sans sièges"),
                  ("Générations", "1994-2006, 2007-2016 et depuis 2022")],
         videos=[("nH2jGupoShc", "Le kit en vidéo")], variantes=[("fiat-scudo", "Fiat Scudo", "moyen")]),
    dict(slug="talento", nom="Fiat Talento", court="Talento", cat="moyen", groupe="van", anciens=[W + "talento/"],
         versions="Versions normale, longue et extra-longue.",
         mesures=M_VAN_LARGE + [("Génération", "depuis 2016")], videos=V_VAN_L, variantes=[("talento", "Fiat Talento", "moyen")]),
    dict(slug="opel-vivaro", nom="Opel Vivaro et Zafira Life", court="Vivaro", cat="moyen", groupe="van", anciens=[W + "opel-vivaro/"],
         versions="M et XL : même kit.",
         mesures=[("Lit", "185 à 190 cm"), ("Largeur du kit", "120 cm (130 à 135 cm avec les rabats)"), ("Profondeur", "120 cm"),
                  ("Hauteur", "environ 50,5 cm avec sièges, 40 à 44 cm sans sièges"),
                  ("Générations", "1994-2006, 2007-2016, depuis 2017 et depuis 2019"), ("Places assises", "5 ou 6 places")],
         videos=[("nH2jGupoShc", "Le kit Vivaro en vidéo"), ("2bG_8c_w93Y", "Le kit en détail")],
         variantes=[("opel-vivaro", "Opel Vivaro / Zafira", "moyen")]),
    dict(slug="ford-transit-custom", nom="Ford Transit Custom et Tourneo Custom", court="Transit Custom", cat="moyen", groupe="van",
         anciens=[W + "ford-transit-custom/"], titre="Ford Transit Custom",
         mesures=[("Lit", "160 à 165 × 185 à 190 cm (Transit Custom)"), ("Largeur du kit", "163 cm en 3 parties (Transit Custom), 120 cm (Tourneo Custom)"),
                  ("Largeur avec matelas", "130 à 135 cm (Tourneo Custom)"), ("Hauteur", "environ 55 cm avec sièges, 40 à 44 cm sans sièges")],
         videos=[("x_w3zGccQYg", "Le kit Transit Custom en vidéo"), ("RBJzicbq6xc", "Le kit en détail")],
         variantes=[("ford-transit-custom", "Ford Transit / Tourneo Custom", "moyen")]),
    dict(slug="nv200", nom="Nissan NV200 et Evalia", court="NV200", cat="moyen", groupe="van", anciens=[W + "nv200/"],
         mesures=[("Lit", "180 cm"), ("Largeur du kit", "119 cm (125 cm avec matelas)"), ("Profondeur", "103 cm"),
                  ("Places assises", "les 5 places restent utilisables")],
         videos=[("cIixD2Dj9jI", "Le kit NV200 en vidéo")], variantes=[("nv200", "Nissan NV200 / Evalia", "moyen")]),
    dict(slug="nv300", nom="Nissan NV300 et Primastar", court="NV300", cat="moyen", groupe="van", anciens=[W + "nv300/"],
         versions="Versions normale, longue et extra-longue.",
         mesures=M_VAN_LARGE + [("Générations", "Primastar 2001-2016, NV300 2016-2021, Primastar depuis 2022")],
         videos=V_VAN_L, variantes=[("nv300", "Nissan NV300 / Primastar", "moyen")]),
    dict(slug="hyundai-h1", nom="Hyundai H1", court="H1", cat="moyen", groupe="van", anciens=[W + "hyundai-h1/"],
         mesures=[("Lit", "175 à 190 cm selon la génération"), ("Matelas", "155 × 120 cm"), ("Largeur du kit", "148 cm"),
                  ("Générations", "1997-2007 et 2008-2018"), ("Places assises", "2 à 5 places"),
                  ("Frigo", "logement pour un frigo à compresseur de 15 à 20 L")],
         videos=[("dofrDUImG-U", "Le kit H1 en vidéo")], variantes=[("hyundai-h1", "Hyundai H1", "moyen")]),
    # --- Grands fourgons -----------------------------------------------------------------------
    dict(slug="jumper-boxer-transit", nom="Fiat Ducato, Citroën Jumper et Peugeot Boxer", court="Ducato", cat="grand", groupe="fourgon",
         anciens=[W + "jumper-boxer-transit/", "/fr/camperizar-furgoneta/camperizar-citroen-jumper/"], titre="Ducato, Jumper, Boxer",
         mesures=M_FOURGON + [("Générations", "1994-2002, 2002-2006, 2006-2014 et depuis 2014")],
         videos=V_FOURGON, variantes=[("jumper-boxer-transit", "Fiat Ducato / Citroën Jumper / Peugeot Boxer", "grand")]),
    dict(slug="ford-transit", nom="Ford Transit", court="Transit", cat="grand", groupe="fourgon", anciens=[],
         mesures=M_FOURGON, videos=V_FOURGON, variantes=[("ford-transit", "Ford Transit", "grand")]),
    dict(slug="renault-master", nom="Renault Master et Opel Movano", court="Master", cat="grand", groupe="fourgon", anciens=[],
         mesures=M_FOURGON, videos=V_FOURGON, variantes=[("renault-master", "Renault Master / Opel Movano", "grand")]),
    dict(slug="mercedes-sprinter", nom="Mercedes Sprinter", court="Sprinter", cat="grand", groupe="fourgon", anciens=[],
         mesures=M_FOURGON, videos=V_FOURGON, variantes=[("mercedes-sprinter", "Mercedes Sprinter", "grand")]),
    dict(slug="vw-crafter", nom="Volkswagen Crafter", court="Crafter", cat="grand", groupe="fourgon", anciens=[], titre="VW Crafter",
         mesures=M_FOURGON, videos=V_FOURGON, variantes=[("vw-crafter", "Volkswagen Crafter", "grand")]),
]

# Contenu commun par groupe (quand le modèle n'a pas de texte propre)
CONTENU = {
    "ludospace": {
        "intro": "Votre {nom} devient mini camping-car en quelques minutes, puis redevient un véhicule de tous les jours. "
                 "Le kit se pose dans le coffre sans perçage : pas de VASP, carte grise inchangée, et vous gardez vos 5 places.",
        "inclus": [("i-bed", "Lit pliant", "187 cm, jusqu'à 220 cm en version longue."),
                   ("i-cook", "Cuisine", "Tiroir extractible pour le réchaud et la vaisselle."),
                   ("i-box", "Rangement", "Coffre à double ouverture et place pour un frigo de 15 L."),
                   ("i-table", "Table", "À l'intérieur ou à l'extérieur, plusieurs hauteurs.")],
        "faq": [("Garde-t-on les 5 places ?", "Oui. Sur ludospace, le kit se replie dans le coffre et vous gardez vos 5 places.")],
        "image": ("/img/kit-carrossier-lit.webp", "Kit camper amovible en phénolique carrossier, lit déplié dans un ludospace", 900, 900),
    },
    "monospace": {
        "intro": "Votre {nom} devient un petit camper pour une ou deux personnes : lit, cuisine et rangement, posés dans le coffre "
                 "sans perçage. Pas de VASP, et vous retrouvez votre voiture quand vous retirez le kit.",
        "inclus": [("i-bed", "Lit", "Matelas sur mesure en 3 pièces, adapté à la hauteur du véhicule."),
                   ("i-cook", "Cuisine", "Tiroir extractible pour le réchaud et la vaisselle."),
                   ("i-box", "Rangement", "Coffre avec accès par le dessus et par l'avant."),
                   ("i-table", "Table extérieure", "L'habitacle est bas : la table s'utilise surtout dehors.")],
        "faq": [("Un kit camper dans un monospace, c'est confortable ?",
                 "Pour une ou deux personnes, oui. L'habitacle est plus bas qu'un ludospace : on y dort bien, mais on cuisine et on mange dehors.")],
        "image": ("/img/kit-pin-rangement.webp", "Kit camper amovible en pin avec tiroirs", 900, 900),
    },
    "van": {
        "intro": "Votre {nom} devient van aménagé en quelques minutes : lit, cuisine et rangements, à retirer quand vous voulez. "
                 "Le kit s'adapte à vos sièges et se pose sans perçage : pas de VASP, carte grise inchangée.",
        "inclus": [("i-bed", "Lit", "185 à 190 cm, matelas sur mesure en option."),
                   ("i-cook", "Cuisine", "Tiroir extractible pour le réchaud et la vaisselle."),
                   ("i-box", "Rangement", "Coffres avec logement pour un frigo jusqu'à 35 L et une douche 12 V."),
                   ("i-table", "Table", "Hauteur réglable : repas, salon ou couchage.")],
        "faq": [("Puis-je garder mes sièges arrière ?",
                 "Oui. Le kit s'adapte : environ 55 cm de haut avec la 2e rangée de sièges, 40 à 44 cm sans sièges.")],
        "image": ("/img/kit-hpl-anthracite.webp", "Kit camper amovible HPL gris anthracite en mode salon dans un van", 900, 822),
    },
    "fourgon": {
        "intro": "Votre {nom} devient fourgon aménagé sans travaux : lit, cuisine et rangements, posés sans perçage et retirés "
                 "quand vous en avez besoin pour travailler. Pas de VASP, carte grise inchangée.",
        "inclus": [("i-bed", "Lit", "180 à 190 × 120 cm, matelas sur mesure en option."),
                   ("i-cook", "Cuisine", "Tiroir extractible pour un réchaud d'un feu ou plus."),
                   ("i-box", "Rangement", "Coffres, modules sur les passages de roue, logement frigo Fr40."),
                   ("i-table", "Table", "Hauteur réglable.")],
        "faq": [("Le kit tient-il pendant la conduite ?",
                 "Oui, comme tout chargement : il s'arrime aux anneaux du véhicule et se replie pendant la route.")],
        "image": ("/img/hero-van-amenage-800.webp", "Véhicule aménagé avec un kit camper en bois, hayon ouvert", 800, 400),
    },
}
FIXATION = ("Le kit se pose dans le coffre, repose sur 3 points d'appui et se sangle aux anneaux d'arrimage d'origine. "
            "Les glissières des tiroirs sont renforcées (30 à 40 kg). Aucun perçage, rien n'est vissé.")
FIXATION_GRAND = ("Le kit se pose sur le plancher, s'arrime aux anneaux du fourgon et se replie pendant la route. "
                  "Les glissières des tiroirs sont renforcées (30 à 40 kg). Aucun perçage, rien n'est vissé.")

# ---------------------------------------------------------------------------
# Redirections : anciennes URL camperizatetodoen1.com/fr/… hors fiches modèle
# ---------------------------------------------------------------------------
REDIRECTIONS = {
    "/fr/": "/",
    "/fr/kit-camperizacion/": "/kit-amenagement/",
    "/fr/kitmueblescamper/": "/guide-kit-meubles-camper/",
    "/fr/contacto/": "/contact/",
    "/fr/sobre-nosotros/": "/contact/",
    "/fr/tienda/": "/boutique/",
    "/fr/oscurecedores-aislantes/": "/occultants-isolants/",
    "/fr/colchones-camper/": "/matelas-camper/",
    "/fr/kit-camperizacion/2-12/": "/accessoires/#version-2-1",
    "/fr/kit-camperizacion/coches-monovolumen-y-4x4/": "/kit-amenagement/#monospaces",
    "/fr/camperizar-furgoneta/": "/kit-amenagement/",
    "/fr/camperizar-furgoneta/camperizacion-integral/": "/kit-amenagement/",
    "/fr/camperizar-furgoneta/bateria/": "/accessoires/#batterie",
    "/fr/camperizar-furgoneta/camperizar-vw-transporter/": "/kit-amenagement/transporter-t4-t5-t6/",
    "/fr/terminos-y-condiciones/": "/conditions-generales-de-vente/",
    "/fr/terminos-y-condiciones/politica-de-privacidad/": "/politique-de-confidentialite/",
    "/fr/gracias/": "/",
}
# Préfixes : toute URL qui commence ainsi (et n'a pas de règle exacte) part vers la cible
REDIRECTIONS_PREFIXES = {
    "/fr/tienda/": "/boutique/",
    "/fr/kit-camperizacion/": "/kit-amenagement/",
    "/fr/camperizar-furgoneta/": "/kit-amenagement/",
    "/fr/": "/",
}
