
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "uwu"

if __name__ == "__main__":
    # Start application on all interfaces, on port 81.
    app.run("0.0.0.0",5000,True,True)