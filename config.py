import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "a hard password"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(os.path.join(basedir,'app'),'static')

    @staticmethod
    def init_app(app):
        pass

    