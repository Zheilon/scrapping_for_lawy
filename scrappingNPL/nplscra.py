import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from utils import writeTextIn
from scrappingNPL.urls import *
from utils import currentDirectory

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


def literatureScrapping(doc: str, url: str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser').get_text()
        writeTextIn(doc, soup)
    else:
        print(f"Error: {response.status_code}")


literatureScrapping(
    currentDirectory(pathbook("los_apóstoles.txt")), searchBook(11, URL)
)
