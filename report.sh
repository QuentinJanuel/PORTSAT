#!/bin/sh

if [ "$1" = "mid" ]; then
    cd mid-report
else
    cd report
fi

compile() {
    pdflatex -interaction nonstopmode report.tex
}

citations() {
    bibtex report
}

compile
citations
compile
compile
