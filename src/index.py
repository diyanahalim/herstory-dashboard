
from waitress import serve # Import the server directly
from app import server

# server = app_dash.server
# Expose the app_dash server for deployment
# server = app_dash.server
# Only expose app_dash; do not run the server here for deployment
# if __name__ == "__main__":
#     app_dash.run_server(debug=False)
if __name__ == "__main__":
    serve(server, host='0.0.0.0', port=8080)