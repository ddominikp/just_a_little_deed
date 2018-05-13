#!/usr/bin/env python3
from screen_utils import newlines
import re

class Note():
    reference_pattern = re.compile(r"""(
        (?:[A-Z]\w+\ et\ al\W?\        |   # Pavlov et al.
        [A-Z]\w+\ and\ [A-Z]\w+\       |   # Pavlov and Blazej
        [A-Z]\w+\ )\((?:\D?\d{4}\D?)*\)|   # Pavlov (1900, 1904)
        \([^(]*\d{4}\w?\)                  # (Pavlov, 1900a)
        )""", re.VERBOSE | re.MULTILINE | re.DOTALL)

    def __init__(self, fragment, chosen_option=0):
        self.__content, self.__levels = fragment.split('Explaining level:\n')
        self.__explained_L, self.__from_L = self.__levels.split('From level:\n')

        self.__chosen_option = chosen_option

    @property
    def content(self):
        return Note.reference_pattern.sub('[ref]', self.__content).strip()

    @property
    def references(self):
        # Zrobic zrobic funkcje odpowiadajace wybranej opcji
        # Moze slownik z wybranymi opcjami-funkcjami
        # Użyć self.__chosen_option
        found_references = Note.reference_pattern.findall(self.__content)
        if not found_references:
            found_references = 'None'

        return found_references

    @property
    def explained_level(self):
        return self.__explained_L.strip()

    @property
    def level_of_fragment(self):
        return self.__from_L.strip()

    def write_three_word_summary(self):
        while True:
            newlines()
            self.three_word_summary = input('Summarize in max 5 words:\n')
            number_of_words = len(self.three_word_summary.split())

            if number_of_words >= 1 and number_of_words < 6:
                newlines(3)
                break
