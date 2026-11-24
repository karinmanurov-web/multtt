#!/bin/sh
# запуск локального сервера из корня репозитория: sh tools/serve.sh &
cd "$(dirname "$0")/.." && exec python3 -m http.server ${PORT:-8765}
