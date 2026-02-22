from rest_framework import serializers
from entradas.models import Entrada
from funciones.api.serializers import FuncionSerializer


class EntradaSerializer(serializers.ModelSerializer):
    funcion = FuncionSerializer(read_only=True)

    class Meta:
        model = Entrada
        fields = ['id', 'funcion', 'asiento', 'fecha_venta']