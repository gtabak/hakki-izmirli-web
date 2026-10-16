#!/usr/bin/env bash
# Run this ON YOUR MAC while the old hakkiizmirli.com hosting is still reachable.
# The original photos belong to the current clinic website. We do not synthesize a doctor's likeness.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p public/upload/6 public/upload/2
curl -fL --retry 3 --connect-timeout 15 \
 'https://hakkiizmirli.com/upload/6/dr-hakki-izmirli-750x0.jpg' \
 -o public/upload/6/dr-hakki-izmirli-750x0.jpg
curl -fL --retry 3 --connect-timeout 15 \
 'https://hakkiizmirli.com/upload/2/dsc-46jj73-1-1903x1269.jpg' \
 -o public/upload/2/dsc-46jj73-1-1903x1269.jpg
file public/upload/6/dr-hakki-izmirli-750x0.jpg public/upload/2/dsc-46jj73-1-1903x1269.jpg
printf '\nOriginal clinic imagery copied into site output. Rebuild ZIP before DNS cutover.\n'
