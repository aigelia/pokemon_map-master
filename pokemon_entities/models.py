from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField()

    def __str__(self):
        return f'{self.title}'