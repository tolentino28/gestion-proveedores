# Generated by Django 4.2 on 2024-12-13 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Front', '0007_alter_cuota_cuotas_pagadas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuota',
            name='id_compra',
            field=models.OneToOneField(db_column='ID_Compra', on_delete=django.db.models.deletion.CASCADE, to='Front.compra'),
        ),
    ]