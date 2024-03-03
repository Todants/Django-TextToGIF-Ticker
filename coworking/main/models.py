from django.db import models


class Promt(models.Model):
    text = models.CharField('promt', max_length=50)

    def __str__(self):
        return self.text
