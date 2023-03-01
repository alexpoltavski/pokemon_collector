from flask import Flask, render_template
from appdata import db,Pokeball

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    hostname="localhost",
    databasename="root$pokedex",
)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG"] = True
app.secret_key = 'This is really unique and secret'
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

@app.route("/")
def show_collection():
    render_template("pokedex.html",pokebals=Pokeball.query.all())
  