from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pelicula, Director


# Vista para listar películas
class PeliculaListView(LoginRequiredMixin, ListView):
    model = Pelicula
    template_name = 'cine/pelicula_list_vc.html'
    context_object_name = 'peliculas'
    paginate_by = 10

    def get_queryset(self):
        return Pelicula.objects.select_related('director').all().order_by('-id')


# Vista para crear película
class PeliculaCreateView(LoginRequiredMixin, CreateView):
    model = Pelicula
    template_name = 'cine/pelicula_form.html'
    fields = ['titulo', 'genero', 'clasificacion', 'duracion_min', 'director', 'fecha_estreno']
    success_url = reverse_lazy('peliculas:pelicula_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Película'
        context['accion'] = 'Crear'
        return context


# Vista para actualizar película
class PeliculaUpdateView(LoginRequiredMixin, UpdateView):
    model = Pelicula
    template_name = 'cine/pelicula_form.html'
    fields = ['titulo', 'genero', 'clasificacion', 'duracion_min', 'director', 'fecha_estreno']
    success_url = reverse_lazy('peliculas:pelicula_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Película'
        context['accion'] = 'Actualizar'
        return context


# Vista para eliminar película
class PeliculaDeleteView(LoginRequiredMixin, DeleteView):
    model = Pelicula
    template_name = 'cine/pelicula_confirm_delete.html'
    success_url = reverse_lazy('peliculas:pelicula_list')
    context_object_name = 'pelicula'


from django.db.models import Q


class PeliculaSearchView(LoginRequiredMixin, ListView):
    model = Pelicula
    template_name = 'cine/busqueda_peliculas.html'
    context_object_name = 'peliculas'
    paginate_by = 10

    def get_queryset(self):
        queryset = Pelicula.objects.select_related('director').all()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(genero__icontains=query) |
                Q(director__nombre__icontains=query) |
                Q(clasificacion__icontains=query)
            ).distinct()

        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['resultados'] = self.get_queryset().count()
        return context
