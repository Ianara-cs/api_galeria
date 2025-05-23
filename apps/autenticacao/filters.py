from django_filters import FilterSet, BooleanFilter, CharFilter
from django.db.models import Q

from django.contrib.auth.models import User

class UsuarioFilters(FilterSet):
    """
    Esta classe permite que seja possível realizar filtragem no model FOTO
    através dos campos informados.
    """
    nome = CharFilter(method='filter_nome', label='Nome, Sobrenome ou Username')
    is_active = BooleanFilter(field_name='is_active', lookup_expr='exact', label='Usuário Ativos',)
    is_staff = BooleanFilter(field_name='is_staff', lookup_expr='exact', label='Usuário Admin',)

    class Meta:
        fields = [
            'nome',
            'is_active',
            'is_staff', 
        ]
        model = User
    
    def filter_nome(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(username__icontains=value)
        )