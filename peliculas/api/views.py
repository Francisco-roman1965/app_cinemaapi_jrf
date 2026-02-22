from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from peliculas.models import Pelicula, Director
from .serializers import PeliculaSerializer, DirectorSerializer, PeliculaTopVendidasSerializer


# Vistas para Directores
class DirectorListCreateView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,  # ✅ 201 Created
                headers=headers
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST  # ✅ 400 Bad Request
        )


class DirectorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"mensaje": "Director eliminado correctamente"},
            status=status.HTTP_204_NO_CONTENT  # ✅ 204 No Content
        )


# Vistas para Películas
class PeliculaListCreateView(generics.ListCreateAPIView):
    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,  # ✅ 201 Created
                headers=headers
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST  # ✅ 400 Bad Request
        )


class PeliculaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"mensaje": "Película eliminada correctamente"},
            status=status.HTTP_204_NO_CONTENT  # ✅ 204 No Content
        )


# Vista para Top Vendidas
class PeliculaTopVendidasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        peliculas = Pelicula.objects.annotate(
            total_entradas=Count(
                'funciones__entradas',
                filter=Q(funciones__entradas__vendido=True) | Q(funciones__entradas__fecha_venta__isnull=False)
            )
        ).filter(
            total_entradas__gt=0
        ).order_by('-total_entradas')

        data = []
        for pelicula in peliculas:
            data.append({
                'titulo': pelicula.titulo,
                'genero': pelicula.genero,
                'total_entradas_vendidas': pelicula.total_entradas
            })

        serializer = PeliculaTopVendidasSerializer(data, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK  # ✅ 200 OK
        )