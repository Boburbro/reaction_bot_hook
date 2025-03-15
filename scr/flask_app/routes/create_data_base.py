from flask import Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from scr.database.database import Database

create_data_base = Blueprint("create_data_base", __name__, template_folder="../templates")

@create_data_base.route("/")
@login_required
def init_db():
    try:
        db = Database()
        db.init_database()
        
        # Log the database initialization
        db.add_activity_log(
            activity_type="DATABASE_INIT",
            description="Database was initialized",
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            username=current_user.username if current_user else None
        )
        
        flash("Database initialized successfully!", "success")
    except Exception as e:
        flash(f"Error initializing database: {str(e)}", "danger")
    
    return redirect(url_for("bots.bot_list"))
