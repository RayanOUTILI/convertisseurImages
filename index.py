# -*- coding: utf-8 -*-
import cgi
from genericpath import isfile
import imp
import os
import re
import shutil
import subprocess
import codecs
import sys


EXEC = "SAeimages.exe"
DIR = os.path.dirname(__file__)
EXEC_PATH = os.path.join(DIR, EXEC)

codes_traitements = {"gris": 1, "inversion": 2,
                     "monochrome": 3, "contour": 4, "fusion": 5}
messages = {"gris": "Conversion de l'image en niveaux de gris",
            "inversion": "Inversion des couleurs",
            "monochrome": "Image monochrome",
            "contour": "Dessin du contour",
            "fusion": "fusion de 2 images"}

os.chdir(DIR)
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Attention, une ligne vide doit séparer l'entête HTTP du contenu (d'où le \n final).
print('<meta content="text/html;charset=utf-8" http-equiv="Content-Type">\n')

data = cgi.FieldStorage()


def traiter_donnees(data):
    """Appelle l'exécutable de traitement d'images.
    
    L'exécutable est appelé autant de fois que de traitements sélectionnés.
    """
    fichier1 = data.getvalue("fichier1")
    if not isinstance(fichier1, str) or not os.path.isfile(fichier1) or not fichier1.endswith(".bmp"):
        footer_content = ["<em>Aucun fichier BMP sélectionné.</em>"]

    else:
        footer_content = [f"<h2>Traitements appliqués à <i>{fichier1}</i></h2><ul>"]
        if fichier1 != "result.bmp":
            shutil.copy(fichier1, "result.bmp")

        for traitement, code in codes_traitements.items():
            if data.getvalue(traitement) == "ok":
                footer_content.append(f"<li>{messages[traitement]}</li>")
                if code == 5:
                    fichier2 = data.getvalue("fichier2")
                    if os.path.isfile(fichier2):
                        subprocess.run([EXEC_PATH, DIR, str(code), "result.bmp", fichier2])
                    else:
                        footer_content = ["2e fichier manquant, fusion impossible !"]
                else:
                    subprocess.run([EXEC_PATH, DIR, str(code), "result.bmp"])
        footer_content.append("</ul>")
    return footer_content


def inclure_css(html: str) -> str:
    """Incorpore les feuilles de style CSS liées directement dans le HTML..."""
    def link2style(match: re.Match) -> str:
        link = match.group(0)
        try:
            # on récupère l'adresse du fichier depuis la baliser <link>
            css_path = re.search(r"""href\s*=\s*["']?([^"']+)["']?""", link).group(1)
            with open(css_path, encoding="utf8") as f:
                # On incorpore le contenu du fichier css directement dans le HTML.
                return f"<style>\n{f.read()}\n</style>"
        except (AttributeError, OSError):
            return link

    return re.sub(r"<\s*link[^>]+stylesheet[^>]*>", link2style, html)


try:
    footer_content = traiter_donnees(data)

    with open("index.html", encoding="utf8") as f:
        html = f.read()
    html = html.replace("<!-- LOG -->",
                        "\n".join(footer_content))
    html = inclure_css(html)
    print(html)

except Exception:
    cgi.print_exception()

