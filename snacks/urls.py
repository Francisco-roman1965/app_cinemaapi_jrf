from django.urls import path
from . import views

app_name = 'snacks'

urlpatterns = [
    path('buscar/', views.SnackSearchView.as_view(), name='snack_search'),
]