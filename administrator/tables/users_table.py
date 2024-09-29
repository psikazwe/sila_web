from core.models import User
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
        view_details_url = reverse('admin:user-detail', args=[record.id])
        view_details_button = f'<a href="{view_details_url}"><i class="fa-regular fa-eye"></i></a>'
        # Second action button - Edit
        edit_url = reverse('admin:user-update', args=[record.id])  # Adjust the URL pattern as necessary
        edit_button = f'<a href="{edit_url}"><i class="fa-regular fa-pen-to-square"></i></a>'
        # Third action button - Delete
        delete_url = reverse('admin:user-delete', args=[record.id])  # Adjust the URL pattern as necessary
        delete_button = f'<a href="{delete_url}" class="danger"><i class="fa-regular fa-trash-can"></i></a>'
        # Combine all buttons inside a div for better layout control
        return mark_safe(f'<div class="action-buttons">{view_details_button} {edit_button} {delete_button}</div>')
    
class AvatarColumn(Column): 
    def render(self, record):
        formatted_avatar = format_html('<i class="fa-regular fa-user"></i>')
        return mark_safe(formatted_avatar)
    
class NameColumn(Column):  # Custom column for the name field
    def render(self, record):
        view_details_url = reverse('admin:user-detail', args=[record.id])
        formatted_name = format_html('<a href="{}" class="link"><span class="value">{}</span></a>',view_details_url, record.id)
        return mark_safe(formatted_name)
    
class IsActiveColumn(Column):  # Custom column for the name field
    def render(self, record):
        if record.is_active:
            text = "Active"
            style = "badge success"
        else:
            text = "Inactive"
            style = "badge failed"
        formatted_is_active = format_html('<span class="{}">{}</span>',style, text)
        return mark_safe(formatted_is_active)
    
class RoleColumn(Column): 
    def render(self, record):
        role = record.role()
        formatted_is_active = format_html('<span class="badge {}">{}</span>', role, role)
        return mark_safe(formatted_is_active)
    
class Table(SingleTableMixin,tables.Table):
    actions = ActionsColumn(verbose_name="Actions")
    is_active = IsActiveColumn()
    role = RoleColumn()
    avatar = AvatarColumn()
    class Meta:
        model = User
        attrs = {"class": "custom_table"}
        sequence = ('avatar','email', 'firstname', 'lastname', 'role')
        exclude = ( 'password', 'last_login', 'id', 'is_superuser', 'is_staff', 'date_joined' )


class Filter(FilterSet):
    class Meta:
        model = User
        fields = {"firstname": ["contains"]}