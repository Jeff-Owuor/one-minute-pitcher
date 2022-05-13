import os

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
    SQLALCHEMY_DATABASE_URI ='postgresql://kkfvxdzbctlrnm:52d984f3b28623ae4b928e62e3823ee693b07fc2dff8b220e12d4f8e0064726b@ec2-34-236-94-53.compute-1.amazonaws.com:5432/d77ca7vm9hn7ou'

class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    
    DEBUG = True
    
config_options = {
'development':DevConfig,
'production':ProdConfig,

}