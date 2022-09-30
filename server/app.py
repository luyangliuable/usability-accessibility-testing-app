from flask_cors import CORS
# from tasks import celery
from flask import Flask
from routes import *
import os

print("test")

def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # register blueprints
    from reports.app import reports_blueprint

    # from controllers.file_controller import file_blueprint
    from routes.download_route import download_blueprint

    # Used as main page of flask ##############################################
    app.register_blueprint(main_blueprint)

    # Used as upload api for flask ################################################
    app.register_blueprint(upload_blueprint)
    app.register_blueprint(algorithm_task_blueprint)

    # Used as mongo document management api for flask #############################
    app.register_blueprint(algorithm_data_blueprint)

    # Used as download file from algorithm to frontend api  #######################
    app.register_blueprint(download_blueprint)

    # Used for getting algorithm status, notes, estimated remaining time and results
    app.register_blueprint(algorithm_status_blueprint)

    # Used for getting job status, notes, estimated remaining time and results
    app.register_blueprint(job_status_blueprint)

    app.register_blueprint(login_blueprint)
    app.register_blueprint(reports_blueprint)
    ###############################################################################
    #                              Enable debug mode                              #
    ###############################################################################
    app.config['DEBUG'] = True
    app.debug = True

    ###############################################################################
    #                                Upload folder                                #
    ###############################################################################
    app.config['UPLOAD_FOLDER'] = "./upload/files"

    ###############################################################################
    #                           Add cors to flask server                          #
    ###############################################################################
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app
