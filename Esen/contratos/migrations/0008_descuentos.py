# Generated by Django 4.2 on 2024-07-14 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0007_reglasaños_tiposoficios'),
    ]

    operations = [
        migrations.CreateModel(
            name='Descuentos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('años', models.IntegerField()),
                ('porcenntaje', models.IntegerField()),
            ],
        ),
    ]
