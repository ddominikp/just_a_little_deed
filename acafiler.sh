#!/bin/bash 

#Not working properly. Need to correct the issue with THE_FILE and the first
#And the first parameter

THE_FILE="$1"
BIBLIOGRAPHY_FILE=/home/blazej/Documents/notatki/bibliografia/bibliography.bibtex
json_data=

#usage () {

#}

is_pdf () {
# Use "file" to check if the file is a PDF.
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
        doi_meta= # This variable is against bad doi obtained from filename
        echo "The file: '$(basename "$THE_FILE")' has no doi in metadata."
        # TODO
        # Find doi in the file itself using pdftotext
    fi
}

get_json_bib () {
    # Get json data about the article
    # Clean it from surrounding whitespaces
    # Add new lines
    if [[ -n $doi_meta ]]; then
        scraped=$(curl -sLH "Accept: text/bibliography; style=bibtex" $doi_meta)
        cleaned=$(while read REPLY; do echo "$REPLY"; done <<< $scraped)
        formated=$(sed 's/,/,\n/g' <<< $cleaned)
        title=$(grep -Po 'title={\K[^}]*' <<< $formated)
        echo -e "Succesfully scraped, cleaned and formated article titled:\n
        $title\n"
        return 0
    else
        return 1
    fi
}

already_present () {
    if grep -o "$title" $BIBLIOGRAPHY_FILE; then
        echo -e "Article titled:\n$title\nis already present in the file.\nOutcome: $?"
    else
        echo -e "Article titled:\n$title\nis not in the file\nOutcome: $?"
        echo "niema $?"
    fi
}

main () {
    if is_pdf; then
        has_doi
        if get_json_bib; then
            echo "\n Super test \n"
            #already_present
            echo "Bibliography file updated"
            echo -e "$formated\n\n" >> $BIBLIOGRAPHY_FILE
        fi
    fi
}

if [[ $# -lt 1 ]]; then
    # Usage
    echo "Use this script with an pdf article"
elif [[ $# -eq 1 ]]; then
    # Use on a file
    main
else 
    while (($#)); do
        THE_FILE="$1"
        main # It uses $1 as an argument, so the first file
        shift # Now the next one is argument $1
    done
fi
