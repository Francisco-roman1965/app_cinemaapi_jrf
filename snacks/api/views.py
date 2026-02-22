from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from snacks.models import Snack
from .serializers import SnackSerializer, ActualizarPreciosSerializer


# Vista para listar y crear snacks
class SnackListCreateView(generics.ListCreateAPIView):
    queryset = Snack.objects.all()
    serializer_class = SnackSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# Vista para ver, actualizar y eliminar un snack específico
class SnackRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snack.objects.all()
    serializer_class = SnackSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"mensaje": "Snack eliminado correctamente"},
            status=status.HTTP_204_NO_CONTENT
        )


# 👇 NUEVA VISTA - ACTUALIZAR PRECIOS
class ActualizarPreciosSnacksView(APIView):
    """
    Endpoint para actualizar precios de snacks aplicando un descuento porcentual
    Usa F expressions para actualización masiva eficiente
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validar datos de entrada
        serializer = ActualizarPreciosSerializer(data=request.data)

        if serializer.is_valid():
            descuento = serializer.validated_data['descuento']

            # Verificar que hay snacks para actualizar
            total_snacks = Snack.objects.count()

            if total_snacks == 0:
                return Response(
                    {"error": "No hay snacks para actualizar"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Aplicar descuento usando F expressions (actualización masiva)
            snacks_actualizados = Snack.objects.update(
                precio_unitario=F('precio_unitario') * (1 - descuento / 100)
            )

            # Obtener snacks actualizados para la respuesta
            snacks = Snack.objects.all().order_by('producto')
            resultado_serializer = SnackSerializer(snacks, many=True)

            return Response({
                "mensaje": f"Precios actualizados correctamente",
                "descuento_aplicado": f"{descuento}%",
                "snacks_actualizados": snacks_actualizados,
                "total_snacks": total_snacks,
                "snacks": resultado_serializer.data
            }, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )