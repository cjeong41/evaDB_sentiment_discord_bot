# evaDB_sentiment_discord_bot
Using evaDB and a discord bot with node.js to get analyzed sentiments from text inputs


# Implementation details:
For the implementation of this project, I used EvaDB, PostgresQL, Node.js (for Discord), and OpenAI’s API. 

- The “!sentiment” command allows the user to see the sentiment of a provided message. So, the user would input “!sentiment <user input text>”. In response, the bot would output whether the overall sentiment is positive or negative. This command would also put that message or <user input text> into a PostgreSQL database that will be used for !summary.
- The “!summary” command allows the user to see an overall sentiment response of the messages/data currently in the PostgreSQL database. The user would input “!summary <any input>”. In response, the bot will go through the messages currently in the database and briefly output and describe the overall sentiment.

For transparency, here is a description of the main files within the project and their purpose: 
- index.js: File used to run the discord bot. Handles taking in the user input and outputting the response into the Discord channel. 
- index_support.js: Contains the waitForFileUpdate function used within index.js. 
- run_openai.py: Handles !sentiment. Connects to EvaDB, PostgreSQL, and ChatGPT to generate appropriate responses.
- input.txt: Holds user input for !sentiment.
- output.txt: Holds response for !sentiment.  
- run_summary.py: Handles !summary. Connects to EvaDB, PostgreSQL, and ChatGPT to generate appropriate responses.
- summaryInput.txt: Holds user input for !summary.
- summaryOutput.txt: Holds response for !summary. 


# Instructions to run:
Make sure you have all modules present in the requirements.txt file downloaded. If not, download them using pip install.
Create your own discord bot within a server and get your Discord token.
Create a .env file and have two variables. Like so:
DISCORD_BOT_ID=<your discord bot id>
OPENAI_API_KEY=<your openAI API key>
Have a local PostgreSQL server running, and input your appropriate parameters for user, password, host, port, and database. Edit the already existing postgres_connect_query parameters within run_openai.py and run_summary.py.
Have three terminals open, so that you can simultaneously run run_openai.py, run_summary.py, and index.js.
Start chatting away :)


# Implications:
In terms of the use cases of these features, a user may want to see the overall sentiment of a message that is in a Discord channel. This bot could be easily implemented within a server so that these commands would be up and running in no time. 
- The !sentiment command would be useful so that if a user wants to see the overall sentiment of a long or complex message that someone has sent, they can input it into the bot, and the bot will let the user know whether the sentiment is positive or negative.
- The !summary command would be useful for users who may have just entered the channel and want to see the overall sentiment of the messages within the channel.
These commands give more range to Discord users so that they can easily identify and find out the mood or direction of discussion within Discord channels, offering more transparency and communication to facilitate a flowing conversation. 

