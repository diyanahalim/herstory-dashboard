from app import app_dash
server = app_dash.server  # Expose the server for deployment

if __name__ == "__main__":
    app_dash.run_server(port=8086, debug=True, dev_tools_ui=False)