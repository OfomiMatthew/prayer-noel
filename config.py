import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'pray_noel.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Christmas Eve Global Prayer
    CHRISTMAS_EVE_PRAYER_TIME = '2025-12-24 20:00:00'
    
    # Pagination
    REQUESTS_PER_PAGE = 20
