# Generated by Django 3.1.1 on 2020-09-10 16:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200901_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='depth',
            field=models.PositiveSmallIntegerField(
                default=9999,
                editable=False,
                validators=[
                    django.core.validators.MaxValueValidator(
                        30, message='Maximum folder depth exceeded.'
                    ),
                ],
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='folder',
            name='parent',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to='core.folder'
            ),
        ),
    ]
