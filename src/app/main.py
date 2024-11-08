from flask import Flask
import sys
sys.path.append("src")  # Ensure 'src' is added to the path

from app.Controller.User_controller import user_bp
from app.Controller.Mortgage_controller import mortgage_bp
from app.View.views import views_bp  # Import the view blueprint

# Specify the correct template folder path
app = Flask(__name__, template_folder="View/templates")

app.secret_key = '12345'

app.register_blueprint(user_bp)
# Register blueprints for API and views
app.register_blueprint(views_bp)
app.register_blueprint(mortgage_bp, url_prefix="/api/mortgage")


if __name__ == "__main__":
    app.run(debug=True)

