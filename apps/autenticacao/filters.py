from django_filters import FilterSet, BooleanFilter, CharFilter

from django.contrib.auth.models import User

class UsuarioFilters(FilterSet):
    """
    Esta classe permite que seja possível realizar filtragem no model FOTO
    através dos campos informados.
    """
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains', label='Nome Usuário',)
    is_active = BooleanFilter(field_name='is_active', lookup_expr='exact', label='Usuário Ativos',)
    is_staff = BooleanFilter(field_name='is_staff', lookup_expr='exact', label='Usuário Admin',)

    class Meta:
        fields = [
            'first_name',
            'is_active',
            'is_staff', 
        ]
        model = User