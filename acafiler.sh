#!/bin/bash

BIBLIOGRAPHY_FILE=/home/blazej/Documents/notatki/bibliografia/bibliography.bibtex
THE_FILE="$1"
json_data=

usage () {

}

is_pdf () {
# Use "file" to check if the file is a PDF.
    file_extension=$(file -b "$THE_FILE")
    if [[ ${file_extension::3} == PDF ]]; then
        return 0 # true
    else
        return 1 # false
    fi
}

#it_is_doi () {
    #if
    #fi
#}

has_doi () {
# Unelegantly check if it has doi url in meta-data
    doi_meta=$(exiftool "$THE_FILE" | sed -n 's/^.*\(10.[0-9]\{4\}.*\)/\1/p'|
               uniq)
    if [[ -n $doi_meta && $doi_meta != $THE_FILE ]]; then #MODYFIKACJA WYMAGANA
        doi_meta=http://dx.doi.org/"$doi_meta"
        # For debug uncomment below
        #echo "$doi_meta"
    else
        echo "The file: '$(basename "$THE_FILE")' has no doi in metadata."
        # TODO
        # Find doi in the file itself using pdftotext
    fi
    return $doi_meta
}

get_json_bib () {
    # Get json data about the article
    # Clean it from surrounding whitespaces
    # Add new lines
    scraped=$(curl -sLH "Accept: text/bibliography; style=bibtex" $doi_meta)
    cleaned=$(while read REPLY; do echo "$REPLY"; done <<< $scraped)
    formated= # Use sed, to add newlines and format it
    echo "Succesfully scraped, cleaned and formated #Title"

    # TODO
    # If connection unsuccessfull - print error msg >&2

}

main () {
    if is_pdf; then
        has_doi
        get_json_bib
    fi
}

main

    
#Check if the file has URL metadata - doi
    #If it does not, next file comes. if this does
    #The procesing starts - adding to .bib, changing     #name to the @one
#Check if one or two parameters
#Check if title in meta-data
#Check if read
