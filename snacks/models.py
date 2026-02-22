from django.db import models
from entradas.models import Entrada
from django.db.models import F  # Para la expresión F del punto 10


# Create your models here.

class Snack(models.Model):
    """
    Modelo que representa un snack o producto de confitería.
    Puede estar asociado opcionalmente a una entrada.
    """

    producto = models.CharField(
        max_length=100,
        verbose_name="Producto",
        help_text="Nombre del producto (ej: Combo 1, Canchita Grande, Gaseosa)"
    )

    cantidad = models.PositiveIntegerField(
        default=1,
        verbose_name="Cantidad",
        help_text="Cantidad disponible en stock"
    )

    precio_unitario = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Precio Unitario",
        help_text="Precio por unidad en soles (S/)"
    )

    # Relación opcional con Entrada (Una entrada puede tener muchos snacks)
    # on_delete=SET_NULL permite que si la entrada se elimina, el snack no desaparezca
    entrada = models.ForeignKey(
        Entrada,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='snacks',
        verbose_name="Entrada asociada",
        help_text="Entrada a la que está asociado este snack (opcional)"
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Snack"
        verbose_name_plural = "Snacks"
        ordering = ['producto']
        db_table = 'snacks'

    def __str__(self):
        """
        Representación en string del objeto.
        """
        precio_formateado = f"S/{self.precio_unitario:.2f}"
        return f"{self.producto} - {precio_formateado} (Stock: {self.cantidad})"

    def save(self, *args, **kwargs):
        """
        Sobrescribimos el método save para formatear el precio.
        """
        # Redondear el precio a 2 decimales
        if self.precio_unitario:
            self.precio_unitario = round(self.precio_unitario, 2)

        super().save(*args, **kwargs)

    @property
    def precio_total(self):
        """Calcula el precio total según la cantidad (para mostrar en templates)"""
        return self.precio_unitario * self.cantidad if self.precio_unitario and self.cantidad else 0

    @property
    def entrada_codigo(self):
        """Propiedad para acceder al código de la entrada asociada"""
        return self.entrada.codigo if self.entrada else "Sin entrada asociada"

    @classmethod
    def aplicar_descuento(cls, min_precio=10, descuento=2):
        """
        Método utilitario para aplicar descuento masivo (punto 10)
        Usa F expressions para actualizar directamente en la BD
        """
        # Filtrar snacks con precio >= min_precio
        snacks_filtrados = cls.objects.filter(precio_unitario__gte=min_precio)

        # Aplicar descuento usando F expressions
        cantidad_actualizada = snacks_filtrados.update(
            precio_unitario=F('precio_unitario') - descuento
        )

        # Retornar los snacks actualizados
        return cls.objects.filter(precio_unitario__gte=min_precio - descuento)
