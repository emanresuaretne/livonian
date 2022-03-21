import re
from tkinter import *
from tkinter.filedialog import askopenfilename
import pandas as pd
import matplotlib.ticker as ticker
import seaborn as sns
import matplotlib.pyplot as plt
root = Tk()
root.withdraw()


def monophtongize(diph):
    diph = diph.replace('’', '')
    if len(diph) == 1:
        return diph
    if (long := re.search('[āǟēīōȱȭǭū]', diph)):
        return long.group()
    if (close := re.search('[iu]', diph)):
        return monophtongize(diph[:close.span()[0]] + diph[close.span()[1]:])
    return diph[0]


def count(words):
    fv = {}
    for word in words:
        vwls = [monophtongize(vw[0]) for vw in re.findall(vowel, word)]
        if len(vwls) < 2:
            continue
        key = f'{vwls[0]},{vwls[1]}'
        fv_key = vwls[0]
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
# строим суммирующую таблицу: по строкам - первая гласная, по столбцам - вторая
table_mt = pd.pivot_table(table, index=["First"], columns=["Second"], values="frequency", fill_value=0)
# строим так называемую "heatmap" - клеточка тем интенсивней закрашена, чем частотней пара гласных
ax = sns.heatmap(table_mt, annot=True, cmap="YlGnBu")

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
plt.show()
