import logging
from django.db import models
from hours.models import Hours
from pagos.models import Pago
from usuarios.models import ValorHoraUsuario


logger = logging.getLogger(__name__)


def liquidar_mes(liquidacion, raise_exception=True):
    """ Liquidar este mes, cerrarlo y crear el pago """
    # ver si ya hay pago
    if liquidacion.pagos.exists():
        if raise_exception:
            raise Exception(f'Ya existe pago para {liquidacion}')
        return
    # ver si hay horas registradas
    horas = Hours.objects.filter(
        user=liquidacion.user,
        date__year=liquidacion.anio,
        date__month=liquidacion.mes,
    )
    if not horas.exists():
        if raise_exception:
            raise Exception(f'No hay horas registradas para {liquidacion}')
        return

    # TODO hacer un resumen de totales por proyecto

    # calcular total
    total = horas.aggregate(models.Sum('hours'))['hours__sum']
    valor_hora = ValorHoraUsuario.get_current_for_user(liquidacion.user)
    if not valor_hora:
        if raise_exception:
            raise Exception(f'No hay valor hora para {liquidacion.user}')
        return
    pago = Pago.objects.create(
        liquidacion=liquidacion,
        moneda=valor_hora.moneda,
        total=total * valor_hora.valor_hora,
        total_horas=total,
    )
    # Marcar todas las horas como liquidadas
    horas.update(liquidacion=liquidacion)
    return pago
