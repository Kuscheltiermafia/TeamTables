from flask import *
import requests

app = Flask(__name__)

README_URL = f"https://github.com/Kuscheltiermafia/TeamCard/blob/main/README.md"

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)