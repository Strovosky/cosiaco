# Generated by Django 5.1.7 on 2025-04-14 23:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('los_cosiacos', '0005_cosiaco_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='cosiaco',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='los_cosiacos.cosiaco', verbose_name='cosiaco'),
        ),
    ]
