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
    total_horas = horas.aggregate(models.Sum('hours'))['hours__sum']
    total_horas = round(total_horas, 2)
    valor_hora = ValorHoraUsuario.get_current_for_user(liquidacion.user)
    total_pago = round(total_horas * valor_hora.valor_hora, 2)
    if not valor_hora:
        if raise_exception:
            raise Exception(f'No hay valor hora para {liquidacion.user}')
        return
    notas = (
        f'Total por horas: {total_horas} x '
        f'{valor_hora.moneda} {valor_hora.valor_hora} '
        f'= {total_pago}\n'
    )
    # ver los adelantos
    adelantos = liquidacion.adelantos.all()
    total_adelantos = adelantos.aggregate(models.Sum('total'))['total__sum']
    if total_adelantos:
        notas += f'Total adelantos: {total_adelantos}\n'
        total_pago -= total_adelantos
    else:
        notas += 'Sin adelantos en esta liquidacion\n'

    pago = Pago.objects.create(
        liquidacion=liquidacion,
        moneda=valor_hora.moneda,
        total=total_pago,
        total_horas=total_horas,
        notas=notas,
    )
    # Marcar todas las horas como liquidadas
    horas.update(liquidacion=liquidacion)
    return pago


def resumen_liquidacion(liquidacion):
    """ Resumen de la liquidacion """
    horas = Hours.objects.filter(
        user=liquidacion.user,
        date__year=liquidacion.anio,
        date__month=liquidacion.mes,
    )
    # agrupar las horas por proyecto
    adelantos = liquidacion.adelantos.all()
    valor_hora = ValorHoraUsuario.get_current_for_user(liquidacion.user)
    proyectos = {
        'adelantos': adelantos,
        'total_adelantos': adelantos.aggregate(models.Sum('total'))['total__sum'],
        'valor_hora': valor_hora,
        'total_horas': 0,
        'total_plata': 0,
        'proyectos': {},
        'total_final': 0,
    }

    for hora in horas:
        pid = f's-{hora.project.id}'
        if pid not in proyectos['proyectos']:
            proyectos['proyectos'][pid] = {
                'name': hora.project.name,
                'project': hora.project,
                'horas': [],
                'total_horas': 0,
                'total_plata': 0,
            }

        ps = proyectos['proyectos'][pid]
        ps['horas'].append(hora)
        ps['total_horas'] += hora.hours
        ps['total_plata'] += hora.hours * valor_hora.valor_hora
        proyectos['total_horas'] += hora.hours
        proyectos['total_plata'] += hora.hours * valor_hora.valor_hora

    proyectos['total_final'] = proyectos['total_plata'] - proyectos['total_adelantos']

    return proyectos
