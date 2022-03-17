import re
# from tkinter import *
# from tkinter.filedialog import askopenfilename
# %matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt
# root = Tk()
# root.withdraw()


def count(words):
    for word in words:
        vwls = re.findall(vowel, word)
        for i in range(len(vwls)):
            key = vwls[i]
            # if len(v_list) <= i:
            #     v_list.append({})
            v_list[i][key] = v_list[i].get(key, 0) + 1

    for i in range(len(v_list)):
        pos = v_list[i]
        wt = sum(pos.values())
        for v in pos.keys():
            v_list[i][v] = round(100 * v_list[i][v] / wt, 2)


word_list = 'livonian_wordlist.txt'
print(f'Имя файла со словами, по которым будем собирать статистику: {word_list}')
phonemes = 'livonian_vowels.txt'
print(f'Имя файла с графемами, которые будем искать в словах из словаря и считать: {phonemes}')
with open(phonemes, encoding="utf-8") as phn:
    vow = phn.read().strip().replace(" ", "|")
vowel = re.compile(vow)
v_list = []
for i in range(6):
    v_list.append({vow: 0 for vow in vow.split('|')})

with open(word_list, encoding="utf-8") as wl:
    words = list(set([word.split('|')[0] for word in wl.readlines()]))
count(words)

wrfile = "result2.txt"
with open(wrfile, "w", encoding="utf-8") as wf:
    wf.write('position\tvowel\tfrequency\n')
    for i in range(len(v_list)):
        for v, freq in v_list[i].items():
            wf.write(f'{i + 1}\t{v}\t{freq}\n')
        wf.write('\n')
