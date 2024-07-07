import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

load_dotenv()


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DB_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

Base = declarative_base()


engine = create_engine(DB_URI)
Session = scoped_session(sessionmaker(bind=engine))


# S3 related settings
BUCKET_NAME = 's3-nord-challenge-data'
CATALOGS = ['0/', '1/']

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
