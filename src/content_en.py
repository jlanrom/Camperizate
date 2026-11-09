"""English version of camperizacionmalaga.com (served under /en/).

register(b) adds the English interface texts, image alt texts and the Spanish <-> English page map
(used for hreflang and the language switcher). pages(b) returns {path: html} for every English page.
`b` is the build module (src/build.py): its helpers (layout, pic, crumbs, cta...) are reused here.
To change a text, edit it in this file and run `python3 src/build.py`.
"""
import html

esc = html.escape

PRICE_NOTE_EN = "Basic spec in L2H2 and L3H2 · L4H2 from €26,000 · advanced spec up to €26,300"
PRICE_EN = "€24,900"

ALT_EN = {
    "furgoneta-camper-playa": "Lifes Campers campervan parked on a beach in Málaga",
    "desayuno-camper-mar": "Breakfast on a campervan chopping board with a sea view",
    "interior-camper-cama-cocina-azulejo-verde": "Campervan interior with rear bed, kitchen with green tiles and wooden ceiling",
    "cocina-camper-azulejo-escamas": "Campervan kitchen with green fish-scale tiles, wooden worktop and fridge",
    "cocina-camper-horno-vistas-mar": "Campervan kitchen with oven and hob next to the sliding door open to the sea",
    "dinette-camper-madera-macrame": "Campervan dinette with wooden table, white cabinets and macramé details",
    "ducha-camper-azulejo-blanco": "Campervan shower with white tiles and black taps",
    "encimera-madera-camper-taza": "Varnished wooden worktop with green tiles and a Lifes Campers mug",
    "encimera-barnizada-camper": "Varnished wooden campervan worktop seen from the cab",
    "camper-puerta-lateral-dinette": "Campervan seen through the sliding door, with dinette, table and kitchen",
    "interior-camper-madera-clara": "Light wood campervan interior with overhead lockers and windows",
    "salon-camper-sofa-claraboya": "Campervan lounge with sofa, roof vent and ceiling lights",
    "cocina-camper-fogon-gas": "Campervan kitchen with gas hob, sink and fold-down table",
    "camper-puertas-traseras-cama": "Campervan opened at the rear doors, showing the bed and the lit interior",
    "cocina-camper-fregadero-nevera": "Campervan kitchen with sink, hob and compressor fridge",
    "camper-cama-trasera-garaje": "Campervan rear doors with raised bed and garage underneath",
    "camper-puerta-lateral-mesa": "Campervan with the sliding door open and an outdoor table",
    "camper-literas-dinette": "Campervan with a lifting bed above the dinette and upholstered seats",
    "cocina-camper-horno-madera": "Campervan kitchen with oven, wooden worktop and wooden floor",
    "cocina-camper-grifo-industrial": "Campervan kitchen with sink, hob and spring pull-down tap",
    "camper-cama-elevable-dinette": "Lifting bed above the dinette of a campervan with a wooden ceiling",
    "cocina-camper-encimera-placa": "Campervan kitchen with wooden worktop and ceramic hob",
    "bano-camper-ducha-wc": "Campervan bathroom with shower and toilet",
    "dinette-camper-tapizado-claro": "Campervan dinette with two upholstered benches and a central table",
    "cocina-camper-azulejo-armarios": "Campervan kitchen with fish-scale tiles, drawers and fold-down table",
    "camper-techo-elevable": "Campervan with the pop-top roof raised",
    "interior-camper-gris-claraboya": "Grey campervan interior with roof vent and vinyl floor",
    "cocina-camper-tapa-madera": "Campervan kitchen unit with wooden lid",
    "cocina-camper-fogon-dos-fuegos": "Two-burner hob in a campervan kitchen",
    "camper-ruedas-todoterreno": "Campervan on all-terrain tyres",
    "peugeot-boxer-camper-frontal": "Converted Peugeot Boxer campervan seen from the front",
    "peugeot-boxer-camper-trasera": "Converted Peugeot Boxer campervan seen from the rear",
    "camper-cama-matrimonio-boxer": "Transverse double bed in a converted Peugeot Boxer",
    "cocina-camper-boxer-azulejo": "Kitchen with tiles and TV in a converted Peugeot Boxer",
    "camper-boxer-vista-interior": "Interior of a converted Peugeot Boxer seen from the bed",
    "camper-boxer-sofa-mesa": "Sofa and side table in a converted Peugeot Boxer",
    "camper-boxer-suelo-madera": "Wooden floor and furniture in a converted Peugeot Boxer",
    "camper-boxer-claraboya-tv": "Roof vent with LED light and TV in a converted Peugeot Boxer",
    "interior-camper-madera-oscura": "Campervan interior with dark wood worktop and decorative tiles",
    "interior-camper-cocina-madera-dinette": "Campervan interior with wooden kitchen, dinette and bed at the back",
    "salon-camper-mesa-asientos-azules": "Campervan lounge with blue seats and table",
    "cocina-camper-madera-tapa-abierta": "Campervan kitchen with the wooden lid open over the hob and sink",
    "cama-camper-transversal": "Transverse double bed in a campervan with roof vent",
    "camper-salon-cama-claraboyas": "Lounge and bed of a campervan with two roof vents",
    "cocina-camper-horno-encimera-nogal": "Campervan kitchen with oven and dark wood worktop",
    "iveco-daily-camper-negra": "Black converted Iveco Daily campervan outside the workshop",
    "iveco-daily-camper-puerta-lateral": "Converted Iveco Daily with the sliding door open",
    "iveco-daily-camper-cama-trasera": "Rear bed and garage in a converted Iveco Daily",
    "iveco-daily-camper-cocina-induccion": "Kitchen with induction hob in a converted Iveco Daily",
    "iveco-daily-camper-interior-cocina": "Interior of a converted Iveco Daily with kitchen and wardrobe",
    "iveco-daily-camper-dinette": "Dinette with table and curtains in a converted Iveco Daily",
    "iveco-daily-camper-salon-mesa": "Lounge with table next to the cab in a converted Iveco Daily",
    "pedro-y-jose-lifes-campers": "Pedro and José, founders of Lifes Campers, at the Málaga workshop",
    "taller-lifes-campers-malaga": "Front of the Lifes Campers workshop in San Julián, Málaga, with campervans",
    "taller-lifes-campers-fachada": "Campervan outside the Lifes Campers workshop in Málaga",
    "entrega-camper-clientes": "Handing over a campervan to its owners at the Lifes Campers workshop",
    "entrega-iveco-daily-clientes": "Handing over a converted Iveco Daily to its owners",
}

# Spanish path -> English path
PAIRS = {
    "/": "/en/",
    "/camperizacion-integral/": "/en/full-campervan-conversion/",
    "/furgonetas/": "/en/vans/",
    "/trabajos/": "/en/our-work/",
    "/contacto/": "/en/contact/",
    "/aviso-legal/": "/en/legal-notice/",
    "/politica-de-privacidad/": "/en/privacy-policy/",
    "/politica-de-cookies/": "/en/cookie-policy/",
}

SPECS_EN = [
    ("Insulation and panelling", ["Double insulation of the whole van: 20 mm Kaiflex on the panels and 10 mm on the ribs.",
                                  "White tongue-and-groove panelling on ceiling and walls; pine panelling on the doors.",
                                  "15 mm marine poplar floor with AC5 laminate."]),
    ("Furniture", ["Complete furniture in marine HPL, resistant to damp and daily use.",
                   "Wall-mounted table, outdoor table and small fold-down table."]),
    ("Power and electrics", ["2 × 100 Ah lithium batteries (200 Ah in total).",
                             "400 W NDS high-profile solar panel with MPPT controller.",
                             "1000 W pure sine wave inverter/charger.",
                             "CBE PC180 control panel.",
                             "Several 12 V sockets, outdoor 230 V socket and plenty of lighting points."]),
    ("Water", ["200 l fresh water tank with Shurflo pressure pump.",
               "Whale / Webasto gas water heater.",
               "Outdoor shower with hot and cold water."]),
    ("Kitchen", ["Kitchen unit with sink and Dometic two-burner hob.",
                 "115 l Webasto Isotherm compressor fridge."]),
    ("Bathroom", ["Bathroom cubicle with joinery door, shower tray and tap.",
                  "Turbovent roof vent in the bathroom."]),
    ("Ventilation, light and windows", ["2 Dometic roof vents: one in the lounge and one over the bed.",
                                        "2 sliding glass windows with blinds and curtains."]),
    ("Sleeping and heating", ["1 or 2 full double beds, 135 × 185 cm.",
                              "Planar diesel night heater."]),
    ("Safety and outdoors", ["Reversing camera.", "Outdoor light and outdoor 230 V socket."]),
    ("Homologation (road-legal paperwork)", ["Approved rear seats so you can travel legally.",
                                             "Full homologation project for the Spanish ITV, handled by us."]),
]

