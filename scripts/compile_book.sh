#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$SCRIPT_DIR/../BigData-Notes"

cd "$PROJECT_DIR"

echo "=== [1/3] First Pass XeLaTeX ==="
/Library/TeX/texbin/xelatex -interaction=nonstopmode -file-line-error main.tex || {
    echo "XeLaTeX Pass 1 failed! Check main.log"
    tail -n 30 main.log
    exit 1
}

echo "=== [2/3] BibTeX Reference Pass ==="
/Library/TeX/texbin/bibtex main || {
    echo "BibTeX warning/notice (non-fatal if no citations yet)"
}

echo "=== [3/4] Second Pass XeLaTeX (Incorporating Citations) ==="
/Library/TeX/texbin/xelatex -interaction=nonstopmode -file-line-error main.tex || {
    echo "XeLaTeX Pass 2 failed! Check main.log"
    tail -n 30 main.log
    exit 1
}

echo "=== [4/4] Third Pass XeLaTeX (Finalizing References and TOC) ==="
/Library/TeX/texbin/xelatex -interaction=nonstopmode -file-line-error main.tex || {
    echo "XeLaTeX Pass 3 failed! Check main.log"
    tail -n 30 main.log
    exit 1
}

if [ -f "main.pdf" ]; then
    echo "=== SUCCESS: Book successfully compiled! ==="
    echo "PDF location: $PROJECT_DIR/main.pdf ($(du -h main.pdf | cut -f1))"
else
    echo "=== ERROR: main.pdf not found ==="
    exit 1
fi
