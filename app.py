from scr.flask_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)














# from flask import Flask, render_template, request, url_for, redirect, jsonify
#
#
# app = Flask(__name__)
#
#
# @app.route("/")
# def hello_world():
#     return render_template("splash.html")
#
#
#
#
#
# # @app.route("/add-user", methods=["GET"])
# # def add_user():
# #     title = request.args.get("title")
# #     subtitle = request.args.get("subtitle")
# #
# #     users.append(
# #         {
# #             "id": 0,
# #             "title": title,
# #             "subtitle": subtitle,
# #         }
# #     )
# #
# #     return redirect(url_for("index"))
# #
# #
# @app.route("/delete-user/<int:id>", methods=["DELETE"])
# def delete_user(id):
#
#     return jsonify({"message": f"Foydalanuvchi {id} o'chirildi"}), 200
#
#
# if __name__ == "__main":
#     app.run(debug=True, port=8888)
