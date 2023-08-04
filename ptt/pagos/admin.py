from django.contrib import admin
from pagos.models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = (
        'liquidacion', 'moneda', 'total', 'pagado',
        'total', 'total_horas', 'created', 'updated',
    )
    list_filter = (
        'moneda',
        'pagado',
        'created',
        'updated',
    )
    search_fields = (
        'liquidacion__user__username',
        'liquidacion__user__first_name',
        'liquidacion__user__last_name',
        'liquidacion__anio',
        'liquidacion__mes',
    )
    ordering = (
        '-liquidacion__anio',
        '-liquidacion__mes',
        'liquidacion__user__username',
    )
    date_hierarchy = 'created'
    readonly_fields = (
        'created',
        'updated',
    )
