from django.urls import path
from .views import SnackListCreateView, SnackRetrieveUpdateDestroyView, ActualizarPreciosSnacksView

urlpatterns = [
    path('', SnackListCreateView.as_view(), name='snack-list'),
    path('<int:pk>/', SnackRetrieveUpdateDestroyView.as_view(), name='snack-detail'),
    path('actualizar-precios/', ActualizarPreciosSnacksView.as_view(), name='snack-actualizar-precios'),
]