#!/bin/sh
# Installe ce qu'il faut pour fabriquer un Reel de Margot avec son (voix française locale, gratuite).
set -e
cd "$(dirname "$0")"
python3 -c "import kokoro_onnx, soundfile" 2>/dev/null || pip install --break-system-packages -q kokoro-onnx soundfile
python3 -c "import playwright" 2>/dev/null || pip install --break-system-packages -q playwright
mkdir -p modeles
V=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s modeles/kokoro-v1.0.onnx ] || curl -sSL -o modeles/kokoro-v1.0.onnx "$V/kokoro-v1.0.onnx"
[ -s modeles/voices-v1.0.bin ] || curl -sSL -o modeles/voices-v1.0.bin "$V/voices-v1.0.bin"
[ -d node_modules/@fontsource/fraunces ] || npm i --silent --no-audit --no-fund @fontsource/fraunces
echo "Prêt : python3 reel.py exemple.json sortie.mp4"
