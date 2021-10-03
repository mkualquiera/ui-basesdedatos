
from flask import Flask, render_template
import db

app = Flask(__name__)

@app.route("/viewpromoter/<id>")
def viewpromotor(id):
    personal_info = db.get_personal_info(id)
    return render_template("promoter.html",personal_info=personal_info)

@app.route("/")
def index():
    return render_template("promoters.html", 
        promoters=db.get_all_promotor_list(),enumerate=enumerate)

if __name__ == "__main__":
    # Start application on all interfaces, on port 81.
    app.run("0.0.0.0",5000,True,True)