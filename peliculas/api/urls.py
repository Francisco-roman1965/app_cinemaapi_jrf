from django.urls import path
from .views import (
    PeliculaListCreateView, PeliculaRetrieveUpdateDestroyView,
    DirectorListCreateView, DirectorRetrieveUpdateDestroyView,
    PeliculaTopVendidasView, PeliculaTopVendidasView
)

urlpatterns = [
    # URLs de Películas
    path('', PeliculaListCreateView.as_view(), name='pelicula-list'),
    path('<int:pk>/', PeliculaRetrieveUpdateDestroyView.as_view(), name='pelicula-detail'),
    path('top-vendidas/', PeliculaTopVendidasView.as_view(), name='pelicula-top-vendidas'),

    # URLs de Directores
    path('directores/', DirectorListCreateView.as_view(), name='director-list'),
    path('directores/<int:pk>/', DirectorRetrieveUpdateDestroyView.as_view(), name='director-detail'),

]