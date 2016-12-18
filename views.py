"""
Module for routing views via functions for Taskr
app, including displaying existing tasks and adding
new tasks, provided user is logged into the session.
"""
import sqlite3
from functools import wraps
from flask import Flask, flash, redirect, \
    render_template, request, session, url_for

app = Flask(__name__)
app.config.from_object('_config')  # retrieve from _config module

def connect_db():
    """ Open connection to Taskr db with full path
    provided by _config module in same directory."""
    return sqlite3.connect(app.config['DATABASE_PATH'])

def login_required(func):
    """ Decorator function for certain routes requiring login 
    values in session object that stores requests for user."""
    @wraps(func)
    def wrap(*args, **kwargs):
        """ Nested function assessing session object for
        'logged_in' key; redirects to login view if not found."""
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap  # call above nested function

@app.route('/logout')
def logout():
    """ Route handling user logging out; includes
    removing logged_in key in session object."""
    session.pop('logged_in', None)
    flash('Logging out.')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    """ Route handling user attempting to login 
    with request form with username and/or password."""
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] \
            or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid credentials. Try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            flash('Welcome!')
            return redirect(url_for('tasks'))
    return render_template('login.html')
