import os
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate  # Import Flask-Migrate
from dotenv import load_dotenv
from models.user import db, User
from controller import authentication
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.inspection import get_inspection_by_regno, get_image_inspection_by_regno  # Ensure you import the model
from sqlalchemy import text
from flask_cors import CORS
  # Import text from SQLAlchemy

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # Semua route untuk origin tertentu

# Setup database URI using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, for reducing overhead

# JWT Setup
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")
jwt = JWTManager(app)

# Initialize db instance
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Swagger UI setup
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'KVI API'}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Route to register a new user
@app.route("/register", methods=["POST"])
def register():
    return authentication.signup()

# Route to authenticate a user (login)
@app.route("/auth", methods=["POST"])
def auth():
    return authentication.login()

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/regNo/<string:regNo>", methods=["GET"])
@jwt_required()
def regno_inspection(regNo):
    return get_inspection_by_regno() 

@app.route("/images/regNo/<string:regNo>", methods=["GET"])
@jwt_required()
def image_regno_inspection(regNo):
    return get_image_inspection_by_regno()


@app.route("/test_dashboard_lokasi", methods=["GET"])
def test_dashboard_lokasi():
    try:
        # Query ke tabel 'dashboard_lokasi'
        result = db.session.execute(text('SELECT * FROM dashboard_lokasi'))
        
        # Ambil nama kolom dari hasil query
        columns = result.keys()
        
        # Mengonversi setiap row menjadi dictionary
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        
        if rows:
            return jsonify({"message": "Table 'dashboard_lokasi' is accessible, data found!", "data": rows}), 200
        else:
            return jsonify({"message": "Table 'dashboard_lokasi' is accessible, but no data found."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/test_dashboard_roda_2", methods=["GET"])
def test_dashboard_roda_2():
    try:
        # Query untuk mengambil semua data dari tabel 'dashboard_roda_2'
        result = db.session.execute(text('SELECT * FROM dashboard_roda_2'))  # Mengambil seluruh data
        
        # Ambil nama kolom dari hasil query
        columns = result.keys()
        
        # Mengonversi setiap row menjadi dictionary
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        
        if rows:
            return jsonify({"message": "Table 'dashboard_roda_2' is accessible, data found!", "data": rows}), 200
        else:
            return jsonify({"message": "Table 'dashboard_roda_2' is accessible, but no data found."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/test_dashboard_roda_4", methods=["GET"])
def test_dashboard_roda_4():
    try:
        # Query untuk mengambil semua data dari tabel 'dashboard_roda_4'
        result = db.session.execute(text('SELECT * FROM dashboard_roda_4'))  # Mengambil seluruh data
        
        # Ambil nama kolom dari hasil query
        columns = result.keys()
        
        # Mengonversi setiap row menjadi dictionary
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        
        if rows:
            return jsonify({"message": "Table 'dashboard_roda_4' is accessible, data found!", "data": rows}), 200
        else:
            return jsonify({"message": "Table 'dashboard_roda_4' is accessible, but no data found."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
