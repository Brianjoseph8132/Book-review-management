from flask import Flask,jsonify, request
from flask_migrate import Migrate
from model import  db, TokenBlocklist
from datetime import datetime
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

migrate = Migrate(app, db)
db.init_app(app)


# Jwt
app.config["JWT_SECRET_KEY"] = "wrretyryttutu" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] =  timedelta(hours=1)
jwt = JWTManager(app)
jwt.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Your email server (Gmail in this case)
app.config['MAIL_PORT'] = 587                # Port for Gmail's SMTP server
app.config['MAIL_USE_TLS'] = True            # Use TLS (Transport Layer Security)
app.config['MAIL_USERNAME'] = 'brian.joseph1@student.moringaschool.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'fstp ggsp oqhu perg'        # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'MAIL_USERNAME'  # Default sender email

mail = Mail(app)



# import all functions in views

from views import *

app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(review_bp)
app.register_blueprint(auth_bp)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None



if __name__ == "__main__":
    app.run(debug=True)