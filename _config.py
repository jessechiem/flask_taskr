"""
Configuration file for Flask Taskr web app;
used for initializing Flask 'app' object in
views module; also defines path creating and
updating path of SQLite3 database for app.
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'Ev\x89\xc9\xf3\x9d\x15\x9c\x8f\xd9X\x9a\x10\x15\xdb\xd4\x98F~\xa5\xc2\xe5\xa5G'
WTF_CSRF_ENABLED = True

DATABASE_PATH = os.path.join(basedir, DATABASE)
