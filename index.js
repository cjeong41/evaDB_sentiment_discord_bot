require('dotenv').config();
const express = require('express');
const app = express();
const Discord = require('discord.js');
const bodyParser = require("body-parser");
// const MindsDBCloud = require('mindsdb-js-sdk');


// const { connectToMindsDBCloud, analyzeTextSentiment} = require("./dispatcher/mindsdb.js")
const { connectToMindsDBCloud, analyzeTextSentiment} = require("./mindsdb")

const client = new Discord.Client({ intents: [
  Discord.GatewayIntentBits.Guilds,
  Discord.GatewayIntentBits.GuildMessages,
  Discord.GatewayIntentBits.MessageContent
]})

// async methods for analysis 

// async function connectToMindsDBCloud() {
//   try {
//     await MindsDBCloud.connect({
//       user: process.env.MINDSDB_USER,
//       password: process.env.MINDSDB_PASS,
//     });
//     console.log("Suceesfully connected to MindsDB Cloud");
//   } catch (error) {
//     console.log("Problem connecting to MindsDB Cloud:", error);
//     throw error;
//   }
// }

// async function analyzeTextSentiment(message) {
//   let retries = 3; // Maximum number of retries
  
//   while (retries > 0) {
//       try {
//       const text = `SELECT sentiment FROM ${sentimentmodel} WHERE comment='${message}'`;
//       const sentimentResponse = await MindsDBCloud.SQL.runQuery(text);
//       if (!sentimentResponse.rows) {
//           throw new Error("Invalid response from MindsDB");
//       }
//       return sentimentResponse;
//       } catch (error) {
//       console.log("Error analyzing sentiment:", error);
//       retries--;
//       if (retries === 0) {
//           throw new Error("Maximum number of retries reached");
//       }
//       await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait for 1 second before retrying
//       }
//   }
//   }
// async function analyzeTextSentiment(message) {
//   let retries = 3; // Maximum number of retries
  
//   while (retries > 0) {
//       try {
//       // const text = `SELECT sentiment FROM ${sentimentmodel} WHERE comment='${message}'`;
//       // const sentimentResponse = await MindsDBCloud.SQL.runQuery(text);
//       // if (!sentimentResponse.rows) {
//       //     throw new Error("Invalid response from MindsDB");
//       // }
//       return sentimentResponse;
//       } catch (error) {
//       console.log("Error analyzing sentiment:", error);
//       retries--;
//       if (retries === 0) {
//           throw new Error("Maximum number of retries reached");
//       }
//       await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait for 1 second before retrying
//       }
//   }
//   }





app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('/', (req, res) => {
  res.send('Discord bot is running!');
});

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('messageCreate', async (message) => {
  if (message.author.bot) return;

  if (message.content.startsWith('!sentiment')) {
    const query = message.content.slice(10).trim();

    const fs = require('fs');
    file_path = 'input.txt'
    // fs.writeFile(file_path, '', (err) => {
    //   if (err) throw err;
    //   console.log('File cleared!');
    // });
    // const content = 'This is the content of the file.';
    fs.writeFile(file_path, query, (err) => {
      if (err) throw err;
      console.log('File saved!');
    });
    
    // await connectToMindsDBCloud();
    // const response = await analyzeTextSentiment(query); 
    

    const filePath = 'response.txt';  // Replace with your file path

    const { waitForFileUpdate } = require('./index_support.js');

    await waitForFileUpdate(filePath)
    // (async () => {
    //   console.log('Waiting for file update...');
    //   await waitForFileUpdate(filePath);
    //   console.log('File has been updated!');
    // })();

    // filePath = "response.txt"
    sentiment = "None sentiment"
    response = "None response"
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) {
        console.error(err);
        return;
      }
      console.log('File contents after input:' + data);
      // console.log(data);
      response = query + " -> " + data;
      console.log("result----->",response);
      sentiment = data;
    });

    function waitUsingCallback(delay, callback) {
      setTimeout(() => {
        console.log(`Waited for ${delay} milliseconds.`);
        callback();
      }, delay);
    }
    
    console.log('Before wait');
    waitUsingCallback(2000, () => {
      console.log('After wait');
      message.reply(JSON.stringify(response));
    });

    // filePath = 'response.txt'
    // await waitForFileUpdate(filePath)
    
    // console.log('sentiment: ' + data)
    // response = query + " -> " + sentiment;
    // console.log("result----->",response);
    // message.reply(JSON.stringify(response.rows[0]));
    // message.reply(JSON.stringify(response));
  }
});

client.login(process.env.DISCORD_BOT_ID);
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Express app is listening on port ${PORT}!`);
});

// require('dotenv').config()
// const { Client, IntentsBitField } = require('discord.js')
// const client = new Client({
//     intents: [
//         IntentsBitField.Flags.Guilds,
//         IntentsBitField.Flags.GuildMembers,
//         IntentsBitField.Flags.GuildMessages,
//         IntentsBitField.Flags.MessageContent
//     ]
// })

// client.login(process.env.DISCORD_BOT_ID)

// client.on('ready', () => {
//     console.log('logged in as ${client.user.tag}!')
// })

