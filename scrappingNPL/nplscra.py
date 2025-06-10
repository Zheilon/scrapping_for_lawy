import json

import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from utils import writeTextIn, createDocTxt
from scrappingNPL.Jactions import readJson, json_path
from alertcolors import *

pathbook = lambda namebook: f"scrappingNPL/books/{namebook}"


def translateEsToEn(text):
    return GoogleTranslator('auto', 'es').translate(text)


def rangeToDivide(len_text: int):
    if len_text <= 5000:
        return 1

    if len_text <= 10000:
        return 2

    if len_text <= 50000:
        return 50

    if len_text <= 100000:
        return 100

    if len_text <= 1000000:
        return 170

    if len_text <= 10000000:
        return 210


def fragmentText(text: str) -> list[list[str]]:
    text_len = len(text)
    fraction = rangeToDivide(len(text))
    parts = text_len // fraction

    print(f"Longitud de texto: {len(text):,.0f}")
    print(f"Fracción de corte: {rangeToDivide(len(text)):,.0f}")
    print(f"Partes por Fracción: {parts:,.0f}")

    acc = 0
    matrix_frags = []
    for step in range(fraction):
        fract_list = []
        text_fragment = ""
        for word in range(acc, min(text_len, (parts + acc) + 1)):
            text_fragment += text[word]
            acc += 1
        fract_list.append(text_fragment)
        matrix_frags.append(fract_list)

    return matrix_frags


def translate(fileEn: str, fileToTraduce: str):
    with open(fileEn, "r", encoding="utf-8") as file:
        matrix_frag = fragmentText(file.read())
        traduce = ""
        for fragments in matrix_frag:
            traduce += GoogleTranslator('auto', 'es').translate(fragments[0])

    writeTextIn(fileToTraduce, traduce)


def get_html_gutenberg_url(book_id: int) -> str:
    return f"https://www.gutenberg.org/files/{book_id}/{book_id}-h/{book_id}-h.htm"


def scrappingInText(doc: str, url: str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser').get_text()
        writeTextIn(doc, soup)
    else:
        print(f"Error: {response.status_code}")


def scrappingInTags(doc: str, url: str):
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser').find_all('p')
        content = [p.get_text(strip=True) for p in soup]
        writeTextIn(doc, "\n".join(content))
        green(f"Scrapping: {url} was success!")


def scrappingAll(path: str):
    json_books = readJson()
    for book in json_books:
        path_book = createDocTxt(path, book['title'])
        scrappingInTags(path_book, get_html_gutenberg_url(book['id']))


def get_gutenberg_ids_in_spanish(limit):
    url = "https://gutendex.com/books"
    params = {
        "languages": "es",
        "page": 1
    }
    ids = []
    while len(ids) < limit:
        print(f"Buscando en página {params['page']}...")
        res = requests.get(url, params=params)
        data = res.json()

        for book in data["results"]:
            idb = book["id"]
            title = book["title"]

            ids.append({"id": idb, "title": title, "url": get_html_gutenberg_url(idb)})
            print(f"ID encontrado: {book['id']} - {book['title']}")

            if len(ids) >= limit:
                break

        if not data["next"]:
            break

        params["page"] += 1

    return ids