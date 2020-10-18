from myapp import app

if __name__ == '__main__':
    app.run(
        host=app.config['SELF_SERVER'],
        port=app.config['SELF_SERVER_PORT'],
        threaded=True,
        debug=app.config['DEBUG']
    )
