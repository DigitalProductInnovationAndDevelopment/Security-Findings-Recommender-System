
from sqlalchemy import create_engine
import os

from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

def get_db_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "app")
    
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"



engine = create_engine(get_db_url(),echo=True)


Session = sessionmaker(engine)
