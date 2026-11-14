"""Página «Opciones y acabados» (/opciones-y-acabados/ y /en/options-and-finishes/).

Recoge las configuraciones y colores que se ven en las entregas publicadas en Instagram
(@malagalifescamper). Las fotos están en src/fotos/ y sus textos alternativos, en ALT_OPC.
"""
from html import escape as esc

PATH = {"es": "/opciones-y-acabados/", "en": "/en/options-and-finishes/"}

# slug -> (texto alternativo en español, en inglés)
ALT_OPC = {
    "cama-elevable-electrica-dinette-mostaza": ("Cama eléctrica subida al techo sobre una dinette con sofás mostaza y mesa central", "Electric bed raised to the ceiling above a dinette with mustard sofas and a central table"),
    "camper-cama-electrica-subida-trasera": ("Camper vista desde las puertas traseras con la cama eléctrica recogida arriba y el salón debajo", "Camper seen from the rear doors with the electric bed stowed up high and the lounge below"),
    "camper-dos-camas-elevable-blanca": ("Dos camas en la parte trasera de una camper: una elevable arriba y otra fija abajo, con colchones blancos", "Two beds at the back of a camper: a lifting bed on top and a fixed one below, with white mattresses"),
    "cama-elevable-somier-lamas": ("Cama elevable con somier de lamas sobre la cama inferior, techo de lamas de madera y claraboya", "Lifting bed with a slatted base above the lower bed, wooden slat ceiling and roof vent"),
    "cama-elevable-sofas-cama-azul-noche": ("Cama superior recogida y sofás convertidos en cama doble con tapizado azul noche", "Upper bed stowed and sofas turned into a double bed with midnight-blue upholstery"),
    "camper-dos-camas-garaje-azul": ("Puertas traseras abiertas con dos camas en azul noche y garaje con armarios de madera debajo", "Rear doors open showing two midnight-blue beds and a garage with wooden lockers below"),
    "camper-dos-camas-tapizado-fucsia": ("Dos camas con tapizado fucsia, somier de lamas y techo de friso de pino", "Two beds with fuchsia upholstery, slatted base and pine-clad ceiling"),
    "cama-superior-somier-verde-oliva": ("Cama superior con somier de lamas y colchón verde oliva sobre la cama inferior", "Upper bed with a slatted base and olive-green mattress above the lower bed"),
    "garaje-pasante-bajo-cama": ("Garaje pasante bajo la cama, forrado en madera, con luz y puertas laterales", "Through-garage under the bed, wood-lined, with a light and side lockers"),
    "cama-fija-trasera-garaje-rotulo": ("Cama fija trasera con colchón beige y nombre de la camper rotulado en el frontal", "Fixed rear bed with a beige mattress and the camper's name lettered on the front"),
    "cama-fija-trasera-garaje-gris": ("Cama fija trasera con garaje debajo, muebles en gris textil y techo de lamas", "Fixed rear bed with a garage below, grey textile-finish furniture and slat ceiling"),
    "sofas-en-u-cama-azul-petroleo": ("Cama trasera formada con los sofás en U, tapizado azul petróleo y techo de madera oscura", "Rear bed made from the U-shaped sofas, petrol-blue upholstery and dark wood ceiling"),
    "crafter-sofas-en-u-crema": ("Salón en U con tapizado crema en una Volkswagen Crafter, techo de pino y armarios blancos", "U-shaped lounge with cream upholstery in a Volkswagen Crafter, pine ceiling and white cabinets"),
    "cama-gran-formato-terracota": ("Cama de gran formato con colchón terracota que ocupa la zona trasera de la camper", "Large-format bed with a terracotta mattress filling the back of the camper"),
    "garaje-bandeja-extraible": ("Garaje trasero con bandeja extraíble que sale por las puertas traseras", "Rear garage with a pull-out tray that slides out through the back doors"),
    "dinette-sofas-enfrentados-gris-perla": ("Dinette con sofás enfrentados gris perla, mesa de madera y muebles en roble claro", "Dinette with facing pearl-grey sofas, wooden table and light-oak furniture"),
    "dinette-turquesa-vista-trasera": ("Dinette trasera con sofás turquesa y mesa central vista desde las puertas traseras", "Rear dinette with turquoise sofas and a central table seen from the back doors"),
    "dinette-arena-techo-lamas": ("Dinette con sofás color arena, mesa blanca y techo de lamas de madera", "Dinette with sand-coloured sofas, white table and wooden slat ceiling"),
    "asientos-giratorios-mesa-bambu": ("Asientos delanteros giratorios con mesa de bambú y muebles en gris textil", "Swivel front seats with a bamboo table and grey textile-finish furniture"),
    "banco-mostaza-mesa-pared": ("Banco con cojines mostaza, mesa abatible a la pared y cortina a juego", "Bench with mustard cushions, wall-mounted folding table and matching curtain"),
    "dinette-tapizado-cuero-cognac": ("Dinette en L con tapizado color coñac, techo de lamas y ventana con mosquitera", "L-shaped dinette in cognac upholstery, slat ceiling and window with insect screen"),
    "dinette-azul-marino-ventana": ("Dinette con tapizado azul marino, mesa blanca y encimera de madera oscura", "Dinette with navy-blue upholstery, white table and dark wood worktop"),
    "mesa-ilustrada-asientos-giratorios": ("Mesa verde salvia con una ilustración de montañas y asientos delanteros giratorios", "Sage-green table with a mountain illustration and swivel front seats"),
    "dinette-naranja-pino-natural": ("Dinette trasera con cojines naranja, interior de pino natural y cama superior", "Rear dinette with orange cushions, natural pine interior and upper bed"),
    "cocina-encimera-marmol-blanco": ("Cocina de camper con encimera efecto mármol blanco, placa de cristal y grifo negro", "Camper kitchen with a white marble-effect worktop, glass hob and black tap"),
    "cocina-marmol-verde-encimera-bambu": ("Cocina con frontal de mármol verde y dorado, encimera de bambú y nevera de compresor", "Kitchen with a green and gold marble splashback, bamboo worktop and compressor fridge"),
    "cocina-encimera-madera-rustica-grifo-rosa": ("Encimera de madera maciza de borde natural con fregadero redondo y grifo rosa", "Live-edge solid wood worktop with a round sink and pink tap"),
    "cocina-horno-fuegos-tapa-madera": ("Cocina con horno, fuegos de gas y tapa de madera barnizada levantada", "Kitchen with an oven, gas burners and a varnished wooden lid raised"),
    "cocina-fuegos-gas-azulejo-beige": ("Fuegos de gas sobre encimera de madera clara con azulejo beige alargado", "Gas burners on a light wood worktop with elongated beige tiles"),
    "cocina-azulejo-verde-grifo-dorado": ("Cocina con azulejo verde, grifo negro y dorado, fregadero negro y muebles blancos", "Kitchen with green tiles, black and gold tap, black sink and white cabinets"),
    "cocina-tres-fuegos-gas": ("Cocina en L con fuegos de gas, grifo dorado y vista hacia la dinette", "L-shaped kitchen with gas burners, gold tap and a view towards the dinette"),
    "cocina-placa-escamas-verde": ("Placa de cristal en encimera de bambú con azulejo de escamas verde oscuro", "Glass hob on a bamboo worktop with dark-green fish-scale tiles"),
    "cocina-escamas-salvia-fregadero": ("Fregadero con tapa en encimera de bambú y azulejo de escamas verde salvia", "Sink with a lid on a bamboo worktop and sage-green fish-scale tiles"),
    "cocina-azulejo-hidraulico-color": ("Cocina con azulejo hidráulico de colores, placa de cristal, nevera y tiradores de cuero", "Kitchen with colourful patterned tiles, glass hob, fridge and leather handles"),
    "cocina-placa-tiradores-cuero": ("Placa de cristal, cajones blancos con tiradores de cuero y azulejo hidráulico azul", "Glass hob, white drawers with leather handles and blue patterned tiles"),
    "cocina-muebles-negros-bambu": ("Cocina con muebles negros, tiradores de cuero, encimera de bambú y fuegos de gas", "Kitchen with black cabinets, leather handles, bamboo worktop and gas burners"),
    "cocina-encimera-madera-oscura": ("Cocina larga con encimera de madera oscura, fuegos de gas y armarios blancos", "Long kitchen with a dark wood worktop, gas burners and white cabinets"),
    "fregadero-tapa-bambu-grifo-negro": ("Fregadero oculto bajo tapa de bambú y grifo negro flexible", "Sink hidden under a bamboo lid and flexible black tap"),
    "cocina-sprinter-madera-natural": ("Cocina de Mercedes Sprinter en madera natural con fregadero, grifo negro y azulejo beige", "Mercedes Sprinter kitchen in natural wood with sink, black tap and beige tiles"),
    "cocina-crafter-gas-nevera": ("Cocina de Volkswagen Crafter con fuegos de gas, nevera y azulejo metro blanco", "Volkswagen Crafter kitchen with gas burners, fridge and white metro tiles"),
    "bano-panel-marmol-blanco": ("Baño con paredes efecto mármol blanco de vetas negras, ducha y grifo negro", "Bathroom with white marble-effect walls with black veining, shower and black tap"),
    "bano-puerta-cristal-vetas": ("Puerta de baño con ventanas translúcidas y armario alto", "Bathroom door with translucent windows and tall wardrobe"),
    "bano-azulejo-metro-tarima": ("Baño con azulejo metro blanco, WC de cassette, ducha negra y tarima de madera", "Bathroom with white metro tiles, cassette toilet, black shower and wooden duckboard"),
    "bano-azulejo-metro-wc": ("Baño con azulejo metro blanco, WC de cassette y ducha con grifo negro", "Bathroom with white metro tiles, cassette toilet and shower with black tap"),
    "bano-arco-azulejo-verde": ("Baño con puerta en arco y azulejo verde en espiga, junto a la dinette", "Bathroom with an arched doorway and green herringbone tiles, next to the dinette"),
    "bano-puerta-espejo-redondo": ("Puerta de baño con espejo redondo y listones de madera", "Bathroom door with a round mirror and wooden battens"),
    "bano-ventana-cortina": ("Baño con ventana, azulejo blanco, ducha negra y cortina", "Bathroom with a window, white tiles, black shower and curtain"),
    "ducha-claraboya-grifo-negro": ("Ducha con claraboya, azulejo blanco y grifería negra", "Shower with a roof vent, white tiles and black fittings"),
    "techo-lamas-madera-tapizado-turquesa": ("Techo de lamas de madera con luz LED bajo los armarios y sofás turquesa", "Wooden slat ceiling with LED light under the cabinets and turquoise sofas"),
    "techo-friso-pino-claraboya": ("Techo de friso de pino con claraboya y focos empotrados", "Pine-clad ceiling with a roof vent and recessed spotlights"),
    "techo-madera-oscura-friso-blanco": ("Techo de madera oscura, paredes de friso blanco y suelo de madera", "Dark wood ceiling, white tongue-and-groove walls and wood-effect floor"),
    "techo-lamas-paredes-pino": ("Techo de lamas y paredes de pino natural vistos desde las puertas traseras", "Slat ceiling and natural pine walls seen from the rear doors"),
    "techo-pino-flexos-lectura": ("Techo de pino con flexos de lectura y claraboya sobre la cama", "Pine ceiling with reading lights and a roof vent above the bed"),
    "panel-control-tactil-camper": ("Panel de control táctil de la camper con interruptores y USB", "Camper touch control panel with switches and USB socket"),
    "rotulo-personalizado-camper": ("Nombre de la camper rotulado sobre la ventana y asientos giratorios", "Camper name lettered above the window and swivel seats"),
    "dinette-tv-friso-blanco": ("Dinette con televisión en brazo extensible, friso blanco y armario de baño", "Dinette with a TV on an extending arm, white panelling and bathroom cabinet"),
    "camper-ducato-gris-ruedas-todoterreno": ("Fiat Ducato gris camperizada con llantas negras y ruedas todoterreno", "Grey camperised Fiat Ducato with black wheels and all-terrain tyres"),
    "camper-boxer-escalon-toldo": ("Peugeot Boxer camperizada con escalón y puerta lateral abierta", "Camperised Peugeot Boxer with entry step and open side door"),
    "sprinter-cama-elevable-dinette": ("Mercedes Sprinter 4x4 con cama elevable sobre la dinette y sofás grises", "Mercedes Sprinter 4x4 with a lifting bed above the dinette and grey sofas"),
}