PROJECTS_EN = [
    ("Black Iveco Daily", "Full conversion on an Iveco Daily: rear bed with garage, induction hob kitchen, dinette and wardrobe."),
    ("Dark wood and transverse bed", "Dark wood worktops, oven, lounge with blue seats and a transverse bed under two roof vents."),
    ("Peugeot Boxer 2023", "Boxer with transverse double bed, tiled kitchen, sofa, roof vent and wooden floor."),
    ("Green tiles and natural wood", "Kitchen with fish-scale tiles, oven, shower, dinette and wooden ceiling."),
    ("Light wood and a roomy lounge", "Bright interior in light wood, lounge with sofa and a full kitchen."),
    ("Lifting bed and a dinette for four", "Lifting bed above the dinette, rear garage and kitchen with oven."),
    ("Full bathroom and ceramic hob kitchen", "Bathroom with shower and toilet, upholstered dinette and tiled kitchen."),
    ("Pop-top roof and off-road kit", "Campervan with pop-top roof, grey interior and all-terrain tyres."),
]

REVIEWS_EN = [
    ("Delighted with the work. The end result has been excellent, with a high-quality finish and exclusive details that make the difference. Even after delivery they have always been ready to make any adjustment.", "Juan Sánchez"),
    ("The best. They made a dream I'd had for many years come true. Delighted with the work; both José and Pedro were really attentive throughout the whole process.", "Raúl Hijano"),
    ("Very good professionals, the whole team. José and Pedro were very attentive to all our needs and guided us towards the best options. Fair value for money.", "Pepa Puchero"),
]

