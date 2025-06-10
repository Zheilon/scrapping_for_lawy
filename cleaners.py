import json
import re
from utils import currentDirectory, transformTypeTxt, readLinesFrom, writeLinesIn, readTextFrom
from scrappingNPL.urls import searchBook, NAME
from alertcolors import *
import pyphen
from pathlib import Path
from scrappingNPL.Jactions import readJson
from concurrent.futures import ThreadPoolExecutor

bookName = transformTypeTxt(searchBook(15, NAME))
general_path = currentDirectory(f"scrappingNPL/books/{bookName}")
yellow(f"Path = {general_path}")


def deleteWhiteSpaces(path: str):
    lines = []
    with open(path, "r", encoding="utf-8") as file:
        text = file.readlines()
        for z in text:
            if len(z) > 1:
                lines.append(z)

    writeLinesIn(path, lines)


def removeGutenbergArticles(path: str):
    newLines = []
    target = 0
    with open(path, "r", encoding="utf-8") as file:
        file_text = file.readlines()
        for word in file_text:

            if word.startswith("*** END OF THE PROJECT GUTENBERG EBOOK"):
                target = 1

            if target == 0:
                newLines.append(word)

    writeLinesIn(path, newLines)


def removeSymbolInText(text: str, key_string: str) -> str:
    """
    Consideraciones: solo extre un solo patrón, si hay 2 extrae uno, pero
    se queda el otro.

    Funcionamiento: Extrae cadenas de los textos que tengan este patrón: p. xxx, p. xxx,
    siendo estos encontrados dentro de los textos. Esta función es funcional
    para una longitud del key_string de 2.
    """
    paterns_des = [f"p. {z}" for z in range(0, 10)]
    len_des = len(paterns_des[0])

    paterns_cen = [f"p. {z}" for z in range(10, 100)]
    len_cen = len(paterns_cen[0])

    paterns_cien = [f"p. {z}" for z in range(100, 1000)]
    len_cien = len(paterns_cien[0])

    if any(z in text for z in paterns_des) or any(z in text for z in paterns_cen) or any(
            z in text for z in paterns_cien):

        #..------------------- New Intent -------------------..#
        key_string_len = len(key_string)
        official_array = []
        acc = 0
        acc_next = 1
        for z in range(len(text)):
            first_temp = ""
            second_temp = ""
            for w in range(acc, min(len(text), acc + key_string_len)):
                first_temp += text[w]
                official_array.append({"symbol": first_temp, "pos": w})
                acc += 1

            for w in range(acc_next, min(len(text) - 1, acc_next + key_string_len)):
                second_temp += text[w]
                official_array.append({"symbol": second_temp, "pos": w})
                acc_next += 1

        # ¿Por que puse ese pos en la última linea de este for con un -1?
        # pues esa "pos" me apuntaba al carácter posterior, yo necesito el anterior,
        # para saber de donde comienza el string.

        pos = [d['pos'] - 1 for d in official_array if d['symbol'] == key_string]

        isEqual = lambda pat: True if (any(pat == z for z in paterns_des)
                                       or any(pat == z for z in paterns_cen)
                                       or any(pat == z for z in paterns_cien)) else False

        decrement = max(len_des, len_cen, len_cien)
        after_key_string = text[pos:]
        character_getted = ""

        for w in range(len(after_key_string)):
            temp = ""
            limit = min(decrement, len(after_key_string))
            for z in range(limit):
                temp += after_key_string[z]

            if isEqual(temp):
                character_getted = temp
                break
            else:
                decrement -= 1

        text_final = ""
        for z in range(len(text)):
            if pos > z or z > (pos + len(character_getted) - 1):
                text_final += text[z]

        cleaned_spaces = [z for z in text_final.split() if z]

        #print(f"Len character getted = {len(character_getted)}")
        #print(f"Position getted: {pos}")
        #print(f"Character = {text[pos]}")
        #print(f"\nLenght Des: {len(paterns_des[0])}\nLenght Cen: {len(paterns_cen[0])}\nLenght Cien: {len(paterns_cien[0])}")

        print(f"Decremento inicial: {decrement}")
        green(f"Texto original: {text}")
        blue(f"texto after: {after_key_string}")
        cian(f"Resultado Final: {' '.join(cleaned_spaces)}\n----------------------------------")

        return ' '.join(cleaned_spaces)

    return text

