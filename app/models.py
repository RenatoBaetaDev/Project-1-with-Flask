from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from flask import url_for


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class Rate(db.Model):
    __tablename__ = 'rates'
    manga_id = db.Column(db.Integer, db.ForeignKey('mangas.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    value = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),  index=True)
    email = db.Column(db.String(255), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    rated_mangas = db.relationship(
        'Rate', foreign_keys=[Rate.user_id],
        backref=db.backref('rated', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return '<User %r>' % self.username
    
    @property
    def password(self):
        raise AttributeError('password is not readable')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def alreadyRated(self, mangaId):
        return self.rated_mangas.filter_by(
            manga_id=mangaId
        ).first() is not None

    def rate(self, manga, value):
        if not self.alreadyRated(manga):
            rate = Rate(user_id=self, manga_id=manga, value=value)            
            db.session.add(rate)
            db.session.commit()

    def unrate(self, mangaId):
        rate = self.rated_mangas.filter_by(manga_id=mangaId).first()
        if rate:
            db.session.delete(rate)
            db.session.commit

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%d-%m-%Y")]

class Manga(db.Model):
    __tablename__ = 'mangas'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    synopsis = db.Column(db.String(64))
    chapters = db.relationship('Chapter', backref='manga')
    image = db.Column(db.String(128))
    release_date = db.Column(db.DateTime())
    conclusion_date = db.Column(db.DateTime())

    users_rate = db.relationship(
        'Rate', foreign_keys=[Rate.manga_id],
        backref=db.backref('whoRated', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )        

    def userRate(self, user):
        rate = self.users_rate.filter_by(
            user_id=user
        ).first() # is not None    
        if rate is not None:
            return rate.value
        return 0

    def __repr__(self):
        return '<Manga %r>' % self.title    

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id'         : self.id,
           'title'      : self.title,
           'release_date': dump_datetime(self.release_date),
           # This is an example how to deal with Many2Many relations
        #    'many2many'  : self.serialize_many2many
       }

    @property
    def serialize_many2many(self):
       """
       Return object's relations in easily serializable format.
       NB! Calls many2many's serialize property.
       """
       return [ item.serialize for item in self.many2many]        

class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    manga_id = db.Column(db.Integer, db.ForeignKey('mangas.id'))
    number = db.Column(db.Integer)    
    release_date = db.Column(db.DateTime())
    pages = db.relationship('Page', backref='chapter')

    def __repr__(self):
        return '<Chapter %r>' % self.number     

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id'         : self.id,
           'title'      : self.title,
           'number'     : self.number,
           'release_date': dump_datetime(self.release_date),
       }        


class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
    page_number = db.Column(db.Integer)
    image = db.Column(db.String(128))

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id'             : self.id,
           'page_number'    : self.page_number,    
           'image'          : url_for('static', filename=self.image),
           # This is an example how to deal with Many2Many relations
        #    'many2many'  : self.serialize_many2many
       }