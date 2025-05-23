from django_filters import FilterSet, NumberFilter, BooleanFilter

from apps.core.models import Comentario, Foto

class FotosFilters(FilterSet):
    """
    Esta classe permite que seja possível realizar filtragem no model FOTO
    através dos campos informados.
    """
    foto_id = NumberFilter(field_name='foto_id', lookup_expr='exact', label='ID da foto', )
    usuario_id = NumberFilter(field_name='usuario_id__id', lookup_expr='exact', label='ID do usuário', )
    aprovada = BooleanFilter(field_name='aprovada', lookup_expr='exact', label='Foto aprovada', )

    class Meta:
        fields = [
            'foto_id',
            'usuario_id',
            'aprovada', 
        ]
        model = Foto

class ComentarioFilters(FilterSet):
    """
    Esta classe permite que seja possível realizar filtragem no model COMENTARIO
    através dos campos informados.
    """
    usuario_id = NumberFilter(field_name='usuario_id', lookup_expr='exact', label='ID do usuário', )
    foto_id = NumberFilter(field_name='foto_id', lookup_expr='exact', label='ID da foto', )

    class Meta:
        fields = [
            'usuario_id', 
            'foto_id', 
        ]
        model = Comentario