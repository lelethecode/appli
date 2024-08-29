import os
from myapp.config import app
from myapp import app
from flask import Flask
app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

