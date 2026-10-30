#!/usr/bin/env bash
# Downloads the font sources needed by build.py.
# Set CACHE_DIR to reuse already downloaded archives.
set -euo pipefail

cd "$(dirname "$0")/.."
CACHE_DIR="${CACHE_DIR:-.cache}"
mkdir -p "$CACHE_DIR" fonts/nerd-fonts fonts/fira/distr/ttf fonts/jetbrainsmono/fonts/ttf

check_sha() {
  if command -v sha256sum >/dev/null 2>&1; then
    echo "$2  $1" | sha256sum -c -
  else
    echo "$2  $1" | shasum -a 256 -c -
  fi
}

fetch() {
  local url="$1" file="$2" sha="$3"
  if [[ ! -f "$CACHE_DIR/$file" ]]; then
    echo "Downloading $file"
    curl -fL --retry 3 --retry-delay 2 -o "$CACHE_DIR/$file" "$url"
  else
    echo "Using cached $file"
  fi
  check_sha "$CACHE_DIR/$file" "$sha"
}

fetch "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.5.1/Hack.zip" \
      "Hack-NF-3.5.1.zip" \
      "fa24da7de7cefe7766614d27762570b20453c852fc1d5b657111666df9a5e449"

fetch "https://github.com/tonsky/FiraCode/releases/download/3.1/FiraCode_3.1.zip" \
      "FiraCode_3.1.zip" \
      "cbcabd2c412ee4c3fec4688be8387de18a33bb77bc5c5988e9fd9293a0b9dbb7"

fetch "https://github.com/JetBrains/JetBrainsMono/releases/download/v2.242/JetBrainsMono-2.242.zip" \
      "JetBrainsMono-2.242.zip" \
      "4e315b4ef176ce7ffc971b14997bdc8f646e3d1e5b913d1ecba3a3b10b4a1a9f"

unzip -o -q "$CACHE_DIR/Hack-NF-3.5.1.zip" -d fonts/nerd-fonts
unzip -o -q -j "$CACHE_DIR/FiraCode_3.1.zip" "ttf/FiraCode-Regular.ttf" "ttf/FiraCode-Bold.ttf" -d fonts/fira/distr/ttf
unzip -o -q -j "$CACHE_DIR/JetBrainsMono-2.242.zip" \
  "fonts/ttf/JetBrainsMono-Regular.ttf" \
  "fonts/ttf/JetBrainsMono-Bold.ttf" \
  "fonts/ttf/JetBrainsMono-Italic.ttf" \
  "fonts/ttf/JetBrainsMono-BoldItalic.ttf" \
  -d fonts/jetbrainsmono/fonts/ttf

echo "Dependencies ready."
