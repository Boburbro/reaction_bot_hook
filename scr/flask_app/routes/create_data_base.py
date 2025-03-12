from flask import Blueprint, redirect, url_for
from scr.database.database import Database

create_data_base = Blueprint("create_data_base", __name__, template_folder="../templates")

@create_data_base.route("/")
def init_db():
    Database().init_database()
    return redirect(url_for("index.home"))
