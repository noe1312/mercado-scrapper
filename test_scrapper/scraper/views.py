import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    return render(request, 'scraper/index.html')

def scrape(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        url = f'https://listado.mercadolibre.com.ar/{search_query.replace(" ", "-")}#D[A:{search_query}]'
        r = requests.get(url)

        products_array = []

        if r.status_code == 200:
            contenido = r.content
            soup = BeautifulSoup(contenido, 'html.parser')

            # Obtener la última página
            try:
                pagination = soup.find('nav', {'aria-label': 'Paginación'})
                page_buttons = pagination.find_all('li', {'class': 'andes-pagination__button'})
                page_numbers = [int(button.text) for button in page_buttons if button.text.isdigit()]
                last_page_number = max(page_numbers) if page_numbers else 1
            except Exception as e:
                last_page_number = 1

            # Iterar sobre las páginas
            for page in range(0, last_page_number):
                page_url = f'https://listado.mercadolibre.com.ar/{search_query.replace(" ", "-")}_Desde_{page * 50 + 1}_NoIndex_True'
                result = requests.get(page_url)


                if result.status_code == 200:
                    content_pagination = result.content
                    soup_pagination = BeautifulSoup(content_pagination, 'html.parser')
                    divs = soup_pagination.find_all('div', {'class': 'poly-card__content'})

                    for item in divs:
                        data = {}
                        data['nombre_articulo'] = item.find('h3', {'class': 'poly-component__title-wrapper'}).text
                        data['precio'] = item.find('span', {'class': 'andes-money-amount__fraction'}).text
                        data['link'] = item.find('a', {'class': 'poly-component__title'})['href']
                        img_tag = item.find('img', {'class': 'poly-component__picture'})
                        data['img'] = img_tag.get('src') if img_tag and img_tag.get('src') else img_tag.get('data-src') if img_tag else ''

                        products_array.append(data)

        return render(request, 'scraper/results.html', {'products': products_array})

    return JsonResponse({'error': 'Invalid request'}, status=400)