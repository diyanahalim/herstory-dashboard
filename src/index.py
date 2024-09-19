from src.app import app
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

server = app.server  # Expose the server for deployment

if __name__ == "__main__":
    app.run_server(debug=False)