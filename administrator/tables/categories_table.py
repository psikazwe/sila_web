from core.models import Service, Category
from django.utils.html import format_html
from django_tables2 import SingleTableMixin, tables
from django_tables2.columns import Column
from django_filters import FilterSet

from django.utils.safestring import mark_safe
from django.urls import reverse



class ActionsColumn(Column):
    empty_values = list()
    orderable = False 
    def render(self, record):
        # First action button - View Details
        view_details_url = reverse('admin:category-detail', args=[record.id])
        view_details_button = f'<a href="{view_details_url}"><i class="fa-regular fa-eye"></i></a>'
        # Second action button - Edit
        edit_url = reverse('admin:category-update', args=[record.id])  # Adjust the URL pattern as necessary
        edit_button = f'<a href="{edit_url}"><i class="fa-regular fa-pen-to-square"></i></a>'
        # Third action button - Delete
        delete_url = reverse('admin:category-delete', args=[record.id])  # Adjust the URL pattern as necessary
        delete_button = f'<a href="{delete_url}" class="danger"><i class="fa-regular fa-trash-can"></i></a>'
        # Combine all buttons inside a div for better layout control
        return mark_safe(f'<div class="action-buttons">{view_details_button} {edit_button} {delete_button}</div>')

class ServiceCountColumn(Column):
    empty_values = list()
    orderable = False 
    def render(self, record):
        return record.services.count()

class NameColumn(Column):  # Custom column for the name field
    def render(self, record):
        view_details_url = reverse('admin:category-detail', args=[record.id])
        formatted_name = format_html('<a href="{}" class="link"><span class="value">{}</span></a>',view_details_url, record.name)
        return mark_safe(formatted_name)
    

class Table(tables.Table):
    service_count = ServiceCountColumn(accessor='service_count', verbose_name='Number of Services')
    actions = ActionsColumn(verbose_name="Actions")
    name = NameColumn()
    class Meta:
        model = Category
        fields = { "id", "name", "description", }
        attrs = {"class": "custom_table"}
        exclude = ("description", "id")

class Filter(FilterSet):
    class Meta:
        model = Category
        fields = {"name": ["contains"]}
        # fields = {"name": ["exact", "contains"], "description": ["exact", "contains"] , "category": ["exact"]}