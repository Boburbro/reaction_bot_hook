from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("splash.html")


@app.route("/index")
def index():
    users = [
        {"id": 1, "title": "User1", "subtitle": "Subtitle1"},
        {"id": 2, "title": "User2", "subtitle": "Subtitle2"},
        {"id": 3, "title": "User3", "subtitle": "Subtitle3"},
        {"id": 4, "title": "User4", "subtitle": "Subtitle4"},
    ]
    return render_template("index.html", users=users)


@app.route("/add-user", methods=["POST"])
def add_user():
    print(request.values)
    return "done"


if __name__ == "__main":
    app.run(debug=True)
