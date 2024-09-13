from app import app_dash

# commented since not needed for deployment 
server = app_dash.server
if __name__ == "__main__":
    app_dash.run_server(debug=False)