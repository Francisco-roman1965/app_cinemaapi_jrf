from django.contrib import admin
from .models import Pelicula, Director

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'nacionalidad', 'fecha_nacimiento']
    search_fields = ['nombre', 'nacionalidad']

@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'genero', 'clasificacion', 'duracion_min', 'director', 'fecha_estreno']
    list_filter = ['genero', 'clasificacion']
    search_fields = ['titulo', 'director__nombre']