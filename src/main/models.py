from django.db import models

from shopping.models import Item

class Shirt(Item):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    SIZE_CHOICES = (
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
    )
    size = models.IntegerField(choices=SIZE_CHOICES)

class Fruit(Item):
    pass