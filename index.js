require('dotenv').config();
const express = require('express');
const app = express();
const Discord = require('discord.js');
const bodyParser = require("body-parser");

const client = new Discord.Client({ intents: [
  Discord.GatewayIntentBits.Guilds,
  Discord.GatewayIntentBits.GuildMessages,
  Discord.GatewayIntentBits.MessageContent
]})

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