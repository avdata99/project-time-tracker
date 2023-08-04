from django.contrib import admin
from usuarios.models import ProyectoUsuario, ValorHoraUsuario


@admin.register(ProyectoUsuario)
class ProyectoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'proyecto')
    list_filter = ('user', 'proyecto')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created', 'updated')


@admin.register(ValorHoraUsuario)
class ValorHoraUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'desde', 'valor_hora', 'moneda')
    list_filter = ('user', 'moneda')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created', 'updated')
