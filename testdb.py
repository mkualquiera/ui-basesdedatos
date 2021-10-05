from logging import lastResort
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
        + fix_name_casing(gen_text(openness=0.1,closureness=0.1,namelen=random.randint(3,4))) \
        + random.choice(CITY_SUFFIXES)
    return fix_name_casing(name)

CHAIN_SUFFIXES = [" Tech", " S.A.", "studios", " Electronics", 
    " International", " United", "ify", "", "", "", ""]

def gen_chain_name():
    name = gen_text(openness=0.7,closureness=0.1,germanness=0.3) \
        + random.choice(CHAIN_SUFFIXES)
    return fix_name_casing(name)

MALE_NAMES = ["Aarón","Abdul","Abel","Abelardo","Abraham","Adam","Adán","Adolfo","Adrián","Adriano","Agustín","Aladino","Alan","Alberto","Alejandro","Alessandro","Alexis","Alfonso","Alonso","Ãlvaro","Andrés","Angel","Antonio","Ariel","Armando","Arturo","Augusto","Aurelio","Baltazar","Bartolomé","Belisario","Benjamín","Benedicto","Bernarndo","Boris","Braulio","Brian","Bruno","Caín","Camilo","Carlos","Casimiro","César","Christian","Cristóbal","Claudio","Clemente","Constancio","Constantino","Cristian","Cristóbal","Daniel","Dario","David","Diego","Domingo","Edgar","Eduardo","Elías","Emilio","Enrique","Ernesto","Esteban","Eugenio","Ezequiel","Fabián","Federico","Felipe","Félix","Fermín","Fernando","Fidel","Francisco","Gabriel","Gerardo","Germán","Gilberto","Giovanni","Gonzalo","Gregorio","Guillermo","Gustavo","Héctor","Heriberto","Hugo","Hilario","Humberto","Hilario","Ignacio","Isaac","Ismael","Iván","Jacobo","Jaime","Jairo","Javier","Jesús","Joaquín","Jorge","José","Juan","Julián","Kevin","Leandro","Leonardo","Leopoldo","Lucas","Luis","Manuel","Marcos","Mario","Martín","Mateo","Matías","Maximiliano","Máximo","Miguel","Nelson","Néstor","Nicolás","Octavio","Omar","Oscar","Orlando","Ovidio","Pablo / Paulo","Patricio","Pedro","Rafael","Ramiro","Ramón","Raúl","Ricardo","Roberto","Rubén","Salvador","Samuel","Santiago","Sergio","Simón","Teodoro","Tito","Tobías","Tomás","Ulises","Valentín","Vicente","Víctor","Wilfredo","William","Zacarías"]
FEMALE_NAMES = ["Adelaida","Adriana","Alejandra","Alba","Alicia","Alina","Anabel","Ana","Anastasia","Andrea","Anita","Ãngela","Angelina","Antonia","Amalia","Amelia","Amparo","Astrid","Aurora","Bárbara","Beatriz","Berta","Blanca","Camelia","Camila","Carina","Carla","Carolina","Carlota","Carmen","Casandra","Catalina","Cecilia","Celeste","Celia","Clara","Claudia","Cristina","Cristela","Dalia","Damaris","Daniela","Débora","Diana","Dina","Dolores","Dora","Doris","Edith","Elba","Elena","Eliana","Elisa","Elisabet","Elvira","Ema","Emilia","Esperanza","Estefanía","Ester","Estrella","Estela","Eugenia","Evangelina","Fabiola","Fátima","Filomena","Francisca","Fanny","Frida","Gabriela","Gina","Giovanna","Giselle","Gladis","Gloria","Griselda","Guadalupe","Heidi","Helena","Heli","Hilda","Hortensia","Ileana","Inés","Ingrid","Irene","Irma","Isabel","Irene","Janet","Jazmín","Jennifer","Jésica","Jezabel","Jimena","Joana","Josefina","Juana","Juanita","Judith","Julia","Julieta","Juliana","Karen","Katherine","Laura","Leticia","Lilia","Liliana","Lisa","Lola","Lorena","Lucrecia","Lucía","Luciana","Luz","Magalí","Magdalena","Manuela","María","María José","Marian","Mariana","Marina","Marisol","Marta","Matilde","Melisa","Mercedes","Micaela","Michelle","Miriam","Mónica","Naomi","Natacha","Natalí","Natalia","Nicole","Nora","Ofelia","Olga","Pamela","Paola","Patricia","Paula","Paulina","Pilar","Rafaela","Raquel","Rebeca","Regina","Renata","Rocío","Rosa","Rosalba","Sabrina","Salomé","Samanta","Sandra","Sara","Silvia","Soledad","Sonia","Sofía","Stefanía","Susana","Tamara","Tania","Tatiana","Teresa","Tulia","Valentina","Valeria","Vanesa","Verónica","Victoria","Vilma","Virginia","Viviana","Ximena","Zoraida"]
LAST_NAMES  = ["Acevedo","Acosta","Agudelo","Álvarez","Arango","Arias","Ávila","Barrera","Bedoya","Beltrán","Bernal","Buitrago","Caicedo","Calderón","Cárdenas","Cardona","Carvajal","Castillo","Castro","Contreras","Correa","Cortes","Cruz","Delgado","Díaz","Duque","Escobar","Fernández","Flórez","Forero","Franco","García","Garzón","Gil","Giraldo","Gómez","González","Guerrero","Gutiérrez","Guzmán","Henao","Hernández","Herrera","Hurtado","Jaramillo","Jiménez","León","Londoño","López","Lozano","Marín","Martínez","Medina","Mejía","Méndez","Mendoza","Molina","Montoya","Mora","Morales","Moreno","Mosquera","Muñoz","Orozco","Ortega","Ortiz","Osorio","Ospina","Parra","Peña","Pérez","Pineda","Pinzón","Quintero","Ramírez","Ramos","Restrepo","Reyes","Rincón","Ríos","Rivera","Rodríguez","Rojas","Romero","Ruiz","Salazar","Sánchez","Sierra","Silva","Suárez","Torres","Trujillo","Uribe","Valencia","Vargas","Vásquez","Vega","Velásquez","Vélez","Zapata"]

