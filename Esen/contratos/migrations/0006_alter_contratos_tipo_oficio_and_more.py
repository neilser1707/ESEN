# Generated by Django 4.2 on 2024-07-14 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0005_contratos_tipo_oficio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratos',
            name='tipo_oficio',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='valor_incapacidad_permanente',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='valor_incapacidad_temporal',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='valor_muerte',
            field=models.IntegerField(),
        ),
    ]
