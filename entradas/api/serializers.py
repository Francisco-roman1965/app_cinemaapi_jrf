from rest_framework import serializers
from entradas.models import Entrada
from funciones.api.serializers import FuncionSerializer


class EntradaSerializer(serializers.ModelSerializer):
    funcion_detalle = FuncionSerializer(source='funcion', read_only=True)

    class Meta:
        model = Entrada
        fields = ['id', 'codigo', 'funcion', 'funcion_detalle', 'asiento', 'vendido', 'fecha_venta']
        extra_kwargs = {
            'funcion': {'write_only': True},  # Para enviar el ID al crear
        }