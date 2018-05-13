#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from screen_utils import roll_the_screen, clear_screen, newlines
from Note_class import Note

from collections import OrderedDict
import re
import os, sys, time, subprocess

import pyperclip

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

def chose_option():
    possible_options = {'a':1}
    try:
        chosen_option = input('\nPick a letter\n').lower()
        possible_options[chosen_option] # Will terminate if not in dict
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
    previous_fragments = set()
    copied_fragments = []
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

def add_details(string):
    string = string + '\n'*2 + 'Explaining level:\n<++>'
    string = string + '\n'*2 + 'From level:\n<++>'
    return string

def separate(string):
    string = string + '\n\n\n##\n'
    return string
# Wymyślić jak wystandaryzować poziomy analizy (np. cyframi)

def vim_edit(copied_fragments):
    with open('editing_place.txt', 'w') as editing_place:

        for i in range(len(copied_fragments)):
            fragment = copied_fragments[i]
            fragment = add_details(fragment)

            if i < len(copied_fragments) - 1:
                fragment = separate(fragment)

            editing_place.write(fragment)

    subprocess.call(['vi', 'editing_place.txt'])

def load_back_edited():
    with open('editing_place.txt') as editing_place:
        corrected_string = editing_place.read()

    os.remove('editing_place.txt')

    corrected_fragments = corrected_string.split('\n\n\n##\n')
    return corrected_fragments

def main():
    intro_usage()
    chosen_option = chose_option() # Will be used in the future

    copied_fragments = paste_copied_fragments()
    vim_edit(copied_fragments)
    corrected_fragments = load_back_edited()
    clear_screen()

    gathered_notes = OrderedDict()

    for number, fragment in enumerate(corrected_fragments, start=1):
        gathered_notes[number] = Note(fragment, chosen_option)
    
    newlines()

    for i in gathered_notes:
        print(str(i) + ':', gathered_notes[i].content)
        newlines()
        print('References: ', gathered_notes[i].references)
        print('Note from level: ', gathered_notes[i].level_of_fragment)
        print('Explaining level: ', gathered_notes[i].explained_level)
        gathered_notes[i].write_three_word_summary()
        #dodac tutaj short opis
    newlines()

    # gathered_notes = {0: Note().content
    #                            .references
    #                            .level_of_fragment
    #                            .explained_level}
    return gathered_notes

if __name__ == '__main__':
    main()
