from pathlib import Path
from alertcolors import red, green

def currentDirectory(path: str):
    absolute = Path(__file__).resolve().parent
    return (absolute / path).resolve()


def writeTextIn(doc: str, text: str):
    with open(doc, "w", encoding="utf-8") as file:
        file.write(text + "\n")

def writeLinesIn(doc: str, lines: list[str]):
    with open(doc, "w", encoding="utf-8") as file:
        file.writelines(lines)

def readLinesFrom(doc: str):
    with open(doc, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return lines

def readTextFrom(doc: str):
    with open(doc, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def transformTypeTxt(name: str):
    lowerName = ""
    enghWhiteSpaces = name.strip()
    for chars in enghWhiteSpaces:
        if chars != ' ':
            lowerName += chars.lower()
        elif chars == ' ':
            lowerName += '_'

    second = ""
    for chars in lowerName:
        if chars != ',':
            second += chars

    three = ""
    for chars in second:
        if chars != ';':
            three += chars

    four = ""
    for chars in three:
        if chars != ':':
            four += chars

    five = ""
    for chars in four:
        if chars != '.':
            five += chars

    return five + ".txt"


def createDocTxt(path: str, name: str):
    pathWithdoc = f"{path}\\{transformTypeTxt(name)}"
    if Path(pathWithdoc).is_file() and Path(pathWithdoc).exists():
        red(f"\nEl archivo {pathWithdoc} ya existe")
        return

    with open(pathWithdoc, "w", encoding="utf-8") as file:
        file.write("")
        green(f"\nArchivo: {pathWithdoc}\nCreado con exito!")

    return pathWithdoc