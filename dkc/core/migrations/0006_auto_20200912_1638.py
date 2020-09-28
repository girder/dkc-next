# Generated by Django 3.1.1 on 2020-09-12 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200910_2019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='folder',
            options={'ordering': ['name']},
        ),
        migrations.AddIndex(
            model_name='folder',
            index=models.Index(fields=['parent', 'name'], name='core_folder_parent__50a462_idx'),
        ),
        migrations.AddConstraint(
            model_name='folder',
            constraint=models.UniqueConstraint(
                fields=('parent', 'name'), name='folder_siblings_name_unique'
            ),
        ),
        migrations.AddConstraint(
            model_name='folder',
            constraint=models.UniqueConstraint(
                condition=models.Q(parent=None), fields=('name',), name='root_folder_name_unique'
            ),
        ),
    ]