from rest_framework import serializers
from peliculas.models import Pelicula, Director


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'nombre', 'nacionalidad']


class PeliculaSerializer(serializers.ModelSerializer):
     director = DirectorSerializer(read_only=True)

     class Meta:
         model = Pelicula
         fields =['id', 'titulo', 'genero', 'clasificacion', 'duracion_min', 'director']

class PeliculaTopVendidasSerializer(serializers.Serializer):
    titulo = serializers.CharField()
    genero = serializers.CharField()
    total_entradas_vendidas = serializers.IntegerField()