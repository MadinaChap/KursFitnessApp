const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow () {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true // Включить доступ к Node.js API в процессе рендеринга
    }
  });

  mainWindow.loadFile('main/main_page.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

// Запуск сервера на Python
const pythonServer = spawn('python', ['path/to/your/server.py']);

pythonServer.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

pythonServer.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

pythonServer.on('close', (code) => {
  console.log(`child process exited with code ${code}`);
});
