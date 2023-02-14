import csv
import os
import subprocess as sp

paths = {
    'notepad':"C:\\Windows\\\\System32\\notepad.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe",
    'csv.excel': r"C:\\Program Files\\Microsoft Office\\",
    'line':"C:\\Users\\"
}

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_notepad():
    sp.Popen(paths['notepad'])

def open_cmd():
    os.system('start cmd')

def open_calculator():
    sp.Popen(paths['calculator'])

def open_excel():
    sp.Popen(paths['csv.excel'])

def open_line():
    sp.Popen(paths['line'])