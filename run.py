import os
from config import app,create_app

from flask import Flask
app = Flask(__name__)
app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

