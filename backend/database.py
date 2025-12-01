from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# Get the folder where this file (database.py) is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Point to the pacific.db file inside that folder
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'pacific.db')}"