
from flask import Flask, render_template
import db

app = Flask(__name__)

@app.route("/viewpromoter/<id>")
def viewpromotor(id):
    return render_template("promoter.html",
        personal_info=db.get_personal_info(id),
        capacitations=db.get_promoter_capacitations(id),
        comments=db.get_promoter_comments(id),
        pos_info=db.get_promoter_pos_info(id))

@app.route("/")
def index():
    return render_template("promoters.html", 
        promoters=db.get_all_promotor_list(),enumerate=enumerate)

if __name__ == "__main__":
    # Start application on all interfaces, on port 81.
    app.run("0.0.0.0",5000,True,True)