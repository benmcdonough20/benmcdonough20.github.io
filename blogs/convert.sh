#!/bin/bash
#!/bin/bash
set -e

INPUT_FILE="$1"
BASENAME="${INPUT_FILE%.*}"
CLEANED_FILE="${BASENAME}_cleaned.tex"
OUTPUT_HTML="${BASENAME}.html"

# Step 1: Fix physics macros (generates ${BASENAME}_cleaned.tex)
python ../fix_macros.py "$INPUT_FILE"

# Step 2: Render to HTML using Pandoc
pandoc "$CLEANED_FILE" \
    -F pandoc-crossref \
    --citeproc \
    --bibliography=refs.bib \
    --mathjax \
    --csl=../ieee.csl \
    --metadata link-citations=true \
    -f latex \
    -t html \
    -o "$OUTPUT_HTML"
