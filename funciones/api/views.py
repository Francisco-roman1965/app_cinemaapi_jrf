from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from funciones.models import Funcion
from .serializers import FuncionSerializer


class FuncionListCreateView(generics.ListCreateAPIView):
    queryset = Funcion.objects.all()
    serializer_class = FuncionSerializer
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


class FuncionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Funcion.objects.all()
    serializer_class = FuncionSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"mensaje": "Función eliminada correctamente"},
            status=status.HTTP_204_NO_CONTENT  # ✅ 204 No Content
        )