from flask import Flask
from routes.index import index_bp
from routes.home import home_bp
from routes.login import login_bp
from routes.signup import signup_bp
from routes.logout import logout_bp

from flask_cors import CORS

def load_configs(app):
    import os
    from dotenv import load_dotenv
    load_dotenv()
    app.config['DEBUG'] = os.getenv("DEBUG", "True") == "True"
    app.config['PORT'] = int(os.getenv("PORT", 8080))
    app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST", "localhost")
    app.config['MYSQL_USER'] = os.getenv("MYSQL_USER", "root")
    app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD", "root")
    app.config['MYSQL_DB'] = os.getenv("MYSQL_DB", "footbee")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_default_secret_key')

def create_app():
    app = Flask(__name__)
    CORS(app)
    # load configs from environment
    load_configs(app)
    
    # Register blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(logout_bp)
    
    return app


if __name__ == "__main__":
    app = create_app()
    port=app.config.get("PORT", 5000)
    debug=app.config.get("DEBUG", True)
    app.run(host="0.0.0.0", port=port, debug=debug)
