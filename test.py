import requests 
from bs4 import BeautifulSoup
import pandas as pd

# Array para añadir los objetos
products_array = []

string = input('¿Qué quieres buscar? ')
url = 'https://listado.mercadolibre.com.ar/{}#D[A:{}]'.format(string.replace(' ', '-'), string)
r = requests.get(url)

# Verificar si la solicitud fue exitosa
if r.status_code == 200:
    contenido = r.content
    soup = BeautifulSoup(contenido, 'html.parser')

    # Obtener la última página
    try:
        pagination = soup.find('nav', {'aria-label': 'Paginación'})
        page_buttons = pagination.find_all('li', {'class': 'andes-pagination__button'})
        page_numbers = [int(button.text) for button in page_buttons if button.text.isdigit()]
        last_page_number = max(page_numbers) if page_numbers else 1
        print("Última página:", last_page_number)
    except Exception as e:
        print("Error al obtener la última página:", e)
        last_page_number = 1

    # Iterar sobre las páginas
    for page in range(0, last_page_number):
        # Construir la URL de la página actual
        page_url = f'https://listado.mercadolibre.com.ar/{string.replace(" ", "-")}_Desde_{page * 50 + 1}_NoIndex_True'
        result = requests.get(page_url)

        if result.status_code == 200:
            content_pagination = result.content
            soup_pagination = BeautifulSoup(content_pagination, 'html.parser')
            divs = soup_pagination.find_all('div', {'class': 'poly-card__content'})

            for item in divs:
                data = {}
                data['nombre articulo'] = item.find('h3', {'class': 'poly-component__title-wrapper'}).text
                data['precio'] = item.find('span', {'class': 'andes-money-amount__fraction'}).text
                data['link'] = item.find('a', {'class': 'poly-component__title'})['href']
                products_array.append(data)
        else:
            print(f"Error al acceder a la página {page + 1}: {result.status_code}")

    # Convertir a DataFrame de pandas
    df = pd.DataFrame(products_array)
    print(df)

else:
    print("Error en la solicitud inicial:", r.status_code)

# CORREGIR LOS LINKS QUE TE DA
