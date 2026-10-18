# Seguimiento de kitamenagement.fr y kitcampermodulare.it

Objetivo: saber cada semana si el paso de camperizatetodoen1.com/fr/ e /it/ a las webs nuevas funciona y qué mejorar.
Revisión: **lunes, 15 minutos**. Apuntar los números en la tabla del final.

## 1. Las tres preguntas
1. **¿Google pasa el tráfico a las webs nuevas?** (semanas 1-8)
2. **¿Llegan visitas de calidad?** (impresiones, clics y posición por página)
3. **¿Se convierten en contactos y ventas?** (lo que de verdad importa)

## 2. Dónde mirar

| Fuente | Qué mirar | Dónde |
| --- | --- | --- |
| Search Console – camperizatetodoen1.com | Clics de las URL /fr/ y /it/ (filtro «La URL contiene /fr/») | Rendimiento → Páginas |
| Search Console – kitamenagement.fr y kitcampermodulare.it | Páginas indexadas, clics, impresiones, posición, consultas | Indexación → Páginas; Rendimiento |
| Stripe | Pagos por web (metadata `site`), pagos empezados y no terminados | Pagos; Payment Links → cada enlace |
| Holded | Pedidos con etiqueta `web-fr` / `web-it` | Ventas → Pedidos |
| WhatsApp / Tally / e-mail | Contactos que vienen de cada web | Preguntar «¿de qué web nos escribes?» o campo en Tally |
| Cloudflare (opcional) | Visitas y páginas más vistas, sin cookies | Workers → Analytics / Web Analytics |

## 3. Punto de partida
- **/fr/ en Webnode: unos 11.200 clics al año** (≈ 930 al mes, ≈ 215 a la semana). Páginas fuertes: portada, Dacia Jogger,
  catálogo, Kangoo, Partner, Dokker, Berlingo, Transporter, Rifter, NV200.
- **/it/**: sacar el dato de Search Console (últimos 12 meses, URL que contienen /it/) y apuntarlo aquí.
- Ventas y contactos actuales de Francia e Italia: apuntarlos de las últimas 8 semanas para poder comparar.

## 4. Semáforo

| Indicador | Verde | Amarillo | Rojo → qué hacer |
| --- | --- | --- | --- |
| Páginas indexadas en la web nueva (de 50) | > 40 a las 4 semanas | 20-40 | < 20: revisar Indexación, pedir indexación de las fichas fuertes, comprobar sitemap |
| Clics de la web nueva ÷ clics que tenía /fr/ (/it/) | > 70 % a las 6 semanas | 40-70 % | < 40 % a las 8 semanas: comprobar que el script de Webnode sigue puesto; mirar qué páginas no han pasado |
| Clics totales (vieja + nueva) frente al punto de partida | ≥ 90 % | 70-90 % | < 70 %: buscar las consultas perdidas y reforzar esas fichas |
| CTR en Google (clics ÷ impresiones) | > 3 % | 1,5-3 % | < 1,5 % en una página con muchas impresiones: reescribir su título y descripción |
| Contactos por semana | igual o más que antes | -25 % | menos de la mitad: revisar botones «Scrivici / Écrivez-nous», formulario y WhatsApp |
| Pedidos pagados al mes | igual o más que antes | — | 0 en 4 semanas con visitas normales: probar la compra entera, revisar precios y envío |
| Pagos empezados y no terminados en Stripe | < 50 % | 50-70 % | > 70 %: el problema está en el pago (envío caro, campos, idioma) |

## 5. Qué mejorar después (por orden)
1. **Fichas con muchas impresiones y pocos clics** → mejor título y descripción (en Search Console: Rendimiento → Páginas, ordenar por impresiones).
2. **Fichas sin fotos propias** de los modelos que más tráfico traen (Jogger, Kangoo, Partner, Dokker, Berlingo) → fotos reales (`docs/PHOTOS.md`).
3. **Consultas en posición 5-15** → ampliar el texto de esa ficha o la guía con lo que busca la gente.
4. **Contacto en el idioma de cada web** → formulario Tally en italiano y campo de origen (web y página).
5. **Pruebas sociales** → actualizar reseñas y nota cada mes; añadir reseñas por modelo cuando las haya.
6. **Artículos** que respondan a búsquedas reales (homologación, qué kit para cada modelo, comparativas) → enlazados a las fichas.

## 6. Registro semanal

| Semana | Webnode /fr/ clics | .fr clics | .fr indexadas | Webnode /it/ clics | .it clics | .it indexadas | Contactos FR | Contactos IT | Pedidos FR | Pedidos IT | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 19/10 |  |  |  |  |  |  |  |  |  |  | Inicio: redirecciones /fr/ (16/10) e /it/ (18/10) |
