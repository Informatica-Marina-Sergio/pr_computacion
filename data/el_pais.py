import requests
from bs4 import BeautifulSoup
import pandas as pd


urls_delito_odio = ["https://elpais.com/noticias/delitos-odio/"]
urls_no_odio = ["https://elpais.com/noticias/educacion/", "https://elpais.com/noticias/medio-ambiente/"]
encabezado = "https://elpais.com"
links_odio = []
links_no_odio = []
no_pages = 5
no_pages_no1 = 2
no_pages_no2 = 2

for page in range(no_pages):
    urls_delito_odio.append("https://elpais.com/noticias/delitos-odio/" + str(page + 1) + "/")

for page in range(no_pages_no1):
    urls_no_odio.append("https://elpais.com/noticias/educacion/" + str(page + 1) + "/")

for page in range(no_pages_no2):
    urls_no_odio.append("https://elpais.com/noticias/medio-ambiente/" + str(page + 1) + "/")

for url in urls_delito_odio:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.findAll("h2", {"class": "c_t"})
    for result in results:
        link = result.find("a")
        if 'album' not in link["href"]:
            links_odio.append(encabezado + link["href"])


for url in urls_no_odio:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.findAll("h2", {"class": "c_t"})
    for result in results:
        link = result.find("a")
        if 'album' not in link["href"]:
            links_no_odio.append(encabezado + link["href"])

titulos = []
sub_titulos = []
noticias = []
delito_odio = []

contador = 1

for link in links_odio:
    delito_odio.append(1)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    titulo_aux = soup.find("h1", {"class": "a_t"})
    titulo = titulo_aux.text.strip()
    titulos.append(titulo)
    try:
        sub_titulo = soup.find("h2", {"class": "a_st"})
        sub_titulo_aux = sub_titulo.text.strip()
        sub_titulos.append(sub_titulo_aux)
    except:
        sub_titulos.append(None)
    article_body = soup.find("div", {"class": "a_c clearfix"})
    parrafos = article_body.findAll("p")
    noticia_completa = ""
    for parrafo in parrafos:
        if "Suscríbase aquí a la newsletter" not in parrafo.text:
            p = parrafo.text.strip()
            noticia_completa += p
        else:
            print('ok')
    noticias.append(noticia_completa)

for link in links_no_odio:
    delito_odio.append(0)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    titulo_aux = soup.find("h1", {"class": "a_t"})
    titulo = titulo_aux.text.strip()
    titulos.append(titulo)
    try:
        sub_titulo = soup.find("h2", {"class": "a_st"})
        sub_titulo_aux = sub_titulo.text.strip()
        sub_titulos.append(sub_titulo_aux)
    except:
        sub_titulos.append(None)
    article_body = soup.find("div", {"class": "a_c clearfix"})
    parrafos = article_body.findAll("p")
    noticia_completa = ""
    for parrafo in parrafos:
        if "Suscríbase aquí a la newsletter" not in parrafo.text:
            p = parrafo.text.strip()
            noticia_completa += p
        else:
            print('ok')
    noticias.append(noticia_completa)

df = pd.DataFrame(list(zip(titulos, sub_titulos,noticias,delito_odio)),columns =['titulos', 'sub_titulos','noticias','delito_odio'])
writer = pd.ExcelWriter('el_pais.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']
(max_row, max_col) = df.shape
column_settings = [{'header': column} for column in df.columns]
worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
worksheet.set_column(0, max_col - 1, 12)
writer.save()



