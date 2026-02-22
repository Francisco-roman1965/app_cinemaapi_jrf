from django.contrib import admin
from .models import Snack

@admin.register(Snack)
class SnackAdmin(admin.ModelAdmin):
    list_display = ['id', 'producto', 'cantidad', 'precio_unitario', 'fecha_registro']
    list_filter = ['fecha_registro']
    search_fields = ['producto']