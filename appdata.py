from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template,url_for,  redirect

db = SQLAlchemy()

class Ptype(db.Model):

    __tablename__ = "types"
    id = db.Column(db.Integer, primary_key=True)
    ptype = db.Column(db.String(32))
    image = db.Column(db.String(256))
    exemplars = db.relationship('Power',back_populates='type')
    locs = db.relationship("Loc_av",back_populates="type")


class Coach(db.Model):

    __tablename__ = "coaches"

    id = db.Column(db.Integer, primary_key=True)
    coach = db.Column(db.String(32))
    entry_url = db.Column(db.String(256))
    master = db.Column(db.String(32)) #curator?
    pokemons = db.relationship("Pokeball", back_populates="owner")
    user = db.relationship("User", back_populates="coach")

class User(db.Model):
    __tablename__ = "cusers"

    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'))
    email = db.Column(db.String(256))
    password = db.Column(db.String(256)) #that's hash! not real password
    coach = db.relationship("Coach", back_populates="user")

class Exp(db.Model):

    __tablename__ = "exp"

    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer)
    level = db.Column(db.Integer)
    group = db.Column(db.Integer)
    exemplars = db.relationship("Pokeball", back_populates="exp")

class Pokemon(db.Model):

    __tablename__ = "pokemons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    origin = db.Column(db.String(32))
    image = db.Column(db.String(256))
    evo = db.Column(db.String(32))
    evofrom = db.Column(db.String(32))
    minlvl = db.Column(db.Integer)
    condition = db.Column(db.String(256))
    exemplars = db.relationship("Pokeball",back_populates="pokemon")
    types = db.relationship('Power', back_populates='pokemon')

    def locat(self,n=1):
        res=[]
        if n==1:
            origin='Карта №1'
        else: origin='Карта №2'
        for i in self.types:
            for j in i.type.locs:
                if j.loc.loc_type==origin:
                    res.append(j.loc.loc_name)
        result=set(res)
        return result

class Power(db.Model):

    __tablename__ = "powers"

    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemons.id'))
    type_id = db.Column(db.Integer,db.ForeignKey('types.id'))
    pokemon = db.relationship("Pokemon",back_populates="types")
    type = db.relationship("Ptype",back_populates="exemplars")

class Pokeball(db.Model):

    __tablename__ = "pokedex"

    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.ForeignKey('coaches.id'))
    pokemon_id = db.Column(db.ForeignKey('pokemons.id'))
    exp_points = db.Column(db.ForeignKey('exp.id'))
    status = db.Column(db.String(32))
    exp = db.relationship("Exp", back_populates="exemplars")
    owner = db.relationship("Coach", back_populates="pokemons")
    pokemon = db.relationship("Pokemon", back_populates="exemplars")


class Loc(db.Model):

    __tablename__ = "locs"

    id = db.Column(db.Integer, primary_key=True)
    loc_name = db.Column(db.String(32))
    loc_type = db.Column(db.String(32))
    types = db.relationship("Loc_av",back_populates="loc")

class Loc_av(db.Model):

    __tablename__ = "locavs"

    id = db.Column(db.Integer, primary_key=True)
    loc_id = db.Column(db.ForeignKey('locs.id'))
    ptype_id = db.Column(db.ForeignKey('types.id'))
    cond = db.Column(db.String(32))
    type = db.relationship("Ptype",back_populates="locs")
    loc = db.relationship("Loc",back_populates="types")