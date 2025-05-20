#Url general
general_url = "http://www.secretariasenado.gov.co/senado/basedoc"

#Constitución Colombiana - Desde la sección 1 hasta la 15. 1
constitucion = "/ constitucion_politica_1991 . html"

#Código Civil - Desde la sección 1 hasta la 83. 1
c_civil = "/ codigo_civil . html"

#Código Penal - Desde la sección 1 hasta la 19. 0
c_penal = "/ ley_0599_2000 . html"

#Código de procedimiento penal - Desde la sección 1 hasta la 13. 0
c_procdPenal2004 = "/ ley_0906_2004 . html"

#Código de comercio - Desde la sección 1 hasta la 63. 1
c_comercio = "/ codigo_comercio . html"  #Dejo espacios para luego hacer el split!

#Código de Procedimiento Administrativo y de lo Contencioso Administrativo (CPACA) - Desde la sección 1 hasta la 7. 0
c_proced_admin = "/ ley_1437_2011 . html"

#Código sustantivo del trabajo - Desde la sección 1 hasta la 17. 0
c_trabajo = "/ codigo_sustantivo_trabajo . html"

#Código general del proceso - Desde la sección 1 hasta la 15. 0
c_general_pro = "/ ley_1564_2012 . html"

#Código de la Infancia y la Adolescencia - Desde la sección 1 hasta 4. 0
c_infancia_adolesc = "/ ley_1098_2006 . html"

#-----------------------------------------------------------------------------------------------------------------------

#Ley 100 de 1993 (Seguridad Social) - Desde la sección 1 hasta 6. 0
l_seguridad_so = "/ ley_0100_1993 . html"

listToSearchCodes = [
    {"code": constitucion,
     "num_sections": 15,
     "remove_range": ["Inicio", "TRANSITORIO ACL02021-10"]
     },
    {"code": c_civil,
     "num_sections": 83,
     "remove_range": ["Inicio", "2684"]
     },
    {"code": c_penal,
     "num_sections": 19,
     "remove_range": ["Inicio", "476"]
     },
    {"code": c_procdPenal2004,
     "num_sections": 13,
     "remove_range": ["Inicio", "CAPÍTULO ÚNICO-2-8"]
     },
    {"code": c_comercio,
     "num_sections": 63,
     "remove_range": ["Inicio", "2038"]
     },
    {"code": c_proced_admin,
     "num_sections": 7,
     "remove_range": ["Inicio", "309"]
     },
    {"code": c_trabajo,
     "num_sections": 17,
     "remove_range": ["Inicio", "NP1"]
     },
    {"code": c_general_pro,
     "num_sections": 15,
     "remove_range": ["Inicio", "627"]
     },
    {"code": c_infancia_adolesc,
     "num_sections": 4,
     "remove_range": ["Inicio", "217"]
     },
]

toSearchsCodes = {
    "constitucion": constitucion,
    "c_civil": c_civil,
    "c_penal": c_penal,
    "c_pro_penal_2024": c_procdPenal2004,
    "c_comercio": c_comercio,
    "c_pro_admin": c_proced_admin,
    "c_sus_trabajo": c_trabajo,
    "c_general_pro": c_general_pro,
    "c_infacia_adolesc": c_infancia_adolesc
}

toSearchLaws = {
    "law_seguridad_social": l_seguridad_so
}


def divideToUseInScrappingRunner(url_gen, n_range):
    urlSplited = url_gen.split(' ')
    insertW = f"_pr0{n_range}"
    urlSplited.insert(len(urlSplited) - 2, insertW)
    return general_url + ("".join(urlSplited))


def useInScrappingSingle(url_gen):
    urlSplited = url_gen.split(' ')
    return general_url + ("".join(urlSplited))