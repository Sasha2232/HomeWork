# Generated by Django 5.0.6 on 2024-07-02 14:15

import bboard.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0004_alter_bb_rubric'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bb',
            options={'get_latest_by': 'published', 'ordering': ['-published', 'title'], 'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.AlterField(
            model_name='bb',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, validators=[bboard.models.validate_even], verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='bb',
            name='title',
            field=models.CharField(error_messages={'invalid': 'Неправильное название товара!'}, max_length=50, validators=[django.core.validators.RegexValidator(code='invalid', message='Слишком мало букавак!', regex='^.{4,}$')], verbose_name='Товар'),
        ),
    ]
