# Pagos con Stripe (Payment Links)

La tienda (`/boutique/`) no tiene servidor: cada botón de compra abre un **Payment Link** de Stripe.
Todo está en la cuenta **Camperizatetodoen1** (modo real). Los enlaces están en `STRIPE` dentro de `tools/build.py`;
tras cambiarlos, ejecuta `python3 tools/build.py`. Los precios salen del formulario Tally «Configura tu mueble»
(`tools/catalogue.py`).

## Cómo está montado

- **Kits** (precios TTC, IVA incluido; metadatos `site=kitamenagement.fr` y `cle`, que usa la facturación a Holded):

  | Kit | Pino | Carrossier | HPL | Entrega en Francia |
  | --- | --- | --- | --- | --- |
  | Ludospace y monovolumen (`mini`) | 500 € | 550 € | 800 € | 200 € |
  | Van compacto, XL y Maxi (`moyen`) | 700 € | 750 € | 1.000 € | 250 € |
  | Gran furgón (`grand`) | 800 € | 850 € | 1.100 € | 250 € |

  Colchón: +150 €. Retirada en Nîmes: gratis.
- **36 enlaces de kit** = 3 categorías × 3 acabados × con/sin colchón × retirada/entrega. El colchón y la entrega van
  como líneas aparte, así el recibo sale desglosado.
- **6 opciones** como artículos opcionales en todos los enlaces de kit (como en el formulario Tally):
  escuadra abatible en el cajón de cocina +25, lado izquierdo bandeja +25, lado izquierdo cajón +50,
  lado izquierdo cajón con escuadra +75, escurridor +35, versión 2+1 +100.
- **9 enlaces de accesorios**, con cantidad de 1 a 5.
- Todos: dirección de facturación y teléfono obligatorios, campo «Modèle et année du véhicule» (kits y occultants),
  dirección de envío en Francia en los de entrega, aviso «sur mesure : pas de droit de rétractation» y CGV junto al
  botón, y tras pagar → `https://kitamenagement.fr/merci/`.
- La web añade `?client_reference_id=<modelo>` (p. ej. `berlingo-xl`): en el pago se ve qué vehículo eligió.
- Imágenes de los productos: las del formulario Tally (`storage.tally.so`).

## Pendiente en el panel de Stripe

1. **Ajustes → Detalles públicos**: poner la URL de las CGV `https://kitamenagement.fr/conditions-generales-de-vente/`
   para poder activar la casilla obligatoria de aceptación en los enlaces.
2. **IVA**: confirmar con el gestor el tratamiento de las ventas a Francia (ver `facturacion/README.md`).
3. Hacer **una compra real de prueba** (réchaud de 29 €) y reembolsarla.

## Enlaces

