# Generated by Django 4.2 on 2024-07-10 22:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('agentes', '0004_alter_tomador_agente_direcc'),
    ]

    operations = [
        migrations.AddField(
            model_name='tomador_agente',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]