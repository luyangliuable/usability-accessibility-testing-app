# # register blueprints
# from routes.main import main_blueprint
# from routes.algorithm_status_api import algorithm_status_blueprint
# from routes.job_status_api import job_status_blueprint
from routes.upload_api import upload_blueprint
# from routes.algorithm_data_api import algorithm_data_blueprint
from routes.user import user_blueprint
# from routes.algorithm_task_api import algorithm_task_blueprint

from routes.results import results_blueprint
from routes.signal import signals_blueprint
from routes.status import status_blueprint
