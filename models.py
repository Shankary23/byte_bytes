class FoodItem:
    def __init__(self, name, price, category, popularity_rating):
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating


class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def filter_by_category(self, category):
        return [item for item in self.items if item.category == category]


class Order:
    def __init__(self, customer, items=None):
        self.customer = customer
        self.items = items if items is not None else []

    def compute_total(self):
        return sum(item.price for item in self.items)


class Customer:
    def __init__(self, name):
        self.name = name
        self.purchase_history = []

    def verify_user(self):
        return len(self.purchase_history) > 0

