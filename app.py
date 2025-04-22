from flask import Flask
from routes.index import index_bp
from routes.home import home_bp
from routes.login import login_bp
from routes.signup import signup_bp
from routes.logout import logout_bp

app = Flask(__name__)
app.config.from_object("config.Config")

# Register blueprints
app.register_blueprint(index_bp)
app.register_blueprint(login_bp)
app.register_blueprint(home_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(logout_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080, debug=True)
