#!/bin/bash

# Configuración
REPO_DIR="/home/mannel/eos-agent"
BRANCH="data-publish"
FILES_TO_COMMIT="data/eos_data.json data/eos_data.csv"
COMMIT_MSG="Update EOS data ($(date +'%Y-%m-%d %H:%M:%S'))"

cd "$REPO_DIR" || exit 1

# Asegura que estamos en el repositorio correcto
git checkout "$BRANCH" 2>/dev/null || git checkout -b "$BRANCH"

# Verifica si hay cambios en los ficheros
if git diff --quiet -- $FILES_TO_COMMIT; then
  echo "No hay cambios para publicar."
  exit 0
fi

# Añadir, hacer commit y push
git add $FILES_TO_COMMIT
git commit -m "$COMMIT_MSG"
git push origin "$BRANCH"

echo "✔ Datos publicados en la rama $BRANCH."
