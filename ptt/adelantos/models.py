from django.db import models
from usuarios.enums import Moneda


class Adelanto(models.Model):
    liquidacion = models.ForeignKey(
        'liquidaciones.Liquidacion',
        on_delete=models.CASCADE,
        related_name='adelantos',
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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
