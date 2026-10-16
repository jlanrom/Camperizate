# Enlaces de pago de Stripe (Payment Links)

La tienda (`/boutique/`) no tiene servidor: cada botón de compra abre un **Payment Link** de Stripe.
Se crean una vez en el panel de Stripe y se pegan en `STRIPE` dentro de `tools/build.py`.
Mientras un enlace está vacío, su botón dice «Commander par message» y abre el formulario de Tally.

## 0. Una sola vez, antes de crear enlaces

1. **Ajustes → Detalles públicos de la empresa**: nombre «Camperizate», e-mail y teléfono de atención,
   y la URL de condiciones: `https://kitamenagement.fr/conditions-generales-de-vente/`.
   Esto permite pedir al cliente que acepte las CGV en la página de pago.
2. **IVA**: los precios de la web son TTC (IVA incluido). Al crear cada precio, márcalo como
   «incluye impuestos». Consulta con el gestor qué IVA aplicar a las ventas a Francia (OSS o IVA francés
   por el local de Nîmes) y si conviene activar Stripe Tax.
3. **Tarifas de envío** (Productos → Tarifas de envío), créalas una vez y reutilízalas:
   - `Retrait au showroom de Nîmes` · 0 €
   - `Livraison France métropolitaine – ludospace` · 200 €
   - `Livraison France métropolitaine – van compact` · 250 €
   - `Avec mon kit ou retrait à Nîmes` · 0 € (para accesorios)
4. **Opciones del kit** como productos (para añadirlas como «artículos opcionales» en los enlaces de kit):
   Équerre rabattable 25 € · Plateau frigo 25 € · Tiroir frigo coulissant 50 € · Égouttoir 35 € · Version 2+1 100 €.

## 1. Los 12 enlaces de kit

| Clave en `STRIPE` | Nombre del producto en Stripe | Precio TTC | Envío |
| --- | --- | --- | --- |
| `kit-mini-pin-sans` | Kit ludospace – Phénolique pin – sans matelas | 500 € | ludospace |
| `kit-mini-pin-avec` | Kit ludospace – Phénolique pin – avec matelas | 650 € | ludospace |
| `kit-mini-carrossier-sans` | Kit ludospace – Phénolique carrossier – sans matelas | 550 € | ludospace |
| `kit-mini-carrossier-avec` | Kit ludospace – Phénolique carrossier – avec matelas | 700 € | ludospace |
| `kit-mini-hpl-sans` | Kit ludospace – HPL de peuplier – sans matelas | 800 € | ludospace |
| `kit-mini-hpl-avec` | Kit ludospace – HPL de peuplier – avec matelas | 950 € | ludospace |
| `kit-moyen-pin-sans` | Kit van compact – Phénolique pin – sans matelas | 700 € | van compact |
| `kit-moyen-pin-avec` | Kit van compact – Phénolique pin – avec matelas | 850 € | van compact |
| `kit-moyen-carrossier-sans` | Kit van compact – Phénolique carrossier – sans matelas | 750 € | van compact |
| `kit-moyen-carrossier-avec` | Kit van compact – Phénolique carrossier – avec matelas | 900 € | van compact |
| `kit-moyen-hpl-sans` | Kit van compact – HPL de peuplier – sans matelas | 1000 € | van compact |
| `kit-moyen-hpl-avec` | Kit van compact – HPL de peuplier – avec matelas | 1150 € | van compact |

Ajustes de **cada** enlace de kit (Productos → Enlaces de pago → Nuevo):

- Cantidad: fija en 1.
- **Artículos opcionales**: las 5 opciones del kit.
- **Recoger direcciones del cliente**: dirección de envío, país Francia (añade Bélgica o Suiza si enviáis allí).
- **Tarifas de envío**: «Retrait au showroom de Nîmes» y la de su categoría (ludospace o van compact).
- **Pedir número de teléfono**: sí.
- **Campo personalizado** (texto, obligatorio): `Modèle et année du véhicule`.
- **Aceptar condiciones**: sí (usa la URL de CGV del paso 0).
- **Después del pago**: redirigir a `https://kitamenagement.fr/merci/`.
- Idioma: automático (el cliente francés lo verá en francés).

La web añade `?client_reference_id=<modelo>` al enlace (por ejemplo `berlingo` o `dacia-jogger-lodgy`).
Así sabes qué vehículo eligió en la tienda; el campo personalizado lo confirma con sus palabras.

## 2. Los 9 enlaces de accesorios

| Clave en `STRIPE` | Producto | Precio TTC |
| --- | --- | --- |
| `occultants` | Occultants isolants 9 couches | 149 € |
| `frigo-15` | Frigo à compresseur 15 L | 220 € |
| `frigo-35` | Frigo à compresseur 35 L | 300 € |
| `batterie` | Batterie lithium | 750 € |
| `batterie-onduleur` | Batterie lithium + onduleur | 975 € |
| `rechaud` | Réchaud | 29 € |
| `rechaud-cartouches` | Réchaud + 3 cartouches | 35 € |
| `toilettes` | Toilettes portables | 110 € |
| `douche` | Douche portable | 75 € |

Mismos ajustes que los kits, sin artículos opcionales. En «Occultants» añade también el campo
`Modèle et année du véhicule`, porque se hacen a medida. Envío: «Avec mon kit ou retrait à Nîmes»
(y, si queréis enviarlos sueltos, una tarifa de envío propia, que está pendiente de definir).

## 3. Activarlos en la web

1. Copia la URL de cada enlace (`https://buy.stripe.com/...`) en su clave de `STRIPE` en `tools/build.py`.
2. Ejecuta `python3 tools/build.py`. Al final indica cuántos enlaces faltan.
3. Haz commit y push. En la rama `kitamenagement` se publica sola.

Prueba primero en **modo de prueba** de Stripe (enlaces `https://buy.stripe.com/test_...`)
con la tarjeta `4242 4242 4242 4242` y después sustituye los enlaces por los reales.
