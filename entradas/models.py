from django.db import models
from funciones.models import Funcion


# Create your models here.

class Entrada(models.Model):
    """
    Modelo que representa una entrada para una función.
    Cada entrada tiene un asiento específico y puede estar vendida o no.
    """

    # Código único para la entrada
    codigo = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Código",
        help_text="Código único de la entrada (ej: ENT-001-2024)"
    )

    # Relación con Funcion (Una función puede tener muchas entradas)
    funcion = models.ForeignKey(
        Funcion,
        on_delete=models.CASCADE,
        related_name='entradas',
        verbose_name="Función",
        help_text="Función a la que pertenece esta entrada"
    )

    asiento = models.CharField(
        max_length=10,
        verbose_name="Asiento",
        help_text="Número de asiento (ej: A1, B12, C5)"
    )

    vendido = models.BooleanField(
        default=False,
        verbose_name="Vendido",
        help_text="Indica si la entrada ya fue vendida"
    )

    fecha_venta = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Venta",
        help_text="Fecha y hora en que se vendió la entrada (solo si está vendida)"
    )

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"
        ordering = ['funcion', 'asiento']
        db_table = 'entradas'
        # Asegurar que no haya dos entradas con el mismo asiento para la misma función
        unique_together = ['funcion', 'asiento']

    def __str__(self):
        """
        Representación en string del objeto.
        """
        estado = "VENDIDA" if self.vendido else "DISPONIBLE"
        fecha_funcion = self.funcion.fecha_hora.strftime("%d/%m/%Y")
        return f"{self.codigo} - {self.funcion.pelicula.titulo} ({fecha_funcion}) - Asiento: {self.asiento} [{estado}]"

    def save(self, *args, **kwargs):
        """
        Sobrescribimos el método save para:
        1. Generar un código automático si no se proporciona
        2. Manejar la fecha de venta automáticamente
        """
        # Si no hay código, generar uno automático
        if not self.codigo:
            import datetime
            import random
            fecha_actual = datetime.datetime.now()
            año = fecha_actual.year
            mes = fecha_actual.month
            dia = fecha_actual.day
            random_num = random.randint(1000, 9999)
            self.codigo = f"ENT-{año}{mes:02d}{dia:02d}-{random_num}"

        # Si se marca como vendido y no tiene fecha_venta, poner la fecha actual
        if self.vendido and not self.fecha_venta:
            from django.utils import timezone
            self.fecha_venta = timezone.now()

        # Si se desmarca como vendido, limpiar la fecha_venta
        if not self.vendido:
            self.fecha_venta = None

        super().save(*args, **kwargs)

    @property
    def precio_actual(self):
        """Propiedad para obtener el precio de la función asociada"""
        return self.funcion.precio if self.funcion else None

    @property
    def pelicula_titulo(self):
        """Propiedad para acceder al título de la película desde la entrada"""
        return self.funcion.pelicula.titulo if self.funcion else None


from django.db import models

# Create your models here.
