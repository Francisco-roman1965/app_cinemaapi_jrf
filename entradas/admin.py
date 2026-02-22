from django.contrib import admin
from .models import Entrada

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo', 'funcion', 'asiento', 'vendido', 'fecha_venta']
    list_filter = ['vendido', 'fecha_venta']
    search_fields = ['codigo', 'asiento']