# --------------------------------------------------------------------------- vans
VANS_EN = [
    {
        "slug": "fiat-ducato", "name": "Fiat Ducato", "brand": "Fiat", "model": "Ducato",
        "card": "Europe's favourite camper base. Wide, front-wheel drive and a low floor.",
        "title": "Fiat Ducato Campervan Conversion in Málaga | Lifes Campers",
        "desc": "Full campervan conversion of Fiat Ducato L2H2, L3H2 and L4H2 in Málaga: transverse bed, kitchen, bathroom, solar and homologation. From €24,900.",
        "intro": "The Fiat Ducato is the most popular base for campervans in Europe, and for good reason: it is wide, front-wheel drive and has a low, flat floor. A perfect starting point for a full conversion.",
        "hero": "interior-camper-cocina-madera-dinette",
        "photos": ["cama-camper-transversal", "cocina-camper-madera-tapa-abierta", "salon-camper-mesa-asientos-azules", "camper-salon-cama-claraboyas"],
        "body": """
<h2>Why the Ducato makes such a good camper</h2>
<p>Its big advantage is <strong>interior width</strong>: it is one of the few vans where a double bed fits <strong>transversely</strong>, from side to side. That frees up more than half a metre of length for the kitchen, the bathroom or a more comfortable lounge.</p>
<p><strong>Front-wheel drive</strong> keeps the load floor low and free of a transmission tunnel, so it is easy to step in and you gain headroom. And as the base of most motorhomes, you will find parts and garages anywhere in Europe.</p>
<h2>Which version to choose</h2>
<ul>
<li><strong>L2H2</strong>: the best balance. Transverse bed, kitchen, compact bathroom and a dinette with approved seats, while still easy to drive in town.</li>
<li><strong>L3H2</strong>: about 60 cm more. Room for a bigger bathroom, more storage or a rear garage for bikes.</li>
<li><strong>L4H2</strong>: for a fixed bed plus a separate lounge, or for more than two travellers.</li>
<li><strong>H3</strong>: if you are tall or want overhead lockers without ducking.</li>
</ul>
<h2>How we convert it</h2>
<p>We start from our full conversion —double Kaiflex insulation, marine HPL furniture, 200 Ah of lithium with 400 W of solar, 200 l of water, Dometic kitchen, bathroom and Planar heating— and adapt the layout to your Ducato and the way you travel. We also handle the homologation project.</p>
""",
        "facts": [
            ("Versions we recommend", "L2H2, L3H2, L4H2 (and H3 for extra headroom)"),
            ("Drive", "Front-wheel"),
            ("Approx. external length", "L2: 5.41 m · L3: 6.00 m · L4: 6.36 m"),
            ("Approx. internal height", "H2: 1.93 m · H3: 2.17 m"),
            ("Approx. max. internal width", "1.87 m (fits a transverse bed)"),
            ("Twin vans", "Peugeot Boxer, Citroën Jumper, Opel Movano (from 2021) and Toyota Proace Max"),
        ],
        "faq": [
            ("Which Ducato is best for a campervan?", "For two people, the L2H2 is the best balance between living space and ease of driving and parking. If you want a bigger bathroom or a rear garage, look at the L3H2."),
            ("Does a transverse double bed fit in a Ducato?", "Yes. It is one of its big advantages: the interior width lets the bed run from side to side, leaving more space for the rest of the camper."),
            ("How much does a Fiat Ducato conversion cost?", "Our full conversion with the complete specification starts at €24,900, with homologation and warranty included. On the L4H2 it starts at €26,000. Prices do not include the van."),
        ],
    },
    {
        "slug": "peugeot-boxer", "name": "Peugeot Boxer", "brand": "Peugeot", "model": "Boxer",
        "card": "Same body as the Ducato. We have converted several: see the result.",
        "title": "Peugeot Boxer Campervan Conversion in Málaga | Lifes Campers",
        "desc": "Full campervan conversion of Peugeot Boxer L2H2, L3H2 and L4H2 in Málaga: transverse bed, kitchen, bathroom, solar power and homologation. From €24,900.",
        "intro": "The Peugeot Boxer shares its body with the Fiat Ducato and the Citroën Jumper, so it has the same strengths: width for a transverse bed, a low floor and plenty of usable space. The photos show a 2023 Boxer we converted in our workshop.",
        "hero": "camper-cama-matrimonio-boxer",
        "photos": ["peugeot-boxer-camper-frontal", "cocina-camper-boxer-azulejo", "camper-boxer-sofa-mesa", "camper-boxer-claraboya-tv"],
        "body": """
<h2>A converted Boxer, inside</h2>
<p>The Boxer in the photos is a <strong>2023 2.2 BlueHDi 140 hp</strong>. We fitted it with a transverse double bed at the back, a tiled kitchen with a wooden worktop, a sofa with a side table, a roof vent with LED light, a TV, 200 Ah of lithium, a 400 W solar panel, 200 litres of water, a 115-litre Webasto fridge and Planar heating.</p>
<h2>Boxer, Ducato or Jumper: which one?</h2>
<p>Inside they are practically the same: same lengths (L1 to L4), same heights (H1 to H3) and the same width. The differences are in the engines, standard equipment, price and dealer network. Our advice: pick the one you find in the best condition at the best price; the conversion will be the same.</p>
<h2>Things to bear in mind</h2>
<ul>
<li><strong>Version</strong>: we recommend at least an L2H2 for standing headroom and space for a bathroom.</li>
<li><strong>Factory windows</strong>: if your Boxer already has windows, we use them in the design; if not, we fit sliding glass windows with blinds.</li>
<li><strong>Weight</strong>: with a standard car licence (category B) the limit is 3,500 kg. We design with the final weight in mind so you can travel fully loaded and legal.</li>
</ul>
""",
        "facts": [
            ("Versions we recommend", "L2H2, L3H2, L4H2"),
            ("Drive", "Front-wheel"),
            ("Approx. external length", "L2: 5.41 m · L3: 6.00 m · L4: 6.36 m"),
            ("Approx. internal height", "H2: 1.93 m · H3: 2.17 m"),
            ("Approx. max. internal width", "1.87 m (fits a transverse bed)"),
            ("Twin vans", "Fiat Ducato, Citroën Jumper, Opel Movano (from 2021)"),
        ],
        "faq": [
            ("Is converting a Boxer the same as a Ducato?", "Yes. The body and internal dimensions are the same, so the conversion and the price are too."),
            ("Which Boxer should I buy for a conversion?", "An L2H2 or L3H2 with 140 hp or more if you will travel loaded or in the mountains. Message us before you buy and we will help you check it."),
            ("How much does a Peugeot Boxer conversion cost?", "Our full conversion with the complete specification starts at €24,900, homologation and warranty included (van not included)."),
        ],
    },
    {
        "slug": "citroen-jumper", "name": "Citroën Jumper", "brand": "Citroën", "model": "Jumper",
        "card": "The Ducato and Boxer's twin. A great second-hand option.",
        "title": "Citroën Jumper Campervan Conversion in Málaga | Lifes Campers",
        "desc": "Full campervan conversion of Citroën Jumper L2H2, L3H2 and L4H2 in Málaga, plus tips for buying a used Jumper to convert. From €24,900 with homologation.",
        "intro": "The Citroën Jumper is the third twin of the Ducato and Boxer family. Same width, same versions and the same camper potential, and it is often available second-hand at a very good price.",
        "hero": "interior-camper-cama-cocina-azulejo-verde",
        "photos": ["cocina-camper-azulejo-escamas", "cocina-camper-horno-vistas-mar", "dinette-camper-madera-macrame", "ducha-camper-azulejo-blanco"],
        "body": """
<h2>Buying a used Jumper to convert</h2>
<p>Many customers come to us with a used Jumper, and it is a great choice if you pick well. This is what we recommend checking before you buy:</p>
<ul>
<li><strong>Version and size</strong>: make sure it is an H2 (high roof) and ideally an L2 or L3. The registration document shows it.</li>
<li><strong>Rust</strong>: check the underside, wheel arches, door edges and the roof where the roof vents and solar panel will go.</li>
<li><strong>Maintenance</strong>: service history, mileage and the state of the clutch and timing belt.</li>
<li><strong>Windows and bulkhead</strong>: a van with factory windows or rear seats can save work; the cargo bulkhead is usually removed.</li>
<li><strong>Gross weight</strong>: check the maximum authorised mass (usually 3,500 kg for a standard car licence).</li>
</ul>
<p>Send us the advert on WhatsApp and we will tell you what we think before you buy.</p>
<h2>How we convert it</h2>
<p>Just like a Ducato or a Boxer: transverse bed, full kitchen, bathroom with shower, dinette with approved seats and all the equipment of our full conversion.</p>
""",
        "facts": [
            ("Versions we recommend", "L2H2, L3H2, L4H2"),
            ("Drive", "Front-wheel"),
            ("Approx. external length", "L2: 5.41 m · L3: 6.00 m · L4: 6.36 m"),
            ("Approx. internal height", "H2: 1.93 m · H3: 2.17 m"),
            ("Approx. max. internal width", "1.87 m (fits a transverse bed)"),
            ("Twin vans", "Fiat Ducato, Peugeot Boxer, Opel Movano (from 2021)"),
        ],
        "faq": [
            ("Is a used Jumper worth converting?", "Yes, if the bodywork and mechanics are sound. A second-hand Jumper L2H2 or L3H2 is one of the best value bases."),
            ("Can you check the van before I buy it?", "Send us the advert or bring it to the workshop and we will tell you what we see: version, condition and whether it suits the camper you want."),
            ("How much does a Citroën Jumper conversion cost?", "From €24,900 for the full conversion with the complete specification, homologation and warranty included."),
        ],
    },
    {
        "slug": "opel-movano", "name": "Opel Movano", "brand": "Opel", "model": "Movano",
        "card": "Check the year: from 2021 it is a Ducato twin; before, a Renault Master.",
        "title": "Opel Movano Campervan Conversion in Málaga | Lifes Campers",
        "desc": "Full campervan conversion of the Opel Movano in Málaga. Differences between the pre-2021 Movano (Master-based) and the current one (Ducato-based). From €24,900.",
        "intro": "The Opel Movano is a special case: depending on the year, it is a different van inside. Knowing which one you have is key to designing the camper properly.",
        "hero": "camper-puerta-lateral-dinette",
        "photos": ["interior-camper-madera-clara", "salon-camper-sofa-claraboya", "cocina-camper-fogon-gas", "cocina-camper-fregadero-nevera"],
        "body": """
<h2>Two very different Movanos</h2>
<ul>
<li><strong>Movano from 2021</strong>: shares its body with the Fiat Ducato, Peugeot Boxer and Citroën Jumper. Front-wheel drive, same dimensions and the width that allows a transverse bed.</li>
<li><strong>Movano up to 2021</strong>: a twin of the Renault Master (and the Nissan NV400). It came with front or rear-wheel drive, and its interior is a little narrower, so the layout changes.</li>
</ul>
<p>They are easy to tell apart from the front, but if in doubt, send us the registration or year and we will check.</p>
<h2>How we design the camper for each model</h2>
<p>On the current Movano we use the Ducato-family layout: transverse rear bed, full kitchen and bathroom. On the older one we decide with you between a longitudinal bed or a shorter transverse bed, depending on your height and how much room you want for the bathroom and lounge.</p>
<p>Either way, the equipment is that of our full conversion: Kaiflex insulation, marine HPL furniture, 200 Ah of lithium with 400 W of solar, 200 litres of water, kitchen, bathroom, heating and homologation.</p>
""",
        "facts": [
            ("Versions we recommend", "L2H2 or larger"),
            ("Movano from 2021", "Ducato-based · front-wheel drive · transverse bed possible"),
            ("Movano up to 2021", "Renault Master-based · front or rear-wheel drive · slightly narrower inside"),
            ("Internal height", "H2: enough to stand up (check your version)"),
            ("Twin vans (current)", "Fiat Ducato, Peugeot Boxer, Citroën Jumper"),
        ],
        "faq": [
            ("How do I know which Movano I have?", "If it is from 2021 onwards, it is normally the Ducato-based version. Send us a photo or the registration year and we will check."),
            ("Does a transverse bed fit in a Movano?", "In the current Movano, yes, just like a Ducato. In the older one (Master-based) it depends on your height; we look at it together at the design stage."),
            ("How much does an Opel Movano conversion cost?", "From €24,900 for the full conversion, with homologation and warranty included (van not included)."),
        ],
    },
    {
        "slug": "renault-master", "name": "Renault Master", "brand": "Renault", "model": "Master",
        "card": "Tough and widely available. Front or rear-wheel drive depending on version.",
        "title": "Renault Master Campervan Conversion in Málaga | Lifes Campers",
        "desc": "Full campervan conversion of Renault Master L2H2 and L3H2 in Málaga: layout, front or rear-wheel drive, beds and homologation. From €24,900 with warranty.",
        "intro": "The Renault Master is one of the best-selling large vans in Spain, so it is easy to find second-hand at a good price. It is tough, comfortable to drive and a very capable camper base.",
        "hero": "camper-cama-elevable-dinette",
        "photos": ["camper-cama-trasera-garaje", "camper-literas-dinette", "cocina-camper-horno-madera", "cocina-camper-grifo-industrial"],
        "body": """
<h2>What you need to know about the Master</h2>
<p>The Master comes in <strong>front-wheel drive</strong> (lower floor, the most common in L2H2) and <strong>rear-wheel drive</strong> versions (more payload, often with twin rear wheels and a slightly higher floor). For a two or four-berth camper, front-wheel drive is usually the more practical choice.</p>
<p>Its interior is <strong>a little narrower than the Ducato family</strong>. So in many Masters we plan a longitudinal bed or a lifting bed above the dinette, which sleeps four without giving up the lounge.</p>
<h2>Layouts that work best</h2>
<ul>
<li><strong>Raised rear bed with garage</strong>: room for bikes, boards or luggage underneath.</li>
<li><strong>Lifting bed above the dinette</strong>: lounge by day, bedroom by night. Ideal for families.</li>
<li><strong>Side kitchen with oven</strong> and a compact bathroom next to the sliding door.</li>
</ul>
<p>The Master shares its body with the Nissan NV400 and the pre-2021 Opel Movano, so everything here applies to them too.</p>
""",
        "facts": [
            ("Versions we recommend", "L2H2, L3H2"),
            ("Drive", "Front or rear-wheel, depending on version"),
            ("Internal width", "A little less than the Ducato family: longitudinal or lifting bed"),
            ("Internal height", "H2: enough to stand up"),
            ("Twin vans", "Nissan NV400 / Interstar and Opel Movano (up to 2021)"),
        ],
        "faq": [
            ("Front or rear-wheel drive Master for a camper?", "For most campers we recommend front-wheel drive: lower floor and more usable headroom. Rear-wheel drive makes sense if you will carry a lot of weight."),
            ("Can four people sleep in a converted Master?", "Yes, with a lifting bed above the dinette and approved rear seats."),
            ("How much does a Renault Master conversion cost?", "From €24,900 for the full conversion with the complete specification, homologation and warranty (van not included)."),
        ],
    },
    {
        "slug": "volkswagen-crafter", "name": "Volkswagen Crafter", "brand": "Volkswagen", "model": "Crafter",
        "card": "Car-like comfort, automatic gearbox and 4MOTION option.",
        "title": "Volkswagen Crafter Campervan Conversion in Málaga | Lifes Campers",
        "desc": "Full campervan conversion of the Volkswagen Crafter (and MAN TGE) in Málaga: front, rear-wheel drive or 4MOTION, layout and homologation. From €24,900.",
        "intro": "The Volkswagen Crafter is the choice for drivers who want a car-like drive: smooth ride, driver assistance systems and an automatic gearbox available. An excellent base for a premium camper.",
        "hero": "interior-camper-gris-claraboya",
        "photos": ["cocina-camper-tapa-madera", "cocina-camper-fogon-dos-fuegos", "desayuno-camper-mar", "encimera-madera-camper-taza"],
        "body": """
<h2>Why choose a Crafter</h2>
<ul>
<li><strong>Three types of drive</strong>: front, rear and 4MOTION (all-wheel). 4MOTION is ideal for tracks, snow or the beach.</li>
<li><strong>Automatic gearbox</strong> available on many versions, very comfortable on long trips.</li>
<li><strong>Usable interior</strong>, with fairly straight walls that make fitting furniture easier.</li>
<li>Its twin, the <strong>MAN TGE</strong>, is converted in exactly the same way.</li>
</ul>
<h2>Versions and sizes</h2>
<p>Volkswagen uses its own naming for wheelbases and roofs. The equivalent of a Ducato L2H2 is the <strong>medium wheelbase, high roof</strong> Crafter; for more space, the long wheelbase. Its interior is a little narrower than a Ducato's, so we decide the bed orientation with you according to your height.</p>
<h2>How we convert it</h2>
<p>With the full specification of our complete conversion, paying special attention to weight, as 4MOTION and automatic versions are heavier as standard. If you are after more adventurous use, we can add all-terrain tyres, protection or a pop-top roof.</p>
""",
        "facts": [
            ("Versions we recommend", "Medium or long wheelbase, high roof"),
            ("Drive", "Front, rear or 4MOTION"),
            ("Gearbox", "Manual or automatic, depending on version"),
            ("Internal width", "A little less than the Ducato family"),
            ("Twin van", "MAN TGE"),
        ],
        "faq": [
            ("Which Crafter is best for a camper?", "A medium wheelbase, high roof Crafter is the equivalent of an L2H2 and the best balance. Go for 4MOTION if you will leave the tarmac."),
            ("Do you also convert the MAN TGE?", "Yes. It is the same van as the Crafter, so the conversion is identical."),
            ("How much does a Volkswagen Crafter conversion cost?", "From €24,900 for the full conversion with the complete specification, homologation and warranty (van not included). Extras such as a pop-top roof or off-road tyres are quoted separately."),
        ],
    },
    {
        "slug": "mercedes-sprinter", "name": "Mercedes Sprinter", "brand": "Mercedes-Benz", "model": "Sprinter",
        "card": "The premium benchmark: quality, resale value and rear-wheel or 4x4 drive.",
        "title": "Mercedes Sprinter Campervan Conversion in Málaga | Lifes Campers",
        "desc": "Full campervan conversion of the Mercedes Sprinter in Málaga: rear, front-wheel drive or 4x4, layout, weight and homologation. From €24,900 with warranty.",
        "intro": "The Mercedes Sprinter is the premium van par excellence: build quality, reliability and a very high resale value. If you want a camper for many years and many miles, it is a safe bet.",
        "hero": "interior-camper-madera-oscura",
        "photos": ["cocina-camper-horno-encimera-nogal", "camper-salon-cama-claraboyas", "salon-camper-mesa-asientos-azules", "cama-camper-transversal"],
        "body": """
<h2>The Sprinter's strengths</h2>
<ul>
<li><strong>Rear-wheel drive</strong> as standard on many versions (front-wheel and 4x4 also available): very good for towing and for traction when loaded.</li>
<li><strong>Automatic gearbox</strong> available and top-level ride comfort.</li>
<li><strong>Resale value</strong>: a converted, homologated Sprinter holds its price very well.</li>
</ul>
<h2>What to consider in the design</h2>
<p>The Sprinter is <strong>narrower inside than the Ducato</strong>, so a transverse bed only works for people of average height. For taller people we usually plan a longitudinal bed or a layout with a rear bed and a convertible dinette.</p>
<p>In rear-wheel drive versions the floor is a little higher, which the roof height makes up for. And as with any large van, we keep an eye on the <strong>final weight</strong> so you do not exceed 3,500 kg if you drive on a standard car licence.</p>
<h2>How we convert it</h2>
<p>With the full specification of our complete conversion, marine HPL furniture and finishes worthy of the base: wooden worktops, indirect lighting and all the wiring accessible for maintenance.</p>
""",
        "facts": [
            ("Versions we recommend", "Medium or long, high roof"),
            ("Drive", "Rear, front or 4x4, depending on version"),
            ("Gearbox", "Manual or automatic"),
            ("Internal width", "Less than the Ducato family: transverse bed only for average height"),
            ("Strength", "Quality and resale value"),
        ],
        "faq": [
            ("Does a transverse bed fit in a Sprinter?", "For people of average height, yes. If you are taller, we will recommend a longitudinal bed so you sleep well."),
            ("Rear or front-wheel drive for a Sprinter camper?", "Rear-wheel drive is the most common and the best if you carry a lot of weight or tow. Front-wheel drive gives a slightly lower floor. 4x4 is for off-road use."),
            ("How much does a Mercedes Sprinter conversion cost?", "From €24,900 for the full conversion with the complete specification, homologation and warranty (van not included)."),
        ],
    },
    {
        "slug": "ford-transit", "name": "Ford Transit", "brand": "Ford", "model": "Transit",
        "card": "Easy to find, with front, rear or all-wheel drive.",
        "title": "Ford Transit Campervan Conversion in Málaga | Lifes Campers",
        "desc": "Full campervan conversion of Ford Transit L2H2, L3H2 and L3H3 in Málaga: front, rear or all-wheel drive, layout and homologation. From €24,900 with warranty.",
        "intro": "The large Ford Transit is a very versatile camper base: easy to find, good on the road and available with front, rear or all-wheel drive.",
        "hero": "dinette-camper-tapizado-claro",
        "photos": ["cocina-camper-encimera-placa", "bano-camper-ducha-wc", "cocina-camper-azulejo-armarios", "encimera-barnizada-camper"],
        "body": """
<h2>Why a Transit</h2>
<ul>
<li><strong>L2H2, L3H2, L3H3 and L4H3 versions</strong>: there is one for every kind of traveller.</li>
<li><strong>Front, rear or all-wheel drive (AWD)</strong> depending on version: choose according to whether you will stay on tarmac or go on tracks.</li>
<li><strong>A good network of garages</strong> all over Spain for servicing.</li>
</ul>
<h2>Recommended layout</h2>
<p>In a Transit L2H2 or L3H2, a layout with a <strong>full bathroom with shower and toilet</strong> next to the sliding door works very well, with the kitchen opposite, a dinette with approved seats behind the front seats and the bed at the back.</p>
<p>As with any large van, the equipment is that of our full conversion and we handle the homologation for you.</p>
""",
        "facts": [
            ("Versions we recommend", "L2H2, L3H2, L3H3"),
            ("Drive", "Front, rear or all-wheel (AWD), depending on version"),
            ("Internal height", "H2 or H3: standing headroom"),
            ("Strength", "Availability and versatility"),
        ],
        "faq": [
            ("Which Transit is best for a camper?", "The front-wheel drive L2H2 or L3H2 is the most practical for two people. If you are tall, the H3 gives extra headroom."),
            ("Can a Transit have a full bathroom?", "Yes. An L2H2 or larger has room for a bathroom with shower and toilet."),
            ("How much does a Ford Transit conversion cost?", "From €24,900 for the full conversion with the complete specification, homologation and warranty (van not included)."),
        ],
    },
    {
        "slug": "iveco-daily", "name": "Iveco Daily", "brand": "Iveco", "model": "Daily",
        "card": "Truck chassis, rear-wheel drive and big payload. See the one we built.",
        "title": "Iveco Daily Campervan Conversion in Málaga | Lifes Campers",
        "desc": "Full campervan conversion of the Iveco Daily in Málaga: ladder-frame chassis, rear-wheel drive, huge space and payload. See our converted Daily.",
        "intro": "The Iveco Daily is the most truck-like of the large vans: ladder-frame chassis, rear-wheel drive and a huge payload. The photos show the black Daily we converted in our workshop.",
        "hero": "iveco-daily-camper-negra",
        "photos": ["iveco-daily-camper-interior-cocina", "iveco-daily-camper-cocina-induccion", "iveco-daily-camper-cama-trasera", "iveco-daily-camper-dinette"],
        "body": """
<h2>Our converted Iveco Daily</h2>
<p>This black Daily has a raised rear bed with a garage underneath, a kitchen with induction hob and wooden worktop, a wardrobe, a dinette with table next to the cab and all the equipment of our full conversion: insulation, solar power with lithium, water, heating and homologation.</p>
<h2>The Daily's advantages</h2>
<ul>
<li><strong>Ladder-frame chassis</strong>, like a truck: very tough and built to work loaded for many years.</li>
<li><strong>Rear-wheel drive</strong> and, on many versions, an 8-speed automatic gearbox.</li>
<li><strong>Versions over 3,500 kg</strong>: if you hold a C1 licence, you can go for a heavier Daily and forget about the weight limit.</li>
</ul>
<h2>Things to bear in mind</h2>
<p>Because of the chassis, the floor is higher than in a Ducato, so there is one more step to climb in and a high-roof version is advisable. If you drive on a standard car licence, remember the version must be rated at 3,500 kg; we design the camper so you stay within the limit.</p>
""",
        "facts": [
            ("Versions we recommend", "High-roof panel van, medium or long wheelbase"),
            ("Drive", "Rear-wheel"),
            ("Chassis", "Ladder frame (truck type)"),
            ("Gross weight", "3,500 kg versions (car licence) and heavier (C1 licence)"),
            ("Strength", "Toughness and payload"),
        ],
        "faq": [
            ("Can I drive an Iveco Daily camper on a car licence?", "Yes, if the version has a maximum authorised mass of 3,500 kg. Heavier versions require a C1 licence."),
            ("Is the Daily good for long trips?", "Yes. Its chassis and rear-wheel drive make it very durable for many miles with a load. It is less nimble in town than a Ducato."),
            ("How much does an Iveco Daily conversion cost?", "Our full conversion with the complete specification starts at €24,900, with homologation and warranty. For very long versions we give you a tailored quote."),
        ],
    },
]


