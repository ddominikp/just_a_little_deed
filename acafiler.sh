#!/bin/bash

BIBLIOGRAPHY_DIR=/home/blazej/Documents/notatki/bibliografia/bibliography.bibtex
THE_FILE="$1"

it_is_pdf () {
# Use "file" to check if the file is a PDF.
    file_extension=$(file -b "$THE_FILE")
    if [[ ${file_extension::3} == PDF ]]; then
        return 0 # true
    else
        return 1 # false
    fi
}

has_doi_in_meta () {
# Unelegantly check if it has doi url in meta-data
# And save it in the bib file
    doi_meta=$(exiftool "$THE_FILE" | sed -n 's/^.*\(10.[0-9]\{4\}.*\)/\1/p'|
               uniq)
    if [[ -n $doi_meta && $doi_meta != $THE_FILE ]]; then #MODYFIKACJA WYMAGANA
        doi_meta=http://dx.doi.org/"$doi_meta"
        echo "$doi_meta"
    else
        echo "The file: '$(basename "$THE_FILE")' has no doi in metadata."
        # TODO
        # Find doi in the file itself using pdftotext
    fi
}

main () {
    if it_is_pdf; then
        has_doi_in_meta
# Having doi, it gets bib data from from the internet,then adds to bib file.
        curl -LH "Accept: text/bibliography; style=bibtex" $doi_meta # >> \
#        $BIBLIOGRAPHY_DIR 
    fi
}
main

    
#Check if the file has URL metadata - doi
    #If it does not, next file comes. if this does
    #The procesing starts - adding to .bib, changing     #name to the @one
#Check if one or two parameters
#Check if title in meta-data
#Check if read
