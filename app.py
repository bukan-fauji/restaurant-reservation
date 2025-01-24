from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.user_routes import user_bp
from routes.reservation_routes import reservation_bp
from routes.menu_routes import menu_bp
from routes.order_routes import order_bp
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'admin'
jwt = JWTManager(app)

Swagger(app)
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(reservation_bp, url_prefix='/reservations')
app.register_blueprint(menu_bp, url_prefix='/menu')
app.register_blueprint(order_bp, url_prefix='/orders')

if __name__ == '__main__':
    app.run(debug=True)
