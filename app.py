import sys
from flask import Flask, request, render_template
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/find_game", methods=["POST"])
def find_game():
    game_name = request.json["game_name"]
    print("Testing the 'REST' API ", game_name)
    return "ok", 200


if __name__ == "__main__":
    args = sys.argv[1:]
    if "-d" in args or "--Debug" in args:
        app.config["TEMPLATES_AUTO_RELOAD"] = True
        app.config["DEBUG"] = True
        app.jinja_env.auto_reload = True

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