print(removeSymbolInText("hoa p. 23 holaa el paisaje esta!!", 'p.'))


def adaptExtractor(path):
    with open(path, "r", encoding="utf-8") as file:
        readed = file.readlines()
    arr = [removeSymbolInText(text, "p.") for text in readed]
    writeLinesIn(path, arr)


def removeTildesArcaicas(path: str):
    reemplazos = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U'
    }

    arr = []
    lines = readLinesFrom(path)
    for line in lines:
        newline = line
        for tilde, sin_tilde in reemplazos.items():
            newline = re.sub(rf'(?<=\b){tilde}(?=\b)', sin_tilde, newline)
        arr.append(newline)

    writeLinesIn(path, arr)


def removeAfterFIN(path: str):
    key_word = 'FIN\n'
    target = ""
    lines = readLinesFrom(path)
    arr = []

    if key_word not in lines:
        red(f"Palabra clave {key_word} no encontrada!")
        return

    for z in lines:
        if target != key_word:
            arr.append(z)
            target = z

    writeLinesIn(path, arr)


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


def removePagesSymbols(path: str):
    typeOne = lambda pag: f"[p. {pag}]"
    typeTwo = lambda pag: f"[{pag}]"
    typeThree = lambda pag: f"{{{pag}}}"
    typeFour = lambda pag: f"[Pg {pag}]"
    typeFive = lambda pag: f"[PG {pag}]"
    typeSix = lambda pag: f"[Pág. {pag}]"
    typeSeven = lambda pag: f"(p{pag})"

    symbolTypes = [
        typeFunct(num)
        for typeFunct in (typeOne, typeTwo, typeThree, typeFour, typeFive, typeSix, typeSeven)
        for num in range(1, 1201)
    ]

    arr = []
    book_readed = readLinesFrom(path)
    for phrase in book_readed:
        if not any(sym in phrase for sym in symbolTypes):
            arr.append(phrase)
        else:
            modified = extractKeyStr(phrase, "[", "]")
            modified = extractKeyStr(modified, "{", "}")
            arr.append(modified)

    writeLinesIn(path, arr)


def removeInitSpaces(path: str):
    arr = []
    book_readed = readLinesFrom(path)
    for line in book_readed:
        arr.append(line.lstrip())

    writeLinesIn(path, arr)


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
    #vocab function:
    # len(LastSilaba) > [Promedio(len(Silabas anteriores))]
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
        isSilaba = False

        lastSilaba: str = silabas[-1]
        pastSilabas = silabas[:-1]
        len_vocabs = [len(z) for z in pastSilabas]

        average = 0
        for vocabs in len_vocabs:
            average += vocabs / len(len_vocabs)

        if len(lastSilaba) > average:
            isSilaba = True

        if (lastSilaba.endswith('n') or lastSilaba.endswith('s')) and isSilaba:
            if lastSilaba[-2] in vocab.keys():
                for k, v in vocab.items():
                    if k == lastSilaba[-2]:
                        splited[z] = word[:-2] + v + lastSilaba[-1]

    print(splited)

    for z, w in index_of_comaWord:
        splited[z] = splited[z] + w

    final_text = ' '.join(splited)
    return final_text


def grammarCorrection(path: str):
    arr = []
    lines = readLinesFrom(path)
    for line in lines:
        grammar = orthografyCorrectionAgudas(line)
        arr.append(grammar)
    print(arr)


def processBook(path: str):
    deleteWhiteSpaces(path)
    removeGutenbergArticles(path)
    removeAfterFIN(path)
    removePagesSymbols(path)
    removeInitSpaces(path)
    removeTildesArcaicas(path)
    adaptExtractor(path)
    deleteWhiteSpaces(path)
    yellow(f"Limpieza terminada en: {path}\n")


def cleanAll():
    books = Path(currentDirectory("scrappingNPL/books"))
    for book in books.iterdir():
        if book.is_file():
            processBook(str(book))