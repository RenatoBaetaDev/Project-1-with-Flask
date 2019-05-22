from flask_wtf import FlaskForm
from flask_uploads import UploadSet, IMAGES
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.fields.html5 import EmailField, DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired


from app.models import Manga

images = UploadSet('images', IMAGES)

class MangaRegistrationForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired()
    ])
    synopsis = StringField('Synopsis', validators=[
        DataRequired()
    ])
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(images, 'Images Only!')
    ])
    release_date = DateField('Release date', validators=[
        DataRequired()
    ])            
    submit = SubmitField('Register')

    def validate_name(self, field):
        if Manga.query.filter_by(title=field.data).first():
            raise ValidationError('Manga already registered.')
       