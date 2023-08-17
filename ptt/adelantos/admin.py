from django.contrib import admin
from adelantos.models import Adelanto


@admin.register(Adelanto)
class AdelantoAdmin(admin.ModelAdmin):
    list_display = ('liquidacion', 'user', 'moneda', 'total', 'created')
    list_filter = ('liquidacion__user',)

    def user(self, obj):
        return obj.liquidacion.user
