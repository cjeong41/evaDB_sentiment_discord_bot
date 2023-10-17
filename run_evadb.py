import os
import time
import evadb
import MySQLdb
from gpt4all import GPT4All

# source "/Users/chrisjeong/evadb-venv/bin/activate"
# python -m run_evadb

# ----local llm-----
# llm = GPT4All("wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin")
llm = GPT4All("ggml-model-gpt4all-falcon-q4_0.bin")
# Connect to EvaDB and get a database cursor for running queries
cursor = evadb.connect().cursor()

# List all the built-in functions in EvaDB
print(cursor.query("SHOW FUNCTIONS;").df())

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
  CREATE TABLE review_table (sentiment VARCHAR(10), review VARCHAR(1000))
}
""").df()

query = """
USE postgres_data {
  INSERT INTO review_table (sentiment, review) VALUES ('positive', 'This food is amazing')
}
"""
cursor.query(query).df()

query = """
USE postgres_data {
  INSERT INTO review_table (sentiment, review) VALUES ('negative', 'This food is terrible')
}
"""
cursor.query(query).df()

context = cursor.query("SELECT * FROM postgres_data.review_table;").df()
# context = cursor.query("SELECT sentiment FROM postgres_data.review_table;").df()

print(context)


# conn = MySQLdb.connect(host='localhost', user='postgres', passwd='evadb546', db='postgres')
# cursor = conn.cursor()
# cursor_dict = conn.cursor(MySQLdb.cursors.DictCursor)
# cursor.execute("SELECT sentiment, review FROM review_table")
# result_set = cursor.fetchall()
# for row in result_set:
#     print(row["sentiment"])
    # print "%s, %s" % (row["name"], row["category"])


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

    query = f"""Use this as an example: {context}
    Is this statement positive or negative: {file_content}. Respond with only 'positive' or 'negative'. Do not respond in table format
    """
    print(query)


    full_response = llm.generate(query)
    print('full_response: ' + full_response)

    file_path = 'response.txt'
    with open(file_path, 'w') as file:
        # full_response = "pos"
        file.write(full_response)

# Replace with your file path
file_path_to_watch = 'input.txt'

watch_file(file_path_to_watch)