T = {
    "es": {
        "title": "Opciones y acabados para tu camper: camas, cocina, baño y colores | Lifes Campers",
        "desc": "Todas las configuraciones que montamos en Málaga: cama eléctrica elevable, cama fija con garaje, dinette, cocina de gas o placa, baño con ducha, colores de tapicería, encimeras y techos.",
        "crumb": "Opciones y acabados", "kicker": "Configura tu camper",
        "h1": "Opciones y acabados de nuestras campers",
        "lead": "Estas son las distribuciones, colores y acabados que ya hemos montado en furgonetas de clientes. Cada camper se diseña a medida: combina lo que más te guste y lo adaptamos a tu furgoneta.",
        "toc": "En esta página", "photos": "fotos",
        "note": "Las fotos son entregas reales de nuestro taller. Algunas opciones pueden cambiar el presupuesto final; te lo concretamos al cerrar el diseño.",
        "pal_label": "Colores de tapicería", "pal_h": "Colores que ya han elegido nuestros clientes",
        "pal_text": "Tapizamos sofás, colchones y cojines en el tono que quieras. Estos son algunos de los que hemos hecho:",
        "visit_h": "¿Lo quieres ver en persona?",
        "visit": "Los acabados se aprecian mejor de cerca. Escríbenos, cuéntanos qué opciones te gustan y te enseñamos campers en el taller de San Julián, Málaga.",
        "visit_btn": "Pedir información", "visit_msg": "Hola, me gustaría información sobre las opciones y acabados de vuestras campers.",
        "more": "Ver más trabajos", "more_href": "/trabajos/",
    },
    "en": {
        "title": "Campervan Options and Finishes: Beds, Kitchens, Bathrooms, Colours | Lifes Campers",
        "desc": "Every layout we build in Málaga: electric lifting bed, fixed bed with garage, dinette, gas or electric hob, bathroom with shower, upholstery colours, worktops and ceilings.",
        "crumb": "Options and finishes", "kicker": "Design your camper",
        "h1": "Options and finishes for your camper",
        "lead": "These are the layouts, colours and finishes we have already built into our customers' vans. Every camper is bespoke: mix the ones you like and we adapt them to your van.",
        "toc": "On this page", "photos": "photos",
        "note": "The photos show real handovers from our workshop. Some options may change the final quote; we confirm it when we close the design.",
        "pal_label": "Upholstery colours", "pal_h": "Colours our customers have chosen",
        "pal_text": "We upholster sofas, mattresses and cushions in the shade you want. These are some we have made:",
        "visit_h": "Want to see it in person?",
        "visit": "Finishes are best appreciated up close. Message us, tell us which options you like and we'll show you campers at our workshop in San Julián, Málaga.",
        "visit_btn": "Ask for information", "visit_msg": "Hello, I'd like information about the options and finishes for your campers.",
        "more": "See more of our work", "more_href": "/en/our-work/",
    },
}

