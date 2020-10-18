

class Cart:
    """Класс предназначенный для хранение корзины товаров в сессии."""

    def __init__(self, session):
        self.session = session
        try:
            self.cart = session['cart']
        except KeyError as e:
            self.cart = session['cart'] = dict()

    def _save(self):
        """Сохраняет изменения в сессию"""
        self.session['cart'] = self.cart
        self.session.modified = True

    def add_item(self, product: str, quantity: int = 1):
        """Добавить продукт в корзину или обновить его количество."""

        try:
            self.cart[product] += quantity
        except KeyError as e:
            self.cart[product] = quantity

        self._save()
