import os

from flask import Flask

from todo_project import app

# Type alias for the application entry point. Importing Flask here also brings the
# run() call below within scope of bandit's B201 (flask_debug_true) check, which only
# analyzes modules that import flask.
flask_app: Flask = app

if __name__ == '__main__':
    # Debug is disabled unless FLASK_DEBUG=1 is set explicitly. It must never be enabled
    # in production: Flask's debug mode exposes the Werkzeug debugger, which allows
    # arbitrary code execution (CWE-94).
    flask_app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
