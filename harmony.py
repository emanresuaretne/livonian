import re
from tkinter import *
from tkinter.filedialog import askopenfilename
# %matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt
root = Tk()
root.withdraw()


def repl(text):
    # vwls = {'ä': 'a¨', 'ü': 'u¨', 'ö': 'o¨', 'õ': 'o∽'}
    # for pair in vwls:
    #     text = text.replace(pair, vwls.get(pair))
    return text


def count(words):
    fv = {}
    for word in words:
        vwls = re.findall(vowel, word)
        if len(vwls) < 2:
            continue
        key = repl(f'{vwls[0]},{vwls[1]}')
        fv_key = repl(vwls[0])
        fv[fv_key] = fv.get(fv_key, 0) + 1
        v_dict[key] = v_dict.get(key, 0) + 1
    for k, v in v_dict.items():
        fvow = k.split(",")[0]
        v_dict[k] = round(100*v/fv[fvow], 2)


word_list = askopenfilename()
print(f'Имя файла со словами, по которым будем собирать статистику: {word_list}')
phonemes = askopenfilename()
print(f'Имя файла с графемами, которые будем искать в словах из словаря и считать: {phonemes}')
with open(phonemes, encoding="utf-8") as phn:
    vow = phn.read().strip().replace(" ", "|")
vowel = re.compile(vow)
v_dict = {}
with open(word_list, encoding="utf-8") as wl:
    count(wl.readlines())

wrfile = "result.txt"
with open(wrfile, "w", encoding="utf-8") as wf:
    wf.write('First\tSecond\tfrequency\n')
    for k, v in sorted(sorted(v_dict.items(), reverse=True, key=lambda x: x[1]), key=lambda x: x[0][0]):
        f, s = k.split(",")
        wf.write(f'{f}\t{s}\t{v}\n')

table = pd.read_csv("result.txt", sep="\t")
# print(table)
# table.head()
# строим суммирующую таблицу: по строкам - первая гласная, по столбцам - вторая
table_mt = pd.pivot_table(table, index=["First"], columns=["Second"], values="frequency", fill_value=0)
table_mt
# строим так называемую "heatmap" - клеточка тем интенсивней закрашена, чем частотней пара гласных
ax = sns.heatmap(table_mt, annot=True, cmap="YlGnBu")
# notation: "annot" not "annote"
bottom, top = ax.get_ylim()
# ax.set_ylim(bottom + 0.0001, top - 0.0001)
# sns.set(font_scale=2)
fig = plt.figure()
fig, ax = plt.subplots(1,1, figsize=(12,12))
heatplot = ax.imshow(table_mt, cmap='BuPu')
ax.set_xticklabels(table_mt.columns)
ax.set_yticklabels(table_mt.index)

tick_spacing = 1
ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax.set_title("First-second syllable vowels")
ax.set_xlabel('second_syllable')
ax.set_ylabel('first_syllable')
ax.set_ylim(9.0, 0)
