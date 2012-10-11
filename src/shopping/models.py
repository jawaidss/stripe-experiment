from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc

class Order(models.Model):
    user = models.ForeignKey(User)
    datetime = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc))

    class Meta:
        ordering = ('user', 'datetime',)

    def __unicode__(self):
        return '%s @ %s' % (self.user, self.datetime)

    def count(self):
        return self.item_set.count()

    def total(self):
        return self.item_set.aggregate(total=models.Sum('price'))['total']

class Item(models.Model):
    order = models.ForeignKey(Order)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('order', 'name',)

    def __unicode__(self):
        return '%s - %s' % (self.order, self.name)