# (id, (título es, en), (intro es, en), [((opción es, en), (texto es, en), [fotos])])
SECTIONS = [
    ("camas", ("Distribución y camas", "Layout and beds"),
     ("La cama marca la distribución de la camper. Trabajamos con cuatro soluciones y las combinamos según cuántas personas vayáis a dormir.",
      "The bed sets the camper's layout. We work with four solutions and combine them depending on how many of you will sleep on board."),
     [
         (("Cama eléctrica elevable", "Electric lifting bed"),
          ("Sube al techo con un botón y deja libre el salón de día. Por la noche baja sobre la dinette y tienes cama sin montar nada.",
           "It rises to the ceiling at the press of a button and frees up the lounge during the day. At night it lowers over the dinette, ready to sleep in without setting anything up."),
          ["cama-elevable-electrica-dinette-mostaza", "camper-cama-electrica-subida-trasera", "sprinter-cama-elevable-dinette"]),
         (("Dos camas: elevable + inferior", "Two beds: lifting + lower"),
          ("Una cama superior con somier de lamas y otra abajo, que de día son sofás. Cuatro plazas para dormir en la misma furgoneta.",
           "An upper bed with a slatted base and another below that works as sofas by day. Four sleeping places in the same van."),
          ["camper-dos-camas-elevable-blanca", "cama-elevable-somier-lamas", "cama-elevable-sofas-cama-azul-noche", "camper-dos-camas-garaje-azul", "camper-dos-camas-tapizado-fucsia", "cama-superior-somier-verde-oliva"]),
         (("Cama fija trasera con garaje", "Fixed rear bed with garage"),
          ("Siempre montada, transversal y en alto. Debajo queda un garaje para bicis, tablas, sillas o el material de trabajo.",
           "Always made up, crosswise and raised. Underneath there is a garage for bikes, boards, chairs or work gear."),
          ["cama-fija-trasera-garaje-rotulo", "cama-fija-trasera-garaje-gris", "garaje-pasante-bajo-cama"]),
         (("Sofás en U convertibles", "Convertible U-shaped sofas"),
          ("Un salón amplio con sofás a los lados que se convierte en una cama de matrimonio grande. Ideal para quien quiere espacio de día.",
           "A spacious lounge with side sofas that turns into a large double bed. Ideal if you want space during the day."),
          ["sofas-en-u-cama-azul-petroleo", "crafter-sofas-en-u-crema", "cama-gran-formato-terracota"]),
         (("Garaje con bandeja extraíble", "Garage with pull-out tray"),
          ("Bajo la cama puede ir una bandeja que sale por las puertas traseras para cargar y descargar sin agacharse.",
           "Under the bed we can fit a tray that slides out through the rear doors, so you load and unload without bending over."),
          ["garaje-bandeja-extraible"]),
     ]),
    ("comedor", ("Comedor y asientos", "Dining and seating"),
     ("Los asientos delanteros giratorios se suman al comedor. Elegimos mesa, tapizado y posición según cómo uses la camper.",
      "The swivel front seats join the dining area. We choose the table, upholstery and position based on how you use the camper."),
     [
         (("Dinette trasera con sofás enfrentados", "Rear dinette with facing sofas"),
          ("Dos sofás frente a frente con mesa central de pie. Cómoda para comer cuatro y, en muchas configuraciones, se convierte en cama.",
           "Two sofas facing each other with a central pedestal table. Comfortable for four to eat and, in many layouts, it becomes a bed."),
          ["dinette-sofas-enfrentados-gris-perla", "dinette-turquesa-vista-trasera", "dinette-arena-techo-lamas", "dinette-naranja-pino-natural"]),
         (("Asientos giratorios y mesa delantera", "Swivel seats and front table"),
          ("Los asientos de la cabina giran hacia el salón y comparten mesa con el banco trasero homologado.",
           "The cab seats swivel towards the lounge and share a table with the homologated rear bench."),
          ["asientos-giratorios-mesa-bambu", "mesa-ilustrada-asientos-giratorios", "rotulo-personalizado-camper"]),
         (("Banco con mesa abatible", "Bench with folding table"),
          ("Un banco lateral con mesa que se pliega a la pared: deja el pasillo libre cuando no la usas.",
           "A side bench with a table that folds against the wall, keeping the aisle clear when you don't need it."),
          ["banco-mostaza-mesa-pared"]),
         (("Dinette en L", "L-shaped dinette"),
          ("Sofá en esquina con mesa regulable, muy aprovechado en furgonetas largas como la L4H3.",
           "Corner sofa with an adjustable table, a great use of space in long vans such as the L4H3."),
          ["dinette-tapizado-cuero-cognac", "dinette-azul-marino-ventana", "dinette-tv-friso-blanco"]),
     ]),
    ("cocina", ("Cocina", "Kitchen"),
     ("Cocina lineal o en L, con fregadero, nevera de compresor y una extensión de encimera abatible para tener más superficie de trabajo.",
      "Straight or L-shaped kitchen with sink, compressor fridge and a folding worktop extension for extra work surface."),
     [
         (("Fuegos de gas u horno", "Gas burners or oven"),
          ("Fogón de dos o tres fuegos y, si cocinas mucho, horno integrado. Con tapa de madera que hace de encimera cuando está cerrada.",
           "Two or three burners and, if you cook a lot, a built-in oven. With a wooden lid that doubles as worktop when closed."),
          ["cocina-horno-fuegos-tapa-madera", "cocina-tres-fuegos-gas", "cocina-fuegos-gas-azulejo-beige", "cocina-crafter-gas-nevera"]),
         (("Placa eléctrica de cristal", "Electric glass hob"),
          ("Placa empotrada a ras de encimera, fácil de limpiar, alimentada por la instalación eléctrica de la camper.",
           "Hob fitted flush with the worktop, easy to clean and powered by the camper's electrical system."),
          ["cocina-placa-escamas-verde", "cocina-placa-tiradores-cuero", "cocina-encimera-marmol-blanco"]),
         (("Encimeras", "Worktops"),
          ("Bambú, madera clara maciza, madera oscura barnizada, efecto mármol blanco o madera de borde natural. El fregadero puede ir oculto bajo una tapa.",
           "Bamboo, light solid wood, dark varnished wood, white marble effect or live-edge wood. The sink can hide under a lid."),
          ["cocina-marmol-verde-encimera-bambu", "cocina-encimera-madera-oscura", "cocina-encimera-madera-rustica-grifo-rosa", "fregadero-tapa-bambu-grifo-negro", "cocina-sprinter-madera-natural"]),
         (("Frontales y azulejos", "Splashbacks and tiles"),
          ("Azulejo de escamas (verde oscuro o salvia), hidráulico de colores, metro blanco o verde, mármol verde o beige alargado.",
           "Fish-scale tiles (dark green or sage), colourful patterned tiles, white or green metro tiles, green marble or long beige tiles."),
          ["cocina-escamas-salvia-fregadero", "cocina-azulejo-hidraulico-color", "cocina-azulejo-verde-grifo-dorado"]),
         (("Muebles y tiradores", "Cabinets and handles"),
          ("Frentes blancos, negros, gris piedra, verde salvia o roble. Tiradores negros, de cuero o con uñero. Grifo negro, dorado o de color.",
           "Fronts in white, black, stone grey, sage green or oak. Black, leather or recessed handles. Black, gold or coloured tap."),
          ["cocina-muebles-negros-bambu"]),
     ]),
    ("bano", ("Baño y ducha", "Bathroom and shower"),
     ("Baño cerrado con WC de cassette y ducha, revestido para que aguante el agua. Cambian el acabado de las paredes y la puerta.",
      "Enclosed bathroom with cassette toilet and shower, lined to withstand water. The wall finish and door are up to you."),
     [
         (("Azulejo metro blanco", "White metro tiles"),
          ("El clásico: luminoso y fácil de limpiar, con grifería negra. Puede llevar tarima de madera en el plato o ventana.",
           "The classic: bright and easy to clean, with black fittings. It can have a wooden duckboard on the tray or a window."),
          ["bano-azulejo-metro-wc", "bano-azulejo-metro-tarima", "ducha-claraboya-grifo-negro", "bano-ventana-cortina"]),
         (("Efecto mármol", "Marble effect"),
          ("Paredes efecto mármol blanco con vetas oscuras para un baño más elegante.",
           "White marble-effect walls with dark veining for a more elegant bathroom."),
          ["bano-panel-marmol-blanco"]),
         (("Azulejo de color", "Coloured tiles"),
          ("Verde en espiga con puerta en arco, o el color que combine con tu cocina.",
           "Green herringbone with an arched doorway, or the colour that matches your kitchen."),
          ["bano-arco-azulejo-verde"]),
         (("Puertas de baño", "Bathroom doors"),
          ("Lisa, con ventanas translúcidas o con espejo redondo y listones de madera.",
           "Plain, with translucent windows or with a round mirror and wooden battens."),
          ["bano-puerta-cristal-vetas", "bano-puerta-espejo-redondo"]),
     ]),
    ("techos", ("Techos, paredes y suelo", "Ceilings, walls and floor"),
     ("El revestimiento define el estilo del interior: más nórdico, más cálido o más moderno.",
      "The lining sets the interior's style: more Nordic, warmer or more modern."),
     [
         (("Techo de lamas de madera", "Wooden slat ceiling"),
          ("Lamas de madera sobre fondo oscuro, con focos y tiras LED integrados.",
           "Wooden slats over a dark background, with built-in spotlights and LED strips."),
          ["techo-lamas-madera-tapizado-turquesa", "techo-lamas-paredes-pino"]),
         (("Friso de pino natural", "Natural pine cladding"),
          ("Madera clara en techo y, si quieres, en paredes: el interior más cálido y luminoso.",
           "Light wood on the ceiling and, if you like, the walls: the warmest, brightest interior."),
          ["techo-friso-pino-claraboya", "techo-pino-flexos-lectura"]),
         (("Madera oscura y friso blanco", "Dark wood and white panelling"),
          ("Techo en madera oscura con paredes de friso blanco y suelo de madera a juego.",
           "Dark wood ceiling with white tongue-and-groove walls and matching wood-effect floor."),
          ["techo-madera-oscura-friso-blanco"]),
     ]),
    ("extras", ("Iluminación y extras", "Lighting and extras"),
     ("Los detalles que hacen la camper más tuya y más cómoda en ruta.",
      "The details that make the camper more yours and more comfortable on the road."),
     [
         (("Panel de control y luces", "Control panel and lighting"),
          ("Panel táctil para manejar la instalación de la camper, tiras LED bajo los armarios, focos empotrados y flexos de lectura.",
           "Touch panel to run the camper's systems, LED strips under the cabinets, recessed spotlights and reading lights."),
          ["panel-control-tactil-camper", "techo-pino-flexos-lectura"]),
         (("Personalización", "Personal touches"),
          ("El nombre de tu camper rotulado, una mesa ilustrada o la televisión en brazo extensible.",
           "Your camper's name lettered on, an illustrated table or a TV on an extending arm."),
          ["rotulo-personalizado-camper", "mesa-ilustrada-asientos-giratorios", "dinette-tv-friso-blanco"]),
         (("Exterior", "Exterior"),
          ("Escalón de acceso y ruedas todoterreno para salir del asfalto.",
           "Entry step and all-terrain tyres to leave the tarmac behind."),
          ["camper-boxer-escalon-toldo", "camper-ducato-gris-ruedas-todoterreno"]),
     ]),
]

