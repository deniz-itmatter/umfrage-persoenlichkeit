from flask import Flask
from flask_migrate import Migrate
from models import db
from config import config
from filters import register_filters
import os

def create_app(config_name=None):
    """Application Factory Pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialisiere Extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register custom filters
    register_filters(app)
    
    # Registriere Blueprints
    from routes.main import main_bp
    from routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return "Seite nicht gefunden", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return "Interner Serverfehler", 500
    
    # CLI Commands
    @app.cli.command()
    def init_db():
        """Initialisiert die Datenbank"""
        db.create_all()
        print("Datenbank initialisiert!")
    
    @app.cli.command()
    def reset_db():
        """Setzt die Datenbank zurück"""
        db.drop_all()
        db.create_all()
        print("Datenbank zurückgesetzt!")
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)