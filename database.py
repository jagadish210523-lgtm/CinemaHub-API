from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


URL_DATABASE = 'mysql+pymysql://root:210523@localhost:3306/cinemahub'
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()