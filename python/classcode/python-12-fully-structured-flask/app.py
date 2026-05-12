"""
Flask Application Entry Point
Uses Layered Architecture Pattern
"""
from flask import Flask
from Controller.meals_controller import meals_blueprint

# Initialize Flask app
app = Flask(__name__)

# Register blueprints
app.register_blueprint(meals_blueprint)

# Initialize database (creates table if not exists)
from DAO.dao_factory import DAOFactory
DAOFactory.get_meals_dao()


if __name__ == '__main__':
    app.run(debug=True, port=5005)


