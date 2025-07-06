from django.shortcuts import render
from django.http import JsonResponse
from selenium import webdriver

from django.shortcuts import redirect
from django.contrib import messages
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .models import PrecioHistorico
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
import time
import random
from decimal import Decimal

def index(request):
    return render(request, 'scraper/index.html')
def contacto(request):
    return render(request, 'scraper/contacto.html')
def about_us(request):
    return render(request, 'scraper/sobre_nosotros.html')
def usuario(request):
    return render(request, 'scraper/usuario.html')

def grafico_producto(request, producto_id):
    historial = PrecioHistorico.objects.filter(id=producto_id).order_by('fecha')
    producto = get_object_or_404(PrecioHistorico, id=producto_id)
    return render(request, 'scraper/grafico_producto.html', {
        'historial': historial,
        'nombre': producto.nombre,
        'producto': producto 
    })
    


def enviar_contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')

        # Podés guardar en base de datos o enviar un email aquí
        print(f"Nuevo contacto: {nombre} - {email} - {mensaje}")

        messages.success(request, 'Gracias por tu mensaje. Te responderemos pronto.')
        return redirect('contacto')  # Asegurate de que 'contacto' sea el nombre de la URL

    return redirect('contacto')



def scrape(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')

        # Configurar opciones de Chrome (modo headless)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Usar webdriver-manager para manejar el chromedriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        products_array = []

        url = f'https://listado.mercadolibre.com.ar/{search_query.replace(" ", "-")}#D[A:{search_query}]'
        driver.get(url)
        time.sleep(random.uniform(2.5,5.5))

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
            time.sleep(random.uniform(2.5,5.5))

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
                    
                    nuevo = PrecioHistorico.objects.create(
                        nombre=data['nombre_articulo'],
                        precio=Decimal(data['precio'].replace('.', '')),  
                        link=data['link']
                    )
                    data['id'] = nuevo.id
                    
                    products_array.append(data)
                except Exception as e:
                    print("Error procesando producto:", e)

        driver.quit()
        return render(request, 'scraper/results.html', {'products': products_array})

    return JsonResponse({'error': 'Invalid request'}, status=400)
