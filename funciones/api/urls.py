from django.urls import path
from .views import FuncionListCreateView, FuncionRetrieveUpdateDestroyView

urlpatterns = [
    path('', FuncionListCreateView.as_view(), name='funcion-list'),
    path('<int:pk>/', FuncionRetrieveUpdateDestroyView.as_view(), name='funcion-detail'),
]