from flask import session, redirect, url_for, flash, render_template
from flask_login import login_required
from . import main
from .forms import NameForm

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Parece que você alterou o nome!')
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'))


@main.route('/user/<name>')
@login_required
def user(name):
    return render_template('user.html', name=name) 