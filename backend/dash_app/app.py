# Main Dash application logic
from . import create_dash_app
from flask import Flask

server = Flask(__name__)

app = create_dash_app(server)

if __name__ == '__main__':
    app.run_server(debug=True)
