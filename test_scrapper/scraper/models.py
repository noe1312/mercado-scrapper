from django.db import models

class PrecioHistorico(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    link = models.URLField()

    def __str__(self):
        return f"{self.nombre} - ${self.precio} ({self.fecha})"
