# Generated by Django 3.1.2 on 2020-11-04 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_initial_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terms',
            fields=[
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name='created'
                    ),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name='modified'
                    ),
                ),
                (
                    'tree',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name='terms',
                        serialize=False,
                        to='core.tree',
                    ),
                ),
                ('text', models.TextField()),
                ('checksum', models.CharField(editable=False, max_length=32)),
            ],
            options={
                'verbose_name': 'terms of use',
                'verbose_name_plural': 'terms of use',
            },
        ),
        migrations.CreateModel(
            name='TermsAgreement',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name='created'
                    ),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name='modified'
                    ),
                ),
                ('checksum', models.CharField(max_length=32)),
                (
                    'terms',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='agreements',
                        to='core.terms',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='terms_agreements',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name='termsagreement',
            index=models.Index(fields=['terms', 'user'], name='core_termsa_terms_i_6f2ce1_idx'),
        ),
        migrations.AddConstraint(
            model_name='termsagreement',
            constraint=models.UniqueConstraint(
                fields=('terms', 'user'), name='terms_agreement_unique'
            ),
        ),
    ]
