from django.core import validators
from django.db import models
from django_extensions.db.models import TimeStampedModel
from treebeard.mp_tree import MP_Node


class Folder(TimeStampedModel, MP_Node):
    node_order_by = ['name']
    name = models.CharField(
        max_length=255,
        validators=[
            validators.RegexValidator(
                regex=r'/', inverse_match=True, message='Name may not contain forward slashes.'
            )
        ],
    )

    # TODO: What max_length?
    description = models.TextField(max_length=3000)

    # # TODO: owner on_delete policy?
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # # Prevent deletion of quotas while a folder references them
    # quota = models.ForeignKey(Quota, on_delete=models.PROTECT)

    # TimeStampedModel also provides "created" and "modified" fields
