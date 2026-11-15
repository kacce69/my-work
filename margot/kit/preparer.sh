#!/bin/sh
# Installe ce qu'il faut pour fabriquer un Reel de Margot avec son.
#   sh preparer.sh          l'essentiel : rendu des images, son, calage d'une prise de voix
#   sh preparer.sh kokoro   en plus, la voix de secours Kokoro (française, locale, gratuite ; environ 340 Mo à télécharger)
set -e
cd "$(dirname "$0")"
python3 -c "import numpy, soundfile, PIL" 2>/dev/null || pip install --break-system-packages -q numpy soundfile pillow
python3 -c "import playwright" 2>/dev/null || pip install --break-system-packages -q playwright
[ -x /usr/bin/google-chrome ] || python3 -m playwright install chromium
python3 -c "import faster_whisper" 2>/dev/null || pip install --break-system-packages -q faster-whisper
[ -d node_modules/@fontsource/fraunces ] || npm i --silent --no-audit --no-fund @fontsource/fraunces
fc-list 2>/dev/null | grep -q "Inter" || [ -d node_modules/@fontsource/inter ] || npm i --silent --no-audit --no-fund @fontsource/inter
command -v ffmpeg >/dev/null || echo "ATTENTION : ffmpeg est introuvable (apt-get install ffmpeg)"
if [ "$1" = "kokoro" ]; then
  python3 -c "import kokoro_onnx" 2>/dev/null || pip install --break-system-packages -q kokoro-onnx
  mkdir -p modeles
  V=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
  [ -s modeles/kokoro-v1.0.onnx ] || curl -sSL -o modeles/kokoro-v1.0.onnx "$V/kokoro-v1.0.onnx"
  [ -s modeles/voices-v1.0.bin ] || curl -sSL -o modeles/voices-v1.0.bin "$V/voices-v1.0.bin"
fi
echo "Prêt. Aperçu sans voix : python3 reel.py specs/DEMO.json /tmp/essai/x.mp4 --apercu=4 --muet"
