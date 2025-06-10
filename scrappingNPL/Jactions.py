import json
from utils import currentDirectory
from alertcolors import red, green, yellow

json_path = currentDirectory("scrappingNPL/gutenberg_books_to_train.json")

def readJson() -> list[dict]:
    """
    Lee un archivo json. Retornando este.
    """
    with open(json_path, "r", encoding="utf-8") as file:
        readed = json.load(file)
    return readed


def searchBookIn(iD: int, key: str):
    return readJson()[iD - 1][key]


def autoIncrementID():
    """
    Se posiciona en el último id de la lista, sumandole a este 1.
    """
    return readJson()[-1]['id'] + 1


def writeNewBook(title: str, language: str, author: str, url: str, include: int):
    """
    Agrega a la lista de libros ya existentes un nuevo libro.
    """
    book = {
        "id": autoIncrementID(),
        "title": title,
        "language": language,
        "author": author,
        "url": url,
        "processed": 0,
        "include": include
    }
    json_books = readJson()

    if any(b["title"] == book["title"] for b in json_books):
        red(f"\nEl título {book['title']} ya existe.")
        return

    json_books.append(book)
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(json_books, file, indent=4, ensure_ascii=False)
        green(f"\nTítulo: {book['title']}\nAgregado con exito!")


def whichNeedCleaning():
    """
    Retorna una lista de títulos que necesitan ser limpiados para su posterio uso.
    """
    forProcess = list(
        map(lambda p: (p['id'], p['title'], p['author']),
            filter(lambda x: x["processed"] == 0 and x["include"] == 1, readJson()))
    )
    yellow(f"\nNecesitan procesamiento: {len(forProcess)}")
    for z in forProcess:
        red(z)


def exist(name_book: str):
    return any(book['title'] == name_book for book in readJson())