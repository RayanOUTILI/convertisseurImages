# -*- coding: utf-8 -*-
"""
Lance le serveur.

Attention, le pare-feu de Windows risque de bloquer la connexion par défaut.
Windows va ouvrir un dialogue demandant s'il faut autoriser l'accès', répondre oui.
Ce dialogue est parfois caché par une autre fenêtre, donc naviguer entre les fenêtres au besoin.

Une fois le serveur lancé, ce script va ouvrir la page d'index (générée par `index.py` à partir de `index.html`)
dans le navigateur par défaut.
"""
import webbrowser
import http.server
import os

PORT = 8888
server_address = ("", PORT)
URL = f"http://localhost:{PORT}/index.py"

os.chdir(os.path.dirname(__file__))

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ["/"]
print("Serveur actif sur le port :", PORT)

httpd = server(server_address, handler)
webbrowser.open_new(URL)
httpd.serve_forever()
