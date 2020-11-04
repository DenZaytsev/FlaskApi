from json import dumps

from flask import session, request, Response
from flask.views import MethodView
from pydantic import ValidationError

from serializers import CartSerializer
from service.cart import Cart


class BaseView(MethodView):
    ...


class CartView(BaseView):

    def get(self):

        cart = Cart(session)

        data = {
            'cartContent': cart.cart,
            'allItemQuantity': cart.get_quantity_of_all_items()
        }

        return Response(status=200, response=dumps(data), mimetype='application/json')


class CartAddView(BaseView):

    def post(self):
        """Принимает продукт и его кол-во, после чего добавляет товар в корзину."""

        cart = Cart(session)
        data = request.get_json()

        try:
            cart_item = CartSerializer(**data)
        except ValidationError as err:
            return Response(status=400, response=err.json(), mimetype='application/json')

        cart.add_item(cart_item.product, cart_item.quantity)

        return Response(status=201, response=dumps(cart.cart))

    def get(self):

        cart = Cart(session)

        data = {
            'cartContent': cart.cart,
            'allItemQuantity': cart.get_quantity_of_all_items()
        }
        return Response(status=200, response=dumps(data), mimetype='application/json')
