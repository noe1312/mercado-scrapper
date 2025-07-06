from django.urls import path
from .views import enviar_contacto
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrape/', views.scrape, name='scrape'),
    path('grafico/<int:producto_id>/', views.grafico_producto, name='grafico_producto'),
    path('contacto',views.contacto ,name='contacto'),
    path('nosotros',views.about_us ,name='about_us'),
    path('usuario',views.usuario ,name='usuario'),
        path('enviar_contacto/', enviar_contacto, name='enviar_contacto'),


]