def register(b):
    b.ALTS["en"] = ALT_EN
    b.UI["en"] = {
        "html_lang": "en", "in_language": "en-GB", "og_locale": "en_GB", "home": "/en/",
        "biz_desc": "Full campervan conversion workshop for large vans in Málaga: bespoke design, furniture, solar power, water, homologation and warranty.",
        "skip": "Skip to content", "menu": "Open menu", "home_aria": "home", "nav_aria": "Main",
        "wa_msg": "Hello, I'd like information about a campervan conversion.",
        "wa_aria": "Message us on WhatsApp",
        "foot_tag": "Bespoke full campervan conversions in Málaga. Large vans, materials that last, homologation and warranty.",
        "foot_contact": "Contact", "foot_vans": "Vans", "foot_follow": "Follow us", "foot_legal": "Legal",
        "legal": [("/en/legal-notice/", "Legal notice"), ("/en/privacy-policy/", "Privacy"), ("/en/cookie-policy/", "Cookies")],
        "foot_right": "Campervan conversions in Málaga",
        "crumbs_home": "Home", "crumbs_aria": "Breadcrumb",
        "cta_title": "Ready for the next step?",
        "cta_text": "Tell us which van you have (or are looking for) and how you travel. We reply on WhatsApp and design your camper with you.",
        "cta_btn": "Message us on WhatsApp",
        "switch_label": "Español", "switch_short": "ES",
        "van_prefix": "/en/vans/",
        "nav": [("/en/full-campervan-conversion/", "Full conversion"), ("/en/vans/", "Vans"),
                ("/en/our-work/", "Our work"), ("/en/contact/", "Contact")],
        "vans": VANS_EN,
    }
    b.UI["es"]["switch_label"] = "English"
    for es, en in PAIRS.items():
        b.ALTERNATES[es] = b.ALTERNATES[en] = {"es": es, "en": en}
    for v in VANS_EN:
        es, en = f'/furgonetas/{v["slug"]}/', f'/en/vans/{v["slug"]}/'
        b.ALTERNATES[es] = b.ALTERNATES[en] = {"es": es, "en": en}


