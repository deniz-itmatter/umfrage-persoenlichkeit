import os
from datetime import timedelta

class Config:
    """Basis-Konfiguration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Datenbank Pool-Einstellungen für hohe Concurrent-Load
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 30,
        'pool_timeout': 30
    }
    
    # Session-Konfiguration
    SESSION_COOKIE_SECURE = False  # True in Production mit HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    """Entwicklungs-Konfiguration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///survey_dev.db'

class ProductionConfig(Config):
    """Produktions-Konfiguration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://survey_user:survey_password@db:5432/survey_db'
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Test-Konfiguration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}