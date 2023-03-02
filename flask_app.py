from flask import Flask, render_template
from appdata import db,Pokeball
import configparser

CONFIG_PATH = "server.config"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    hostname = config.get("Database", "hostname"),
    databasename = config.get("Database", "databasename"),
    username = config.get("Database", "username"),
    password = config.get("Database", "password"),
)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG"] = True
app.secret_key = 'This is really unique and secret'
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

@app.route("/")
def show_collection():
    return render_template("pokedex.html",pokebals=Pokeball.query.all())


 