from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Hours(models.Model):
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='hours',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='hours',
    )
    date = models.DateField(
        default=timezone.now,
    )
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    url = models.URLField(
        null=True, blank=True,
        help_text='URL to issue, PR or any important reference',
    )

    class Meta:
        verbose_name_plural = 'hours'
