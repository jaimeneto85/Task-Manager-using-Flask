"""Environment-based configuration.

The SAME codebase runs in every environment; only the selected configuration
differs. The active profile is chosen by the APP_ENV environment variable
(see todo_project/__init__.py). Secrets (SECRET_KEY, DATABASE_URI) come from the
environment / a secret store -- never hardcode them for staging or production.
"""
import os


class BaseConfig:
    """Settings shared by every environment."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')          # no default in the base profile
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class DevelopmentConfig(BaseConfig):
    """Local development: debug on, SQL echo, plain HTTP."""
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-not-a-secret')  # convenience locally
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(BaseConfig):
    """Automated tests: CSRF disabled, ephemeral DB injected via DATABASE_URI."""
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'testing-only')
    SESSION_COOKIE_SECURE = False


class StagingConfig(BaseConfig):
    """Pre-production: production-like, secrets required, HTTPS enforced."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'


class ProductionConfig(BaseConfig):
    """Production: hardened, secrets required, HTTPS enforced."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    PREFERRED_URL_SCHEME = 'https'


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
