from math import radians
from os import name
import mysql.connector

import random

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

DATABASE = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="promoterdb"
)

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
def register_supervisor(id,chain_id):
    CURSOR.execute(("INSERT INTO supervisor (supervisorinfoid,supervisorchainid)"
        "VALUES (%s, %s)"), (id, chain_id))

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

def gen_name(namelen=None,openness=0.5,closureness=0.5,germanness=0.0):
    if namelen == None:
        namelen = random.randint(3,6)
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyzñ"
    result = ""
    for i in range(namelen):
        if random.random() < germanness:
            result += random.choice(consonants)
        elif random.random() < openness:
            result += random.choice(vowels)
        else:
            result += random.choice(consonants)
            result += random.choice(vowels)
    if random.random() < closureness:
        result += random.choice(consonants)
    return result

def fix_name_casing(name):
    return name[0].upper() + name[1:]

CITY_PREFIXES = ["Santa Fe de ", "Valle del ", "Valle de ", "Ciudad del ",
    "Ciudad de ", "Santa ", "", "", "", "", "", "", ""]

CITY_SUFFIXES = [" de Cristo", " del Rosario", " del Señor", " del Evangelio",
    " del Santo", " de los Santos", " de los Apóstoles", "", "", "", "", "", "",
    "","","","","","","","","","",""," del Socorro"]

def gen_city_name():
    name = random.choice(CITY_PREFIXES) \
        + fix_name_casing(gen_name(openness=0.1,closureness=0.1)) \
        + random.choice(CITY_SUFFIXES)
    return fix_name_casing(name)

CHAIN_SUFFIXES = [" Tech", " S.A.", "studios", " Electronics", 
    " International", " United", "ify", "", "", "", ""]

def gen_chain_name():
    name = gen_name(openness=0.7,closureness=0.1,germanness=0.3) \
        + random.choice(CHAIN_SUFFIXES)
    return fix_name_casing(name)

def gen_person_name():
    names = [ fix_name_casing(gen_name(openness=0.2,germanness=0.1,
        closureness=0.2,namelen=random.randint(2,4))) for i in range(4) ]
    result = names[0]
    for name in names[1:]:
        result += " " + name 
    return result

def gen_id():
    return random.randint(1000000000,2999999999)

def gen_phone():
    phone = ""
    if random.random() < 0.2:
        phone += "+"
        phone += str(random.randint(1,99))
        phone += " "
    for i in range(len("3045625371")):
        phone += str(random.randint(0,9))
    return phone

ADDR_TYPES = ["Carrera","Calle","Diagonal","Transversal","Avenida"]    
ADDR_SUFFIXES = ["","","","","","","A","B","C","D","AA","DD"]    
ADDR_CARDINALITY = ["","","","","",""," Norte"," Sur"]

def gen_addr():
    addr = (random.choice(ADDR_TYPES) + " " +
        str(random.randint(1,120)) + random.choice(ADDR_SUFFIXES) + 
        random.choice(ADDR_CARDINALITY) + " #" + str(random.randint(1,120)) + 
        random.choice(ADDR_SUFFIXES) + "-" + str(random.randint(1,300)))
    return addr

def test_db():
    cities = [ register_city(gen_city_name()) for i in range(5) ]
    chains = [ register_chain(gen_chain_name()) for i in range(10) ] 
    posi = [ register_pos(random.choice(chains),random.choice(cities),
        gen_addr()) for i in range(30) ]
    
    promoter_ids = list(set([ gen_id() for i in range(30) ]))

    for pid in promoter_ids:
        register_personal_info(pid,gen_person_name(),gen_phone())
        register_promotor(pid,random.choice(posi))

    supervisor_ids = list(set([ gen_id() for i in range(30) ]))

    for sid in supervisor_ids:
        register_personal_info(sid,gen_person_name(),gen_phone())
        register_supervisor(sid,random.choice(chains))

    trainer_ids = list(set([ gen_id() for i in range(30) ]))

    for tid in trainer_ids:
        register_personal_info(tid,gen_person_name(),gen_phone())
        register_trainer(tid)