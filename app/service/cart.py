from dataclasses import dataclass, asdict


class Cart:
    """Класс предназначенный для хранение корзины товаров в сессии."""

    def __init__(self, session):
        self.session = session
        try:
            self.cart = session['cart']
        except KeyError:
            self.cart = session['cart'] = dict()

    def _save(self):
        """Сохраняет изменения в сессию"""
        self.session['cart'] = self.cart
        self.session.modified = True

    def add_item(self, product: str, quantity: int = 1):
        """Добавить продукт в корзину или обновить его количество."""

        try:
            self.cart[product] += quantity
        except KeyError:
            self.cart[product] = quantity

        self._save()

    def get_quantity_of_all_items(self):
        """Возвращает кол-во всех вещей в корзине."""
        return sum(quantity for quantity in self.cart.values())

    def __str__(self):
        return self.cart


@dataclass
class Item:
    ...