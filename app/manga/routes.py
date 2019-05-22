import os
from flask import session, redirect, url_for, flash, render_template, request
from flask_login import login_required
from . import manga
from .forms import MangaRegistrationForm
from app.models import Manga
from werkzeug.utils import secure_filename
from flask import current_app as app

@manga.route('/list')
def list():
    return render_template('manga/mangas.html')

@manga.route('/mangas/register', methods=['GET','POST'])
def register():
    form = MangaRegistrationForm()
    if form.validate_on_submit():
        file = request.files['file']
        if file:
            filename = secure_filename(form.title.data)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        manga = Manga(
            title=form.title.data,
            synopsis=form.synopsis.data,
            release_date=form.release_date.data,
            image=app.config['UPLOAD_FOLDER']+filename
        )
        db.session.add(manga)
        db.session.commit()
        flash('Manga Registered!')
        return redirect(url_for('manga.list'))
    return render_template('manga/register.html', form=form)