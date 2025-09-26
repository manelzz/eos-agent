#!/bin/bash

# Ruta absoluta del directorio del script (por si se ejecuta desde otro sitio)
cd "$(dirname "$0")"

# 1. Actualizar fecha actual en UTC en last-check.json
echo "{\"lastCheck\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > ./data/last-check.json
echo "✔️ Fecha actualizada en data/last-check.json"

# 2. Añadir archivos a git
git add ./data/eos_data.json ./data/eos_data.csv ./data/last-check.json

# 3. Comprobar si hay cambios antes de hacer commit
if git diff --cached --quiet; then
  echo "⚠️ No hay cambios para hacer commit. Nada que subir."
  exit 0
fi

# 4. Hacer commit con mensaje automático
COMMIT_MSG="📦 Publicar datos EOS actualizados ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
git commit -m "$COMMIT_MSG"
echo "✅ Commit creado: $COMMIT_MSG"

# 5. Hacer push a la rama data-publish
git push origin data-publish
echo "🚀 Push a GitHub completado en rama data-publish"
