# python script
from math import fabs
import requests
from bs4 import BeautifulSoup
import pandas as pd


no_pages = 5
no_pages_no1 = 2
no_pages_no2 = 3
urls_odio = []
urls_no_odio = []
links_de_odio = []
links_no_odio = []
for i in range(no_pages):
    urls_odio.append("https://www.heraldo.es/tags/temas/delitos_odio.html/" + str(i + 1) + "/")

for i in range(no_pages_no1):
    urls_no_odio.append("https://www.heraldo.es/salud/" + str(i + 1) + "/")

for i in range(no_pages_no2):
    urls_no_odio.append("https://www.heraldo.es/ocio-y-cultura/" + str(i + 1) + "/")

for url in urls_odio:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.findAll("h1", {"class": "title"})
    for result in results:
        link = result.find("a")
        links_de_odio.append("https://www.heraldo.es" + link["href"])

for url in urls_no_odio:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.findAll("h1", {"class": "title"})
    for result in results:
        link = result.find("a")
        links_no_odio.append("https://www.heraldo.es" + link["href"])


titulos_list = []
sub_titulos_list = []
noticias_list = []
delito_odio = []
contador = 1

for link in links_de_odio:
    print(link)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        titulo = soup.find("h1", {"class": "title"}).text.strip()
    except: 
        titulo = None
    try:
        sub_titulo = soup.find("p", {"class": "epigraph"}).text.strip()
    except:
        sub_titulo = None
    noticia = soup.find("div", {"class": "content-modules"})
    try:
        list_noticia = noticia.findAll("p", recursive=False)
        noticia_completa = ""
        for i in list_noticia:
            noticia_completa += i.text.strip()
    except: 
        noticia_completa = None
    titulos_list.append(titulo)
    sub_titulos_list.append(sub_titulo)
    noticias_list.append(noticia_completa)
    delito_odio.append(1)
    contador += 1


for link in links_no_odio:
    print(link)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        titulo = soup.find("h1", {"class": "title"}).text.strip()
    except: 
        titulo = None
    try:
        sub_titulo = soup.find("p", {"class": "epigraph"}).text.strip()
    except:
        sub_titulo = None
    noticia = soup.find("div", {"class": "content-modules"})
    try:
        list_noticia = noticia.findAll("p", recursive=False)
        noticia_completa = ""
        for i in list_noticia:
            noticia_completa += i.text.strip()
    except: 
        noticia_completa = None
    titulos_list.append(titulo)
    sub_titulos_list.append(sub_titulo)
    noticias_list.append(noticia_completa)
    delito_odio.append(0)
    contador += 1


df = pd.DataFrame(list(zip(titulos_list, sub_titulos_list,noticias_list,delito_odio)),columns =['titulos', 'sub_titulos','noticias','delito_odio'])
writer = pd.ExcelWriter('heraldo.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']
(max_row, max_col) = df.shape
column_settings = [{'header': column} for column in df.columns]
worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
worksheet.set_column(0, max_col - 1, 12)
writer.save()
