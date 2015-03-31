import os
from glob import glob
from unidecode import unidecode
from datetime import datetime,date

from ignored import problems2m
from elly import *

cls3m = Cls.query.filter_by(classname="3m").all()[0]

lista3m = [
    ["Apró", "Alexandra"],
    ["Barát", "Krisztina"],
    ["Berec", "Judit"],
    ["Börcsök", "Norbert"],
    ["Boros Gyevi", "Ádám"],
    ["Borsos", "Teodóra"],
    ["Dobó", "Márk"],
    ["Horti", "Katalin"],
    ["Juhász", "Bence"],
    ["Kálmán", "Szilárd"],
    ["Kovács", "Attila"],
    ["Mucsi", "Edina"],
    ["Orosz", "Kinga"],
    ["Szkocsovszki", "Zsolt"],
    ["Terhes", "Balázs"],
    ["Tóth", "Bálint"]]

lista=map(lambda x : [unidecode(x[0].replace(" ","")).lower()+"3m",x[0],x[1],'pass',cls3m],lista3m)


for s in lista:
    user = User(*s)
    db.session.add(user)

db.session.commit()
