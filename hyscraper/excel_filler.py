#!/usr/bin/env python3
import openpyxl
import clipaster

gathered_notes = clipaster.main()

wb = openpyxl.Workbook()
sheet = wb.active

for number, note in gathered_notes.items():
    number = str(number)
    sheet['C' + number] = note.content
    sheet['E' + number] = ", ".join(note.references)
    sheet['F' + number] = note.level_of_fragment
    sheet['G' + number] = note.explained_level
    sheet['H' + number] = note.three_word_summary

wb.save('output.xlsx')



