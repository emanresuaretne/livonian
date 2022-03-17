from subprocess import check_output
from re import search

words = []
for i in range(23500, 25000, 10):
    page = check_output('curl http://www.livones.net/lingua/en/vardnica/' + str(i), shell=True, encoding='utf-8')
    word = search(r'(?<="vards"><b>).*?(?=</b></span>)', page)
    if word:
        print(word.group())
        with open('wordlist2.txt', 'a', encoding='utf-8') as f:
            f.write(word.group() + '\n')
