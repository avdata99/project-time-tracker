# Generated by Django 4.2.3 on 2023-07-23 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="project",
            options={"verbose_name_plural": "projects"},
        ),
    ]
