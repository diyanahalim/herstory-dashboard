# to test locally
from waitress import serve
from src.app import server
from app import app_dash, server

if __name__ == "__main__":
    serve(server, host='0.0.0.0', port=8080)

# for deployment
# from app import app_dash
# from src.app import server

# if __name__ == "__main__":
#     pass