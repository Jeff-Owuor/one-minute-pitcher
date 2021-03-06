import os
from sqlalchemy import create_engine, exc


class Config:
    '''
    General configuration parent class
    
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://paulineapondi:1989@localhost/pitched'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST ='app/static/photos'
class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = create_engine(os.environ.get("DATABASE_URL").replace("://", "ql://", 1), pool_recycle=3600)
    DEBUG = True
    
class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass
    
config_options = {
'development':DevConfig,
'production':ProdConfig,

}