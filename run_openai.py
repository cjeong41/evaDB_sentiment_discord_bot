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


# client = OpenAI()

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)

cursor = evadb.connect().cursor()


cursor.query("""
USE postgres_data {
  DROP TABLE review_table
}
""").df()

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

cursor.query("""
USE postgres_data {
  CREATE TABLE review_table (review VARCHAR(1000))
}
""").df()

query = """
USE postgres_data {
  INSERT INTO review_table (review) VALUES ('This food is amazing')
}
"""
cursor.query(query).df()

query = """
USE postgres_data {
  INSERT INTO review_table (review) VALUES ('This food is terrible')
}
"""
cursor.query(query).df()

query = """
USE postgres_data {
  INSERT INTO review_table (review) VALUES ('This food is not great')
}
"""
cursor.query(query).df()


def insert_vendor(vendor_name):
    """ insert a new vendor into the vendors table """
    # sql = """INSERT INTO review_table(review)
    #          VALUES(%s) RETURNING vendor_id;"""
    sql = """INSERT INTO review_table(review)
             VALUES(%s);"""
    conn = None
    # vendor_id = None
    try:
        conn = psycopg2.connect(database="postgres", user="postgres", password="evadb546", host="localhost", port=5432)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (vendor_name,))
        # get the generated id back
        # vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    # return vendor_id

# insert_vendor('This food is atrocious')


print('waiting')

# response = cursor.query("""
# SELECT ChatGPT(
#   "Is the review positive or negative. Only reply 'positive' or 'negative'. Here are examples. The food is very bad: negative. The food is very good: postive.",
#   review
# )
# FROM postgres_data.review_table;
# """).df()

# print(response)

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
    print("Executing the action...")

    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        # Read the entire file content
        file_content = file.read()
        print('File content: ' + file_content)

    insert_vendor(file_content)
    
    # full_response = cursor.query("""
    #     SELECT ChatGPT(
    #     "Is this review: {file_content} positive or negative. Only reply 'positive' or 'negative'."
    #     )
    #      """).df() 
    

    # full_response = cursor.query("""
    #     SELECT ChatGPT(
    #     "Review: I hate this food. Rate this review positive or negative. Only reply 'positive' or 'negative'."
    #     )
    #      """)
    
    
    # cursor.query("""
    #     USE postgres_data {
    #     INSERT INTO review_table (review) VALUES ('{file_content}')
    #     }
    #     """).df()

    

    # full_response = cursor.query("""
    #     SELECT ChatGPT(
    #     "Is the review positive or negative. Only reply 'positive' or 'negative'. Here are examples. The food is very bad: negative. The food is very good: postive.",
    #     review
    #     )
    #     FROM postgres_data.review_table;
    #     """).df()
    # full_response = "place holder"


    # query = f"""Use this as an example: {context}
    # Is this statement positive or negative: {file_content}. Respond with only 'positive' or 'negative'. Do not respond in table format
    # """
    # print(query)
    # full_response = llm.generate(query)

    # query = f"""
    #     SELECT ChatGPT(
    #     "Review: {file_content}. Rate this review positive or negative. Only reply 'positive' or 'negative'.",
    #     review
    #     )
    #     FROM postgres_data.review_table;
    #     """
    # query = """SELECT review FROM review_table;"""
    

    query = f"""
        SELECT ChatGPT(
        "Review: {file_content}. Rate this review positive or negative. Only reply 'positive' or 'negative'."
        );
        """
    full_response = cursor.query(query).df()


    print(full_response.iloc[0]['chatgpt.response'])

    file_path = 'response.txt'
    with open(file_path, 'w') as file:
        file.write(full_response.iloc[0]['chatgpt.response'])

# Replace with your file path
file_path_to_watch = 'input.txt'

watch_file(file_path_to_watch)

