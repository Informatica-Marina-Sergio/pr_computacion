import requests
from bs4 import BeautifulSoup
import pandas as pd


no_pages = 4
no_pages_no = 2
urls_odio = []
urls_no_odio = []
links_de_odio = []
links_no_odio = []
for i in range(no_pages):
        urls_odio.append("https://www.lasexta.com/temas/delitos_de_odio-"+str(i+1))

for URL in urls_odio:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.findAll("a",{"class":"link-noticia"})
        for result in results:
                links_de_odio.append(result["href"])

for i in range(no_pages_no):
        urls_no_odio.append("https://www.lasexta.com/noticias/ciencia-tecnologia-"+str(i+1))

for i in range(no_pages_no):
        urls_no_odio.append("https://www.lasexta.com/noticias/economia-"+str(i+1))

for URL in urls_no_odio:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.findAll("a",{"class":"link-noticia"})
        for result in results:
                links_no_odio.append(result["href"])

titulos_list = []
sub_titulos_list = []
noticias_list = []
delito_odio = []
contador = 1
for link in links_de_odio:
	page = requests.get(link)
	soup = BeautifulSoup(page.content, "lxml")
	titulo = soup.find("h1",{"class":"title-new"}).text.strip()
	titulos_list.append(titulo)
	sub_titulo = soup.find("sumary",{"class":"entradilla"}).text.strip()
	sub_titulos_list.append(sub_titulo)
	noticia = soup.find("div",{"class":"articleBody"})
	
	list_noticia = noticia.findAll("p",recursive=False)
	noticia_completa = ""
	for i in list_noticia:
		if i.has_attr("class"):
			continue
		noticia_completa += i.text.strip()
	noticias_list.append(noticia_completa)
	delito_odio.append(1)
	contador += 1

for link in links_no_odio:
	page = requests.get(link)
	soup = BeautifulSoup(page.content, "lxml")
	titulo = soup.find("h1",{"class":"title-new"}).text.strip()
	titulos_list.append(titulo)
	sub_titulo = soup.find("sumary",{"class":"entradilla"}).text.strip()
	sub_titulos_list.append(sub_titulo)
	noticia = soup.find("div",{"class":"articleBody"})
	
	list_noticia = noticia.findAll("p",recursive=False)
	noticia_completa = ""
	for i in list_noticia:
		if i.has_attr("class"):
			continue
		noticia_completa += i.text.strip()
	noticias_list.append(noticia_completa)
	delito_odio.append(0)
	contador += 1

df = pd.DataFrame(list(zip(titulos_list, sub_titulos_list,noticias_list,delito_odio)),columns =['titulos', 'sub_titulos','noticias','delito_odio'])
writer = pd.ExcelWriter('la_sexta.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']
(max_row, max_col) = df.shape
column_settings = [{'header': column} for column in df.columns]
worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
worksheet.set_column(0, max_col - 1, 12)
writer.save()
