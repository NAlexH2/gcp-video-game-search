
from flask.views import MethodView
from flask import render_template, request
from igdb_api import find_game

class Index(MethodView):
    
    # A sneaky way to display a default version OR the response the user
    # submitted to the app to produce - the on in the "if" statement.
    def post(self):
        if request.method == "POST":
            return find_game(request)
        return render_template("index.html")

    # Required to have *something*, but we never use this. Flask gets very angry
    # if we don't have both for index.
    def get(self):
        return render_template("index.html")