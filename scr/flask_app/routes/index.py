from flask import Blueprint, render_template
from flask_login import login_required

index = Blueprint('index', __name__, template_folder='../templates')

@index.route("/")
@login_required
def home():
    return render_template("index.html")

