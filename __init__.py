"""
The flask application package.
"""
from flask import Flask
from flask_cors import CORS
import api

app = Flask(__name__)
CORS(app)

# APIの追加

app.register_blueprint(api.bp)

if __name__ == '__main__':
    app.run()
