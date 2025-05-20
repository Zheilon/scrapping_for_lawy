import requests
import time
from bs4 import BeautifulSoup
from utils import writeTextIn
from selenium import webdriver
from scrapping.urls import divideToUseInScrappingRunner, toSearchsCodes, toSearchLaws, listToSearchCodes, useInScrappingSingle

#constitución init char = Inicio, end char = TRANSITORIO ACL02021-10
#Cod. Comercio init char = Inicio, end char = 2038
#Cod. Civil init char = Inicio, end char = 2684

doc_const = "const_co_off.txt"
doc_comercio = "comercio.txt"
doc_civil = "co_civil.txt"

linkTexts = ["Concordancias", "Resumen de Notas de Vigencia", "Jurisprudencia Concordante", "Antecedentes",
             "Jurisprudencia Unificación", "Jurisprudencia Vigencia", "Legislación Anterior", "Notas de Vigencia",
             "Notas del Editor"]

js_functions = []


def areNumbers(textLine: str):
    try:
        int(textLine)
        return True
    except ValueError:
        return False


def cleanDoc(doc: str, charR1: str, charR2: str):
    newLines = []
    clean = []
    with open(doc, "r", encoding="utf-8") as file:
        for z in file.readlines():
            repeatWords = True if z == "Disposiciones analizadas por Avance Jurídico Casa Editorial S.A.S.©\n" or z == "Las notas de vigencia, concordancias, notas del editor, forma de presentación y disposición de la compilación están protegidas por las normas sobre derecho de autor. En relación con estos valores jurídicos agregados, se encuentra prohibido por la normativa vigente su aprovechamiento en publicaciones similares y con fines comerciales, incluidas -pero no únicamente- la copia, adaptación, transformación, reproducción, utilización y divulgación masiva, así como todo otro uso prohibido expresamente por la normativa sobre derechos de autor, que sea contrario a la normativa sobre promoción de la competencia o que requiera autorización expresa y escrita de los autores y/o de los titulares de los derechos de autor. En caso de duda o solicitud de autorización puede comunicarse al teléfono 617-0729 en Bogotá, extensión 101. El ingreso a la página supone la aceptación sobre las normas de uso de la información aquí contenida. \n" or z == "\t\t\tÚltima actualización: 31 de Diciembre de 2024 - (Diario Oficial No. 52.986 - 31 de Diciembre de 2024)\n" or z == "\t\t\tISSN [1657-6241 (En linea)]\n" or z == "\t\t\t\"Leyes desde 1992 - Vigencia Expresa y Sentencias de Constitucionalidad\"\n" or z == "Anterior | Siguiente\n" or z == "Siguiente\n" or z == "Anterior\n" or z == "\t\t\tDerechos de autor reservados - Prohibida su reproducción\n" or z.startswith("Leyes desde 1992 - Vigencia expresa y control de constitucionalidad") else False

            if f"{charR1}\n" == z or f"{charR2}\n" == z:
                clean.append(z)

            if not repeatWords and not clean and len(z) > 5 and not areNumbers(z):
                newLines.append(z)

            if len(clean) - 1 == 1:
                if clean[len(clean) - 1] == f"{charR2}\n":
                    clean = []

    with open(doc, "w", encoding="utf-8") as file:
        file.writelines(newLines)


#cleanDoc(doc_comercio, "Inicio", "2038")


def executeScrappingFirstOne(doc):
    driver = webdriver.Chrome()

    for z in range(1, 151):
        js_functions.append(f"insRow{z}()")

    url_max = f"http://www.secretariasenado.gov.co/senado/basedoc/codigo_comercio.html"
    driver.get(url_max)
    #reponse = requests.get(url_max)

    time.sleep(2)

    for js in js_functions:
        try:
            driver.execute_script(js)
        except Exception as e:
            print(f"[!] Enlace no encontrado: {js} | : {e}")

    text = BeautifulSoup(driver.page_source, 'html.parser').get_text()
    writeTextIn(doc=doc, text=text)

    driver.quit()


#executeScrappingFirstOne(doc_comercio)


def executeScrapping(doc: str, url_gen: str, sections: int):
    driver = webdriver.Chrome()

    for z in range(1, 151):
        js_functions.append(f"insRow{z}()")

    for z in range(1, sections + 1):
        chain = f"0{z}" if len(str(z)) == 1 else z
        driver.get(divideToUseInScrappingRunner(url_gen, chain))

        time.sleep(2)

        for js in js_functions:
            try:
                driver.execute_script(js)
            except Exception as e:
                print(f"[!] Enlace no encontrado: {js} en sección 0{chain}: {e}")

        text = BeautifulSoup(driver.page_source, 'html.parser').get_text()
        writeTextIn(doc=doc, text=text)

    driver.quit()


def scrappingSingle(doc: str, driver, url):
    driver.get(useInScrappingSingle(url))
    time.sleep(1)

    for js in js_functions:
        try:
            driver.execute_script(js)
        except Exception as e:
            print(f"[!] Enlace no encontrado: {js} en sección: {e}")

    text = BeautifulSoup(driver.page_source, 'html.parser').get_text()
    writeTextIn(doc, text)


def scrappingRunner(doc: str):
    driver = webdriver.Chrome()

    for z in range(1, 151):
        js_functions.append(f"insRow{z}()")

    for search in listToSearchCodes:
        scrappingSingle(doc, driver, search["code"])
        for section in range(1, search["num_sections"] + 1):
            chain = f"0{section}" if len(str(section)) == 1 else section
            driver.get(divideToUseInScrappingRunner(search["code"], chain))

            time.sleep(1)

            for js in js_functions:
                try:
                    driver.execute_script(js)
                except Exception as e:
                    print(f"[!] Función no encontrada: {js} - msg={e}")

            text = BeautifulSoup(driver.page_source, 'html.parser').get_text()
            writeTextIn(doc, text)

        time.sleep(1)
        cleanDoc(doc, charR1=search["remove_range"][0], charR2=search["remove_range"][1])
        time.sleep(1)

    driver.quit()