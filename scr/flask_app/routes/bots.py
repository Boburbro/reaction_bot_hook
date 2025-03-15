from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from scr.database.database import Database
import sqlite3

bots = Blueprint("bots", __name__, template_folder = "../templates")


@bots.route("/")
@login_required
def bot_list():
    db = Database()
    
    # First check if the database is initialized
    if not db.is_initialized():
        return render_template("bots.html", bots=[], db_initialized=False, 
                              error_message="Database not initialized. Please initialize the database first.")
    
    try:
        bots_list = db.fetch_bots()
        
        # Check if the result is a list (successful query)
        if isinstance(bots_list, list):
            print(bots_list)
            return render_template("bots.html", bots=bots_list, db_initialized=True)
        # If it's not a list but also not an exception, it might be an error object
        else:
            error_str = str(bots_list)
            return render_template("bots.html", bots=[], db_initialized=False, 
                                  error_message=f"Database error: {error_str}")
            
    except Exception as e:
        error_str = str(e)
        return render_template("bots.html", bots=[], db_initialized=False, 
                              error_message=f"An error occurred: {error_str}")



@bots.route("/<int:id>", methods = ["DELETE"])
@login_required
def delete_bot(id):
    try:
        db = Database()
        # Get bot details before deletion for logging
        bot = db.get_bot_by_id(id)
        bot_title = bot['title'] if bot else f"ID: {id}"
        
        result = db.delete_bot(id)
        
        if result:
            # Log the activity
            db.add_activity_log(
                activity_type="BOT_DELETE",
                description=f"Bot '{bot_title}' was deleted",
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                username=current_user.username if current_user else None
            )
            
        return jsonify({"message": f"Bot {id} o'chirildi", "success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@bots.route("/", methods=["POST", "PUT"])
@login_required
def add_or_update_bot():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Invalid data"}), 400

        db = Database()

        if request.method == "POST":
            if "title" not in data or "token" not in data:
                return jsonify({"success": False, "message": "title va token talab qilinadi"}), 400

            result = db.add_bot(
                title=data["title"],
                token=data["token"],
            )
            
            if result:
                # Log the activity
                db.add_activity_log(
                    activity_type="BOT_ADD",
                    description=f"New bot '{data['title']}' was added",
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get('User-Agent'),
                    username=current_user.username if current_user else None
                )
                return jsonify({"success": True, "message": "Bot qo'shildi"}), 201
            else:
                return jsonify({"success": False, "message": f"Token already exists"}), 400

        elif request.method == "PUT":
            if "id" not in data or "title" not in data or "token" not in data:
                return jsonify({"success": False, "message": "id, title va token talab qilinadi"}), 400

            # Get original bot details for logging
            original_bot = db.get_bot_by_id(data["id"])
            
            updated = db.update_bot(
                bot_id=data["id"],
                title=data["title"],
                token=data["token"],
            )

            if updated:
                # Log the activity
                original_title = original_bot['title'] if original_bot else f"ID: {data['id']}"
                db.add_activity_log(
                    activity_type="BOT_UPDATE",
                    description=f"Bot '{original_title}' was updated to '{data['title']}'",
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get('User-Agent'),
                    username=current_user.username if current_user else None
                )
                return jsonify({"success": True, "message": "Bot yangilandi"}), 200
            else:
                return jsonify({"success": False, "message": "Bot topilmadi"}), 404

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
