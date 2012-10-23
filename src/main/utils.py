from shopping.utils import Item
from models import Shirt as ShirtModel, Fruit as FruitModel

class Shirt(Item):
    model = ShirtModel

    def __init__(self, name, description, price, size):
        super(Shirt, self).__init__(name, description, price)
        self.size = size

    def get_description(self):
        description = super(Shirt, self).get_description()
        size = [size for _, size in ShirtModel.SIZE_CHOICES if _ == self.size][0]
        return '%s Size: %s' % (description, size)

    def to_model(self, order):
        shirt = super(Shirt, self).to_model(order)
        shirt.size = self.size
        return shirt

class Fruit(Item):
    model = FruitModel