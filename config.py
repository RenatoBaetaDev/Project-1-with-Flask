import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "a hard password"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
    DEBUG = True
    UPLOAD_FOLDER = '/static/mangas'

    @staticmethod
    def init_app(app):
        pass

    