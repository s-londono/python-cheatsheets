from ..worldbankapp import app
# Flask automatically looks for html files in the templates folder.
from flask import render_template


@app.route("/")
@app.route("/index")
def index():
    # Specify the HTML file to be rendered when accessing this paths
    return render_template("index.html")


@app.route("/project-one")
def project_one():
    return render_template("project_one.html")
