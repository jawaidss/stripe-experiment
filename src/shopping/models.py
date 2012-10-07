from django.core.urlresolvers import reverse
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name