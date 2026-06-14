import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from prometheus_flask_exporter import PrometheusMetrics

from todo_project.config import config_by_name


app = Flask(__name__)

# Select configuration by APP_ENV (development by default). The test suite sets
# TESTING=1, which forces the testing profile (CSRF off, ephemeral DB via DATABASE_URI).
app_env = os.environ.get('APP_ENV', 'development')
if os.environ.get('TESTING') == '1':
    app_env = 'testing'
app.config.from_object(config_by_name[app_env])

if not app.config.get('SECRET_KEY'):  # pragma: no cover - guard for misconfigured staging/prod
    raise RuntimeError('SECRET_KEY must be set (provide it via a secret store in staging/production)')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'danger'

bcrypt = Bcrypt(app)

# Prometheus instrumentation: auto-tracks HTTP request count/latency/exceptions and
# exposes them at GET /metrics for Prometheus to scrape.
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Task Manager application', version='1.0.0')

# Always put Routes at end
from todo_project import routes
from todo_project import models

with app.app_context():
    db.create_all()