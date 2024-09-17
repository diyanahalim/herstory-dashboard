# to test locally
from src.app import app_dash 

server = app_dash.server
# Expose the app_dash server for deployment
# server = app_dash.server
# Only expose app_dash; do not run the server here for deployment
if __name__ == "__main__":
    app_dash.run_server(debug=False)

# for deployment
# from app import app_dash
# from src.app import server

# if __name__ == "__main__":
#     pass