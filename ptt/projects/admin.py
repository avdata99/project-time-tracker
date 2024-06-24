from django.contrib import admin
from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'description')
    ordering = ('name',)

    def full_name(self, obj):
        return obj.full_name
    full_name.admin_order_field = 'name'