| Clave | URL |
| --- | --- |
| `kit-mini-pin-sans-retrait` | https://buy.stripe.com/8x2aEW88C5EJ5vJdWD6EU01 |
| `kit-mini-pin-avec-retrait` | https://buy.stripe.com/4gMdR8agKc37ganbOv6EU02 |
| `kit-mini-carrossier-sans-retrait` | https://buy.stripe.com/9B6fZg9cG8QVaQ3dWD6EU03 |
| `kit-mini-carrossier-avec-retrait` | https://buy.stripe.com/aFa28q9cG0kp0bpaKr6EU04 |
| `kit-mini-hpl-sans-retrait` | https://buy.stripe.com/eVq9ASbkOaZ38HV8Cj6EU05 |
| `kit-mini-hpl-avec-retrait` | https://buy.stripe.com/eVqbJ0ex0ebfaQ3f0H6EU06 |
| `kit-moyen-pin-sans-retrait` | https://buy.stripe.com/6oU8wO88Cc376zNf0H6EU07 |
| `kit-moyen-pin-avec-retrait` | https://buy.stripe.com/eVq5kCfB44AF4rF19R6EU08 |
| `kit-moyen-carrossier-sans-retrait` | https://buy.stripe.com/4gM9AS1Ke6IN7DRaKr6EU09 |
| `kit-moyen-carrossier-avec-retrait` | https://buy.stripe.com/8x228q2Oi3wBcYbdWD6EU0a |
| `kit-moyen-hpl-sans-retrait` | https://buy.stripe.com/fZu28q9cG5EJ5vJg4L6EU0b |
| `kit-moyen-hpl-avec-retrait` | https://buy.stripe.com/cNidR89cG7MR0bpdWD6EU0c |
| `kit-mini-pin-sans-livraison` | https://buy.stripe.com/00w7sKdsWebf1ft9Gn6EU0d |
| `kit-mini-pin-avec-livraison` | https://buy.stripe.com/fZufZg88C1ot3nB19R6EU0e |
| `kit-mini-carrossier-sans-livraison` | https://buy.stripe.com/aFaaEWbkOc37bU7dWD6EU0f |
| `kit-mini-carrossier-avec-livraison` | https://buy.stripe.com/dRm00ifB44AFgan19R6EU0g |
| `kit-mini-hpl-sans-livraison` | https://buy.stripe.com/9B69ASgF84AFaQ35q76EU0h |
| `kit-mini-hpl-avec-livraison` | https://buy.stripe.com/6oU14mfB43wB6zNcSz6EU0i |
| `kit-moyen-pin-sans-livraison` | https://buy.stripe.com/14A3cu2Oi0kp8HV8Cj6EU0j |
| `kit-moyen-pin-avec-livraison` | https://buy.stripe.com/4gM6oG0Ga8QV2jx19R6EU0k |
| `kit-moyen-carrossier-sans-livraison` | https://buy.stripe.com/cNiaEW1Ke3wB9LZcSz6EU0l |
| `kit-moyen-carrossier-avec-livraison` | https://buy.stripe.com/aFa4gygF88QV4rF8Cj6EU0m |
| `kit-moyen-hpl-sans-livraison` | https://buy.stripe.com/dRm4gyfB4c377DRdWD6EU0n |
| `kit-moyen-hpl-avec-livraison` | https://buy.stripe.com/3cI9ASagK8QVf6jbOv6EU0o |
| `kit-grand-pin-sans-retrait` | https://buy.stripe.com/aFa3cuagK3wB3nB2dV6EU0y |
| `kit-grand-pin-avec-retrait` | https://buy.stripe.com/aFa9AS0Ga9UZ8HVf0H6EU0z |
| `kit-grand-carrossier-sans-retrait` | https://buy.stripe.com/4gMeVc4WqaZ31ft2dV6EU0A |
| `kit-grand-carrossier-avec-retrait` | https://buy.stripe.com/00w6oGfB41ot2jxaKr6EU0B |
| `kit-grand-hpl-sans-retrait` | https://buy.stripe.com/8x214m0Ga1ot2jx7yf6EU0C |
| `kit-grand-hpl-avec-retrait` | https://buy.stripe.com/9B66oGcoSd7bbU705N6EU0D |
| `kit-grand-pin-sans-livraison` | https://buy.stripe.com/6oU4gy60ud7bf6j6ub6EU0E |
| `kit-grand-pin-avec-livraison` | https://buy.stripe.com/00w8wOdsWaZ32jxcSz6EU0F |
| `kit-grand-carrossier-sans-livraison` | https://buy.stripe.com/8x25kC74y2sx9LZ6ub6EU0G |
| `kit-grand-carrossier-avec-livraison` | https://buy.stripe.com/7sY28q60ugjnaQ3g4L6EU0H |
| `kit-grand-hpl-sans-livraison` | https://buy.stripe.com/8x2cN4bkO7MR2jx6ub6EU0I |
| `kit-grand-hpl-avec-livraison` | https://buy.stripe.com/3cIdR84Wq3wB4rF8Cj6EU0J |
| `occultants` | https://buy.stripe.com/bJe3cufB40kp8HV3hZ6EU0p |
| `frigo-15` | https://buy.stripe.com/8x24gy60u0kp9LZbOv6EU0q |
| `frigo-35` | https://buy.stripe.com/00waEWfB43wB8HVcSz6EU0r |
| `batterie` | https://buy.stripe.com/5kQeVc9cG7MR0bp8Cj6EU0s |
| `batterie-onduleur` | https://buy.stripe.com/00w14mex0c378HVg4L6EU0t |
| `rechaud` | https://buy.stripe.com/5kQbJ04Wq3wBbU7dWD6EU0u |
| `rechaud-cartouches` | https://buy.stripe.com/cNi3cu3Sm4AF9LZ19R6EU0v |
| `toilettes` | https://buy.stripe.com/6oU14m1Ke0kp5vJaKr6EU0w |
| `douche` | https://buy.stripe.com/3cIeVcbkO4AF1ft19R6EU0x |
