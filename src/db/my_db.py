from sqlalchemy import create_engine, NullPool
import os

from sqlalchemy.orm import sessionmaker


from config import config

engine = create_engine(
    config.get_db_url(),
    echo=os.getenv("DB_DEBUG", "false") == "true",
    poolclass=NullPool,
)


Session = sessionmaker(engine)


def get_db():
    try:
        with Session() as session:
            yield session
    finally:
        session.close()
