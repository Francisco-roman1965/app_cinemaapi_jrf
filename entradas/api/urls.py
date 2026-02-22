from django.urls import path
from .views import EntradaListCreateView, EntradaRetrieveUpdateDestroyView

urlpatterns = [
    path('', EntradaListCreateView.as_view(), name='entrada-list'),
    path('<int:pk>/', EntradaRetrieveUpdateDestroyView.as_view(), name='entrada-detail'),
]