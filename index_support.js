function waitForFileUpdate(filePath) {
    const fs = require('fs');
    return new Promise((resolve) => {
      const watcher = fs.watch(filePath, (event, filename) => {
        if (event === 'change' && filename) {
          watcher.close();
          resolve();
        }
      });
    });
  }

module.exports = {
    waitForFileUpdate
};