# (nombre es, en, color aproximado para la muestra, foto)
PALETTE = [
    (("Gris perla", "Pearl grey"), "#b9b4ad", "dinette-sofas-enfrentados-gris-perla"),
    (("Arena", "Sand"), "#c9b08c", "dinette-arena-techo-lamas"),
    (("Crema", "Cream"), "#e6dccb", "crafter-sofas-en-u-crema"),
    (("Mostaza", "Mustard"), "#d1a032", "cama-elevable-electrica-dinette-mostaza"),
    (("Naranja", "Orange"), "#e0752b", "dinette-naranja-pino-natural"),
    (("Terracota", "Terracotta"), "#b0502f", "cama-gran-formato-terracota"),
    (("Coñac", "Cognac"), "#a0653a", "dinette-tapizado-cuero-cognac"),
    (("Turquesa", "Turquoise"), "#3e8e8f", "dinette-turquesa-vista-trasera"),
    (("Azul petróleo", "Petrol blue"), "#2f6170", "sofas-en-u-cama-azul-petroleo"),
    (("Azul marino", "Navy blue"), "#2f3e5c", "dinette-azul-marino-ventana"),
    (("Azul noche", "Midnight blue"), "#3d4054", "cama-elevable-sofas-cama-azul-noche"),
    (("Verde oliva", "Olive green"), "#8b8a4a", "cama-superior-somier-verde-oliva"),
    (("Fucsia", "Fuchsia"), "#9c1f6e", "camper-dos-camas-tapizado-fucsia"),
    (("Blanco roto", "Off-white"), "#eeeae2", "camper-dos-camas-elevable-blanca"),
]


