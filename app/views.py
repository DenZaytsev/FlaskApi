from json import dumps

from flask import session, request, Response
from flask_classy import FlaskView, route
from pydantic import ValidationError

from service.cart import Cart
from serializers import CartSerializer


class CartView(FlaskView):

    @route('/')
    def cart(self):
        cart = Cart(session)
        return dumps(cart.cart)

    @route('add-to-cart/')
    def add_to_cart(self):
        cart = Cart(session)
        data = request.form.to_dict()

        try:
            cart_item = CartSerializer(**data)
        except ValidationError as err:
            return Response(status=404, response=err.json())

        cart.add_item(cart_item.product, cart_item.quantity)

        return Response(status=200, response=dumps(cart.cart))
