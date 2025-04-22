from flask import Flask
from auth.routes import auth_bp

app = Flask(__name__)
app.config.from_object("config.Config")

# Register blueprints
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080, debug=True)
