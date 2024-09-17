from src.app import app_dash

server = app_dash.server  # Expose the server for deployment

if __name__ == "__main__":
    app_dash.run_server(debug=False)