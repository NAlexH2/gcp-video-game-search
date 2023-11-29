import sys, getopt
import flask, os
from flask import render_template

app = flask.Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "-d" in args or "--Debug" in args:
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.config['DEBUG'] = True
        app.jinja_env.auto_reload = True
        
            
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
