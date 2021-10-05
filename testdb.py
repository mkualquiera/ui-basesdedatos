from db import *
import random
import datetime
from dateutil.relativedelta import relativedelta

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyzñ"

def gen_text(namelen=None,openness=0.5,closureness=0.5,germanness=0.0):
    if namelen == None:
        namelen = random.randint(3,6)
    
    result = ""
    for i in range(namelen):
        if random.random() < germanness:
            result += random.choice(CONSONANTS)
        elif random.random() < openness:
            result += random.choice(VOWELS)
        else:
            result += random.choice(CONSONANTS)
            result += random.choice(VOWELS)
    if random.random() < closureness:
        result += random.choice(CONSONANTS)
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
        + fix_name_casing(gen_text(openness=0.1,closureness=0.1)) \
        + random.choice(CITY_SUFFIXES)
    return fix_name_casing(name)

CHAIN_SUFFIXES = [" Tech", " S.A.", "studios", " Electronics", 
    " International", " United", "ify", "", "", "", ""]

def gen_chain_name():
    name = gen_text(openness=0.7,closureness=0.1,germanness=0.3) \
        + random.choice(CHAIN_SUFFIXES)
    return fix_name_casing(name)

def gen_person_name():
    names = [ fix_name_casing(gen_text(openness=0.2,germanness=0.1,
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

PRODUCTS = ["Clock", "Phone", "Pad", "Reader", "Laptop", "Pod", "Player", 
    "Notebook"]

MARKETIVES = [" Plus", " Omega", " X", " Power", " Smart", " Super", 
    " Retro", " Future", " Instant", "", "", ""]

def gen_subject():
    result = ""
    if random.random() < 0.4:
        result += random.choice(VOWELS)
    if random.random() < 0.3:
        result += random.choice(PRODUCTS)
    else:
        result += fix_name_casing(gen_text(namelen=4,openness=0.7,
            closureness=0.2,germanness=0.2))
    result += random.choice(MARKETIVES)
    if random.random() < 0.5:
        result += " " + str(random.randint(2,20))
    return result

ADDR_TYPES = ["Carrera","Calle","Diagonal","Transversal","Avenida"]    
ADDR_SUFFIXES = ["","","","","","","A","B","C","D","AA","DD"]    
ADDR_CARDINALITY = ["","","","","",""," Norte"," Sur"]

def gen_addr():
    addr = (random.choice(ADDR_TYPES) + " " +
        str(random.randint(1,120)) + random.choice(ADDR_SUFFIXES) + 
        random.choice(ADDR_CARDINALITY) + " #" + str(random.randint(1,120)) + 
        random.choice(ADDR_SUFFIXES) + "-" + str(random.randint(1,300)))
    return addr

def random_date(start=None, end=None):
    if start == None:
        start = datetime.datetime.now()-relativedelta(years=10)
    if end == None:
        end = datetime.datetime.now()
    return (start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )).date().isoformat()

def gen_comment():
    result = gen_text()
    for i in range(random.randint(10,20)):
        result += " " + gen_text(random.randint(1,5),germanness=0.2)
    result += "."
    return fix_name_casing(result)

def test_db():
    init_database("forwardeng.sql")

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
        register_supervisor(sid)
        for i in range(random.randint(0,17)):
            promoter_id = random.choice(promoter_ids)
            register_evaluation(promoter_id, sid, random_date(), gen_comment())

    trainer_ids = list(set([ gen_id() for i in range(30) ]))

    subject_ids = [ register_subject(gen_subject()) for i in range(40) ]

    for tid in trainer_ids:
        register_personal_info(tid,gen_person_name(),gen_phone())
        register_trainer(tid)

        trainer_subjects = list(set([ random.choice(subject_ids) for i in 
            range(random.randint(1,5))]))
        
        for subject_id in trainer_subjects:
            register_trainer_subject(tid, subject_id)

        for i in range(random.randint(0,17)):
            promoter_id = random.choice(promoter_ids)
            register_capacitation(promoter_id,tid,
                random_date(),random.choice(trainer_subjects),
                random.randint(1,5))

