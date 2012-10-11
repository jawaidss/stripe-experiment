class Cart:
    def __init__(self):
        self.items = []
        self.total = 0

    def add(self, request, item):
        if item not in self.items:
            self.items.append(item)
            self.items.sort(key=lambda item: item.name)
            self.total += item.price

            request.session.modified = True

            return True

        return False

    def remove(self, request, id):
        for item in self.items:
            if item.id == id:
                self.items.remove(item)
                self.total -= item.price

                request.session.modified = True

                return item

        return None

class Item:
    def __init__(self, name, description, price, **kwargs):
        self.id = int(id(self))
        self.name = name
        self.description = description
        self.price = price
        self.kwargs = kwargs

def get_or_create_cart(request):
    return request.session.setdefault('shopping-cart', Cart())