# --------------------------------------------------------------------------- pages
def _vans_grid(b):
    cards = "".join(f'<a class="van" href="/en/vans/{v["slug"]}/"><div><p class="label">{esc(v["brand"])}</p>'
                    f'<h3>{esc(v["model"])}</h3><p>{esc(v["card"])}</p></div><span class="more">See the conversion →</span></a>'
                    for v in VANS_EN)
    return f'<div class="vans">{cards}</div>'


def _reviews(b):
    items = "".join(f'<figure class="review"><div class="stars" aria-label="5 stars">★★★★★</div><blockquote>“{esc(t)}”</blockquote>'
                    f'<figcaption>{esc(n)} · Google review (translated from Spanish)</figcaption></figure>' for t, n in REVIEWS_EN)
    return f"""<section class="section"><div class="wrap">
<div class="section-head"><p class="label">What our customers say</p><h2>Reviews from people already travelling in their Lifes Campers</h2></div>
<div class="reviews">{items}</div>
<p style="margin-top:22px"><a href="{b.MAPS}" target="_blank" rel="noopener">See all our reviews on Google →</a></p>
</div></section>"""


def page_home(b):
    wa, WA_SVG, pic = b.wa, b.WA_SVG, b.pic
    mosaic_slugs = ["interior-camper-cocina-madera-dinette", "cocina-camper-azulejo-escamas", "cama-camper-transversal",
                    "iveco-daily-camper-negra", "bano-camper-ducha-wc", "camper-salon-cama-claraboyas",
                    "cocina-camper-horno-vistas-mar", "camper-cama-matrimonio-boxer", "iveco-daily-camper-cocina-induccion"]
    mosaic = "".join(b.thumb_link(s, "home", "big" if i == 0 else "") for i, s in enumerate(mosaic_slugs))
    body = f"""
<section class="hero"><div class="wrap">
  <div>
    <p class="kicker">Bespoke full campervan conversions in Málaga</p>
    <h1>Your home on wheels, handmade from start to finish.</h1>
    <p class="lead">We convert large vans —Ducato, Boxer, Jumper, Movano, Crafter, Sprinter and similar— with everything included: insulation, furniture, solar power, water, kitchen, bathroom and bed. With homologation and warranty, so your investment is a joy and not a risk.</p>
    <div class="actions">
      <a class="btn btn-wa" href="{wa()}" target="_blank" rel="noopener">{WA_SVG}Message us on WhatsApp</a>
      <a class="btn btn-line" href="/en/our-work/">See our work</a>
    </div>
    <ul class="trust"><li>Homologation included</li><li>Approved seats</li><li>Warranty</li><li>Ready in 3 months</li></ul>
  </div>
  <div class="hero-img">{pic("interior-camper-cama-cocina-azulejo-verde", eager=True)}</div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="trio">
    <div><p class="label">01</p><h3>Truly bespoke</h3><p>We design the layout with you and build it piece by piece in our Málaga workshop.</p></div>
    <div><p class="label">02</p><h3>Materials that last</h3><p>Marine HPL, marine-grade floors and serious insulation. Built for years of real use, not for the photo.</p></div>
    <div><p class="label">03</p><h3>Legal and guaranteed</h3><p>Full homologation and approved rear seats. We handle all the paperwork at the Spanish ITV for you.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><p class="label">Our work</p><h2>Campervans built in Málaga</h2>
  <p class="lead">Every camper is different. What does not change is the care in the finish: joints, edges, wiring and fixings built to last.</p></div>
  <div class="mosaic">{mosaic}</div>
  <div class="actions"><a class="btn btn-dark" href="/en/our-work/">See all our work</a></div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="price">
    <div>
      <p class="label">Full conversion · from</p>
      <p class="amount">{PRICE_EN}</p>
      <p class="note">Homologation and warranty included · Ready in 3 months</p>
      <p class="muted" style="font-size:.95rem">{PRICE_NOTE_EN}</p>
      <p>Full conversion on your Ducato, Boxer, Jumper, Sprinter, Crafter or Transit type van. Don't have one yet? We'll help you find it.</p>
      <div class="actions"><a class="btn btn-dark" href="/en/full-campervan-conversion/">See everything included</a></div>
    </div>
    <div class="price-card"><ul>
      <li>Double Kaiflex insulation and tongue-and-groove panelling</li>
      <li>Complete marine HPL furniture</li>
      <li>200 Ah lithium, 400 W solar panel and 1000 W inverter</li>
      <li>200 l water tank, hot water and outdoor shower</li>
      <li>Dometic kitchen and 115 l compressor fridge</li>
      <li>Bathroom with shower, 2 roof vents and Planar heating</li>
      <li>Homologation project and approved rear seats</li>
    </ul></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><p class="label">Large vans, from L2H2</p><h2>Choose your van</h2>
  <p class="lead">We specialise in large vans because they allow a real home: fixed bed, full kitchen, bathroom and standing headroom.</p></div>
  {_vans_grid(b)}
</div></section>

<section class="section alt"><div class="wrap split">
  <div>{pic("pedro-y-jose-lifes-campers")}</div>
  <div>
    <p class="label">About us</p>
    <h2>Don't dream your life, live your dreams</h2>
    <p>We are Pedro and José, two friends who shared the same dream and decided to make it happen. Today, together with our team, we convert vans in our workshop in San Julián, Málaga.</p>
    <p>We like doing things properly, with a personal touch: we are with you from the design to the handover, and we are still there afterwards for any adjustment.</p>
    <p>Want to see how we work? Come and visit the workshop. We speak English.</p>
    <div class="actions"><a class="btn btn-line" href="/en/contact/">How to find us</a></div>
  </div>
</div></section>

{_reviews(b)}
{b.cta()}
"""
    return b.layout("/en/", "Campervan Conversions in Málaga | Lifes Campers",
                    "Bespoke full campervan conversions of large vans in Málaga: Ducato, Boxer, Jumper, Sprinter, Crafter… From €24,900 with homologation and warranty.",
                    body)


