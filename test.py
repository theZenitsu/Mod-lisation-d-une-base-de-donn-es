from sqlalchemy import create_engine, func, Float

from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, Ville, Annonce, Equipement, AnnonceEquipement
import os

# Database URL (adjust as needed)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:karzal@localhost:5432/immobilier_db")

# Set up the engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_annonces_by_city(city_name):
    """Récupérer toutes les annonces pour une ville spécifique"""
    city = session.query(Ville).filter_by(name=city_name).first()
    if city:
        annonces = session.query(Annonce).filter(Annonce.ville == city).all()
        for annonce in annonces:
            print(f"{annonce.title}, {annonce.price}")
    else:
        print(f"Aucune ville trouvée avec le nom {city_name}")

def filter_annonces_by_rooms_and_baths(nb_rooms_min, nb_baths_min):
    """Filtrer les annonces selon le nombre de pièces et de salles de bain"""
    annonces = session.query(Annonce).filter(
        Annonce.nb_rooms >= nb_rooms_min,
        Annonce.nb_baths >= nb_baths_min
    ).all()
    for annonce in annonces:
        print(f"{annonce.title}, {annonce.price}")

def filter_annonces_by_price(price_min, price_max):
    """Filtrer les annonces par plage de prix"""
    annonces = session.query(Annonce).filter(
        Annonce.price.cast(Float) >= price_min,
        Annonce.price.cast(Float) <= price_max
    ).all()
    for annonce in annonces:
        print(f"{annonce.title}, {annonce.price}")

def get_annonces_with_equipement(equipement_name):
    """Obtenir les annonces avec un équipement spécifique"""
    equipement = session.query(Equipement).filter_by(name=equipement_name).first()
    if equipement:
        annonces = session.query(Annonce).join(AnnonceEquipement).join(Equipement).filter(
            AnnonceEquipement.equipement_id == equipement.id
        ).all()
        for annonce in annonces:
            print(f"{annonce.title}, {annonce.price}")
    else:
        print(f"Aucun équipement trouvé avec le nom {equipement_name}")

def count_annonces_by_city():
    """Compter le nombre d'annonces par ville"""
    result = session.query(Ville.name, func.count(Annonce.id)).join(Annonce).group_by(Ville.name).all()
    for city, count in result:
        print(f"{city}: {count} annonces")

def find_annonces_by_surface(min_surface, max_surface):
    """Trouver les annonces selon la surface"""
    annonces = session.query(Annonce).filter(
        Annonce.surface_area >= min_surface,
        Annonce.surface_area <= max_surface
    ).all()
    for annonce in annonces:
        print(f"{annonce.title}, {annonce.surface_area} m²")

def get_annonces_by_date_range(date_start, date_end):
    """Récupérer les annonces par date de publication"""
    annonces = session.query(Annonce).filter(
        Annonce.datetime >= date_start,
        Annonce.datetime <= date_end
    ).all()
    for annonce in annonces:
        print(f"{annonce.title}, {annonce.datetime}")

if __name__ == "__main__":
    # Example queries
    print("1. Annonces à Paris:")
    get_annonces_by_city('Paris')
    print("\n")

    print("2. Annonces avec au moins 3 pièces et 2 salles de bain:")
    filter_annonces_by_rooms_and_baths(3, 2)
    print("\n")

    print("3. Annonces entre 250000 et 400000 euros:")
    filter_annonces_by_price(250000, 400000)
    print("\n")

    print("4. Annonces avec l'équipement 'Balcon':")
    get_annonces_with_equipement('Balcon')
    print("\n")

    print("5. Nombre d'annonces par ville:")
    count_annonces_by_city()
    print("\n")

    print("6. Annonces avec une surface entre 60 et 100 m²:")
    find_annonces_by_surface(60, 100)
    print("\n")

    print("7. Annonces publiées entre 2024-05-01 et 2024-06-30:")
    get_annonces_by_date_range(datetime(2024, 5, 1), datetime(2024, 6, 30))

    # Close the session
    session.close()
