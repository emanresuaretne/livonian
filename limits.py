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
    wf.write('Position\tVowel\tFrequency\n')
    for i in range(len(v_list)):
        for v, freq in v_list[i].items():
            wf.write(f'{i + 1}\t{v}\t{freq}\n')
        wf.write('\n')


table = pd.read_csv("result2.txt", sep="\t")
# print(table)
# table.head()
# строим суммирующую таблицу: по строкам - первая гласная, по столбцам - вторая
table_mt = pd.pivot_table(table, index=["Vowel"], columns=["Position"], values="Frequency", fill_value=0)
table_mt
# строим так называемую "heatmap" - клеточка тем интенсивней закрашена, чем частотней пара гласных
ax = sns.heatmap(table_mt, annot=True, cmap="YlGnBu")
# notation: "annot" not "annote"
bottom, top = ax.get_ylim()
# ax.set_ylim(bottom + 0.0001, top - 0.0001)
# sns.set(font_scale=2)
fig = plt.figure()
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
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
