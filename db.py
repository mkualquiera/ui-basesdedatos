from math import radians
from os import name,system
import mysql.connector
from mysql.connector import cursor

def database_mutator(fun):
    def result(*argv,**kwargs):
        global CURSOR
        CURSOR = DATABASE.cursor()
        funresult = fun(*argv,**kwargs)
        DATABASE.commit()
        return funresult
    return result

def database_accesor(fun):
    def result(*argv,**kwargs):
        global CURSOR
        CURSOR = DATABASE.cursor()
        funresult = fun(*argv,**kwargs)
        return funresult
    return result

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "agentdb"

DATABASE = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

def init_database(filename):
    system(f"mysql --host={DB_HOST} --user={DB_USER} --password={DB_PASSWORD} \
         {DB_NAME} < {filename}")

@database_mutator
def register_city(name):
    CURSOR.execute(("INSERT INTO city (cityname) VALUES (%s);"
        "SELECT LAST_INSERT_ID();"), (name,))
    CURSOR.nextset()
    ((city_id,),) = CURSOR.fetchall()
    return city_id

@database_mutator
def register_chain(name):
    CURSOR.execute(("INSERT INTO chain (chainname) VALUES (%s);"
        "SELECT LAST_INSERT_ID();"), (name,))
    CURSOR.nextset()
    ((chain_id,),) = CURSOR.fetchall()
    return chain_id

@database_mutator
def register_pos(chain_id,city_id,address):
    CURSOR.execute(("INSERT INTO pos (poschainid, poscityid, posaddress) "
        "VALUES (%s, %s, %s);"
        "SELECT LAST_INSERT_ID();"), (chain_id,city_id,address))
    CURSOR.nextset()
    ((pos_id,),) = CURSOR.fetchall()
    return pos_id

@database_mutator
def register_personal_info(id,name,phone):
    CURSOR.execute(("INSERT INTO personal_info (infoid,infoname,infophone)"
        "VALUES (%s, %s, %s)"), (id, name, phone))
    
@database_mutator
def register_agent(id,pos_id):
    CURSOR.execute(("INSERT INTO agent (agentinfoid,agentposid)"
        "VALUES (%s, %s)"), (id, pos_id))

@database_mutator
def register_supervisor(id):
    CURSOR.execute(("INSERT INTO supervisor (supervisorinfoid)"
        "VALUES (%s)"), (id,))

@database_mutator
def register_trainer(id):
    CURSOR.execute(("INSERT INTO trainer (trainerinfoid)"
        "VALUES (%s)"), (id,))

@database_accesor
def get_all_user_data():
    CURSOR.execute("SELECT * FROM personal_info")
    return CURSOR.fetchall()

@database_accesor
def get_all_agent_list():
    CURSOR.execute("""
    SELECT infoid,infoname,infophone,chainname,cityname FROM agent 
    INNER JOIN personal_info ON agent.agentinfoid = personal_info.infoid
    INNER JOIN pos ON agent.agentposid = pos.posid
    INNER JOIN city ON pos.poscityid = city.cityid
    INNER JOIN chain ON pos.poschainid = chain.chainid;
    """);
    return CURSOR.fetchall()

@database_accesor
def get_cities_list():
    CURSOR.execute("SELECT * FROM city")
    return CURSOR.fetchall()

@database_accesor
def get_topic_list():
    CURSOR.execute("SELECT * FROM topic")
    return CURSOR.fetchall()

@database_accesor
def get_trainer_list():
    CURSOR.execute(("SELECT trainerinfoid,infoname FROM trainer "
        "INNER JOIN personal_info on trainer.trainerinfoid = "
        "personal_info.infoid;"))
    return CURSOR.fetchall()

@database_accesor
def get_chains_in_city(cityid):
    CURSOR.execute(("SELECT DISTINCT(chainid),chainname FROM pos "
        "INNER JOIN city ON city.cityid = pos.poscityid "
        "INNER JOIN chain ON chain.chainid = pos.poschainid "
        "WHERE poscityid=(%s);"),(cityid,))
    return CURSOR.fetchall()

