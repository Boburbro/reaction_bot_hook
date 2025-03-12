from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from scr.database.database import Database

bots = Blueprint("bots", __name__, template_folder = "../templates")


@bots.route("/")
def bot_list():
    try:
        bots_list = Database().fetch_bots()
        if isinstance(bots_list, list):
            return render_template("bots.html", bots = bots_list)
        return render_template("create-data-base.html")
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



@bots.route("/<int:id>", methods = ["DELETE"])
def delete_bot(id):
    try:
        db = Database()
        db.delete_bot(id)
        return  jsonify({"message": f"Bot {id} o'chirildi", "success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@bots.route("/", methods=["POST", "PUT"])
def add_or_update_bot():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Invalid data"}), 400

        db = Database()

        if request.method == "POST":
            if "title" not in data or "token" not in data:
                return jsonify({"success": False, "message": "title va token talab qilinadi"}), 400

            db.add_bot(
                title=data["title"],
                token=data["token"],
            )
            return jsonify({"success": True, "message": "Bot qo‘shildi"}), 201

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
