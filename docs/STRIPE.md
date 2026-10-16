# Pagos con Stripe (Payment Links)

La tienda (`/boutique/`) no tiene servidor: cada botón de compra abre un **Payment Link** de Stripe.
Todo está creado en la cuenta **Camperizatetodoen1** (modo real) el 16/10/2026.
Los enlaces están en `STRIPE` dentro de `tools/build.py`; tras cambiarlos, ejecuta `python3 tools/build.py`.

## Cómo está montado

- **Productos** (precios TTC, IVA incluido; metadato `site=kitamenagement.fr` y `cle`):
  6 kits (ludospace / van compact × pin / carrossier / HPL), «Matelas sur mesure» 150 €,
  «Livraison – kit ludospace» 200 €, «Livraison – kit van compact» 250 €,
  5 opciones (équerre 25, plateau frigo 25, tiroir frigo 50, égouttoir 35, version 2+1 100)
  y 9 accesorios.
- **24 enlaces de kit** = 6 kits × con/sin colchón × retirada/entrega. El colchón y la entrega van como líneas
  aparte, así el recibo sale desglosado. Las 5 opciones aparecen como **artículos opcionales** en la página de pago.
- **9 enlaces de accesorios**, con cantidad ajustable de 1 a 5. Se entregan con el kit o se recogen en Nîmes.
- Todos los enlaces: dirección de facturación y teléfono obligatorios; campo «Modèle et année du véhicule»
  (kits y occultants); los de entrega piden dirección de envío en Francia; tras pagar → `https://kitamenagement.fr/merci/`.
- La web añade `?client_reference_id=<modelo>` (p. ej. `berlingo`): en el pago verás qué vehículo eligió en la tienda.

La conexión de Stripe usada no permite crear **tarifas de envío**: por eso la entrega es un producto más
y el cliente la elige en la tienda (paso 4), no en la página de pago.

## Pendiente en el panel de Stripe

1. **Ajustes → Detalles públicos**: añadir la URL de condiciones
   `https://kitamenagement.fr/conditions-generales-de-vente/`. Después se puede activar en cada enlace la casilla
   obligatoria «Acepto las CGV». Hasta entonces, cada enlace lo indica con una frase junto al botón de pago.
2. **IVA**: los precios están marcados como «IVA incluido». Confirmar con el gestor el tratamiento de las ventas
   a Francia (OSS o IVA francés) y si activar Stripe Tax.
3. **Facturas**: si las necesitáis para Holded, se puede activar «crear factura tras el pago» en cada enlace
   (Stripe cobra una pequeña comisión por factura).
4. Hacer **una compra real de prueba** (por ejemplo, el réchaud de 29 €) y reembolsarla, para ver el recorrido completo.

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
| `occultants` | https://buy.stripe.com/bJe3cufB40kp8HV3hZ6EU0p |
| `frigo-15` | https://buy.stripe.com/8x24gy60u0kp9LZbOv6EU0q |
| `frigo-35` | https://buy.stripe.com/00waEWfB43wB8HVcSz6EU0r |
| `batterie` | https://buy.stripe.com/5kQeVc9cG7MR0bp8Cj6EU0s |
| `batterie-onduleur` | https://buy.stripe.com/00w14mex0c378HVg4L6EU0t |
| `rechaud` | https://buy.stripe.com/5kQbJ04Wq3wBbU7dWD6EU0u |
| `rechaud-cartouches` | https://buy.stripe.com/cNi3cu3Sm4AF9LZ19R6EU0v |
| `toilettes` | https://buy.stripe.com/6oU14m1Ke0kp5vJaKr6EU0w |
| `douche` | https://buy.stripe.com/3cIeVcbkO4AF1ft19R6EU0x |
