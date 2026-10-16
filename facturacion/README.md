# Facturación automática Stripe → Holded

Cuando un cliente paga en kitamenagement.fr con un Payment Link de Stripe, este servicio (un Worker de
Cloudflare, independiente de la web) hace todo esto solo:

```
Pago en Stripe ──webhook──► Worker /stripe
                               │ 1. comprueba la firma de Stripe y que el pago es de kitamenagement.fr
                               │ 2. Holded: busca el cliente por e-mail exacto o lo crea
                               │ 3. Holded: crea el PEDIDO (serie «Línea SO»)
                               │ 4. Holded: envía el pedido al cliente por e-mail (PDF + resumen,
                               │            plazos de entrega, derecho de desistimiento, CGV)
                               │ 5. Holded: crea la FACTURA (borrador por defecto)
                               │ 6. Holded: registra el cobro en la factura (si hay tesorería configurada)
                               ▼
               cada paso se apunta en el pago de Stripe (metadatos holded_*)
```

**Sin duplicados.** Cada paso hecho queda apuntado en el propio pago de Stripe. Si Stripe reenvía el aviso
(lo hace si algo falla), los pasos ya hechos se saltan: nunca hay dos facturas ni dos correos.

**Si algo falla.** El Worker responde con error y Stripe reintenta automáticamente durante 3 días. Los fallos
se ven en Stripe → Desarrolladores → Webhooks y en los registros del Worker en Cloudflare.

**Pagos de otras webs.** Solo procesa los pagos cuyos enlaces tienen el metadato `site=kitamenagement.fr`
(los 33 enlaces de la web francesa). El resto se ignora.

## Decisiones pendientes (antes de activarlo de verdad)

| Ajuste | Ahora | Qué decidir (con el gestor) |
| --- | --- | --- |
| IVA (`TAX_KEY`, `TAX_BY_COUNTRY`) | IVA 21 % español, como vuestras facturas actuales | Si las ventas a particulares de otros países de la UE superan 10.000 €/año, se aplica el IVA del país del cliente (20 % en Francia) y se declara por OSS. Hay que crear ese impuesto en Holded y ponerlo en `TAX_BY_COUNTRY`. |
| Serie de facturas (`HOLDED_INVOICE_SERIES_ID`) | Serie por defecto de Holded | Mejor una serie propia para la web francesa, para no mezclar numeraciones. |
| Aprobar facturas (`APPROVE_INVOICE`) | `false`: quedan en borrador, como ahora | `true` les da número definitivo (y las envía a VeriFactu si lo tenéis activo). Con `SEND_INVOICE=true` se manda también la factura al cliente. |
| Tesorería (`HOLDED_TREASURY_ID`) | Vacía: no se registra el cobro | Crear en Holded una cuenta «Stripe» (tipo pasarela) y poner su id, para conciliar los pagos con los ingresos de Stripe. |

## Instalación (una vez)

1. **Clave de Holded (API v2)**: Holded → Configuración → Desarrolladores → API → crear clave con permisos de contactos, pedidos de venta y facturas (lectura y escritura).
2. **Clave restringida de Stripe**: Stripe → Desarrolladores → Claves API → «Crear clave restringida» con
   permisos *Checkout Sessions: lectura*, *Products: lectura*, *PaymentIntents: escritura*.
3. **Publicar el Worker** en Cloudflare: Workers → Crear → Importar un repositorio →
   `jlanrom/Camperizate`, rama `kitamenagement`, **directorio raíz `facturacion`**.
   (O desde un ordenador: `cd facturacion && npx wrangler deploy`.)
4. **Secretos** del Worker (Settings → Variables and Secrets, tipo *Secret*):
   `HOLDED_API_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`.
5. **Webhook de Stripe**: Desarrolladores → Webhooks → añadir destino
   `https://<url-del-worker>/stripe` con los eventos `checkout.session.completed` y
   `checkout.session.async_payment_succeeded`. Copiar su «secreto de firma» (`whsec_…`) en `STRIPE_WEBHOOK_SECRET`.

## Probarlo sin riesgo

1. Con `DRY_RUN = "true"` (valor actual) el Worker no escribe nada en Holded ni envía correos: solo registra
   lo que haría. Haz una compra pequeña (el réchaud de 29 €) y mira los registros del Worker en Cloudflare.
2. Si todo cuadra, pon `DRY_RUN = "false"`, repite la compra, comprueba en Holded el contacto, el pedido, la
   factura y el correo recibido, y reembolsa el pago en Stripe (y anula la factura borrador).

## Desarrollo

- `node test/test.mjs`: pruebas sin red (firma, IVA y redondeos de todo el catálogo, recorrido completo,
  reenvío sin duplicados, pagos de otras webs, modo prueba) y vista previa del correo.
- Texto del correo y del pedido: `src/commande.js`. Llamadas a Holded: `src/holded.js` (API v2, `Authorization: Bearer`).

## Pendiente para más adelante

- Reembolsos: crear la factura rectificativa en Holded cuando se reembolsa en Stripe (`charge.refunded`).
- Plantilla de correo de Holded propia (Configuración → Plantillas) y pasar su id en el envío.