def page_integral(b):
    specs = "".join(f'<div class="spec"><div><span class="n">{i + 1:02d}</span><h3>{esc(t)}</h3></div>'
                    f'<ul>{"".join(f"<li>{esc(x)}</li>" for x in items)}</ul></div>' for i, (t, items) in enumerate(SPECS_EN))
    faqs = [
        ("Does the price include the van?", "No. The price (from €24,900) is for the complete conversion of your van. If you don't have one yet, we'll help you find the right base."),
        ("Why does the price vary?", "The basic specification costs €24,900 on L2H2 and L3H2 vans and €26,000 on L4H2. With more advanced equipment it goes up to €26,300. Homologation is always included."),
        ("Which vans do you work with?", "We focus on large vans from L2H2: Fiat Ducato, Peugeot Boxer, Citroën Jumper, Opel Movano, Renault Master, Volkswagen Crafter, Mercedes Sprinter, Ford Transit and Iveco Daily."),
        ("How long does it take?", "About 3 months from booking to handing over your camper, finished and homologated."),
        ("Is homologation included?", "Yes. We prepare and handle the full homologation project for the Spanish ITV, including approved rear seats so you can travel legally."),
        ("Can the equipment be customised?", "Yes. The specification is a guide and is adapted to your van and the way you travel. The final price depends on the configuration we agree."),
        ("How do I pay?", "A €1,000 deposit to book your production slot, 40% when work starts, 40% once most of the work is done and the remaining 20% on delivery."),
    ]
    faq_h, faq_sc = b.faq_block(faqs)
    cr, cr_sc = b.crumbs([("Full conversion", "/en/full-campervan-conversion/")])
    service = {"@type": "Service", "name": "Full campervan conversion", "serviceType": "Campervan conversion",
               "provider": {"@id": b.SITE + "/#negocio"}, "areaServed": "Spain",
               "offers": {"@type": "Offer", "price": "24900", "priceCurrency": "EUR",
                          "priceSpecification": {"@type": "PriceSpecification", "minPrice": 24900, "maxPrice": 26300, "priceCurrency": "EUR"},
                          "description": "Complete specification, homologation and warranty included. Price of the conversion, van not included."}}
    body = f"""
<section class="hero"><div class="wrap">
  <div>
    {cr}
    <p class="kicker">What the conversion includes</p>
    <h1>Full campervan conversion</h1>
    <p class="lead">Everything you need to travel off-grid in comfort, built and homologated in our Málaga workshop. This is our standard specification, area by area.</p>
    <ul class="trust"><li>Homologation included</li><li>Approved seats</li><li>Warranty</li><li>Ready in 3 months</li></ul>
  </div>
  <div class="hero-img">{b.pic("interior-camper-cocina-madera-dinette", eager=True)}</div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="section-head"><p class="label">Standard specification</p><h2>Area by area</h2></div>
  <div class="specs">{specs}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="price">
    <div>
      <p class="label">The investment · from</p>
      <p class="amount">{PRICE_EN}</p>
      <p class="muted" style="font-size:.95rem">{PRICE_NOTE_EN}</p>
      <p>Full conversion with all the equipment on this page, on your van, or we'll help you find one.</p>
      <p class="note">3 months from booking to handing over your camper.</p>
    </div>
    <div>{b.pic("cama-camper-transversal")}</div>
  </div>
  <h2 style="margin-top:56px">Payment plan</h2>
  <div class="steps">
    <div class="step"><p class="label">Step 01</p><h3>Booking</h3><strong>€1,000</strong><p>We reserve your production slot.</p></div>
    <div class="step"><p class="label">Step 02</p><h3>On starting</h3><strong>40%</strong><p>Work on your camper begins.</p></div>
    <div class="step"><p class="label">Step 03</p><h3>During the build</h3><strong>40%</strong><p>Once most of the work is done.</p></div>
    <div class="step"><p class="label">Step 04</p><h3>On delivery</h3><strong>20%</strong><p>You collect your camper, finished and homologated.</p></div>
  </div>
  <p class="muted" style="margin-top:18px;font-size:.92rem">Indicative specification of the full conversion; it can be adapted to the van and the needs of each project. Price and payment plan subject to the final configuration agreed.</p>
</div></section>

<section class="section alt"><div class="wrap narrow">
  <p class="label">Frequently asked questions</p><h2>What people ask us most</h2>
  {faq_h}
</div></section>
{b.cta()}
"""
    return b.layout("/en/full-campervan-conversion/", "Full Campervan Conversion: What's Included and Price | Lifes Campers",
                    "Full campervan conversion from €24,900: Kaiflex insulation, marine HPL furniture, 200 Ah lithium, 400 W solar, water, kitchen, bathroom, heating and homologation. Málaga.",
                    body, [cr_sc, faq_sc, service], active="/en/full-campervan-conversion/")


