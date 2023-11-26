import evadb
import os
import time
import psycopg2
# from config import config

# from openai import OpenAI
import openai
from dotenv import load_dotenv

load_dotenv()


# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_KEY"] = os.getenv('OPENAI_API_KEY')

cursor = evadb.connect().cursor()

cursor.query("""
DROP DATABASE IF EXISTS postgres_data;
""").df()

postgres_connect_query = """CREATE DATABASE postgres_data
WITH ENGINE = 'postgres',
PARAMETERS = {
    "user": "postgres",
    "password": "evadb546",
    "host": "localhost",
    "port": "5432",
    "database": "postgres"
};
"""
cursor.query(postgres_connect_query).execute()



# def insert_vendor(vendor_name):
#     """ insert a new vendor into the vendors table """
#     # sql = """INSERT INTO review_table(review)
#     #          VALUES(%s) RETURNING vendor_id;"""
#     sql = """INSERT INTO review_table(review)
#              VALUES(%s);"""
#     conn = None
#     # vendor_id = None
#     try:
#         conn = psycopg2.connect(database="postgres", user="postgres", password="evadb546", host="localhost", port=5432)
#         # create a new cursor
#         cur = conn.cursor()
#         # execute the INSERT statement
#         cur.execute(sql, (vendor_name,))
#         # get the generated id back
#         # vendor_id = cur.fetchone()[0]
#         # commit the changes to the database
#         conn.commit()
#         # close communication with the database
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()

    # return vendor_id

# insert_vendor('This food is atrocious')


print('waiting')


def watch_file(file_path):
    # Get the initial modification time of the file
    last_mod_time = os.path.getmtime(file_path)

    while True:
        # Check the modification time of the file
        current_mod_time = os.path.getmtime(file_path)

        # If the modification time has changed, execute the desired action
        if current_mod_time != last_mod_time:
            print("File has been changed! Performing the action...")
            # Call the function or code you want to execute when the file changes
            perform_action()

            # Update the last modification time
            last_mod_time = current_mod_time

        # Add a delay to control the frequency of checks
        time.sleep(2)  # Adjust this delay (in seconds) based on your needs

def perform_action(): 
    # Define the action you want to perform when the file changes
    # *******Dont need to actually read this one, by here, you know file has been changed. Just execute summary, no input needed.
    print("Executing the action...")

    query = """
        USE postgres_data {
        SELECT review FROM review_table
        }
        """
    summary = cursor.query(query).df()
    print(summary)
    query = f"""
        SELECT ChatGPT(
        "Table: {summary}. Summarize this table of reviews overall in one sentence. "
        );
        """
    full_response = cursor.query(query).df()

    print(full_response)


    file_path = 'summaryResponse.txt'
    with open(file_path, 'w') as file:
        # full_response = "pos"
        file.write(full_response.iloc[0]['chatgpt.response'])

# Replace with your file path
file_path_to_watch = 'summaryInput.txt'

watch_file(file_path_to_watch)

