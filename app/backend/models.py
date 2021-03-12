from django.db import models
from django.contrib.auth import get_user_model


class Blob(models.Model):
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True
    )
    filename = models.CharField(max_length=256, unique=True)
    s3_name = models.CharField(max_length=256)
    content_type = models.CharField(max_length=128)

    def get_owner_name(self):
        if self.owner:
            return self.owner.username
        return None

    def __str__(self):
        return f"{self.filename}"

    def __repr__(self):
        return f"{self.filename}"
