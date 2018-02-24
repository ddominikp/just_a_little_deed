#!/bin/bash

#Not working properly. Need to correct the issue with THE_FILE and the first
#And the first parameter



BIBLIOGRAPHY_FILE=/home/blazej/Documents/notatki/bibliografia/bibliography.bibtex
json_data=

#usage () {

#}

is_pdf () {
# Use "file" to check if the file is a PDF.
    THE_FILE="$1"
    file_extension=$(file -b "$THE_FILE")
    if [[ ${file_extension::3} == PDF ]]; then
        return 0 # true
    else
        return 1 # false
    fi
}

has_doi () {
# Unelegantly check if it has doi url in meta-data
    doi_meta=$(exiftool "$THE_FILE" | sed -n 's/^.*\(10.[0-9]\{4\}.*\)/\1/p'|
               uniq)
    if [[ -n $doi_meta && $doi_meta != $THE_FILE ]]; then
        doi_meta=http://dx.doi.org/"$doi_meta"
    else
        echo "The file: '$(basename "$THE_FILE")' has no doi in metadata."
        # TODO
        # Find doi in the file itself using pdftotext
    fi
}

get_json_bib () {
    # Get json data about the article
    # Clean it from surrounding whitespaces
    # Add new lines
    scraped=$(curl -sLH "Accept: text/bibliography; style=bibtex" $doi_meta)
    cleaned=$(while read REPLY; do echo "$REPLY"; done <<< $scraped)
    formated=$(sed 's/,/,\n/g' <<< $cleaned)
    title=$(grep -Po 'title={\K[^}]*' <<< $formated)
    echo -e "Succesfully scraped, cleaned and formated article titled:\n $title"
    # TODO
    # If connection unsuccessfull - print error msg >&2

}

main () {
    if is_pdf; then
        has_doi
        get_json_bib
        echo -e "$formated\n\n" >> $BIBLIOGRAPHY_FILE
    fi
}

if [[ $# -lt 1 ]]; then
    # Usage
    echo "Use this script with an pdf article"
elif [[ $# -eq 1 ]]; then
    # Use on  a file
    main
else 
    while (($#)); do
        main # it uses $1 as an argument, so the first file
        shift # now the next one is argument $1
    done
fi
    
#Check if the file has URL metadata - doi
    #If it does not, next file comes. if this does
    #The procesing starts - adding to .bib, changing     #name to the @one
