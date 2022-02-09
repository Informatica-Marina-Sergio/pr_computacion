import requests
from bs4 import BeautifulSoup
import pandas as pd

main_delito_url = 'https://as.com/tag/delitos_odio/a/'
futbol_url = 'https://as.com/tag/futbol/a/'
baloncesto_url = 'https://as.com/tag/baloncesto/a/'

page = requests.get(main_delito_url)
soup = BeautifulSoup(page.content, "html.parser")
no_pages = soup.find("p",{"class":"page-number"})
no_pages = int(no_pages.text.split(' ')[-1].strip())

urls_odio = []
urls_no_odio = []
for i in range(no_pages):
        urls_odio.append(main_delito_url+str(i+1))
for i in range(no_pages//2):
        urls_no_odio.append(futbol_url+str(i+1))
for i in range(no_pages//2):
        urls_no_odio.append(baloncesto_url+str(i+1))



links_odio = []
links_no_odio = []

for URL in urls_odio:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.findAll("div",{"class":"rrss-wrapper"})
        for result in results:
                links_odio.append(result["data-url"])
              


for URL in urls_no_odio:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.findAll("div",{"class":"rrss-wrapper"})
        for result in results:
                links_no_odio.append(result["data-url"])

titulos_list = []
sub_titulos_list = []
noticias_list = []
delito_odio = []
count = 0
for link in links_odio:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "lxml")
    try:
        titulo = soup.find("h1",{"class":"art-headline"}).text.strip()
    except:
        try:
            titulo = soup.find("h1",{"class":"titular-articulo"}).text.strip()
        except:
            titulo = None
    titulos_list.append(titulo)
    try:
        sub_titulo = soup.find("h2",{"class":"art-opening"}).text.strip()
    except:
        try:
            sub_titulo = soup.find("h2",{"class":"cont-entradilla-art"}).text.strip()
        except:
            sub_titulo = None
    sub_titulos_list.append(sub_titulo)
    try:
        noticia = soup.find("div",{"class":"cuerpo_noticia"})
        list_noticia = noticia.findAll("p",recursive=False)
    except:
        try:
            noticia = soup.find("div",{"class":"int-articulo"})
            list_noticia = noticia.findAll("p",recursive=False)
        except:
            list_noticia = None

    if list_noticia is None:
        noticia_completa = None
    else:
        noticia_completa = ""
        for i in list_noticia:
            if i.has_attr("class") or i.has_attr("id") :
                continue
            noticia_completa += i.text.strip()

    noticias_list.append(noticia_completa)
    delito_odio.append(1)
    count += 1
    print(str(count) +"of"+ str(len(links_odio)))
count = 0
for link in links_no_odio:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "lxml")

    try:
        titulo = soup.find("h1",{"class":"art-headline"}).text.strip()
    except:
        try:
            titulo = soup.find("h1",{"class":"titular-articulo"}).text.strip()
        except:
            titulo = None

    titulos_list.append(titulo)
    try:
        sub_titulo = soup.find("h2",{"class":"art-opening"}).text.strip()
    except:
        try:
            sub_titulo = soup.find("h2",{"class":"cont-entradilla-art"}).text.strip()
        except:
            sub_titulo = None

    sub_titulos_list.append(sub_titulo)
    try:
        noticia = soup.find("div",{"class":"cuerpo_noticia"})
        list_noticia = noticia.findAll("p",recursive=False)
    except:
        try:
            noticia = soup.find("div",{"class":"int-articulo"})
            list_noticia = noticia.findAll("p",recursive=False)
        except:
            list_noticia = None

    if list_noticia is None:
        noticia_completa = None
    else:
        noticia_completa = ""
        for i in list_noticia:
            if i.has_attr("class") or i.has_attr("id") :
                continue
            noticia_completa += i.text.strip()

    noticias_list.append(noticia_completa)
    delito_odio.append(0)
    count += 1
    print(str(count) +"of"+ str(len(links_odio)))


df = pd.DataFrame(list(zip(titulos_list, sub_titulos_list,noticias_list,delito_odio)),columns =['titulos', 'sub_titulos','noticias','delito_odio'])

writer = pd.ExcelWriter('as.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']
(max_row, max_col) = df.shape
column_settings = [{'header': column} for column in df.columns]
worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
worksheet.set_column(0, max_col - 1, 12)
writer.save()
