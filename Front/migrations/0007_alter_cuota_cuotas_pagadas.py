# Generated by Django 4.2 on 2024-12-13 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Front', '0006_alter_pago_evidencia_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuota',
            name='cuotas_pagadas',
            field=models.IntegerField(blank=True, db_column='Cuotas_Pagadas', null=True),
        ),
    ]