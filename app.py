# app.py
from manager import app  # Import the app from the manager module

# Run the application
if __name__ == "__main__":
    app.run(debug=True, port=8080)  # Change the port to 8080