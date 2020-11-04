from myapp import app
from views import CartAddView, CartView

app.add_url_rule('/api/cart/', view_func=CartView.as_view('show_cart'))
app.add_url_rule('/api/cart/add-to-cart/', view_func=CartAddView.as_view('add_to_cart'))



if __name__ == '__main__':
    app.run(
        host=app.config['SELF_SERVER'],
        port=app.config['SELF_SERVER_PORT'],
        threaded=True,
        debug=app.config['DEBUG']
    )
