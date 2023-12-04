
from flask.views import MethodView
from flask import render_template, request
from igdb_api import find_game

class Index(MethodView):
    def post(self):
        if request.method == "POST":
            return find_game(request)
        return render_template("index.html")

    def get(self):
        return render_template("index.html")