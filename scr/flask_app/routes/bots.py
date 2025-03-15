from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required
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
        db.delete_bot(id)
        return  jsonify({"message": f"Bot {id} o'chirildi", "success": True}), 200
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

            id_added = db.add_bot(
                title=data["title"],
                token=data["token"],
            )
            if id_added:
                return jsonify({"success": True, "message": "Bot qo'shildi"}), 201
            else:
                return jsonify({"success": False, "message": f"Token already exists"}), 400

        elif request.method == "PUT":
            if "id" not in data or "title" not in data or "token" not in data:
                return jsonify({"success": False, "message": "id, title va token talab qilinadi"}), 400

            updated = db.update_bot(
                bot_id=data["id"],
                title=data["title"],
                token=data["token"],
            )

            if updated:
                return jsonify({"success": True, "message": "Bot yangilandi"}), 200
            else:
                return jsonify({"success": False, "message": "Bot topilmadi"}), 404

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
