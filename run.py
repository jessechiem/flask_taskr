"""
    Starts the Flask server to run the FlaskTaskr app.

    Also useful for testing site, to check if:
        app runs,
        templates are working correctly,
        logic in views.py works,
        database is created and/or up-to-date
"""
from views import app
app.run(debug=True)
