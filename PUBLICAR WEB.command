#!/bin/bash
# Publica la web con todo lo acumulado. Usar SOLO cuando José lo pide.
# Gasta 15 créditos de Netlify (300 gratis al mes = 20 publicaciones).
cd "$(dirname "$0")" || exit 1
git pull --no-rebase -q || { echo "No se pudo traer GitHub. No se publica."; read -r -p "Enter para cerrar"; exit 1; }
MOTIVO="${1:-pedido por José}"
git commit --allow-empty -q -m "[publicar] Web publicada: $MOTIVO ($(date '+%d/%m/%Y %H:%M'))" && git push -q \
  && echo "Pedido de publicación enviado. La web estará al día en 1-2 minutos." \
  || echo "Fallo al subir: no se ha publicado."
[ -t 0 ] && read -r -p "Enter para cerrar"
