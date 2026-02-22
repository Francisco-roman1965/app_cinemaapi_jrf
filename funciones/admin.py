from django.contrib import admin
from .models import Funcion

@admin.register(Funcion)
class FuncionAdmin(admin.ModelAdmin):
    list_display = ['id', 'pelicula', 'fecha_hora', 'estado', 'precio']
    list_filter = ['estado', 'fecha_hora']
    search_fields = ['pelicula__titulo']