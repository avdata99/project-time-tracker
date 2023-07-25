from django.contrib import admin
from hours.models import Hours


@admin.register(Hours)
class HoursAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'date', 'hours')
    search_fields = ('project__name', 'user__username', 'notes')
    date_hierarchy = 'date'
    ordering = ('-date',)
    readonly_fields = ['user']

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
        obj.user = request.user
        super().save_model(request, obj, form, change)
