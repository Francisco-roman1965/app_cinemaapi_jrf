from rest_framework import serializers
from funciones.models import Funcion
from peliculas.models import Pelicula


class FuncionSerializer(serializers.ModelSerializer):
    pelicula_titulo = serializers.ReadOnlyField(source='pelicula.titulo')

    class Meta:
        model = Funcion
        fields = ['id', 'pelicula', 'pelicula_titulo', 'fecha_hora', 'estado', 'precio']