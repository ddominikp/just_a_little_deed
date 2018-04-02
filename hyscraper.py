#!/usr/bin/env python3

import os, pyperclip, time, subprocess

def intro_usage():
    os.system('clear')
    print('\t#####################################################')
    print('\t### HyScraper - Start copying, it will gather it. ###')
    print('\t#####################################################')
    print('\n')
    print('\tChose which type of quotation it has:')
    print('\t[a] Nevertheless, Freedman (1986) has described the...')
    print('\t[b] The psychotropic effects of LSD(3)...')
    print('\n')


def clean_and_strip(fragment):
    fragment = fragment.strip()
    fragment = fragment.replace('\n', ' ')
    return fragment

def paste_copied_fragments():
    copied_fragments = []
    try:
        while True:
            fragment = pyperclip.paste()
            if fragment not in copied_fragments:
                fragment = clean_and_strip(fragment)
                copied_fragments.append(fragment)
                print(fragment)
            time.sleep(0.5)

    except (KeyboardInterrupt, SystemExit): 
        pass
    return copied_fragments


def vim_edit(copied_fragments):
    with open('editing_place.txt', 'w') as editing_place:
        for fragment in copied_fragments:
            separated_fragment = fragment + '\n##\n'
            editing_place.write(separated_fragment)

    subprocess.call(['vi', 'editing_place.txt'])

def load_back_edited():
    with open('editing_place.txt') as editing_place:
        corrected_fragments = editing_place.read()

    corrected_fragments = corrected_fragments.split('\n##\n')
    return corrected_fragments

def main():
    intro_usage()
    input('\nClick enter to start') # To zamienić na wybór opcji później.

    copied_fragments = paste_copied_fragments()

    vim_edit(copied_fragments)
    corrected_fragments = load_back_edited()

    message = "\nWould you like to delete the file with fragments?\n[yes/no]"
    if input(message) == 'yes':
        os.remove('editing_place.txt')
        print('File has been removed')
    else:
        print('Ok.')

    for fragment in corrected_fragments:
        print(fragment, '\n\n')
    
if __name__ == '__main__':
    main()



