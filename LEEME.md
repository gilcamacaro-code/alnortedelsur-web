# Web pública — alnortedelsurvlc.com

Esta carpeta es **la web de la tienda y nada más**. Aquí no hay contabilidad,
ni facturas, ni precios de compra, ni datos de proveedores. Por eso puede ser
pública sin ningún riesgo: es exactamente lo que ya ve cualquier cliente al
entrar en alnortedelsurvlc.com.

## Qué hay aquí

| Archivo | Para qué sirve |
|---|---|
| `index.html` | La página web entera (diseño, textos y SEO en un solo archivo) |
| `assets/img/` | Las fotos de la tienda y de los productos |
| `assets/qr/` | Los códigos QR (web, WhatsApp, Instagram, Facebook, ubicación) |
| `robots.txt` | Le dice a Google que puede indexar la web |
| `sitemap.xml` | El mapa de la web para Google, con las 23 fotos descritas |
| `googleba88389a42c0914f.html` | Verificación de Google Search Console. **No borrar nunca** |

## Cómo se publica

Netlify está conectado a este repositorio:

- Proyecto Netlify: `musical-gumption-fc5168` (se muestra como alnortedelsurvlc.com)
- Cuenta de Netlify: **alnortedelsurvlc@gmail.com**
- Rama `main` · Carpeta de publicación: la raíz · Sin comando de compilación

**Cada cambio que se sube a `main` se publica solo en 1-2 minutos.**

## Por qué la web está separada de la contabilidad

Antes la web vivía dentro del repositorio privado `al-norte-del-sur-libros`,
junto con los libros contables y el TPV. Eso daba dos problemas:

1. **La web dejó de publicarse el 5 de julio de 2026.** Netlify bloquea las
   publicaciones de repositorios privados cuando los cambios vienen firmados
   por más de una persona, y el plan gratuito solo admite una.
2. Cada apunte contable del robot nocturno intentaba reconstruir la web entera,
   gastando tiempo de compilación para nada.

Al estar la web en un repositorio público y aparte, las dos cosas desaparecen,
y la contabilidad sigue privada donde debe estar.

⚠️ **Nunca copies aquí archivos de contabilidad, facturas o precios de coste.**
Este repositorio es público.

## Cómo deshacer todo esto

Volver a conectar Netlify al repositorio antiguo: Netlify → el proyecto →
Project configuration → Build & deploy → Link repository →
`gilcamacaro-code/al-norte-del-sur-libros`, rama `main`, carpeta `web`.
Dos minutos.
