from flask import *
import requests
import markdown

app = Flask(__name__)

README_URL = f"https://github.com/Kuscheltiermafia/TeamCard/blob/main/README.md"

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/about")
def serve_readme():
    try:
        # Fetch the README content
        response = requests.get(README_URL)
        response.raise_for_status()
        readme_md = response.text

        # Convert Markdown to HTML
        readme_html = markdown.markdown(readme_md)

        return Response(readme_html, mimetype='text/html')

    except requests.exceptions.RequestException as e:
        return f"Error fetching README: {e}", 500

if __name__ == '__main__':
    app.run()