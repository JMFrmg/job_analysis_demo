import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Float, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database


engine = create_engine('postgresql://admin:password@postgres_container_bis/job_market')

if not database_exists(engine.url):
    create_database(engine.url)

df = pd.read_csv("data/france_travail_tech.csv")

print(df.shape)
print(df.head())
print(df.columns)

Base = declarative_base()

class JobOffer(Base):
    __tablename__ = "job_offers_tech"
    id = Column(Integer, primary_key=True)
    intitule = Column(String)
    description = Column(Text)
    date_creation = Column(DateTime)
    date_actualisation = Column(DateTime)
    lieu_travail_libelle = Column(String)
    lieu_travail_latitude = Column(Float)
    lieu_travail_longitude = Column(Float)
    lieu_travail_code_postal = Column(String)
    rome_code = Column(String)
    appellation_libelle = Column(String)
    entreprise_nom = Column(String)
    type_contrat = Column(String)
    nature_contrat = Column(String)
    experience_exige = Column(String)
    experience_libelle = Column(String)
    alternance = Column(String)
    origine_offre_url_origine = Column(String)
    entreprise_description = Column(String)
    salaire_libelle = Column(String)

Base.metadata.create_all(engine)

df.to_sql("job_offers_tech", engine, if_exists="replace", index=False)