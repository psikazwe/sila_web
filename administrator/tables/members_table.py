from core.models import Affiliate
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
        view_details_url = reverse('admin:member-detail', args=[record.id])
        view_details_button = f'<a href="{view_details_url}"><i class="fa-regular fa-eye"></i></a>'
        # Second action button - Edit
        edit_url = reverse('admin:member-update', args=[record.id])  # Adjust the URL pattern as necessary
        edit_button = f'<a href="{edit_url}"><i class="fa-regular fa-pen-to-square"></i></a>'
        # Third action button - Delete
        delete_url = reverse('admin:member-delete', args=[record.id])  # Adjust the URL pattern as necessary
        delete_button = f'<a href="{delete_url}" class="danger"><i class="fa-regular fa-trash-can"></i></a>'
        # Combine all buttons inside a div for better layout control
        return mark_safe(f'<div class="action-buttons">{view_details_button} {edit_button} {delete_button}</div>')
    
class AvatarColumn(Column): 
    def render(self, record):
        formatted_avatar = format_html(f'<img src="{record.avatar.url}" alt="{record.name}" class="avatar"/>')
        return mark_safe(formatted_avatar)
    
class NameColumn(Column):  # Custom column for the name field
    def render(self, record):
        view_details_url = reverse('admin:member-detail', args=[record.id])
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
    
class Table(SingleTableMixin,tables.Table):
    actions = ActionsColumn(verbose_name="Actions")
    is_active = IsActiveColumn()
    avatar = AvatarColumn()
    class Meta:
        model = Affiliate
        attrs = {"class": "custom_table"}
        sequence = ('avatar', 'name', 'actions')
        exclude = ( 'facebookURL', 'instagramURL', 'linkedinURL', 'youtubeURL', 'whatsappURL', 'tiktokURL', 'is_active', 'description', 'code', 'id' )


class Filter(FilterSet):
    class Meta:
        model = Affiliate
        fields = {"name": ["contains"]}