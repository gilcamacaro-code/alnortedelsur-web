#!/bin/bash
# Freno de publicación (orden de José, 20/10/2026).
# Netlify ejecuta esto antes de cada publicación:
#   exit 0 = NO publicar (no gasta créditos) · exit 1 = publicar.
# Solo se publica si el último cambio lleva [publicar] en el mensaje.
MSG="$(git log -1 --pretty=%B 2>/dev/null)"
if echo "$MSG" | grep -qF "[publicar]"; then
  echo "Publicación pedida: se publica."
  exit 1
fi
echo "Cambio guardado sin publicar (falta [publicar]). No gasta créditos."
exit 0
