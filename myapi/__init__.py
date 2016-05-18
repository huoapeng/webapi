from flask.ext.sqlalchemy import SQLAlchemy
from json_app import make_json_app

db = SQLAlchemy()
app = make_json_app(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def create_app(config_name):
    app.config.from_object(config_name)
    #app.config.from_envvar('APP_CONFIG_FILE')

    db.init_app(app)

    from router import api_bp
    # api.init_app(app)

    app.register_blueprint(api_bp, url_prefix='/api/v1.0')
    return app

