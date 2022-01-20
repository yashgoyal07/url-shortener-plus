#This bluepint will deal with all functionality 

from re import template
from flask import Blueprint

main_blueprint = Blueprint('main', __name__, template_folder='templates')

from . import views