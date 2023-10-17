const MindsDBCloud = require('mindsdb-js-sdk');

async function connectToMindsDBCloud() {
    try {
      await MindsDBCloud.connect({
        user: process.env.MINDSDB_USER,
        password: process.env.MINDSDB_PASS,
      });
      console.log("Suceesfully connected to MindsDB Cloud");
    } catch (error) {
      console.log("Problem connecting to MindsDB Cloud:", error);
      throw error;
    }
  }
 
async function analyzeTextSentiment(message) {
let retries = 3; // Maximum number of retries

while (retries > 0) {
    try {
    const text = `SELECT sentiment FROM ${sentimentmodel} WHERE comment='${message}'`;
    const sentimentResponse = await MindsDBCloud.SQL.runQuery(text);
    if (!sentimentResponse.rows) {
        throw new Error("Invalid response from MindsDB");
    }
    return sentimentResponse;
    } catch (error) {
    console.log("Error analyzing sentiment:", error);
    retries--;
    if (retries === 0) {
        throw new Error("Maximum number of retries reached");
    }
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait for 1 second before retrying
    }
}
}
// module.exports = analyzeTextSentiment();

// module.exports = connectToMindsDBCloud();
// exports.connectToMindsDBCloud() = connectToMindsDBCloud();
