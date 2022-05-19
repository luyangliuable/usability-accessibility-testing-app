import os
from flask import Flask
from tasks import celery


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # register blueprints
    from main.views import main_blueprint
    from upload.app import upload_blueprint
    from redis_file_manager.app import redis_file_manager_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(upload_blueprint)
    app.register_blueprint(redis_file_manager_blueprint)
    app.debug = True

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    app.debug = True

    return app
