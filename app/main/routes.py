from flask import session, redirect, url_for, flash, render_template, jsonify
from flask_login import login_required
from . import main
from .forms import NameForm
from app.models import User, Role, Manga


@main.route('/', methods=['GET', 'POST'])
def index():
    mangas = Manga.query.all()        
    return render_template('index.html', mangas=mangas)

@main.route('/user/<name>')
@login_required
def user(name):
    return render_template('user.html', name=name) 


@main.route('/about')
def about():
    return render_template('about.html')