# Generated by Django 3.1.1 on 2020-09-10 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200910_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='root_folder',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='+',
                to='core.folder',
            ),
        ),
        migrations.AlterField(
            model_name='folder',
            name='parent',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='child_folders',
                to='core.folder',
            ),
        ),
    ]
