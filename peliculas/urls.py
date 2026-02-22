from django.urls import path
from . import views

app_name = 'peliculas'

urlpatterns = [
    # URLs para vistas basadas en templates
    path('', views.PeliculaListView.as_view(), name='pelicula_list'),
    path('nueva/', views.PeliculaCreateView.as_view(), name='pelicula_create'),
    path('<int:pk>/editar/', views.PeliculaUpdateView.as_view(), name='pelicula_update'),
    path('<int:pk>/eliminar/', views.PeliculaDeleteView.as_view(), name='pelicula_delete'),
    path('buscar/', views.PeliculaSearchView.as_view(), name='pelicula_search'),
]