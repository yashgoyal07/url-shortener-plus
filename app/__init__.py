from flask import Flask


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.secret_key = b'\xce\xdd(B\xdd\xf1\x19\x04\x8c\xf0 BV\x93e\x8c'

    from app.views.main import main_blueprint
    app.register_blueprint(main_blueprint)

    return app