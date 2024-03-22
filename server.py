from flask_app import app
from flask_app.controllers import users_controller, property_controller, dashboard_controller, favorites_controller


if __name__ == "__main__":
    app.run(debug=True)