def page_vans(b):
    cr, cr_sc = b.crumbs([("Vans", "/en/vans/")])
    body = f"""
<section class="section"><div class="wrap">
  {cr}
  <div class="section-head">
    <p class="kicker">Large vans, from L2H2</p>
    <h1>Which van should you convert?</h1>
    <p class="lead">We work with the large vans on the market. All of them make a complete camper, but each has its strengths: width, drive, height or payload. Choose yours and we'll show you how we convert it.</p>
  </div>
  {_vans_grid(b)}
</div></section>

<section class="section alt"><div class="wrap narrow prose">
  <p class="label">Before you choose</p>
  <h2>Why we recommend vans from L2H2</h2>
  <p>On large vans the letter <strong>L</strong> refers to length and <strong>H</strong> to roof height. An <strong>L2H2</strong> (medium length, high roof) is the starting point we recommend: with an H2 roof you can stand up inside, and an L2 fits a double bed, full kitchen, bathroom and a dinette with approved seats.</p>
  <p>If more than two of you travel, or you want a bigger bathroom or a large rear garage, an <strong>L3</strong> or <strong>L4</strong> gives you plenty of room. Just bear in mind parking in town and the total weight.</p>
  <h2>Weight: the key almost nobody looks at</h2>
  <p>With a standard car licence (category B) you can drive vehicles up to <strong>3,500 kg maximum authorised mass</strong>. A full conversion adds weight (furniture, water, batteries…), so we design every camper with the final weight in mind: lithium batteries, light boards and well-placed tanks so you can travel loaded and within the law.</p>
  <h2>Don't have a van yet?</h2>
  <p>Message us before you buy. We'll help you choose the model, version and year to suit your budget and the way you travel, and tell you what to check on a used one.</p>
  <div class="actions"><a class="btn btn-wa" href="{b.wa("Hello, I'm looking for a van to convert and would like some advice.")}" target="_blank" rel="noopener">{b.WA_SVG}Ask us for advice</a></div>
</div></section>
{b.cta()}
"""
    return b.layout("/en/vans/", "Vans to Convert: Ducato, Boxer, Sprinter, Crafter… | Lifes Campers",
                    "Which van to convert into a campervan: Fiat Ducato, Peugeot Boxer, Citroën Jumper, Opel Movano, Renault Master, VW Crafter, Mercedes Sprinter, Ford Transit and Iveco Daily.",
                    body, [cr_sc], active="/en/vans/")


def page_van(b, v):
    cr, cr_sc = b.crumbs([("Vans", "/en/vans/"), (v["name"], f'/en/vans/{v["slug"]}/')])
    faq_h, faq_sc = b.faq_block(v["faq"])
    facts = "".join(f"<tr><th>{esc(k)}</th><td>{esc(x)}</td></tr>" for k, x in v["facts"])
    gallery = "".join(b.thumb_link(s, "van") for s in v["photos"])
    others = "".join(f'<li><a href="/en/vans/{o["slug"]}/">{esc(o["name"])} conversion</a></li>' for o in VANS_EN if o is not v)
    body = f"""
<section class="hero"><div class="wrap">
  <div>
    {cr}
    <p class="kicker">Full conversion · {esc(v["brand"])}</p>
    <h1>{esc(v["name"])} campervan conversion</h1>
    <p class="lead">{v["intro"]}</p>
    <div class="actions">
      <a class="btn btn-wa" href="{b.wa(f'Hello, I would like to convert a {v["name"]}.')}" target="_blank" rel="noopener">{b.WA_SVG}Ask for information</a>
      <a class="btn btn-line" href="/en/full-campervan-conversion/">What's included</a>
    </div>
  </div>
  <div class="hero-img">{b.pic(v["hero"], eager=True)}</div>
</div></section>

<section class="section alt"><div class="wrap narrow prose">
  {v["body"]}
  <h2>{esc(v["name"])}: useful facts</h2>
  <table class="facts">{facts}</table>
  <p class="muted" style="font-size:.9rem">Indicative dimensions and versions: they vary with year and body. We confirm your van's details before designing.</p>
</div></section>

<section class="section"><div class="wrap">
  <div class="price">
    <div>
      <p class="label">Full conversion on a {esc(v["name"])} · from</p>
      <p class="amount">{PRICE_EN}</p>
      <p class="note">Homologation and warranty included · Ready in 3 months</p>
      <p class="muted" style="font-size:.95rem">{PRICE_NOTE_EN}</p>
      <p>Insulation, marine HPL furniture, 200 Ah lithium with 400 W solar, 200 l of water, kitchen, bathroom, heating and homologation. Price of the conversion, van not included.</p>
      <div class="actions"><a class="btn btn-dark" href="/en/full-campervan-conversion/">See the full specification</a></div>
    </div>
    <div class="grid" style="grid-template-columns:repeat(2,1fr);margin:0">{gallery}</div>
  </div>
</div></section>

<section class="section alt"><div class="wrap narrow">
  <p class="label">Frequently asked questions</p><h2>Questions about converting a {esc(v["name"])}</h2>
  {faq_h}
  <h3 style="margin-top:40px">Other vans we convert</h3>
  <ul>{others}</ul>
</div></section>
{b.cta(f"Do you have a {v['name']}?", "Tell us the version and year and we'll propose a bespoke layout. We reply on WhatsApp.")}
"""
    return b.layout(f'/en/vans/{v["slug"]}/', v["title"], v["desc"], body, [cr_sc, faq_sc], active="/en/vans/")


def page_work(b):
    cr, cr_sc = b.crumbs([("Our work", "/en/our-work/")])
    blocks = ""
    for i, ((title, text), (_, _, slugs)) in enumerate(zip(PROJECTS_EN, b.PROJECTS)):
        grid = "".join(b.thumb_link(s, f"p{i}") for s in slugs)
        blocks += f'<article class="project"><h2>{esc(title)}</h2><p>{esc(text)}</p><div class="grid">{grid}</div></article>'
    body = f"""
<section class="section"><div class="wrap">
  {cr}
  <div class="section-head">
    <p class="kicker">Gallery</p>
    <h1>Our campervan conversions</h1>
    <p class="lead">Vans that have left our Málaga workshop. Tap any photo to see it full size.</p>
  </div>
  {blocks}
  <div class="split" style="margin-top:24px">
    <div>{b.pic("taller-lifes-campers-malaga")}</div>
    <div><p class="label">See them in person</p><h2>Visit our workshop</h2>
    <p>Photos are fine, but the finish is best appreciated up close. Message us and come to the workshop in San Julián, Málaga, to see how we work.</p>
    <div class="actions"><a class="btn btn-wa" href="{b.wa("Hello, I'd like to visit the workshop.")}" target="_blank" rel="noopener">{b.WA_SVG}Arrange a visit</a></div></div>
  </div>
</div></section>
{b.cta()}
"""
    return b.layout("/en/our-work/", "Campervan Conversions Built in Málaga | Lifes Campers",
                    "Gallery of full campervan conversions built in Málaga: Iveco Daily, Peugeot Boxer and more. Kitchens, bathrooms, beds and wooden finishes.",
                    body, [cr_sc], active="/en/our-work/")


def page_contact(b):
    cr, cr_sc = b.crumbs([("Contact", "/en/contact/")])
    options = "".join(f"<option>{esc(v['name'])}</option>" for v in VANS_EN)
    body = f"""
<section class="section"><div class="wrap">
  {cr}
  <div class="section-head"><p class="kicker">Let's talk</p><h1>Contact</h1>
  <p class="lead">The quickest way is WhatsApp. You can also call us, email us or come to the workshop. We speak English.</p></div>
  <div class="contact">
    <div>
      <div class="actions" style="margin-top:0">
        <a class="btn btn-wa" href="{b.wa()}" target="_blank" rel="noopener">{b.WA_SVG}WhatsApp {b.TEL1}</a>
        <a class="btn btn-wa" href="https://wa.me/34637313252" target="_blank" rel="noopener">{b.WA_SVG}WhatsApp {b.TEL2}</a>
      </div>
      <dl>
        <dt>Phone</dt><dd><a href="tel:+34637372296">+34 {b.TEL1}</a> · <a href="tel:+34637313252">+34 {b.TEL2}</a></dd>
        <dt>Phone hours</dt><dd>Monday to Friday, 8:00 to 14:00 (Spanish time)</dd>
        <dt>Email</dt><dd><a href="mailto:{b.EMAIL}">{b.EMAIL}</a></dd>
        <dt>Workshop</dt><dd>{esc(b.ADDRESS)}<br><a href="{b.MAPS}" target="_blank" rel="noopener">Open in Google Maps →</a></dd>
      </dl>
      <div style="margin-top:28px">{b.pic("taller-lifes-campers-fachada")}</div>
    </div>
    <form class="form" id="contact-form">
      <h2 style="font-size:1.6rem">Tell us about your project</h2>
      <input type="hidden" name="access_key" value="{b.WEB3FORMS_KEY}">
      <input type="hidden" name="subject" value="New message from camperizacionmalaga.com (English)">
      <input type="hidden" name="from_name" value="Lifes Campers website (EN)">
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">
      <div class="row">
        <div><label for="f-name">Name</label><input id="f-name" name="name" required autocomplete="name"></div>
        <div><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      </div>
      <label for="f-email">Email</label><input id="f-email" name="email" type="email" required autocomplete="email">
      <label for="f-van">Van</label>
      <select id="f-van" name="furgoneta"><option>I don't have a van yet</option>{options}<option>Other</option></select>
      <label for="f-msg">Message</label><textarea id="f-msg" name="message" required placeholder="Van version and year, how many of you travel, what you need…"></textarea>
      <label class="check"><input type="checkbox" required> I have read and accept the <a href="/en/privacy-policy/">privacy policy</a>.</label>
      <button class="btn btn-dark" type="submit">Send message</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</div></section>
"""
    return b.layout("/en/contact/", "Contact | Lifes Campers, Campervan Conversions in Málaga",
                    "Contact Lifes Campers: WhatsApp +34 637 37 22 96 · +34 637 31 32 52. Campervan conversion workshop in San Julián, Málaga. We speak English.",
                    body, [cr_sc], active="/en/contact/")


