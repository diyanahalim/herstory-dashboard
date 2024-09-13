from app import app_dash

# Expose the app_dash server for deployment
server = app_dash.server
# Only expose app_dash; do not run the server here for deployment
# if __name__ == "__main__":
#     app_dash.run_server(debug=False)
# server = app_dash.server