from math import radians
from os import name,system
import mysql.connector

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
DB_NAME = "promoterdb"

DATABASE = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

def init_database(filename):
    system(f"mysql --host={DB_HOST} --user={DB_USER} --password={DB_PASSWORD} {DB_NAME} < {filename}")

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
def register_promotor(id,pos_id):
    CURSOR.execute(("INSERT INTO promoter (promoterinfoid,promoterposid)"
        "VALUES (%s, %s)"), (id, pos_id))

@database_mutator
def register_supervisor(id):
    CURSOR.execute(("INSERT INTO supervisor (supervisorinfoid)"
        "VALUES (%s, %s)"), (id))

@database_mutator
def register_trainer(id):
    CURSOR.execute(("INSERT INTO trainer (trainerinfoid)"
        "VALUES (%s)"), (id,))

@database_accesor
def get_all_user_data():
    CURSOR.execute("SELECT * FROM personal_info")
    return CURSOR.fetchall()

@database_accesor
def get_all_promotor_list():
    CURSOR.execute("""
    SELECT infoid,infoname,infophone,chainname,cityname FROM promoter 
    INNER JOIN personal_info ON promoter.promoterinfoid = personal_info.infoid
    INNER JOIN pos ON promoter.promoterposid = pos.posid
    INNER JOIN city ON pos.poscityid = city.cityid
    INNER JOIN chain ON pos.poschainid = chain.chainid;
    """);
    return CURSOR.fetchall()

@database_accesor
def get_personal_info(id):
    CURSOR.execute("SELECT * FROM personal_info WHERE infoid = %s",(id,));
    result = CURSOR.fetchall();
    return result[0]

@database_mutator
def register_subject(name):
    CURSOR.execute(("INSERT INTO subject (subjectname) VALUES (%s);"
        "SELECT LAST_INSERT_ID();"), (name,))
    CURSOR.nextset()
    ((subject_name,),) = CURSOR.fetchall()
    return subject_name

@database_mutator
def register_trainer_subject(trainer_id,subject_id):
    CURSOR.execute(("INSERT INTO trainer_has_subject (trainerinfoid,subjectid)"
        "VALUES (%s, %s)"), (trainer_id,subject_id))


@database_mutator
def register_capacitation(promoter_id, trainer_id, date, subject_id):
    CURSOR.execute(("INSERT INTO capacitation (capacitationpromoterinfoid,"
        "capacitationtrainerinfoid,capacitationdate,capacitationsubjectid) "
        "VALUES (%s, %s, %s, %s);"
        "SELECT LAST_INSERT_ID();"), (promoter_id,trainer_id,date,subject_id))
    CURSOR.nextset()
    ((subject_name,),) = CURSOR.fetchall()
    return subject_name


@database_mutator
def register_evaluation(promoter_id, supervisor_id, date, comments):
    CURSOR.execute(("INSERT INTO capacitation (evaluationsupervisorinfoid,"
        "evaluationpromoterinfoid,evaluationdate,evaluationcomments) "
        "VALUES (%s, %s, %s, %s);"
        "SELECT LAST_INSERT_ID();"), (supervisor_id,promoter_id,date,comments))
    CURSOR.nextset()
    ((subject_name,),) = CURSOR.fetchall()
    return subject_name