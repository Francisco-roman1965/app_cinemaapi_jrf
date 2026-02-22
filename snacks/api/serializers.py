from rest_framework import serializers
from snacks.models import Snack
from django.db import models

class SnackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = ['id', 'producto', 'precio_unitario', 'fecha_registro']


class ActualizarPreciosSerializer(serializers.Serializer):
    descuento = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0.01,
        max_value=99.99,
        help_text="Porcentaje de descuento a aplicar (1-99%)"
    )

    def validate_descuento(self, value):
        """Validar que el descuento no sea mayor al precio más bajo"""
        from snacks.models import Snack
        precio_minimo = Snack.objects.aggregate(min_precio=models.Min('precio_unitario'))['min_precio']

        if precio_minimo and value >= float(precio_minimo):
            raise serializers.ValidationError(
                f"El descuento ({value}%) no puede ser mayor o igual al precio más bajo disponible (${precio_minimo})"
            )
        return value