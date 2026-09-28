#!/bin/bash
set -euo pipefail

OUT="mlaos_prime_master_geometry.svg"

cat > "$OUT" <<'SVG'
<?xml version="1.0" encoding="UTF-8"?>
<svg
  xmlns="http://www.w3.org/2000/svg"
  width="100mm"
  height="100mm"
  viewBox="0 0 100 100">

  <title>MLAOS-Prime Master Geometry</title>
  <desc>
    Manufacturing reference geometry for the MLAOS-Prime monolithic
    architectural emblem. Master envelope 100 x 100 mm.
  </desc>

  <!-- ============================================================
       MASTER DATUM / ENVELOPE
       ============================================================ -->

  <rect
    x="0"
    y="0"
    width="100"
    height="100"
    rx="7.5"
    ry="7.5"
    fill="none"
    stroke="#111111"
    stroke-width="0.25"/>

  <!-- Return axis -->
  <line
    x1="50"
    y1="4"
    x2="50"
    y2="96"
    stroke="#777777"
    stroke-width="0.15"
    stroke-dasharray="1,1"/>

  <!-- ============================================================
       PRIMARY MONOLITHIC STRUCTURE
       ============================================================ -->

  <!-- Outer structural body -->
  <path
    d="
      M 15,15
      Q 15,10 20,10
      L 80,10
      Q 85,10 85,15
      L 85,85
      Q 85,90 80,90
      L 20,90
      Q 15,90 15,85
      Z"
    fill="#101214"
    stroke="#050505"
    stroke-width="1.0"/>

  <!-- ============================================================
       M / LOWER FOUNDATION
       ============================================================ -->

  <path
    d="
      M 22,72
      L 22,78
      L 34,78
      L 50,64
      L 66,78
      L 78,78
      L 78,72
      L 66,72
      L 50,58
      L 34,72
      Z"
    fill="#17191b"
    stroke="#8d9295"
    stroke-width="0.35"/>

  <!-- ============================================================
       L / PRIMARY VERTICAL LOAD COLUMN
       ============================================================ -->

  <path
    d="
      M 30,22
      L 38,22
      L 38,68
      L 62,68
      L 62,76
      L 30,76
      Z"
    fill="#151719"
    stroke="#aeb3b5"
    stroke-width="0.35"/>

  <!-- ============================================================
       A / CROWN STRUCTURE
       ============================================================ -->

  <path
    d="
      M 27,52
      L 42,22
      L 50,14
      L 58,22
      L 73,52
      L 64,52
      L 58,39
      L 42,39
      L 36,52
      Z"
    fill="#191b1d"
    stroke="#b8bdc0"
    stroke-width="0.35"/>

  <!-- A internal negative-space geometry -->
  <path
    d="
      M 45,33
      L 50,24
      L 55,33
      Z"
    fill="#050505"/>

  <!-- ============================================================
       O / CENTRAL APERTURE
       ============================================================ -->

  <!-- Optical aperture -->
  <circle
    cx="50"
    cy="50"
    r="12"
    fill="#030405"
    stroke="#c7cbd0"
    stroke-width="0.5"/>

  <!-- Recessed optical glass representation -->
  <circle
    cx="50"
    cy="50"
    r="10.5"
    fill="#0a6f82"
    fill-opacity="0.32"
    stroke="#44d9ed"
    stroke-width="0.45"/>

  <!-- ============================================================
       S / CONTINUOUS SERPENTINE LOAD PATH
       ============================================================ -->

  <path
    d="
      M 72,24
      C 61,19 45,19 37,27
      C 29,35 33,43 46,46
      C 61,49 68,54 64,63
      C 60,72 45,78 28,74"
    fill="none"
    stroke="#d4a94b"
    stroke-width="1.1"
    stroke-linecap="round"
    stroke-linejoin="round"/>

  <!-- ============================================================
       HARMONIC SCAR
       Terminates before the O aperture.
       ============================================================ -->

  <path
    d="
      M 22,42
      C 28,39 33,37 38,35
      C 41,34 43,33 45,32"
    fill="none"
    stroke="#c18a38"
    stroke-width="0.45"
    stroke-linecap="round"/>

  <!-- ============================================================
       TITANIUM STRUCTURAL INSERTS
       ============================================================ -->

  <path
    d="M 25,20 L 33,20 L 33,70 L 25,70 Z"
    fill="#8d9498"
    fill-opacity="0.62"/>

  <path
    d="M 67,30 L 75,30 L 75,76 L 67,76 Z"
    fill="#8d9498"
    fill-opacity="0.62"/>

  <!-- ============================================================
       GOLD CONDUCTIVE VEINS
       ============================================================ -->

  <path
    d="
      M 23,64
      C 31,61 37,58 42,53"
    fill="none"
    stroke="#d4af37"
    stroke-width="0.8"
    stroke-linecap="round"/>

  <path
    d="
      M 58,47
      C 64,43 69,39 76,37"
    fill="none"
    stroke="#d4af37"
    stroke-width="0.8"
    stroke-linecap="round"/>

  <!-- ============================================================
       MICROSTRUCTURE / FRACTURE-ARREST INDICATIONS
       ============================================================ -->

  <g
    fill="none"
    stroke="#777d81"
    stroke-width="0.18"
    opacity="0.7">

    <path d="M 19,31 L 25,28 L 30,30"/>
    <path d="M 70,20 L 76,24 L 80,21"/>
    <path d="M 21,82 L 27,79 L 32,82"/>
    <path d="M 69,80 L 74,77 L 81,80"/>

  </g>

  <!-- ============================================================
       DATUM INDICATIONS
       ============================================================ -->

  <g
    fill="#111111"
    stroke="#111111"
    stroke-width="0.2">

    <path d="M 4,94 L 4,86 L 8,90 Z"/>
    <path d="M 6,4 L 6,12 L 10,8 Z"/>

  </g>

  <!-- ============================================================
       CENTER / DIMENSION REFERENCES
       ============================================================ -->

  <g
    fill="#444444"
    font-family="Arial, Helvetica, sans-serif"
    font-size="2.4">

    <text x="43" y="97">RETURN AXIS X = 50.000</text>
    <text x="3" y="7">DATUM B</text>
    <text x="82" y="97">DATUM C</text>

  </g>

  <!-- ============================================================
       DIMENSION LINES
       ============================================================ -->

  <g
    fill="none"
    stroke="#555555"
    stroke-width="0.18">

    <!-- 100 mm width -->
    <line x1="0" y1="3" x2="100" y2="3"/>
    <line x1="0" y1="1.5" x2="0" y2="4.5"/>
    <line x1="100" y1="1.5" x2="100" y2="4.5"/>

    <!-- 100 mm height -->
    <line x1="3" y1="0" x2="3" y2="100"/>
    <line x1="1.5" y1="0" x2="4.5" y2="0"/>
    <line x1="1.5" y1="100" x2="4.5" y2="100"/>

  </g>

  <g
    fill="#333333"
    font-family="Arial, Helvetica, sans-serif"
    font-size="2.8">

    <text x="46" y="2.2">100</text>
    <text x="0.5" y="52" transform="rotate(-90 0.5 52)">100</text>

  </g>

