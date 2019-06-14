import requests
import bs4
import urllib.request
import string
import getpass
import re
import sys
import os
import mutagen.id3
from googlesearch import search
from mutagen.id3 import ID3NoHeaderError
from bs4 import BeautifulSoup
import os
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC
def google_search(fname, title, artist):
    for url in search("AZ lyrics " + title + " " + artist):
        url = url
        break
    print(url)
    return url

def Parse(url):
    source_code = requests.get(url, headers=headers, verify=True)
    plain_text = source_code.text
    # print(plain_text)
    soup = BeautifulSoup(plain_text, "lxml")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # print(text)
    text = text[text.find('Search'):]
    text = text[:text.find('Submit Corrections')]
    lyrics = text
    print(lyrics)
    run_once = 1
    return lyrics , run_once

def Embed(fname,fn, failed, embedded):
    fname = os.path.join(fpath, fn)
    fail = 0
    embed = 0
    print(fname)
    if fname.lower().endswith('.mp3'):
        #     tags=ID3(fname)
        #     if len(tags.getall('USLT::\'en\'')) != 0:
        #         tags.delall('USLT::\'en\'')
        #         print("removing lyrics")
        #         tags.save(fname)
        #         tags.save()
        tags["USLT"] = USLT(encoding=0, lang="eng", text=lyrics)
        tags.save(fname)
        tags.save()
        run_once = 2
        # print(tags['USLT'])
        lol = str(tags['USLT'])
        # print(tags['USLT'])

        if (len(lol) < 50):

            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<=FAILED=' + str(failed) + '>>>>>>>>>>>>>>>>>>>>>>')
            fail = 1
        else:
            print('==========================>Lyrics Embedded=' + str(embedded) + '=================>')
            embed =  1
        return fail, embed
fpath=(os.path.abspath(''))
keyerror=0
embedded=0
failed=0
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

for fn in os.listdir(fpath):
    run_once=0
    lyrics=None
    fname = os.path.join(fpath, fn)

    if fname.lower().endswith('.mp3'):

        try:
            print(fname)
            tags=ID3(fname)
            print(len(tags.getall('USLT')))
            if len(tags.getall('USLT')) != 0:
                print("-------------------------------------")
                continue
            title=str(tags['TIT2'])
            artist=str(tags['TPE1'])
            print(title, artist)

            url = google_search(fname, title, artist)

            lyrics, run_once = Parse(url)

            if run_once==1:

                fail, embed = Embed(fname,fn,failed, embedded)

                failed = failed + fail
                embedded = embedded + embed

        except (KeyError, UnicodeEncodeError, ConnectionError, ID3NoHeaderError, UnicodeEncodeError) as e:
            print("There is no Title and Artist name in song metadata")
            keyerror=keyerror+1
            print('hello')

print('failed objects are---------------')
print(failed)
print('Successful are----------------')
print(embedded)
a=input()