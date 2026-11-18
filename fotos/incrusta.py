"""Incrusta les fotos .webp (i els dibuixos .svg) d'esta carpeta dins de plano-cableado-r4.html.

Les posa com a data URI entre <!--FOTOS--> i <!--/FOTOS-->, perquè la pàgina
es veja igual oberta des del disc o publicada. Torna'l a executar si canvies
o afegeixes una foto:  python fotos/incrusta.py
"""
import base64, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(AQUI, '..', 'plano-cableado-r4.html')

TIPUS = {'.webp': 'image/webp', '.svg': 'image/svg+xml'}
fotos = {}
for f in sorted(os.listdir(AQUI)):
    nom, ext = os.path.splitext(f)
    if ext in TIPUS:
        with open(os.path.join(AQUI, f), 'rb') as fh:
            fotos[nom] = 'data:' + TIPUS[ext] + ';base64,' + base64.b64encode(fh.read()).decode()

with open(HTML, encoding='utf-8') as fh:
    src = fh.read()
bloc = '<!--FOTOS--><script>var FOTO=' + json.dumps(fotos) + ';</script><!--/FOTOS-->'
nou, n = re.subn(r'<!--FOTOS-->.*?<!--/FOTOS-->', lambda m: bloc, src, flags=re.S)
if n != 1:
    raise SystemExit('No trobe el marcador <!--FOTOS--> a la pàgina')
with open(HTML, 'w', encoding='utf-8', newline='') as fh:
    fh.write(nou)
print(len(fotos), 'fotos incrustades:', ', '.join(fotos))

# index.html: la mateixa pàgina amb capçalera completa, per a GitHub Pages
INDEX = os.path.join(AQUI, '..', 'index.html')
cap = ('<!doctype html>\n<html lang="ca">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
       '<style>body{margin:0}</style>\n</head>\n<body>\n')
with open(INDEX, 'w', encoding='utf-8', newline='') as fh:
    fh.write(cap + nou + '\n</body>\n</html>\n')
print('index.html actualitzat')

# pressupost.html: el pressupost amb la mateixa capçalera
with open(os.path.join(AQUI, '..', 'pressupost-r4.html'), encoding='utf-8') as fh:
    pres = fh.read()
with open(os.path.join(AQUI, '..', 'pressupost.html'), 'w', encoding='utf-8', newline='') as fh:
    fh.write(cap.replace('<style>body{margin:0}</style>', '<style>body{margin:0}[hidden]{display:none!important}</style>')
             + pres + '\n</body>\n</html>\n')
print('pressupost.html actualitzat')
