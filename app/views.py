# -*- coding: utf-8 -*-

import os

# import easygui
from flask import render_template, redirect, url_for, request, g
from flask import send_from_directory
from flask_login import login_user, logout_user, current_user, login_required

from app import app, login_manager
from app import db
from .models import User, Party


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def validate_and_add(party):
    # for P in Party.query.all():
    #     if party.name == P.name:
    #         party.count += 1
    party.count += 1;
    for user in User.query.all():
        if user.id == current_user.id:
            user.voted = True
    db.session.commit()


@app.route('/confirm/<id>', methods=['GET', 'POST'])
@login_required
def confirm_selection(id):
    party = None
    Id = int(id)
    for p in Party.query.all():
        if p.id == Id:
            party = p
            break
    if request.method == 'POST':
        if request.form['btn'] == 'אשר':
            validate_and_add(party)
            return redirect(url_for('logout'))
        else:
            return redirect(url_for('index'))
    g.user = current_user
    return render_template('confirm_selection.html',
                           title='Home',
                           user=g.user,
                           party=party)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        return redirect(url_for('confirm_selection', id=request.form['partyId']))
    error = u'הינך מחוייב לבחור באחד מהפתקים'
    g.user = current_user  # global user parameter used by flask framework
    parties = Party.query.all()  # this is a demo comment
    return render_template('index.html',
                           title='Home',
                           error=error,
                           user=g.user,
                           parties=parties)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        ## Validate user
        id = request.form['id']
        user = User.query.filter_by(id=id).first()
        if user is not None:
            if user.first_name == request.form['first_name'] and user.last_name == request.form['last_name']:
                if user.voted == False:
                    login_user(user)  ## built in 'flask login' method that creates a user session
                    return redirect(url_for('index'))
                error = u'המצביע מימש את זכותו להצביע'
            else:
                error = u'פרטים שגויים, נסה שוב'
        else:  ##validation error
            error = u'המצביע אינו מופיע בבסיס הנתונים'

    return render_template('login.html', error=error)  ## will handle the logout request


@app.route('/logout')
@login_required
def logout():
    logout_user()  ## built in 'flask login' method that deletes the user session
    return redirect(url_for('index'))


## secret page that shows the user name
@app.route('/secret', methods=['GET'])
@login_required
def secret():
    return 'This is a secret page. You are logged in as {} {}'.format(current_user.first_name, current_user.last_name)


## will handle the site icon - bonus 2 points for creative new icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