def register(b, alt_en):
    for slug, (es, en) in ALT_OPC.items():
        b.ALT[slug] = es
        alt_en[slug] = en
    b.ALTERNATES[PATH["es"]] = b.ALTERNATES[PATH["en"]] = dict(PATH)


def page(b, lang):
    t = T[lang]
    i = 0 if lang == "es" else 1
    path = PATH[lang]
    cr, cr_sc = b.crumbs([(t["crumb"], path)])
    toc = "".join(f'<a href="#{sid}">{esc(titles[i])}</a>' for sid, titles, _, _ in SECTIONS)
    sections = ""
    for n, (sid, titles, intro, opts) in enumerate(SECTIONS):
        cards = ""
        for k, (name, text, slugs) in enumerate(opts):
            grid = "".join(b.thumb_link(s, f"{sid}{k}") for s in slugs)
            cards += (f'<article class="opt"><h3>{esc(name[i])}</h3><p>{esc(text[i])}</p>'
                      f'<div class="grid">{grid}</div></article>')
        alt_cls = " alt" if n % 2 == 0 else ""
        sections += (f'<section class="section{alt_cls}" id="{sid}"><div class="wrap">'
                     f'<div class="section-head"><p class="label">{n + 1:02d}</p><h2>{esc(titles[i])}</h2>'
                     f'<p class="lead">{esc(intro[i])}</p></div>{cards}</div></section>')
        if sid == "comedor":
            sw = "".join(f'<li><a href="/img/{s}-1200.webp" data-lb="paleta"><img src="/img/{s}-600.webp" width="600" height="600" '
                         f'alt="{esc(b.alt(s))}" loading="lazy" decoding="async"><span><i class="dot" style="background:{c}"></i>'
                         f'{esc(name[i])}</span></a></li>' for name, c, s in PALETTE)
            sections += (f'<section class="section" id="colores"><div class="wrap">'
                         f'<div class="section-head"><p class="label">{esc(t["pal_label"])}</p><h2>{esc(t["pal_h"])}</h2>'
                         f'<p class="lead">{esc(t["pal_text"])}</p></div><ul class="swatches">{sw}</ul></div></section>')
    body = f"""
<section class="section"><div class="wrap">
  {cr}
  <div class="section-head">
    <p class="kicker">{esc(t["kicker"])}</p>
    <h1>{esc(t["h1"])}</h1>
    <p class="lead">{esc(t["lead"])}</p>
  </div>
  <nav class="toc" aria-label="{esc(t["toc"])}">{toc}<a href="#colores">{esc(t["pal_label"])}</a></nav>
  <p class="muted" style="font-size:.92rem">{esc(t["note"])}</p>
</div></section>
{sections}
<section class="section alt"><div class="wrap">
  <div class="split">
    <div>{b.pic("taller-lifes-campers-malaga")}</div>
    <div><h2>{esc(t["visit_h"])}</h2><p>{esc(t["visit"])}</p>
    <div class="actions"><a class="btn btn-wa" href="{b.wa(t["visit_msg"])}" target="_blank" rel="noopener">{b.WA_SVG}{esc(t["visit_btn"])}</a>
    <a class="btn btn-line" href="{t["more_href"]}">{esc(t["more"])}</a></div></div>
  </div>
</div></section>
{b.cta()}
"""
    return b.layout(path, t["title"], t["desc"], body, [cr_sc], active=path, og_img=f"{b.SITE}/img/cama-elevable-electrica-dinette-mostaza-1200.webp")
