import pandas as pd
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from models import Ville, Annonce, Equipement, AnnonceEquipement

data = pd.read_csv(r'appartemetn.csv')

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:karzal@localhost:5432/immobilier_db")



engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

for i, ligne in data.iterrows():

    city = session.query(Ville).filter_by(name=ligne['city_name']).first()
    if not city:
        city = Ville(name=ligne['city_name'])
        session.add(city)
        session.commit()

    annonce = Annonce(
        title=ligne['title'],
        price=ligne['price'],
        datetime=datetime.strptime(ligne['datetime'], "%Y-%m-%d %H:%M:%S"),
        nb_rooms=ligne['nb_rooms'],
        nb_baths=ligne['nb_baths'],
        surface_area=ligne['surface_area'],
        link=ligne['link'],
        city_id=city.id
    )
    session.add(annonce)
    session.commit()

    equipements = ligne['equipements'].split("/")

    for equipe_name in equipements:
        equip = session.query(Equipement).filter_by(name=equipe_name.strip()).first()
        if not equip:
            equip = Equipement(name=equipe_name.strip())
            session.add(equip)
            session.commit()

        annonce_equipement = AnnonceEquipement(
            annonce_id=annonce.id,
            equipement_id=equip.id
        )
        session.add(annonce_equipement)

        session.commit()

session.close()




