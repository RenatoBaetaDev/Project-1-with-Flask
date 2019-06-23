import os
from flask import request, session, redirect, url_for, flash, render_template, jsonify,request, current_app as app
from flask_login import login_required
from . import manga
from .forms import MangaRegistrationForm, MangaEditForm
from app.models import Manga, Chapter, Rate
from werkzeug.utils import secure_filename
from app import db

@manga.route('/mangas/list')
def list():
    mangas = Manga.query.all()
    for manga in mangas:
        manga.rate = manga.userRate(session["user_id"])
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
            image="mangas/"+title+ext
        )
        db.session.add(manga)
        db.session.commit()
        flash('Manga Registered!')
        return redirect(url_for('manga.list'))

    return render_template('manga/register.html', form=form)

@manga.route('/manga/edit/<id>', methods=['GET','POST'])
@login_required
def edit(id):
    manga = Manga.query.filter_by(id=id).first()
    form = MangaEditForm()
    if form.validate_on_submit():

        file = request.files['image']
        filename = file.filename    

        if file:
            path = os.path.join(app.config['UPLOAD_FOLDER'], manga.image)
            if (os.path.isfile(path)):
                os.remove(path)   

            target = os.path.join(app.config['UPLOAD_FOLDER'], 'mangas')        

            if not os.path.isdir(target):
                os.mkdir(target)       

            title = form.title.data
            ext = os.path.splitext(filename)[1]
            destination = "/".join([target, title+ext])
            file.save(destination)

            manga.image = "mangas/"+title+ext 
        else:
            if manga.title != form.title.data:
                target = os.path.join(app.config['UPLOAD_FOLDER'], 'mangas')    
                title = form.title.data
                ext = os.path.splitext(filename)[1]               
                destination = "/".join([target, title+ext])     
                os.rename(
                    os.path.join(app.config['UPLOAD_FOLDER'], manga.image),
                    os.path.join(app.config['UPLOAD_FOLDER'], destination)      
                )
                manga.image = "mangas/"+title+ext 
            

        manga.title = form.title.data
        manga.synopsis = form.synopsis.data
        manga.release_date = form.release_date.data   

        db.session.commit()        
        return redirect(url_for('manga.list'))
    form.title.data = manga.title
    form.synopsis.data = manga.synopsis
    form.release_date.data = manga.release_date   
    form.image.data = url_for('static', filename=manga.image)
    return render_template('manga/edit.html', form=form)


@manga.route('/read/<id>')
def read(id):
    chapters = Chapter.query.filter_by(manga_id=id)
    manga = Manga.query.filter_by(id=id).first()
    manga.image = url_for('static', filename=manga.image)
    return render_template('manga/read.html', chapters=chapters, manga=manga)

@manga.route('/manga/delete/<int:id>')
def delete(id):
    manga = Manga.query.filter_by(id=id).first()
    path = os.path.join(app.config['UPLOAD_FOLDER'], manga.image )
    if (os.path.isfile(path)):
        os.remove(path)    
    db.session.delete(manga)
    db.session.commit()
    return redirect(url_for('manga.list'))

@manga.route('/chapters')
def chapters():
    return render_template('manga/chapters.html')

@manga.route('/getmangas')
def getmangas():
    mangas = Manga.query.all()
    return jsonify(mangas=[i.serialize for i in mangas])

@manga.route('/getchapters')
def getChapters():  
    mangaId = request.args.get('manga', 0, type=int)
    chapters = Chapter.query.filter_by(manga_id=mangaId)    
    return jsonify(chapters=[i.serialize for i in chapters])

@manga.route('/newchapter', methods=['GET','POST'])
def newChapter():
    # uploaded_files = request.files.getlist("page[]")
    # for file in uploaded_files:
    #     print(file)
    # dict = request.form
    # for key in dict:
    #     print('form key '+dict[key])

    return render_template('/manga/chapter/new.html')

@manga.route('/rate', methods=['POST'])
def rate():
    mangaId = request.form.get('manga', 0, type=int)
    userId = session['user_id']
    value = request.form.get('value', 0, type=int)
    # If the user already rated this manga, it will only update that rate
    rate = Rate.query.filter(Rate.user_id==userId, Rate.manga_id==mangaId).first()  
    if rate is not None:
        rate.manga_id=mangaId
        rate.user_id=userId          
        rate.value = value
        db.session.commit()
        return jsonify(result="editou de boas")
    
    rate = Rate(
        manga_id=mangaId,
        user_id=userId,
        value=value
    )
    db.session.add(rate)
    db.session.commit()    
    return jsonify(result="salvou de boas")