from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the db instance
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # Optional: custom table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Store hashed password
    
    

    def __repr__(self):
        return f"<User {self.username}>"

    # Method to set the password (hash it)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password (verify hash)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
