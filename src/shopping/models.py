from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Card(models.Model):
    user = models.ForeignKey(User)
    stripe_customer_id = models.CharField('Stripe customer ID', max_length=100, unique=True)

    class Meta:
        ordering = ('user', 'stripe_customer_id',)

    def __unicode__(self):
        return '%s (%s)' % (self.user, self.stripe_customer_id)

class Order(models.Model):
    user = models.ForeignKey(User)
    stripe_charge_id = models.CharField('Stripe charge ID', max_length=100, unique=True)
    ip_address = models.IPAddressField('IP Address')
    datetime = models.DateTimeField(default=now)

    class Meta:
        ordering = ('user', 'datetime',)

    def __unicode__(self):
        return '%s @ %s' % (self.user, self.datetime)

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