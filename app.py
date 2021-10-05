
from flask import Flask, render_template, jsonify, request, redirect
import db

app = Flask(__name__)

@app.route("/api/v1/cities")
def get_cities():
    result = list(map(lambda x: {'id':x[0],'name':x[1]},db.get_cities_list()))
    return jsonify(result)

@app.route("/api/v1/chains_in_city/<city_id>")
def get_chains_in_city(city_id):
    result = list(map(lambda x: {'id':x[0],'name':x[1]},
        db.get_chains_in_city(city_id)))
    return jsonify(result)

@app.route("/api/v1/pos_in_chains_city/<city_id>/<chain_id>")
def get_pos_in_chains_city(city_id,chain_id):
    result = list(map(lambda x: {'id':x[0],'name':x[1]},
        db.get_pos_in_chain_city(city_id,chain_id)))
    return jsonify(result)

@app.route("/registeragent")
def register_agent():
    if len(request.args) == 0:
        return render_template("registeragent.html")
    else:
        name = request.args.get("agentname")
        id = request.args.get("agentid")
        phone = request.args.get("agentphone")
        db.register_personal_info(id,name,phone)
        pos_id = request.args.get("address")
        db.register_agent(id,pos_id)
        return redirect("/")

@app.route("/viewagent/<id>")
def view_agent(id):
    return render_template("agent.html",
        personal_info=db.get_personal_info(id),
        trainings=db.get_agent_trainings(id),
        comments=db.get_agent_comments(id),
        pos_info=db.get_agent_pos_info(id))

@app.route("/")
def index():
    return render_template("agents.html", 
        agents=db.get_all_agent_list(),enumerate=enumerate)

if __name__ == "__main__":
    # Start application on all interfaces, on port 81.
    app.run("0.0.0.0",5000,True,True)