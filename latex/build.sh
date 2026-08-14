#!/usr/bin/env bash
# Build the foundations paper. XeLaTeX is required — see the header of
# foundations.tex for why the source keeps Unicode rather than transliterating.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
command -v xelatex >/dev/null || { echo "xelatex not on PATH"; exit 1; }
TEXINPUTS=.: latexmk -xelatex -interaction=nonstopmode -halt-on-error foundations.tex
echo
echo "built: $(pwd)/foundations.pdf  ($(pdfinfo foundations.pdf 2>/dev/null | awk '/Pages/{print $2}') pages)"
