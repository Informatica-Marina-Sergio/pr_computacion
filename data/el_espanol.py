import requests
from bs4 import BeautifulSoup
import pandas as pd
urls_delito_odio = ["https://www.elespanol.com/temas/delitos_odio/", "https://www.elespanol.com/temas/delitos_odio/1/"]
urls_no_odio = ["https://www.elespanol.com/temas/empleo/","https://www.elespanol.com/temas/television/"]
encabezado = "https://www.elespanol.com/"
links_odio = []
links_no_odio = []

for URL in urls_delito_odio:
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.findAll("div",{"class":"news-container"})
	for result in results:
		enlace = result.find("a")
		links_odio.append(encabezado + enlace["href"])

for URL in urls_no_odio:
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.findAll("div",{"class":"news-container"})
	for result in results:
		enlace = result.find("a")
		links_no_odio.append(encabezado + enlace["href"])

titulos = []
sub_titulos = []
noticias = []
delito_odio = []

contador = 1

for link in links_odio:
    delito_odio.append(1)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    titulo_aux = soup.find("h1", {"class": "article-header__heading article-header__heading--s3"})
    titulo = titulo_aux.text.strip()
    titulos.append(titulo)
    try:
        sub_titulo = soup.find("h2", {"class":"article-header__subheading"}).text.strip()
        sub_titulos.append(sub_titulo)
    except:
        sub_titulos.append(None)
    article_body = soup.find("div", {"class":"article-body__content","id":"article-body-content"})
    fin = False
    parrafos = ""
    cont = 1
    noticia_completa = ""
    while(fin == False):
        try:
            parrafo = soup.find("p",{"id":"paragraph_" + str(cont)})
            noticia_completa += parrafo.text.strip()
            cont += 1
        except:
            fin = True
    noticias.append(noticia_completa)
    

for link in links_no_odio:
    delito_odio.append(0)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    titulo_aux = soup.find("h1", {"class": "article-header__heading article-header__heading--s3"})
    titulo = titulo_aux.text.strip()
    titulos.append(titulo)
    try:
        sub_titulo = soup.find("h2", {"class":"article-header__subheading"}).text.strip()
        sub_titulos.append(sub_titulo)
    except:
        sub_titulos.append(None)
    article_body = soup.find("div", {"class":"article-body__content","id":"article-body-content"})
    fin = False
    parrafos = ""
    cont = 1
    noticia_completa = ""
    while(fin == False):
        try:
            parrafo = soup.find("p",{"id":"paragraph_" + str(cont)})
            noticia_completa += parrafo.text.strip()
            cont += 1
        except:
            fin = True
    noticias.append(noticia_completa)


df = pd.DataFrame(list(zip(titulos, sub_titulos,noticias,delito_odio)),columns =['titulos', 'sub_titulos','noticias','delito_odio'])
writer = pd.ExcelWriter('el_espanol.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']
(max_row, max_col) = df.shape
column_settings = [{'header': column} for column in df.columns]
worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
worksheet.set_column(0, max_col - 1, 12)
writer.save()
