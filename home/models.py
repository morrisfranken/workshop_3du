from django.db import models


class Uploads(models.Model):
    file            = models.FileField(upload_to='uploads/')
    created_at      = models.DateTimeField(auto_now_add=True)
    classification  = models.CharField(max_length=50, null=True, default=None)


