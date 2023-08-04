from django.db import models


class Moneda(models.TextChoices):
    PESO_ARGENTINO = 'AR'
    DOLAR_USA = 'USD'
    EURO = 'EUR'
