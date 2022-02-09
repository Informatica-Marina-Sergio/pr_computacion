# python script
import requests
from bs4 import BeautifulSoup
import pandas as pd

main_url = "https://www.larazon.es/tags/delitos-odio/"
main_page = requests.get(main_url)
soup = BeautifulSoup(main_page.content, "html.parser")
no_pages = soup.find("a", {"class":"page-button page-last"}).text

url_no_odio = "https://www.larazon.es/economia/"

urls_odio = []
urls_no_odio = []
links_odio = []
links_no_odio = []
for i in range(int(no_pages)):
	urls_odio.append(main_url + str(i + 1) + "/")

for i in range(int(no_pages)):
	urls_no_odio.append(url_no_odio + str(i + 1) + "/")

for URL in urls_odio:
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.findAll("h2",{"class":"card__headline"})
	for result in results:
		enlace = result.find("a")
		links_odio.append(enlace["href"])

for URL in urls_no_odio:
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.findAll("h2",{"class":"card__headline"})
	for result in results:
		enlace = result.find("a")
		links_no_odio.append(enlace["href"])


titulos = []
sub_titulos = []
noticias = []
delito_odio = []



for link in links_odio:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    article = soup.find("article", {"class":"article-body"})
    titulo_aux = article.find("h1",{"class":"opinion-title"})
    if titulo_aux is None:
        titulo_aux = article.find("span")
    titulo = titulo_aux.text.strip()
    titulos.append(titulo)
    sub_titulo = article.find("h2").text.strip()
    sub_titulos.append(sub_titulo)
    parrafos = article.findAll("p")
    noticia_completa = ""
    for parrafo in parrafos:
        noticia_completa += parrafo.text.strip()
    noticias.append(noticia_completa)
    delito_odio.append(1)
for link in links_no_odio:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    article = soup.find("article", {"class":"article-body"})
    titulo_aux = article.find("span")
    titulo = titulo_aux.text.strip()
    titulos.append(titulo)
    sub_titulo = article.find("h2").text.strip()
    sub_titulos.append(sub_titulo)
    parrafos = article.findAll("p")
    noticia_completa = ""
    for parrafo in parrafos:
        noticia_completa += parrafo.text.strip()
    noticias.append(noticia_completa)
    delito_odio.append(0)
	
df = pd.DataFrame(list(zip(titulos, sub_titulos,noticias,delito_odio)),columns =['titulos', 'sub_titulos','noticias','delito_odio'])
writer = pd.ExcelWriter('la_razon.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']
(max_row, max_col) = df.shape
column_settings = [{'header': column} for column in df.columns]
worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
worksheet.set_column(0, max_col - 1, 12)
writer.save()
