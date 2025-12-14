from flask import Flask
from flask_cors import CORS
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp
from flask import request

app = Flask(__name__)

# Configure CORS allow requests dari frontend
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"] 
    }
})

# ngasih izin ke browser supaya request dari frontend tanpa kena blok CORS.
@app.before_request
def skip_preflight_auth():
    if request.method == "OPTIONS":
        return "", 200


app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(chat_bp, url_prefix="/chat")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)

