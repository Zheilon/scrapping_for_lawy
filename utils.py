from pathlib import Path

def currentDirectory(path: str):
    absolute = Path(__file__).resolve().parent
    return (absolute / path).resolve()


def writeTextIn(doc: str, text: str):
    with open(doc, "a", encoding="utf-8") as file:
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
    for chars in name:
        if chars != ' ':
            lowerName += chars.lower()
        elif chars == ' ':
            lowerName += '_'

    second = ""
    for chars in lowerName:
        if chars != ',':
            second += chars

    return second + ".txt"

print(transformTypeTxt("Los Apóstoles"))