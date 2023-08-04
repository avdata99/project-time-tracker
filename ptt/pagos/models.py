import logging
from django.db import models
from usuarios.enums import Moneda


logger = logging.getLogger(__name__)


class Pago(models.Model):
    liquidacion = models.ForeignKey(
        'liquidaciones.Liquidacion',
        on_delete=models.CASCADE,
        related_name='pagos',
    )
    moneda = models.CharField(
        max_length=3,
        choices=Moneda.choices,
        default=Moneda.PESO_ARGENTINO,
    )
    total = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )
    pagado = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.liquidacion} - {self.total} {self.moneda}'
