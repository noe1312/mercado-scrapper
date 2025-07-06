from django.core.management.base import BaseCommand
from scraper.models import PrecioHistorico
from django.utils import timezone
from decimal import Decimal

class Command(BaseCommand):
    help = "Analiza movimientos de precio (+/- $1000) o si pasó 1 mes"

    def handle(self, *args, **kwargs):
        productos = PrecioHistorico.objects.values('nombre', 'link').distinct()

        for producto in productos:
            nombre = producto['nombre']
            link = producto['link']

            # Obtener el último precio registrado
            historico = PrecioHistorico.objects.filter(nombre=nombre).order_by('-fecha').first()
            if not historico:
                continue

            ultimo_precio = historico.precio
            ultima_fecha = historico.fecha

            # Simular precio actual (debes implementar el scraping real aquí)
            precio_actual = self.obtener_precio_actual(link)

            # Comparar fechas y precios
            hoy = timezone.now()
            dias_pasados = (hoy - ultima_fecha).days
            diferencia = precio_actual - ultimo_precio
            abs_diferencia = abs(diferencia)

            if dias_pasados >= 30 or abs_diferencia >= Decimal('1000'):
                PrecioHistorico.objects.create(
                    nombre=nombre,
                    precio=precio_actual,
                    fecha=hoy,
                    link=link
                )
                
                # Mensajes específicos para cada caso
                if abs_diferencia >= Decimal('1000'):
                    if diferencia > 0:
                        mensaje = f"{nombre}: Subida de ${abs_diferencia} (de ${ultimo_precio} a ${precio_actual})"
                    else:
                        mensaje = f"{nombre}: Bajada de ${abs_diferencia} (de ${ultimo_precio} a ${precio_actual})"
                else:
                    mensaje = f"⏳ {nombre}: Actualización mensual a ${precio_actual}"
                    
                self.stdout.write(self.style.SUCCESS(mensaje))

    def obtener_precio_actual(self, link):
        # 💡 Implementa aquí tu lógica real de scraping
        from random import randint
        # Simulamos variaciones de +/- $2000 para testing
        variacion = randint(-2000, 2000)
        ultimo_precio = PrecioHistorico.objects.filter(link=link).order_by('-fecha').first().precio
        return Decimal(int(ultimo_precio) + variacion)
