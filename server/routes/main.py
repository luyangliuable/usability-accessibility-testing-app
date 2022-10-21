import flask as f

main_blueprint = f.Blueprint("main", __name__) #, static_folder='static')

@main_blueprint.route('/', methods=["GET", "POST"])
def check_health():
    return "Flask back-end is online."
