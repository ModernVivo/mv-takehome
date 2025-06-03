from django.db import models

class Paper(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    journal = models.CharField(max_length=255)
    invivo_model = models.CharField(max_length=255)
    abstract = models.TextField()
    condition_sets = models.JSONField(default=list)
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return self.title
