from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required
from scr.database.database import Database

create_data_base = Blueprint("create_data_base", __name__, template_folder="../templates")

@create_data_base.route("/")
@login_required
def init_db():
    try:
        Database().init_database()
        flash("Database initialized successfully!", "success")
    except Exception as e:
        flash(f"Error initializing database: {str(e)}", "danger")
    
    return redirect(url_for("bots.bot_list"))
