from json import dumps

from flask import session, request, Response
from flask_classy import FlaskView, route
from pydantic import ValidationError

from serializers import CartSerializer
from service.cart import Cart


class CartView(FlaskView):

    def get(self):
        cart = Cart(session)
        return dumps({
            'cartContent': cart.cart,
            'allItemQuantity': cart.get_quantity_of_all_items()
        })


class CartAddView(FlaskView):

    def post(self):
        """Принимает продукт и его кол-во, после чего добавляет товар в корзину."""

        cart = Cart(session)
        data = request.form.to_dict()

        try:
            cart_item = CartSerializer(**data)
        except ValidationError as err:
            return Response(status=400, response=err.json())

        cart.add_item(cart_item.product, cart_item.quantity)

        return Response(status=201, response=dumps(cart.cart))

    def get(self):
        cart = Cart(session)
        return dumps({
            'cartContent': cart.cart,
            'allItemQuantity': cart.get_quantity_of_all_items()
        })
