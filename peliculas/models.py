from django.db import models


class Director(models.Model):
    """Modelo para directores de cine"""
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    nacionalidad = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nacionalidad")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    biografia = models.TextField(blank=True, null=True, verbose_name="Biografía")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directores"
        ordering = ['nombre']


class Pelicula(models.Model):
    """Modelo para películas"""
    titulo = models.CharField(max_length=200, verbose_name="Título")
    genero = models.CharField(max_length=100, verbose_name="Género")
    clasificacion = models.CharField(max_length=50, verbose_name="Clasificación")
    duracion_min = models.IntegerField(verbose_name="Duración (minutos)")
    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE,
        related_name='peliculas',
        null=True,
        blank=True,
        verbose_name="Director"
    )
    fecha_estreno = models.DateField(blank=True, null=True, verbose_name="Fecha de estreno")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"
        ordering = ['titulo']