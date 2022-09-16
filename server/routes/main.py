from collections import Counter
from flask import render_template, Blueprint, jsonify, request, Response, send_file, redirect, url_for
import os

main_blueprint = Blueprint("main", __name__) #, static_folder='static')

# ###############################################################################
# #                                   Mongodb                                   #
# ###############################################################################


@main_blueprint.route('/', methods=["GET", "POST"])
def display_flask_working_state():
    return "Flask back-end is online."
