# set your windows encoding to utf-8 in
# control panel-clock and region-region-administrate-
# change system region setting-beta version(then will change to utf-8)

import sys
import requests
from bs4 import BeautifulSoup


def pyout(s):
    file.write(s + "\n")
    print(s)


def head_upper(s):
    return str(s[0]).upper() + s[1:]


def init():
    arg = sys.argv
    origin, target, word = head_upper(arg[1]), head_upper(arg[2]), arg[3]
    if origin not in languages:
        print("Sorry, the program doesn't support %s" % origin.lower())
        exit(0)
    if target != 'All' and target not in languages:
        print("Sorry, the program doesn't support %s" % target.lower())
        exit(0)

    return origin, target, word


def send():
    global r
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://context.reverso.net/translation/%s-%s/%s" \
          % (origin.lower(), target.lower(), word)
    try:
        r = requests.get(url, headers=headers)
    except:
        print("Something wrong with your internet connection")
        exit(0)
    if r.status_code == 200:
        pass
    elif r.status_code == 404:
        print("Sorry, unable to find %s" % word)
        exit(0)
    else:
        print("Something wrong with your internet connection")
        exit(0)
    return BeautifulSoup(r.content, "html.parser")


def extract():
    words, sentences, sentences1, sentences2 = [], [], [], []
    list1 = soup.find_all('span', attrs={"class": "display-term"})
    for i in list1:
        if len(i.text.strip()):
            words.append(i.text)
    list2 = soup.find_all('div', attrs={"class": "example"})
    for i in list2:
        tmp = i.find_all('span', attrs={"class": "text"})
        for j in tmp:
            if len(j.text.strip()):
                sentences.append(j.text.strip())
    return words, sentences


def out(end):
    pyout("%s Translations:" % target)
    for i in range(min(len(words), 3)):
        pyout(words[i])
    pyout("")
    pyout("%s Examples:" % target)
    for i in range(min(len(sentences) // 2, 3)):
        pyout(sentences[i * 2])
        pyout(sentences[i * 2 + 1])
        pyout("")
    pyout("")


if __name__ == '__main__':
    languages = ["Arabic", "German", "English", "Spanish", "French",
                 "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese",
                 "Romanian", "Russian", "Turkish"]
    origin, target, word = init()
    file = open(word + ".txt", mode='w', encoding="utf-8")
    if target == 'All':
        cnt = 0
        for target in languages:
            if target == origin:
                continue
            soup = send()
            words, sentences = extract()
            cnt += 1
            out(target == 12)
    else:
        soup = send()
        words, sentences = extract()
        out(True)
    file.close()
