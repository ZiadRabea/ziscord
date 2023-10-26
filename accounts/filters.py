import django_filters
from .models import profile


class Search(django_filters.FilterSet):
    Searching_Name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = profile
        fields = ('Searching_Name', )