def _legal_holder(b):
    return f"""<table class="facts">
<tr><th>Owner</th><td>CROSSCAMPERS, S.L.</td></tr>
<tr><th>Trade name</th><td>Lifes Campers</td></tr>
<tr><th>Tax ID (CIF)</th><td>B93729606</td></tr>
<tr><th>Registered office</th><td>C/ Pascal, 14 · 29004 Málaga, Spain</td></tr>
<tr><th>Workshop</th><td>{esc(b.ADDRESS)}</td></tr>
<tr><th>Phone</th><td>+34 {b.TEL1} · +34 {b.TEL2}</td></tr>
<tr><th>Email</th><td>{b.EMAIL}</td></tr>
<tr><th>Website</th><td>camperizacionmalaga.com</td></tr>
</table>"""


TRANSLATION_NOTE = ('<p class="muted">This is an English translation for information purposes. '
                    'In the event of any discrepancy, the Spanish version prevails.</p>')


def _legal_page(b, path, title, h1, content, es_path):
    cr, cr_sc = b.crumbs([(h1, path)])
    y, m, d = b.LEGAL_UPDATED.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    body = (f'<section class="section"><div class="wrap narrow prose">{cr}<h1>{esc(h1)}</h1>{TRANSLATION_NOTE}{content}'
            f'<p class="muted">Last updated: {int(d)} {months[int(m) - 1]} {y}. '
            f'<a href="{es_path}" hreflang="es">Versión en español</a>.</p></div></section>')
    return b.layout(path, title, f"{h1} of camperizacionmalaga.com, the website of Lifes Campers (CROSSCAMPERS, S.L.).", body, [cr_sc])


def page_legal_notice(b):
    content = f"""
<h2>1. Company details</h2>
<p>In accordance with article 10 of Spanish Law 34/2002 on Information Society Services and Electronic Commerce (LSSI-CE), the details of the owner of this website are:</p>
{_legal_holder(b)}
<h2>2. Purpose and terms of use</h2>
<p>This website provides information about the campervan conversion services of Lifes Campers. Access is free and does not require registration. Using the site implies acceptance of this legal notice. Users agree to make proper use of the content and not to use it for unlawful purposes or in bad faith.</p>
<h2>3. Prices and commercial information</h2>
<p>The prices and equipment published are indicative, include the conditions stated in each case and may vary depending on the van and the final configuration agreed in writing with each customer.</p>
<h2>4. Intellectual and industrial property</h2>
<p>The texts, photographs, logos and design of this site are the property of CROSSCAMPERS, S.L. or are used with permission. Their reproduction, distribution or transformation without prior written authorisation is prohibited.</p>
<h2>5. Liability</h2>
<p>CROSSCAMPERS, S.L. strives to keep the information on this website accurate and up to date, but accepts no liability for errors or omissions, nor for damage arising from the use of the website or from links to third-party sites, whose content it does not control.</p>
<h2>6. Data protection and cookies</h2>
<p>The processing of personal data is explained in the <a href="/en/privacy-policy/">privacy policy</a> and the use of cookies in the <a href="/en/cookie-policy/">cookie policy</a>.</p>
<h2>7. Applicable law</h2>
<p>This legal notice is governed by Spanish law. Any dispute shall be submitted to the courts that have jurisdiction under the applicable regulations.</p>
"""
    return _legal_page(b, "/en/legal-notice/", "Legal Notice | Lifes Campers", "Legal notice", content, "/aviso-legal/")


def page_privacy(b):
    content = f"""
<h2>1. Data controller</h2>
{_legal_holder(b)}
<h2>2. What data we process and why</h2>
<p>We process the data you give us when you contact us through the contact form, WhatsApp, phone or email (name, email, phone and the details of your enquiry) solely to <strong>reply to your request</strong> and, if you hire us, to manage the business relationship and invoicing.</p>
<h2>3. Legal basis</h2>
<p>The consent you give us when you send your enquiry (art. 6.1.a GDPR) and, where applicable, the performance of a contract or pre-contractual steps at your request (art. 6.1.b GDPR), as well as compliance with legal obligations such as tax obligations (art. 6.1.c GDPR).</p>
<h2>4. Retention</h2>
<p>We keep enquiry data for as long as needed to deal with it and, at most, one year if you do not become a customer. Customer data is kept for the duration of the business relationship and the legal periods that follow.</p>
<h2>5. Recipients</h2>
<p>We do not share your data with third parties unless required by law. To provide the service we use providers acting as data processors: Web3Forms, which receives the form messages and forwards them to us by email, and Cloudflare, which hosts this website. Some of these providers may process data outside the European Economic Area with the safeguards provided for in the GDPR (standard contractual clauses or adequacy frameworks).</p>
<h2>6. Your rights</h2>
<p>You can exercise your rights of access, rectification, erasure, objection, restriction and portability by writing to <a href="mailto:{b.EMAIL}">{b.EMAIL}</a> or by post to C/ Pascal, 14 · 29004 Málaga, Spain, stating which right you wish to exercise. If you believe we have not handled your request properly, you can complain to the Spanish Data Protection Agency (<a href="https://www.aepd.es" target="_blank" rel="noopener">www.aepd.es</a>).</p>
"""
    return _legal_page(b, "/en/privacy-policy/", "Privacy Policy | Lifes Campers", "Privacy policy", content, "/politica-de-privacidad/")


def page_cookies(b):
    content = """
<h2>What are cookies?</h2>
<p>Cookies are small files that some websites store in your browser to remember information about your visit.</p>
<h2>Cookies used on this website</h2>
<p>This website <strong>does not use analytics, advertising or tracking cookies</strong>, and does not include third-party videos, maps or social buttons that would set them. That is why we don't show you a banner asking you to accept them.</p>
<p>Our hosting provider, Cloudflare, may use strictly necessary technical cookies for the site's security (for example, to filter malicious traffic). These cookies do not require consent under article 22.2 of the Spanish LSSI-CE.</p>
<p>Links to WhatsApp, Instagram, Facebook or Google Maps take you to those platforms, which apply their own cookie policies.</p>
<h2>How to manage cookies</h2>
<p>You can view and delete cookies in your browser settings (Chrome, Safari, Firefox, Edge…).</p>
<h2>Changes</h2>
<p>If we add tools that use non-technical cookies in the future, we will update this policy and ask for your consent before setting them.</p>
"""
    return _legal_page(b, "/en/cookie-policy/", "Cookie Policy | Lifes Campers", "Cookie policy", content, "/politica-de-cookies/")


def pages(b):
    out = {
        "/en/": page_home(b),
        "/en/full-campervan-conversion/": page_integral(b),
        "/en/vans/": page_vans(b),
        "/en/our-work/": page_work(b),
        "/en/contact/": page_contact(b),
        "/en/legal-notice/": page_legal_notice(b),
        "/en/privacy-policy/": page_privacy(b),
        "/en/cookie-policy/": page_cookies(b),
    }
    for v in VANS_EN:
        out[f'/en/vans/{v["slug"]}/'] = page_van(b, v)
    return out
