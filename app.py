import sys, os
from flask import Flask
from index import Index
from igdb_api import IGDB_CLIENT_KEY, IGDB_SECRET_KEY, IDGB_AUTH_TOKEN

app = Flask(__name__)
app.add_url_rule("/", view_func=Index.as_view("index"), methods=["POST", "GET"])

def check_keys():
    if IGDB_CLIENT_KEY == None:
        sys.stderr.write("\nMISSING IGDB CLIENT KEY!!!! UNABLE TO LAUNCH!\n\n")
        sys.exit(0)
    if IGDB_SECRET_KEY == None:
        sys.stderr.write("\nNO IGDB API KEY!!!! UNABLE TO LAUNCH!\n\n")
        sys.exit(0)


# Main
if __name__ == "__main__":
    check_keys()
    args = sys.argv[1:]
    if "-d" in args or "--Debug" in args:
        app.config["TEMPLATES_AUTO_RELOAD"] = True
        app.config["DEBUG"] = True
        app.jinja_env.auto_reload = True

    print("\n", IGDB_CLIENT_KEY, ": IGDB CLIENT Key\n")
    print("\n", IGDB_SECRET_KEY, ": IGDB API Key\n")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
