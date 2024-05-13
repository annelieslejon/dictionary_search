from db_models import *
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

db_params = {
    'database': 'amai',
    'user': 'admin',
    'password': 'mirto',
    'host': 'localhost',  # Update if your DB is not on your local machine
    'port': '5432'        # Default PostgreSQL port
}



# Dutch translation of the ID Glosses that we record.
glosses = [
    "Bouwen",
    "Waarom",
    "Hebben",
    "Paard",
    "Melk",
    "Herfst",
    "Valentijn",
    "Telefoneren",
    "Straat",
    "Haas",
    "Hond",
    "Rusten",
    "School",
    "Onthouden",
    "Wat",
    "Vliegtuig",
    "Bel",
    "Kat",
    "Mama",
    "Papa"
]



#ID Glosses that we record. Order should be the same as `glosses`.
id_glosses = [
    "BOUWEN-G-1906",
    "WAAROM-A-13564",
    "HEBBEN-A-4801",
    "PAARD-A-8880",
    "MELK-B-7418",
    "HERFST-B-4897",
    "VALENTIJN-A-16235",
    "TELEFONEREN-D-11870",
    "STRAAT-A-11560",
    "HAAS-A-16146",
    "HOND-A-5052",
    "RUSTEN-B-10250",
    "SCHOOL-A-10547",
    "ONTHOUDEN-A-8420",
    "WAT-A-13657",
    "VLIEGTUIG-B-13187",
    "KLEPELBEL-A-1166",
    "POES-G-9372",
    "MOEDER-A-7676",
    "VADER-G-8975"
]



data_to_insert = zip(glosses, id_glosses)

def insert_multiple_entries(db_params, data_to_insert):
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # SQL to insert data
        query = sql.SQL("INSERT INTO glosses (gloss_name, gloss_full) VALUES (%s, %s);")

        # Execute the query with multiple data
        cursor.executemany(query, data_to_insert)

        print("Data inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting data into the database:", error)
    finally:
        # Closing the connection
        if conn is not None:
            conn.close()




if __name__ == "__main__":
    insert_multiple_entries(db_params, data_to_insert)