def gen_person_name():
    pool = MALE_NAMES if random.random() < 0.5 else FEMALE_NAMES
    result = random.choice(pool) + (f" {random.choice(pool)}" if 
        random.random() < 0.5 else "") + " " + \
        random.choice(LAST_NAMES) + " " + random.choice(LAST_NAMES)
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

def gen_topic():
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
    
    agent_ids = list(set([ gen_id() for i in range(30) ]))

    for pid in agent_ids:
        register_personal_info(pid,gen_person_name(),gen_phone())
        register_agent(pid,random.choice(posi))

    supervisor_ids = list(set([ gen_id() for i in range(30) ]))

    for sid in supervisor_ids:
        register_personal_info(sid,gen_person_name(),gen_phone())
        register_supervisor(sid)
        for i in range(random.randint(0,17)):
            agent_id = random.choice(agent_ids)
            register_evaluation(agent_id, sid, random_date(), gen_comment())

    trainer_ids = list(set([ gen_id() for i in range(30) ]))

    topic_ids = [ register_topic(gen_topic()) for i in range(40) ]

    for tid in trainer_ids:
        register_personal_info(tid,gen_person_name(),gen_phone())
        register_trainer(tid)

        trainer_topics = list(set([ random.choice(topic_ids) for i in 
            range(random.randint(1,5))]))
        
        for topic_id in trainer_topics:
            register_trainer_topic(tid, topic_id)

        for i in range(random.randint(0,17)):
            agent_id = random.choice(agent_ids)
            register_training(agent_id,tid,
                random_date(),random.choice(trainer_topics),
                random.randint(1,5))

