from scrappingNPL.Jactions import *
from scrappingNPL.nplscra import scrappingInText
from utils import createDocTxt
import requests
from alertcolors import *
import os

def pushUp(): print("\n" * 50)


def doScrapping():
    """
    Para esta función yo voy a usar campos predefinidos.
    """
    pushUp()
    yellow("Scrapping")
    title = str(input("Enter title: ")).strip()
    url = str(input("Input url: ")).strip()
    try:
        response = requests.get(url).status_code
        if response == 200:
            if not exist(title):
                docCreated = createDocTxt(path=currentDirectory("scrappingNPL/books"), name=title)
                scrappingInText(doc=docCreated, url=url)
                yellow("\nAdd Json to list of books")
                language = str(input("Enter language: ")).strip()
                author = str(input("Enter author: ")).strip()
                include = int(input("Include to train?: "))
                writeNewBook(title=title, language=language, author=author, url=url, include=include)
            else:
                red(f"El título {title} ya existe!")
        else:
            red(f"Error: Códio de estado = {response} al acceder a la URL.")
    except requests.exceptions.RequestException as rq:
        red(f"Excepción al lanzar petición: {rq}")


def searchBook():
    pass


def SearchForbooksNeedClean():
    pass

def play():
    while True:
        yellow("\nScrapping Web - options")
        green("1. Do scrapping\n2. Search books\n3. Search for books that need to be cleaned\n\nPress x for exit!")

        option = str(input("option: "))

        if option == '1':
            doScrapping()

        if option.lower() == 'x':
            break

play()