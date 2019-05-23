import os
from flask import session, redirect, url_for, flash, render_template, request, current_app as app
from flask_login import login_required
from . import manga
from .forms import MangaRegistrationForm
from app.models import Manga, Chapter
from werkzeug.utils import secure_filename
from app import db

@manga.route('/list')
def list():
    mangas = Manga.query.all()
    return render_template('manga/mangas.html', mangas=mangas)

@manga.route('/mangas/register', methods=['GET','POST'])
@login_required
def register():
    form = MangaRegistrationForm()
    if form.validate_on_submit():
        file = request.files['image']
        filename = file.filename     
        
        target = os.path.join(app.config['UPLOAD_FOLDER'], 'mangas')        
        if not os.path.isdir(target):
            os.mkdir(target)       

        title = form.title.data
        ext = os.path.splitext(filename)[1]
        destination = "/".join([target, title+ext])
        file.save(destination)

        manga = Manga(
            title=title,
            synopsis=form.synopsis.data,
            release_date=form.release_date.data,
            image=title+ext
        )
        db.session.add(manga)
        db.session.commit()
        flash('Manga Registered!')
        return redirect(url_for('manga.list'))
    return render_template('manga/register.html', form=form)

@manga.route('/chapters/<id>')
def chapters(id):
    chapters = Chapter.query.filter_by(manga_id=id)
    manga = Manga.query.filter_by(id=id).first()
    manga.image = url_for('static', filename='mangas/'+manga.image)
    return render_template('manga/chapters.html', chapters=chapters, manga=manga)