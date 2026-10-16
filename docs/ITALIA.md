# Web italiana kitcampermodulare.it (beta)

## Cómo está montado
- **Común a Francia e Italia**: `tools/build.py` (plantillas), `tools/catalogue.py` (modelos, precios de kit, opciones),
  `tools/videos.csv`, fotos, CSS de `public/index.html`, imágenes y fuentes.
- **Solo Italia**: `tools/sites/it.py` (dominio, envío 250/300 €, enlaces Stripe, URL italianas, redirecciones /it/),
  `tools/sites/it_textes.py` (traducción francés → italiano), `tools/sites/it_pages/` (páginas legales en italiano).
- `python3 tools/build.py` genera las dos webs: `public/` (Francia) y `public-it/` (Italia).
  Si un texto francés cambia y no tiene traducción, el build falla y lo lista en `tools/sites/it_a_traduire.txt`.
- Publicación: Worker de Cloudflare propio con `wrangler.it.jsonc` (carpeta `public-it/`), misma rama `kitamenagement`.

## Para publicar la beta
1. Fusionar el PR.
2. Cloudflare → Workers & Pages → Create → Import a repository → `jlanrom/Camperizate`, rama `kitamenagement`.
   Deploy command: `npx wrangler deploy --config wrangler.it.jsonc`.
3. Dominio: en DonDominio, cambiar los DNS de kitcampermodulare.it a los de Cloudflare (Cloudflare → Add a domain te
   da los dos nameservers). Después, en el Worker `kitcampermodulare` → Settings → Domains → añadir `kitcampermodulare.it`
   y `www.kitcampermodulare.it`.
4. Search Console: dar de alta kitcampermodulare.it y enviar `sitemap.xml`.

## Pendiente
- **Stripe Italia: faltan 32 de 45 enlaces.** Creados los 13 primeros (todos los de recogida de mini y moyen, y
  grand-pin-sans-retrait). Productos y precios italianos ya creados (metadata `site=kitcampermodulare.it`):
  - kits: mini pin `price_1UREDQBd58RqKiJCG9NROW1c`, carr `price_1UREDTBd58RqKiJCEe0yj6nO`, hpl `price_1UREDVBd58RqKiJCOqWKJvBX`;
    moyen pin `price_1UREDYBd58RqKiJCGAVwZ8T3`, carr `price_1UREDbBd58RqKiJCMy7Zt9Df`, hpl `price_1UREDeBd58RqKiJCAmWT0eYq`;
    grand pin `price_1UREDgBd58RqKiJCENGJxHG9`, carr `price_1UREDjBd58RqKiJC9YXWKvPi`, hpl `price_1UREDlBd58RqKiJC0Zdp8QZ8`
  - materasso `price_1UREDrBd58RqKiJCDs0hkMhv`; spedizione mini `price_1UREDtBd58RqKiJCwvEkIWWM`,
    moyen `price_1UREDvBd58RqKiJCNhgBPMfI`, grand `price_1UREDxBd58RqKiJChzQjut5F`
  - optional: equerre `price_1UREDzBd58RqKiJCKHU16tnf`, plateau `price_1UREE1Bd58RqKiJCAQhuijWm`,
    tiroir `price_1UREE5Bd58RqKiJCctY0nTC5`, tiroir-equerre `price_1UREE6Bd58RqKiJCt9CFPWmX`,
    egouttoir `price_1UREE8Bd58RqKiJCrNW82vgZ`, 2+1 `price_1UREEBBd58RqKiJCBoydikKG`
  - accessori: occultants `price_1UREEHBd58RqKiJCQZ4l5geT`, frigo-15 `price_1UREEJBd58RqKiJC6zBHbqTM`,
    frigo-35 `price_1UREELBd58RqKiJCrxNfdEFD`, batterie `price_1UREENBd58RqKiJCN6DZ8Sr1`,
    batterie-onduleur `price_1UREEQBd58RqKiJCa5i8q1FG`, rechaud `price_1UREESBd58RqKiJChfQmfPh0`,
    rechaud-cartouches `price_1UREEUBd58RqKiJCekdz8ME2`, toilettes `price_1UREEWBd58RqKiJC0dJOgSPz`,
    douche `price_1UREEYBd58RqKiJCokCftYWT`
  - Enlaces de recogida: kit + (materasso) + 6 optional; campos «Modello e anno del veicolo» y desplegable
    «Punto di ritiro» (La Garriga / Nîmes). Enlaces de envío: + spedizione, dirección de envío IT.
    Accesorios: cantidad 1-5. Sin enlace, la web ofrece «Ordina con un messaggio» (funciona igual).
- **Facturación Stripe → Holded** (`facturacion/`): hoy solo procesa `site=kitamenagement.fr`. Para Italia:
  aceptar también `kitcampermodulare.it`, textos del e-mail en italiano, nota del punto de recogida, IVA (OSS) con el gestor.
- **Redirecciones /it/** de Webnode: preparadas (43 URL) pero apagadas. Cuando la .it esté online, poner
  `REDIRECTION_ACTIVE = True` en `tools/sites/it.py`, ejecutar el build y pegar de nuevo el script en Webnode.
- Revisar con el gestor/abogado las condiciones de venta italianas (`tools/sites/it_pages/`).
- Confirmar envío a islas (la web dice «in Italia»), formulario de contacto en italiano (hoy es el Tally francés),
  imagen para compartir (`og-kitamenagement.jpg`) en italiano.
