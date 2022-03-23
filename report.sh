#!/bin/sh

cd report

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
