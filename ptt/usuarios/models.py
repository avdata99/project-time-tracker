import logging
from django.contrib.auth.models import User
from django.db import models
from usuarios.enums import Moneda


logger = logging.getLogger(__name__)


class ProyectoUsuario(models.Model):
    """ Proyectos que en el que el usuario participa """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='proyectos',
    )
    proyecto = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='usuarios',
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.proyecto.name}'

    class Meta:
        verbose_name_plural = 'proyectos de usuarios'
        unique_together = ('user', 'proyecto')
        ordering = ('user', 'proyecto')


class ValorHoraUsuario(models.Model):
    """ Sueldos de un programador en un período especifico """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='valores_hora',
    )
    desde = models.ForeignKey(
        'liquidaciones.Liquidacion',
        on_delete=models.CASCADE,
        related_name='valores_hora',
    )

    moneda = models.CharField(
        max_length=3,
        choices=Moneda.choices,
        default=Moneda.PESO_ARGENTINO,
    )
    valor_hora = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.valor_hora} {self.moneda}'

    @classmethod
    def get_current_for_user(cls, user):
        """ Devuelve el valor hora actual para un usuario especifico"""
        try:
            valor_hora = cls.objects.filter(
                user=user
            ).order_by(
                '-desde__anio', '-desde__mes'
            )[0]
        except cls.DoesNotExist:
            logger.warning(f'No se encontró valor hora para {user.username}')
            return None
        return valor_hora

    class Meta:
        verbose_name_plural = 'valores hora de usuarios'
        unique_together = ('user', 'desde')
        ordering = ('desde',)
