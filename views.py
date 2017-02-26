"""
Module for routing views via functions for Taskr
app, including displaying existing tasks and adding
new tasks, provided user is logged into the session.
"""
import sqlite3
from functools import wraps
from flask import Flask, flash, redirect, \
    render_template, request, session, url_for
from forms import AddTaskForm

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

@app.route('/tasks/')
@login_required
def tasks():
    """ Queries db for closed and open tasks, and passes onto
    tasks HTML template for rendering.

    With tasks(), users with proper credentials will have full CRUD
    access; they'll be able to Create, Read, Update, and
    Delete from the app's database table."""
    with connect_db() as taskr_db:
        cur_dict = taskr_db.execute('select name, due_date, priority, task_id from tasks where status=1')
        open_tasks = [dict(name=row[0], due_date=row[1], priority=row[2],
                        task_id=row[3]) for row in cur_dict.fetchall()]
        cur_dict = taskr_db.execute('select name, due_date, priority, task_id from tasks where status=0')
        closed_tasks = [dict(name=row[0], due_date=row[1], priority=row[2],
                        task_id=row[3]) for row in cur_dict.fetchall()]
    return render_template(
        'tasks.html',
        form=AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks
    )
        
@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    """ view for creating new tasks; the 'C' in CRUD."""
    with connect_db() as taskr_db:
        name = request.form['name']
        date = request.form['due_date']
        priority = request.form['priority']
        if not name or not date or not priority:
            flash("All fields are required. Please try again.")
            return redirect(url_for('tasks'))
        else:
            taskr_db.execute('insert into tasks (name, due_date, priority, status) \
                values (?, ?, ?, 1)', [
                request.form['name'],
                request.form['due_date'],
                request.form['priority']
                ]
            )
            taskr_db.commit()
            flash("New entry was successfully posted. Thanks.")
            return redirect(url_for('tasks'))

@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    """ view for marking tasks as complete; the 'U' in CRUD."""
    with connect_db() as taskr_db:
        taskr_db.execute('update tasks set status = 0 where task_id='+str(task_id))
        taskr_db.commit()
        flash("The task was marked as complete.")
        return redirect(url_for('tasks'))
            
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    """ view for deleting tasks; the 'D' in CRUD."""
    with connect_db() as taskr_db:
        taskr_db.execute('delete from tasks where task_id='+str(task_id))
        taskr_db.commit()
        flash("The task was deleted.")
        return redirect(url_for('tasks'))
