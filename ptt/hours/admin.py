from django.contrib import admin
from hours.models import Hours


@admin.register(Hours)
class HoursAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'date', 'hours')
    list_filter = ('project', 'user', 'date')
    search_fields = ('project__name', 'user__username', 'notes')
    date_hierarchy = 'date'
    ordering = ('-date',)
