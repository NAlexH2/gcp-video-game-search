import sys, os, json
from requests import post
from igdb.wrapper import IGDBWrapper
from datetime import datetime
from flask import Flask, request, render_template

app = Flask(__name__)

__IGDB_CLIENT_KEY = os.environ.get("IGDB_CLIENT_KEY")
__IGDB_SECRET_KEY = os.environ.get("IGDB_SECRET_KEY")
__IDGB_AUTH_TOKEN = ""


def get_igdb_auth_token():
    auth_post = post(
        "https://id.twitch.tv/oauth2/token?client_id="
        + __IGDB_CLIENT_KEY
        + "&client_secret="
        + __IGDB_SECRET_KEY
        + "&grant_type=client_credentials"
    )
    auth_data = json.loads(auth_post.text)
    return auth_data["access_token"]


def check_keys():
    if __IGDB_CLIENT_KEY == None:
        sys.stderr.write("\nMISSING IGDB CLIENT KEY!!!! UNABLE TO LAUNCH!\n\n")
        sys.exit(0)
    if __IGDB_SECRET_KEY == None:
        sys.stderr.write("\nNO IGDB API KEY!!!! UNABLE TO LAUNCH!\n\n")
        sys.exit(0)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/find_game", methods=["POST"])
def find_game():
    """
    Need to get access token every time a request is made here,
    then make the IGDBWrapper.
     - do this request
        - https://id.twitch.tv/oauth2/token?client_id=123&client_secret=123&grant_type=client_credentials
        (using proper creds)
        - get auth token
        - store in a var as it's a json obj
        - make wrapper below.
        - do fun stuff! :)
    wrapper = IGDBWrapper(__IGDB_CLIENT_KEY, __IGDB_AUTH_KEY)
    """
    game_name = str(request.json["game_name"])

    __IDGB_AUTH_TOKEN = get_igdb_auth_token()
    wrapper: IGDBWrapper = IGDBWrapper(__IGDB_CLIENT_KEY, __IDGB_AUTH_TOKEN)
    games_raw = wrapper.api_request(
        "games",
        "search \""
        + game_name
        + """\";
        f id, name, first_release_date; 
        limit 5; 
        where first_release_date != null;
        """,
    )

    games = json.loads(games_raw)
    games = sorted(games, key=lambda x: x["first_release_date"])
    for game in games:
        dt_object = datetime.utcfromtimestamp(game["first_release_date"])
        game["first_release_date"] = dt_object.strftime("%m/%d/%Y")
    return games, 200


if __name__ == "__main__":
    check_keys()
    args = sys.argv[1:]
    if "-d" in args or "--Debug" in args:
        app.config["TEMPLATES_AUTO_RELOAD"] = True
        app.config["DEBUG"] = True
        app.jinja_env.auto_reload = True

    print("\n", __IGDB_CLIENT_KEY, ": IGDB CLIENT Key\n")
    print("\n", __IGDB_SECRET_KEY, ": IGDB API Key\n")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
