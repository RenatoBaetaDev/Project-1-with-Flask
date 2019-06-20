from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),  index=True)
    email = db.Column(db.String(255), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

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

class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
    page_number = db.Column(db.Integer)
    image = db.Column(db.String(128))