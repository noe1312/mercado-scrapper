import requests 
import pandas 
from bs4 import BeautifulSoup
import unicodecsv as csv

# DataFrame de pandas, para que se vea mas prolijo la informacion 
# colocar 'df' para ver en la terminal
# df = pandas.DataFrame(products_array)

string = input('¿Qué quieres buscar?')
r = requests.get('https://listado.mercadolibre.com.ar/{}#D[A:{}]'.format(string.replace(' ', '-'), string))
contenido = r.content
soup = BeautifulSoup(contenido, 'html.parser')

divs = soup.find_all('div', {'class': 'poly-card__content'})


# Recorre las listas de paginas
try:
        pagination = soup.find('nav', {'aria-label': 'Paginación'})
        # Obtener todos los elementos de paginación
        page_buttons = pagination.find_all('li', {'class': 'andes-pagination__button'})
        
        # Filtrar solo los que son números
        page_numbers = [int(button.text) for button in page_buttons if button.text.isdigit()]
        
        # Obtener el número máximo de página
        last_page_number = max(page_numbers) if page_numbers else 1  # Si no hay números, asumimos 1
        print("Última página:", last_page_number)
except Exception as e:
        print("Error al obtener la última página:", e)
        last_page_number = 1  # Si hay un error, asumimos que hay al menos una página


# Array para añadir los objetos
products_array = []

for page in range(0, last_page_number):
    print(page)

for item in divs:
    data = {}
    data['nombre articulo'] = item.find('h3', {'class': 'poly-component__title-wrapper'}).text
    data['precio'] = item.find('span', {'class': 'andes-money-amount__fraction'}).text
    data['link'] = item.find('a',{'class': 'poly-component__title'})['href']
    products_array.append(data)

# print(products_array)

