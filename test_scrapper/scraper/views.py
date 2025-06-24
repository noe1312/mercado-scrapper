from django.shortcuts import render
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def index(request):
    return render(request, 'scraper/index.html')

def scrape(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')

        # Configurar opciones de Chrome (modo headless)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        # Usar webdriver-manager para manejar el chromedriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        products_array = []

        url = f'https://listado.mercadolibre.com.ar/{search_query.replace(" ", "-")}#D[A:{search_query}]'
        driver.get(url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Detectar última página
        try:
            pagination = soup.find('nav', {'aria-label': 'Paginación'})
            page_buttons = pagination.find_all('li', class_='andes-pagination__button')
            page_numbers = [int(button.text) for button in page_buttons if button.text.isdigit()]
            last_page_number = max(page_numbers) if page_numbers else 1
        except:
            last_page_number = 1

        for page in range(0, last_page_number):
            page_url = f'https://listado.mercadolibre.com.ar/{search_query.replace(" ", "-")}_Desde_{page * 50 + 1}_NoIndex_True'
            driver.get(page_url)
            time.sleep(3)

            soup_page = BeautifulSoup(driver.page_source, 'html.parser')
            divs = soup_page.find_all('div', class_='poly-card__content')

            for item in divs:
                try:
                    data = {
                        'nombre_articulo': item.find('h3', class_='poly-component__title-wrapper').text.strip(),
                        'precio': item.find('span', class_='andes-money-amount__fraction').text.strip(),
                        'link': item.find('a', class_='poly-component__title')['href'],
                    }

                    img_tag = item.find('poly-card__portada')
                    data['img'] = img_tag.get('data-src') or img_tag.get('src') if img_tag else ''

                    products_array.append(data)
                except Exception as e:
                    print("Error procesando producto:", e)

        driver.quit()
        return render(request, 'scraper/results.html', {'products': products_array})

    return JsonResponse({'error': 'Invalid request'}, status=400)
