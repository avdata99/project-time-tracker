# Generated by Django 4.2.3 on 2023-07-23 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hours",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("hours", models.DecimalField(decimal_places=2, max_digits=4)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "url",
                    models.URLField(
                        blank=True,
                        help_text="URL to issue, PR or any important reference",
                        null=True,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hours",
                        to="projects.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hours",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
