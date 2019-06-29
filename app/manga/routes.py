import os
from flask import request, session, redirect, url_for, flash, render_template, jsonify,request, current_app as app
from flask_login import login_required
from . import manga
from .forms import MangaRegistrationForm, MangaEditForm
from app.models import Manga, Chapter, Page, Rate, User
from werkzeug.utils import secure_filename
from app import db
from datetime import datetime

@manga.route('/mangas/list')
def list():
    mangas = Manga.query.all()
    if session.get('user_id'):
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
    manga = Manga.query.filter_by(id=id).first()
    manga.image = url_for('static', filename=manga.image)
    chapters = Chapter.query.filter_by(manga_id=id)
    return render_template('manga/read.html', chapters=chapters,manga=manga)

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

@manga.route('/deletechapter', methods=['POST'])
def deleteChapter():
    chapterId = request.form.get('id', 0, type=int)
    chapter = Chapter.query.filter_by(id=chapterId).first()

    pages = Page.query.filter_by(chapter_id=chapterId)
    if pages:
        for page in pages:
            path = os.path.join(app.config['UPLOAD_FOLDER'], page.image )
            if (os.path.isfile(path)):
                os.remove(path)
            db.session.delete(page)
            db.session.commit()

    db.session.delete(chapter)
    db.session.commit()
    return jsonify(result="deleted")

@manga.route('/newchapter', methods=['GET','POST'])
def newChapter():
    if request.method == 'POST':
        dt = datetime.strptime(request.form['release_date'], '%Y-%m-%d')
        #ADDING CHAPTER
        chapter = Chapter(
            title = request.form['title'],
            manga_id = request.form['manga'],
            number = request.form['number'],
            release_date = dt,
        )

        
        db.session.add(chapter)

        db.session.flush() #cheat to get the Id after insert, 
        chapterId = chapter.id

        db.session.commit()
        #ADDING CHAPTER

        #ADDING PAGES TO CHAPTER
        count = 0
        uploaded_files = request.files.getlist("page[]")
        manga = Manga.query.filter_by(id=request.form['manga']).first()        

        for file in uploaded_files:
            count += 1
            
            filename = file.filename     
            
            #Each manga needs a folder, then each chapter needs one, then we insert the pages in
            mangaTitle = manga.title.replace(" ", "-")

            target = os.path.join(app.config['UPLOAD_FOLDER'], 'mangas')        

            target = os.path.join(target, mangaTitle)     

            if not os.path.isdir(target):
                os.mkdir(target)   

            target = os.path.join(target, 'chapter-' + request.form['number'])   

            if not os.path.isdir(target):
                os.mkdir(target)       

            title = 'page'+str(count)
            ext = os.path.splitext(filename)[1]
            destination = "/".join([target, title+ext])
            file.save(destination)

            page = Page(
                chapter_id = chapterId,
                page_number = count,
                image = 'mangas/' + mangaTitle + '/chapter-' + request.form['number'] + "/" + title + ext
            )

            db.session.add(page)
            db.session.commit()            
       

        flash('Chapter Registered!')
        return redirect(url_for('manga.read', id=manga.id))        

        #ADDING PAGES TO CHAPTER

    return render_template('/manga/chapter/new.html')

@manga.route('/rate', methods=['POST'])
def rate():
    mangaId = request.form.get('manga', 0, type=int)
    userId = session['user_id']
    value = request.form.get('value', 0, type=int)

    user = User.query.filter_by(id=userId).first()

    # If the user already rated this manga, it will only update that rate
    if user.alreadyRated(mangaId):
        rate = Rate.query.filter(Rate.user_id==userId, Rate.manga_id==mangaId).first()         
        rate.value = value
        db.session.commit()
        return jsonify(result="edited")
    
    user.rate(mangaId, value)
    return jsonify(result="saved")

@manga.route('/pages')
def getPages():
    chapterId = request.args.get('id', 0, type=int)
    chapter = Chapter.query.filter_by(id=chapterId).first()

    pages = Page.query.filter_by(chapter_id=chapterId)
    return jsonify(pages=[i.serialize for i in pages])

