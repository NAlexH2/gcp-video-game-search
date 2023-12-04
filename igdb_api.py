import os, json
from flask import Request, render_template, url_for
from requests import post
from igdb.wrapper import IGDBWrapper
from datetime import datetime

IGDB_CLIENT_KEY = os.environ.get("IGDB_CLIENT_KEY")
IGDB_SECRET_KEY = os.environ.get("IGDB_SECRET_KEY")
IDGB_AUTH_TOKEN = ""


def rating_img_producer(x: int) -> str:
    if x == 6:
        return url_for('static',filename="RP.svg")
    elif x == 7 or x == 8:
        return url_for('static',filename="E.svg")
    elif x == 9:
        return url_for('static',filename="E10plus.svg")
    elif x == 10:
        return url_for('static',filename="T.svg")
    elif x == 11:
        return url_for('static',filename="M.svg")
    elif x == 12:
        return url_for('static',filename="AO.svg")
    else:
        return url_for('static',filename="RP.svg")

#  IGDB (internet games database) requires an authorization token instead of
#  using the secret client. While each auth token has a time limit, I'm just
#  allowing each request to get its own token each request.
#
#  In future versions, I'd probably keep track of the token and check if it's
#  become stale or not - if it was coming close to be stale, I'd issue another
#  one, otherwise just use it.
def get_igdb_auth_token():
    auth_post = post(
        "https://id.twitch.tv/oauth2/token?client_id="
        + IGDB_CLIENT_KEY
        + "&client_secret="
        + IGDB_SECRET_KEY
        + "&grant_type=client_credentials"
    )
    auth_data = json.loads(auth_post.text)
    return auth_data["access_token"]


# Route to find the game the user is searching for, return several results.
def find_game(req: Request):
    IDGB_AUTH_TOKEN = get_igdb_auth_token()
    game_name = req.form["game_name"]
    wrapper: IGDBWrapper = IGDBWrapper(IGDB_CLIENT_KEY, IDGB_AUTH_TOKEN)
    games_raw = wrapper.api_request(
        "games",
        'search "'
        + game_name
        + """\";
        f id, name, first_release_date, aggregated_rating, platforms.name, age_ratings.category, 
        age_ratings.rating, url, cover.url;
        limit 20; 
        where first_release_date != null & age_ratings != null;
        """,
    )

    games = json.loads(games_raw)
    games = sorted(games, key=lambda x: x["first_release_date"])

    for game in games:
        dt_object = datetime.utcfromtimestamp(game["first_release_date"])
        game["first_release_date"] = dt_object.strftime("%m/%d/%Y")
        game["age_ratings"] = list(
            filter(lambda rating: rating["category"] == 1, game["age_ratings"])
        )
        if "aggregated_rating" in game:
            game["aggregated_rating"] = int(game["aggregated_rating"])
        if "cover" in game and len(game["cover"]) > 0:
            game["cover"]["url"] = game["cover"]["url"].replace("t_thumb", "t_cover_big_2x")
        if "age_ratings" in game and len(game["age_ratings"]) > 0:
            game["age_ratings"][0]["rating"] = rating_img_producer(game["age_ratings"][0]["rating"])

    return render_template("index.html", games=games)