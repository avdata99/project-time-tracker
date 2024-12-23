import logging
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


logger = logging.getLogger(__name__)


class Liquidacion(models.Model):
    """ Cierre de un periodo de pago """
    anio = models.IntegerField()
    mes = models.IntegerField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liquidaciones',
    )
    abierto = models.BooleanField(
        default=True,
        help_text=(
            'Indica si el periodo de pago '
            'esta abierto o cerrado (pagado)'
        ),
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.anio}-{self.mes}-{self.user.username}'

    @classmethod
    def inicializar_mes(cls, hora_registrada):
        """ Si un usuario registra horas en un mes me aseguro que exista
            la liquidacion correspondiente """
        user = hora_registrada.user
        anio = hora_registrada.date.year
        mes = hora_registrada.date.month
        liquidacion, created = cls.objects.get_or_create(
            anio=anio,
            mes=mes,
            user=user,
        )
        if created:
            logger.info(f'Nueva liquidacion creada: {liquidacion}')
            liquidacion.abierto = True
            liquidacion.save()

        return liquidacion

    def liquidar(self, raise_exception=True):
        from liquidaciones.helpers import liquidar_mes
        return liquidar_mes(self, raise_exception=raise_exception)

    @property
    def resumen(self):
        from liquidaciones.helpers import resumen_liquidacion
        return resumen_liquidacion(self)

    class Meta:
        verbose_name_plural = 'liquidaciones'
        ordering = ('-anio', '-mes')

    def is_last_n_months(self, months=3):
        now = timezone.now()
        last_n_months = now - timezone.timedelta(days=months * 30)
        last_n_str = last_n_months.strftime('%Y-%m')
        this_month = f'{self.anio}-{self.mes}'
        return this_month >= last_n_str
