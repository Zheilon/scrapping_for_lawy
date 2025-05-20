import threading
from utils import currentDirectory, transformTypeTxt, readLinesFrom, writeLinesIn, readTextFrom
from scrappingNPL.urls import searchBook, NAME
from alertcolors import *
import pyphen

bookName = transformTypeTxt(searchBook(11, NAME))
pathBook = currentDirectory(f"scrappingNPL/books/{bookName}")
yellow(f"Path = {pathBook}")


def deleteWhiteSpaces():
    lines = []
    with open(pathBook, "r", encoding="utf-8") as file:
        text = file.readlines()

        for z in text:
            if len(z) > 1:
                lines.append(z)

    writeLinesIn(pathBook, lines)


def removeGutenbergArticles():
    newLines = []
    target = 0
    with open(pathBook, "r", encoding="utf-8") as file:
        file_text = file.readlines()
        for word in file_text:

            if word.startswith("*** END OF THE PROJECT GUTENBERG EBOOK"):
                target = 1

            if target == 0:
                newLines.append(word)

    writeLinesIn(pathBook, newLines)


def removeAfterFIN():
    key_word = 'FIN\n'
    target = ""
    lines = readLinesFrom(pathBook)
    arr = []

    if key_word not in lines:
        red(f"Palabra clave {key_word} no encontrada!")
        return

    for z in lines:
        if target != key_word:
            arr.append(z)
            target = z
    writeLinesIn(pathBook, arr)


def extractKeyStr(text: str, key_ch1: str, key_ch2: str):
    sections = []
    texto_concat = ""

    for z in text:
        if z == key_ch1 or z == key_ch2:
            sections.append(z)

        if not sections:
            texto_concat += z

        if len(sections) - 1 == 1:
            if sections[len(sections) - 1] == key_ch2:
                sections = []

    return texto_concat


def removePagesSymbols():
    typeOne = lambda pag: f"[p. {pag}]"
    typeTwo = lambda pag: f"[{pag}]"
    typeThree = lambda pag: f"{{{pag}}}"
    typeFour = lambda pag: f"[Pg {pag}]"
    typeFive = lambda pag: f"[PG {pag}]"
    typeSix = lambda pag: f"[Pág. {pag}]"

    symbolTypes = [
        typeFunct(num)
        for typeFunct in (typeOne, typeTwo, typeThree, typeFour, typeFive, typeSix)
        for num in range(1, 1201)
    ]

    arr = []
    book_readed = readLinesFrom(pathBook)
    for phrase in book_readed:
        if not any(sym in phrase for sym in symbolTypes):
            arr.append(phrase)
        else:
            modified = extractKeyStr(phrase, "[", "]")
            modified = extractKeyStr(modified, "{", "}")
            arr.append(modified)


def removeInitSpaces():
    arr = []
    book_readed = readLinesFrom(pathBook)
    for line in book_readed:
        arr.append(line.lstrip())
    writeLinesIn(pathBook, arr)


# Optional:
def replaceSomeSubstring(oldC: str, newC: str):
    arr = []
    lines = readLinesFrom(pathBook)
    for line in lines:
        isIn = [newC if sym == oldC else sym for sym in line.split(' ')]
        arr.append(' '.join(isIn))
    writeLinesIn(pathBook, arr)


def orthografyCorrectionAgudas(lines: str):
    """
    Si, a las palabras agudas les falta alguna tilde, esta función
    se encarga de pornersela, y guardarla en un array para luego
    este ser guardo en un .txt
    Ejemplo:
    Japones - Japonés
    Nacion - Nación
    """
    dic = pyphen.Pyphen(lang='es')

    vocab = {
        'a': 'á',
        'e': 'é',
        'i': 'í',
        'o': 'ó',
        'u': 'ú'
    }
    special = {
        1: ",",
        2: "\n"
    }
    #Caso 1: Cuando hay una coma al final de una palabra. #Resuelto
    splited = lines.split(' ')
    index_of_comaWord = []

    for z in range(len(splited)):
        word = splited[z]
        for k, v in special.items():
            if v in word:
                index_of_comaWord.append((z, v))
                splited[z] = ''.join(w for w in splited[z] if w not in ",\n")

    for z in range(len(splited)):
        word = splited[z]
        silabas = dic.inserted(word).split('-')
        print(silabas)



    for z, w in index_of_comaWord:
        splited[z] = splited[z] + w

    final_text = ' '.join(splited)
    return final_text


print(orthografyCorrectionAgudas("la comeson, y fueron desintegracion, nacion, perro"))


def grammarCorrection():
    arr = []
    lines = readLinesFrom(pathBook)
    for line in lines:
        grammar = orthografyCorrectionAgudas(line)
        arr.append(grammar)
    print(arr)


def generalClean():
    deleteWhiteSpaces()
    removeGutenbergArticles()
    removeAfterFIN()
    removePagesSymbols()
    removeInitSpaces()
    grammarCorrection()
    deleteWhiteSpaces()
