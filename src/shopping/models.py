from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.timezone import now

class Card(models.Model):
    user = models.ForeignKey(User)
    stripe_customer_id = models.CharField('Stripe customer ID', max_length=100, unique=True)
    is_default = models.BooleanField()

    class Meta:
        ordering = ('user', '-is_default', 'stripe_customer_id',)

    def __unicode__(self):
        return '%s (%s)%s' % (self.user, self.stripe_customer_id, self.is_default and ' - Default' or '')

    def save(self, *args, **kwargs):
        if self.is_default: # Saving default card
            self.user.card_set.filter(is_default=True).update(is_default=False)
        elif not self.user.card_set.filter(is_default=True) or \
             self.id is not None and self.user.card_set.filter(id=self.id, is_default=True):
            # Saving first card or
            # Saving with no default card
            self.is_default = True

        super(Card, self).save(*args, **kwargs)

@receiver(post_delete, sender=Card)
def post_delete_card_handler(sender, instance, using, **kwargs):
    if instance.is_default: # Deleting default card
        cards = instance.user.card_set.all()

        if cards:
            card = cards[0]
            card.is_default = True
            card.save()

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
    subclass = models.CharField(max_length=100, editable=False)
    # Would break if the name of a subclass is longer than 100 characters

    class Meta:
        ordering = ('order', 'name',)

    def __unicode__(self):
        return '%s - %s' % (self.order, self.name)

    def save(self, *args, **kwargs):
        if not self.subclass:
            # Depends on self._meta
            self.subclass = self._meta.module_name

        super(Item, self).save(*args, **kwargs)

    def get_subclass(self):
        if self.subclass and hasattr(self, self.subclass):
            return getattr(self, self.subclass)

        return self

    def get_description(self):
        return self.description