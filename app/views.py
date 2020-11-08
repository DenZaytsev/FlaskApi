import traceback
from json import dumps
from typing import Dict

from flask import session, request, Response
from flask.views import MethodView
from pydantic import ValidationError

from serializers import CartSerializer
from service.cart import Cart


class BaseView(MethodView):

    def dispatch_request(self, *args, **kwargs):
        try:
            response = super().dispatch_request(*args, **kwargs)
        except Exception as e:
            return self._response(self.get_error_data(e), status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        return Response(
            response=dumps(data),
            status=status,
            mimetype='application/json'
        )

    @staticmethod
    def get_error_data(exception) -> Dict[str, str]:
        data = {
            'errorMessage': str(exception),
            'errorClass': str(exception.__class__),
            'errorTrace': str(traceback.extract_tb(exception.__traceback__))
        }
        return data


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


