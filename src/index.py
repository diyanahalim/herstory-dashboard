from app import app

server = app.server  # Expose the server for deployment

if __name__ == "__main__":
    app.run_server(debug=False)