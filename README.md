# 🛍️ Web Scraper de Productos - MercadoLibre Argentina

Este es un proyecto web desarrollado en Django que permite buscar productos en [MercadoLibre Argentina](https://listado.mercadolibre.com.ar/) y visualizar los resultados, incluyendo el nombre del producto, precio, enlace al producto e imagen.
Todo este proyecto se basa en la famosa pagina de [CamelCamelCamel](https://es.camelcamelcamel.com/) o [OfertasShark](https://www.ofertasshark.cl/)

## 🚀 Funcionalidades

- 🔎 Búsqueda de productos por palabra clave.
- 📄 Scraping de múltiples páginas de resultados.
- 💰 Muestra de nombre, precio, imagen y link directo al producto.
- 🎨 Interfaz estilizada con HTML y CSS.
- 🔄 Pantalla de carga mientras se obtienen los datos (en proceso).

## 🛠️ Tecnologías utilizadas

- Python 3.13+
- Django 5.1.3
- BeautifulSoup4
- Requests
- HTML5 + CSS3

## 📷 Captura de pantalla

### Así es la pantalla principal de busqueda ⤵️
![Pagina principal](imagenes/pagina-principal.png) 

### Y aqui un ejemplo de busqueda ⤵️
![Pagina Busqueda](imagenes/resultado-busqueda.png) 

## Actualizacion (24/06)
Se agrego un Header en la seccion de resultados y Selenium para dar más busquedas de mercado libre 
![Header](imagenes/header-results.png)

## Actualizacion (1/07)
Se corrigio el Headless para evitar el error 403
![Headless](imagenes/imagen-headless.png)

## Actualizacion (1/07)
Se modifico y corrigio la nueva vista donde se pueden ver los precios de cada producto y sus actualizaciones
![Historial](imagenes/historial-precios.png)


## ⚙️ Correcciones
- Hacer imagen visible
- Ver los precios historicos de un mismo producto
- Hacer una pagina principal con valores más baratos historicamente en un carrousel


## PROYECTO
[MERCADO SCRAPPER.docx](https://github.com/user-attachments/files/20734988/MERCADO.SCRAPPER.docx)
