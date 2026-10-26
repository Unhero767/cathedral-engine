#!/bin/bash
# MLAOS-PRIME · MASTER PHASE 1 ENGINE
# One script to forge the living corpus.

set -euo pipefail

BASE="$HOME/MLAOS_TRAINING"
RAW="$BASE/corpus/raw"
CURATED="$BASE/corpus/curated"
REJECTED="$BASE/corpus/rejected"
ARCHIVE="$BASE/corpus/archive/duplicates"
METADATA="$BASE/metadata"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  MLAOS-PRIME · MASTER PHASE 1 ENGINE                     ║"
echo "║  Forging the living corpus.                              ║"
echo "╚══════════════════════════════════════════════════════════╝"

# 1. Consecrate the structure
mkdir -p "$RAW" "$CURATED" "$REJECTED" "$ARCHIVE" "$METADATA"
echo "✓ Directory structure consecrated."

# 2. The Sanctuaries (Targeted extraction only)
TARGET_DIRS=(
  "$HOME/Library/CloudStorage/GoogleDrive-kennydallmier@gmail.com/My Drive/[Visual Assets & Media]/MLAOS-Core/Img/MLAOS PRIME"
  "$HOME/Library/CloudStorage/GoogleDrive-kennydallmier@gmail.com/My Drive/00_MASTER/Mlaos1/MLAOS-Quarantine/New Folder With Items 2"
  "$HOME/Library/CloudStorage/GoogleDrive-kennydallmier@gmail.com/My Drive/[Visual Assets & Media]/New Folder With Items 2"
  "$HOME/Library/CloudStorage/GoogleDrive-kennydallmier@gmail.com/My Drive/00_MASTER/03_Aurelia_Complete/MLAOS"
  "$HOME/Library/CloudStorage/GoogleDrive-kennydallmier@gmail.com/My Drive/00_MASTER/00_CONSOLIDATED_MASTER/01_MLAOS"
  "$HOME/Library/CloudStorage/GoogleDrive-kennydallmier@gmail.com/My Drive/[Visual Assets & Media]/Mlaos_External_Assets"
  "$HOME/Library/CloudStorage/GoogleDrive-kennydallmier@gmail.com/My Drive/00_MASTER/Mlaos1"
  "$HOME/media_vault/blueprints/MLAOS Technical"
)

echo "→ Mapping sanctuaries..."
> /tmp/mlaos_harvest.txt
for dir in "${TARGET_DIRS[@]}"; do
  [[ -d "$dir" ]] && find "$dir" -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.webp" \) 2>/dev/null >> /tmp/mlaos_harvest.txt
done

TOTAL=$(wc -l < /tmp/mlaos_harvest.txt | tr -d ' ')
echo "✓ Discovered $TOTAL candidate images."

# 3. Copy with collision avoidance
echo "→ Copying to raw corpus..."
while IFS= read -r img; do
  filename=$(basename "$img")
  path_hash=$(echo -n "$img" | md5 -q | cut -c1-8)
  dest="$RAW/${path_hash}_${filename}"
  [[ ! -f "$dest" ]] && cp "$img" "$dest" 2>/dev/null || true
done < /tmp/mlaos_harvest.txt

RAW_COUNT=$(ls -1 "$RAW" 2>/dev/null | wc -l | tr -d ' ')
echo "✓ Copied $RAW_COUNT files to raw."

# 4. Deduplicate by content, not name
echo "→ Deduplicating by SHA-256..."
cd "$RAW"
find . -type f -exec shasum -a 256 {} \; | sort > /tmp/mlaos_hashes.txt
awk '{print $1}' /tmp/mlaos_hashes.txt | sort | uniq -d > /tmp/mlaos_dups.txt

DUP_COUNT=$(wc -l < /tmp/mlaos_dups.txt | tr -d ' ')
if [[ "$DUP_COUNT" -gt 0 ]]; then
  while IFS= read -r hash; do
    grep "^$hash" /tmp/mlaos_hashes.txt | tail -n +2 | awk '{print $2}' | while read -r dup; do
      mv "$dup" "$ARCHIVE/" 2>/dev/null || true
    done
  done < /tmp/mlaos_dups.txt
  echo "✓ Archived $DUP_COUNT duplicates."
fi

# 5. Quality Filter (macOS native)
echo "→ Filtering by resolution and aspect ratio..."
cd "$RAW"
for img in *; do
  dims=$(sips -g pixelWidth -g pixelHeight "$img" 2>/dev/null | awk '/pixelWidth/ {w=$2} /pixelHeight/ {h=$2} END {print w"x"h}')
  width=$(echo "$dims" | cut -dx -f1)
  height=$(echo "$dims" | cut -dx -f2)
  
  if ! [[ "$width" =~ ^[0-9]+$ ]] || ! [[ "$height" =~ ^[0-9]+$ ]]; then
    mv "$img" "$REJECTED/"; continue
  fi
  if [[ "$width" -lt 512 || "$height" -lt 512 ]]; then
    mv "$img" "$REJECTED/"; continue
  fi
  
  is_extreme=$(awk "BEGIN {print ($width / $height > 3.0 || $height / $width > 3.0) ? 1 : 0}")
  if [[ "$is_extreme" -eq 1 ]]; then
    mv "$img" "$REJECTED/"; continue
  fi
  
  mv "$img" "$CURATED/"
done

CURATED_COUNT=$(ls -1 "$CURATED" 2>/dev/null | wc -l | tr -d ' ')
REJECTED_COUNT=$(ls -1 "$REJECTED" 2>/dev/null | wc -l | tr -d ' ')
echo "✓ Curated: $CURATED_COUNT | Rejected: $REJECTED_COUNT"

# 6. Forge the JSONL Registry (The script does the writing, not you)
echo "→ Forging metadata registry..."
cd "$CURATED"
> "$METADATA/images.jsonl"
counter=1
for img in *; do
  image_id=$(printf "mlaos_img_%06d" $counter)
  sha256=$(shasum -a 256 "$img" | awk '{print $1}')
  dims=$(sips -g pixelWidth -g pixelHeight "$img" 2>/dev/null | awk '/pixelWidth/ {w=$2} /pixelHeight/ {h=$2} END {print w"x"h}')
  width=$(echo "$dims" | cut -dx -f1)
  height=$(echo "$dims" | cut -dx -f2)
  format=$(echo "$img" | rev | cut -d. -f1 | rev | tr '[:upper:]' '[:lower:]')
  size=$(stat -f%z "$img")
  
  echo "{\"image_id\":\"$image_id\",\"filename\":\"$img\",\"corpus_path\":\"corpus/curated/$img\",\"sha256\":\"$sha256\",\"width\":$width,\"height\":$height,\"format\":\"$format\",\"file_size_bytes\":$size,\"ingested_at\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"curated\",\"tags\":[],\"partition\":null}" >> "$METADATA/images.jsonl"
  ((counter++))
done

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  ✓ PHASE 1 COMPLETE                                      ║"
echo "║  Discovered: $TOTAL                                      ║"
echo "║  Curated:    $CURATED_COUNT                              ║"
echo "║  Rejected:   $REJECTED_COUNT                             ║"
echo "╚══════════════════════════════════════════════════════════╝"
