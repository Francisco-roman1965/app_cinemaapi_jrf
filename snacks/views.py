from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Snack


class SnackSearchView(LoginRequiredMixin, ListView):
    model = Snack
    template_name = 'cine/busqueda_snacks.html'
    context_object_name = 'snacks'
    paginate_by = 10

    def get_queryset(self):
        queryset = Snack.objects.all()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(producto__icontains=query)
            )

        return queryset.order_by('producto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['resultados'] = self.get_queryset().count()
        return context
