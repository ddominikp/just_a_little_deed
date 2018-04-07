#!/usr/bin/env python3
from collections import OrderedDict
import regex as re
import os, sys, time, subprocess, getpass
import pyperclip

def clear_screen():
    print('\033[H\033[J')

def newlines(number=1):
    if number == 1:
        print('')
    elif number == 2:
        print('\n')
    else:
        number -= 1
        print('\n' * number)

def intro_usage():
    clear_screen()
    print('\t#####################################################')
    print('\t### HyScraper - Start copying, it will gather it. ###')
    print('\t#####################################################')
    newlines()
    print('\tWhich reference format it has?:')
    print('\t[a] Nevertheless, Freedman (1986) has described the...')
    print('\t[b] The psychotropic effects of LSD(3)...')
    print('\t[c] DOI has anxiolytic properties[2]...')
    newlines()

def roll_the_screen(number):
    for i in range(number):
        print('')
        time.sleep(0.05)

def chose_option():
    possible_options = {'a':1}
    try:
        chosen_option = input('\nPick a letter\n').lower()
        possible_options[chosen_option] # Option not in dict will terminate
        input('\nUse Enter to start\n')
        roll_the_screen(19)
    except KeyError:
        print('Terminating the program')
        sys.exit()
    return chosen_option


def clean_and_strip(fragment):
    fragment = fragment.strip()
    fragment = fragment.replace('\n', ' ')
    return fragment

def paste_copied_fragments():
    copied_fragments = []
    previous_fragments = set()
    print('\tYour fragments:')
    newlines()
    try:
        while True:
            fragment = pyperclip.paste()
            if fragment not in previous_fragments:
                previous_fragments.add(fragment)

                clean_fragment = clean_and_strip(fragment)
                copied_fragments.append(clean_fragment)

                print(clean_fragment)
                print('')
                print('Number of copied fragments:', len(previous_fragments))
                newlines()
            time.sleep(0.5)

    except (KeyboardInterrupt, SystemExit): 
        pass
    return copied_fragments


def vim_edit(copied_fragments):
    with open('editing_place.txt', 'w') as editing_place:

        for i in range(len(copied_fragments) - 1):
            fragment = copied_fragments[i]
            separated_fragment = fragment + '\n\n\n##\n'
            editing_place.write(separated_fragment)

        editing_place.write(copied_fragments[-1])

    subprocess.call(['vi', 'editing_place.txt'])

def load_back_edited():
    with open('editing_place.txt') as editing_place:
        corrected_string = editing_place.read()

    corrected_fragments = corrected_string.split('\n\n\n##\n')
    return corrected_fragments

def extract_references(fragment, chosen_option=0):
    reference_pattern = re.compile(r"""(
        ([A-Z]\w+\ et\ al\W?\        |   # Pavlov et al.
        [A-Z]\w+\ and\ [A-Z]\w+\     |   # Pavlov and Blazej
        [A-Z]\w+\ )\((\D?\d{4}\D?)*\)|   # Pavlov (1900, 1904)
        \([^(]*\d{4}\w?\)                # (Pavlov, 1900a)
        )""", re.VERBOSE | re.MULTILINE | re.DOTALL)
     
    found = reference_pattern.findall(fragment)
    found = [i[0] for i in found if i] # to get rid of empty matches

    return found

def main():
    intro_usage()
    chosen_option = chose_option()

    copied_fragments = paste_copied_fragments()
    vim_edit(copied_fragments)
    corrected_fragments = load_back_edited()
    clear_screen()

    fragments_references = OrderedDict()

    for number, fragment in enumerate(corrected_fragments):
        
        references = extract_references(fragment)
        if not references:
            references = 'None'
        fragments_references[number] = (fragment, references) 
        
    message = "Would you like to delete the file with fragments?\n[yes/no]"
    if input(message) == 'yes':
        os.remove('editing_place.txt')
        print('File has been removed')
    else:
        print('Ok.')
    
    newlines()
    for i in fragments_references:
        print(str(i) + ':', fragments_references[i][0])
        newlines()
        print(fragments_references[i][1])

if __name__ == '__main__':
    main()
