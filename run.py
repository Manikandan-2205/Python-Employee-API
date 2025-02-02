from app import create_app, init_migrate
from flasgger import Swagger

# Create the Flask application
app = create_app()

# Initialize Swagger
swagger = Swagger(app)

# Initialize migrations
with app.app_context():
    init_migrate(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)