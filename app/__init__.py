from flask import Flask, Response

class MyResponse(Response):
     default_mimetype = 'application/json'

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.response_class = MyResponse

    from app.models import db
    db.init_app(app)

    # Blueprints
    from app.views import nodes
    app.register_blueprint(nodes, url_prefix='/api/v1')

    return app
