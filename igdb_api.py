import os, json
from flask import Request, render_template, url_for
from requests import post
from igdb.wrapper import IGDBWrapper
from datetime import datetime
from gcp_vision_api import analyze_box_art


# Required keys for IGDB
IGDB_CLIENT_KEY = os.environ.get("IGDB_CLIENT_KEY")
IGDB_SECRET_KEY = os.environ.get("IGDB_SECRET_KEY")
IDGB_AUTH_TOKEN = ""

# produces the correct image for the html to display based on the response
# from the IGDB API.
def rating_img_producer(x: int) -> str:
    if x == 6:
        return url_for("static", filename="RP.svg")
    elif x == 7 or x == 8:
        return url_for("static", filename="E.svg")
    elif x == 9:
        return url_for("static", filename="E10plus.svg")
    elif x == 10:
        return url_for("static", filename="T.svg")
    elif x == 11:
        return url_for("static", filename="M.svg")
    elif x == 12:
        return url_for("static", filename="AO.svg")
    else:
        return url_for("static", filename="RP.svg")


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
    # As mentioned above, this is required to setup the IGDBWrapper
    IDGB_AUTH_TOKEN = get_igdb_auth_token()

    # Several options the user can select are passed in and retrieved
    game_name = req.form["game_name"]
    val_limit = req.form["limit"]
    wrapper: IGDBWrapper = IGDBWrapper(IGDB_CLIENT_KEY, IDGB_AUTH_TOKEN)
    
    # And here is *the* request. IGDB uses something called APIcalypse (APIc),
    # and both IGDB and APIc are quite stale. Docs for APIc are no longer
    # managed from the repo, and IGDB has endpoints that just don't return
    # information at all.
    games_raw = wrapper.api_request(
        "games",
        'search "'
        + game_name
        + """\";
        f id, name, first_release_date, aggregated_rating, platforms.name, age_ratings.category, 
        age_ratings.rating, cover.url;
        limit """
        + str(val_limit)
        + """; 
        where first_release_date != null & age_ratings != null;
        """,
    )

    # The response comes back as a string, need to turn it into proper json
    # formatting
    games = json.loads(games_raw)
    
    # Sort results by the release dates
    games = sorted(games, key=lambda x: x["first_release_date"])
    
    # Modify certain json properties in the now formatted and sorted games
    # and remove some that do not apply.
    for game in games:
        
        # Human readable date. This is one endpoint where certain requests were
        # received, but responses were never sent so had to do a workaround to
        # get the release date to be something actually readable.
        dt_object = datetime.utcfromtimestamp(game["first_release_date"])
        game["first_release_date"] = dt_object.strftime("%m/%d/%Y")
        
        # Filter out any ratings that are not ESRB
        game["age_ratings"] = list(
            filter(lambda rating: rating["category"] == 1, game["age_ratings"])
        )
        
        # Convert the rating to an int from a float
        if "aggregated_rating" in game:
            game["aggregated_rating"] = int(game["aggregated_rating"])
            
        # Modify the cover response to be usable
        if "cover" in game and len(game["cover"]) > 0:
            # Get the large cover art instead of a thumbnail
            game["cover"]["url"] = game["cover"]["url"].replace(
                "t_thumb", "t_cover_big_2x"
            )
            
            # Add a proper https header to it. Without this it starts simply
            # with //
            game["cover"]["url"] = "https:" + game["cover"]["url"]
            
            # Use Google Vision API to get some labels to use as alt text for
            # the cover art displayed on the site.
            game["cover"]["alt_text"] = json.dumps(
                analyze_box_art(game["cover"]["url"])
            )
            
            # Remove the weird additions of quotations at the start and end that
            # are always present with the response from the analyze_box_art
            game["cover"]["alt_text"] = game["cover"]["alt_text"][1:-1]

        # If the game has an age rating (which they all *should*), lets capture
        # the proper ratings image to be presented like E, T, M from the ESRB.
        # Images sourced directly from the ESRB as well.
        if "age_ratings" in game and len(game["age_ratings"]) > 0:
            game["age_ratings"][0]["rating"] = rating_img_producer(
                game["age_ratings"][0]["rating"]
            )

    # work is done, show us the money! (if the game exists)
    return render_template("index.html", games=games)
