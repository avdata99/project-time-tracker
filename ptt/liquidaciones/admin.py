from django.contrib import admin
from liquidaciones.models import Liquidacion


@admin.register(Liquidacion)
class LiquidacionAdmin(admin.ModelAdmin):
    list_display = ('anio', 'mes', 'user', 'abierto')
    list_filter = ('user', 'abierto', 'anio', 'mes')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created', 'updated')
    actions = ('cerrar', 'abrir')

    def cerrar(self, request, queryset):
        """ Accion para cerrar liquidaciones """
        for reg in queryset:
            reg.liquidar()
        queryset.update(abierto=False)

    def abrir(self, request, queryset):
        """ Accion para abrir liquidaciones """
        # TODO eliminar los pagos generados
        queryset.update(abierto=True)
