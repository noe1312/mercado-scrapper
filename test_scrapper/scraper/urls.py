from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrape/', views.scrape, name='scrape'),
    path('grafico/<int:producto_id>/', views.grafico_producto, name='grafico_producto'),
]