@database_accesor
def get_pos_in_chain_city(cityid,chainid):
    CURSOR.execute(("SELECT posid,posaddress FROM pos "
        "INNER JOIN city ON city.cityid = pos.poscityid "
        "INNER JOIN chain ON chain.chainid = pos.poschainid "
        "WHERE poscityid=(%s) AND chainid=(%s);"), (cityid,chainid))
    return CURSOR.fetchall()


@database_accesor
def get_personal_info(id):
    CURSOR.execute("SELECT * FROM personal_info WHERE infoid = %s",(id,));
    result = CURSOR.fetchall()
    return result[0]

@database_mutator
def register_topic(name):
    CURSOR.execute(("INSERT INTO topic (topicname) VALUES (%s);"
        "SELECT LAST_INSERT_ID();"), (name,))
    CURSOR.nextset()
    ((topic_name,),) = CURSOR.fetchall()
    return topic_name

@database_mutator
def register_trainer_topic(trainer_id,topic_id):
    CURSOR.execute(("INSERT INTO trainer_has_topic (trainerinfoid,topicid)"
        "VALUES (%s, %s)"), (trainer_id,topic_id))


@database_mutator
def register_training(agent_id, trainer_id, date, topic_id, grade):
    CURSOR.execute(("INSERT INTO training (trainingagentinfoid,"
        "trainingtrainerinfoid,trainingdate,trainingtopicid,"
        "traininggrade) "
        "VALUES (%s, %s, %s, %s, %s);"
        "SELECT LAST_INSERT_ID();"), (agent_id,trainer_id,date,topic_id,
            grade))
    CURSOR.nextset()
    ((topic_name,),) = CURSOR.fetchall()
    return topic_name


@database_mutator
def register_evaluation(agent_id, supervisor_id, date, comments):
    CURSOR.execute(("INSERT INTO evaluation (evaluationsupervisorinfoid,"
        "evaluationagentinfoid,evaluationdate,evaluationcomments) "
        "VALUES (%s, %s, %s, %s);"
        "SELECT LAST_INSERT_ID();"), (supervisor_id,agent_id,date,comments))
    CURSOR.nextset()
    ((topic_name,),) = CURSOR.fetchall()
    return topic_name

@database_accesor
def get_agent_trainings(agent_id):
    CURSOR.execute(("SELECT topicname,traininggrade,trainingdate,"
        "infoname FROM training "
        "INNER JOIN personal_info ON personal_info.infoid = "
        "training.trainingtrainerinfoid "
        "INNER JOIN topic ON topic.topicid = "
        "training.trainingtopicid "
        "WHERE trainingagentinfoid = (%s);"), (agent_id,))
    return CURSOR.fetchall()

@database_accesor
def get_agent_comments(agent_id):
    CURSOR.execute(("SELECT evaluationcomments,evaluationdate,infoname "
        "FROM evaluation INNER JOIN personal_info ON "
        "evaluation.evaluationsupervisorinfoid = personal_info.infoid "
        "WHERE evaluationagentinfoid = (%s);"), (agent_id,))
    return CURSOR.fetchall()

@database_accesor
def get_agent_pos_info(agent_id):
    CURSOR.execute(("SELECT chainname,cityname,posaddress FROM agent "
        "INNER JOIN pos ON pos.posid = agent.agentposid "
        "INNER JOIN city ON pos.poscityid = city.cityid "
        "INNER JOIN chain ON pos.poschainid = chain.chainid "
        "WHERE agentinfoid = (%s);"), (agent_id,))
    return CURSOR.fetchall()[0]


@database_accesor
def get_ids():
    CURSOR.execute("SELECT (infoid) FROM personal_info;")
    return CURSOR.fetchall()