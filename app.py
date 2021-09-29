
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

if __name__ == "__main__":
    # Start application on all interfaces, on port 81.
    app.run("0.0.0.0",5000,True,True)