</svg>
SVG

echo
echo "=============================================="
echo " MLAOS-PRIME SVG MASTER GEOMETRY"
echo "=============================================="
echo
echo "Created:"
echo "  $OUT"
echo
echo "Master envelope:"
echo "  100 x 100 mm"
echo
echo "Nominal body:"
echo "  18 mm"
echo
echo "Optical aperture:"
echo "  Ø24 mm"
echo
echo "Return axis:"
echo "  X = 50 mm"
echo

# Optional raster previews
if command -v rsvg-convert >/dev/null 2>&1; then
    echo "Rendering PNG previews with rsvg-convert..."

    for SIZE in 128 256 512 1024; do
        rsvg-convert \
            -w "$SIZE" \
            -h "$SIZE" \
            "$OUT" \
            -o "mlaos_prime_${SIZE}px.png"
    done

    echo "PNG previews created."
elif command -v magick >/dev/null 2>&1; then
    echo "Rendering PNG previews with ImageMagick..."

    for SIZE in 128 256 512 1024; do
        magick \
            -background none \
            -density 300 \
            "$OUT" \
            -resize "${SIZE}x${SIZE}" \
            "mlaos_prime_${SIZE}px.png"
    done

    echo "PNG previews created."
else
    echo "No SVG rasterizer found."
    echo "SVG master was created successfully."
    echo
    echo "Optional:"
    echo "  brew install librsvg"
    echo "or:"
    echo "  brew install imagemagick"
fi

echo
echo "=============================================="
echo " COMPLETE"
echo "=============================================="
