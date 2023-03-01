from appdata import db,Ptype,Power,Pokemon,Exp,Pokeball,Loc,Loc_av

filename='poks.csv'
lines = open(filename).read().splitlines()

Ptype.__table__.create(db.session.bind, checkfirst=False)


def add_poks(locs):
    secpocs=[]
    for j in locs:
        for i in lines:secpocs.append(add_pokemon(i,j))
    db.session.commit()
    epocs=[]
    for i in secpocs:
        if (i!='')and(i!='EP'):
            epocs.append(i)
    secpocs=[]
    for j in epocs:
        for i in lines:
            secpocs.append(add_pokemon(i,j,0,5))
    db.session.commit()
    epocs=[]
    for i in secpocs:
        if (i!='')and(i!='EP') :
            epocs.append(i)
    secpocs=[]
    for j in epocs:
        for i in lines:
            secpocs.append(add_pokemon(i,j,0,10))
    db.session.commit()
    poks=Pokemon.query.all()
    poks=poks[175:]
    for i in poks:
        if i.evo != 'EP':
            for j in poks:
                if i.evo==j.name:
                    j.evofrom=i.name
    db.session.commit()

def add_pokemon(string, what,fil=4,mnl=0):
    data=string.split(',')
    if len(data)>5:
        if data[fil]==what:
            n=data[6].find('http')
            imurl=data[6][n:]
            n=imurl.find('""')
            imurl=imurl[:n]
            if data[3]=='':
                data[3]='EP'
            if fil==4:
                evfr="PP"
                org=what
            else:
                evfr=data[0]
                org=''
            db.session.add(Pokemon(name=data[0],origin=org, image=imurl, evo=data[3], evofrom=evfr, minlvl=mnl))
            return data[3]
    return ''
def link_power(string):
    data=string.split(',')
    if (len(data)>5) and (data[0]!='') and (data[1]!=''):
        pok=Pokemon.query.filter_by(name=data[0]).first()
        pows=[Ptype.query.filter_by(ptype=data[1]).first(),Ptype.query.filter_by(ptype=data[2]).first()]
        if not ((pok is None) or (pows[0] is None)):
            db.session.add(Power(pokemon_id=pok.id, type_id=pows[0].id))
            if not (pows[1] is None):
                db.session.add(Power(pokemon_id=pok.id, type_id=pows[1].id))
def add_pokebals(massiv):
    n=0
    stat='Актив'
    for i in massiv:
        n+=1
        if n>6:stat='Доступен'
        pok=Pokemon.query.filter_by(name=i[1]).first()
        if not pok is None:
            if pok.evo=='EP':stat='Эволют'
            exp=Exp.query.filter_by(points=i[2]).first()
            if not exp is None:
                if exp.level>14:stat='Прокачан'
                db.session.add(Pokeball(pokemon_id=pok.id,exp_points=exp.id,status=stat))
    db.session.commit()

def fix_status():
    pokebs=Pokeball.query.all()
    n=0
    for i in pokebs:
        n+=1
        stat='Доступен'
        if i.pokemon.evo=='EP':stat='Эволют'
        if i.exp.level>14:stat='Прокачан'
        if n<7:stat='Актив'
        i.status=stat
        db.session.commit()
def add_locs(mass):
    for i in mass:
        tp=Ptype.query.filter_by(ptype=i[0]).first()
        if not tp is None:
            for j in i[1]:
                lc=Loc.query.filter_by(loc_name=j).first()
                if not lc is None:
                    db.session.add(Loc_av(loc_id=lc.id,ptype_id=tp.id,cond=''))