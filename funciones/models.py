from django.db import models
from peliculas.models import Pelicula


# Create your models here.

class Funcion(models.Model):
    """
    Modelo que representa una función de cine.
    Relaciona una película con un horario específico.
    """

    # Estados posibles para una función
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('agotada', 'Agotada'),
        ('cancelada', 'Cancelada'),
        ('proximamente', 'Próximamente'),
    ]

    # Relación con Pelicula (Una película puede tener muchas funciones)
    pelicula = models.ForeignKey(
        Pelicula,
        on_delete=models.CASCADE,
        related_name='funciones',
        verbose_name="Película",
        help_text="Seleccione la película para esta función"
    )

    fecha_hora = models.DateTimeField(
        verbose_name="Fecha y Hora",
        help_text="Formato: YYYY-MM-DD HH:MM:SS"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='disponible',
        verbose_name="Estado",
        help_text="Estado actual de la función"
    )

    precio = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Precio",
        help_text="Precio de la entrada en soles (S/)"
    )

    class Meta:
        verbose_name = "Función"
        verbose_name_plural = "Funciones"
        ordering = ['fecha_hora']  # Ordenamiento por defecto
        db_table = 'funciones'
        # Asegurar que no haya dos funciones de la misma película en el mismo horario
        unique_together = ['pelicula', 'fecha_hora']

    def __str__(self):
        """
        Representación en string del objeto.
        """
        fecha_formateada = self.fecha_hora.strftime("%d/%m/%Y %H:%M")
        return f"{self.pelicula.titulo} - {fecha_formateada} ({self.get_estado_display()})"

    def save(self, *args, **kwargs):
        """
        Sobrescribimos el método save para formatear el precio.
        """
        # Redondear el precio a 2 decimales
        if self.precio:
            self.precio = round(self.precio, 2)

        super().save(*args, **kwargs)

    @property
    def fecha_formateada(self):
        """Propiedad para obtener la fecha formateada"""
        return self.fecha_hora.strftime("%d/%m/%Y")

    @property
    def hora_formateada(self):
        """Propiedad para obtener la hora formateada"""
        return self.fecha_hora.strftime("%H:%M")