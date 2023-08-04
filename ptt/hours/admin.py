from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe
from hours.models import Hours


@admin.register(Hours)
class HoursAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'date', 'hours', 'notes', 'url_')
    search_fields = ('project__name', 'user__username', 'notes')
    date_hierarchy = 'date'
    ordering = ('-date',)

    def get_readonly_fields(self, request, obj=None):
        """ Only superuser can edit user """
        if request.user.is_superuser:
            return []
        else:
            return ['user']

    def url_(self, obj):
        if obj.url:
            return mark_safe(f'<a target="_blank" href="{obj.url}">{obj.url}</a>')
        else:
            return ''

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)

        return queryset

    def get_list_filter(self, request):
        """ Show user filter for superuser """
        if request.user.is_superuser:
            return ('project', 'user', 'date')
        else:
            return ('project', 'date')

    def save_model(self, request, obj, form, change):
        """ force the user to be the logged user """
        if not request.user.is_superuser:
            obj.user = request.user
        super().save_model(request, obj, form, change)
