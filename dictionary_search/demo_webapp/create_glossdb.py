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


db_path = "/home/VGT/dictionary_search/db/embeddings_pf_160/"

ids =  os.listdir(db_path)
id_glosses = [id.split('.npy')[0] for id in ids]
#ID Glosses that we record. Order should be the same as `glosses`.


data_to_insert = id_glosses

def insert_multiple_entries(db_params, data_to_insert):
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        insert_query = "INSERT INTO glosses (gloss_full) VALUES (%s)"

        data_tuples = [(name,) for name in data_to_insert]

        # Execute the query with multiple data
        cursor.executemany(insert_query, data_tuples)
        conn.commit()
        print("Data inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting data into the database:", error)
    finally:
        # Closing the connection
        if conn is not None:
            conn.close()




if __name__ == "__main__":
    insert_multiple_entries(db_params, data_to_insert)