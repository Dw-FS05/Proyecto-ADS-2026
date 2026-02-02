from flask import Flask
import os
from database import db  
from src.routes import api_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:TeGustaSC7C@localhost:5432/eventos_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(host='0.0.0.0', port=5001, debug=True)