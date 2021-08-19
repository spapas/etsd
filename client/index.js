const path = require("path");
const { app, BrowserWindow, protocol } = require('electron')
if (require('electron-squirrel-startup')) return app.quit();

var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);


function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
        }
    })
    
    win.loadURL('https://news.ycombinator.com')
    
}

app.whenReady().then(() => {
    
    createWindow()

    app.on('activate', function() {
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})


app.on('window-all-closed', function() {
    if (process.platform !== 'darwin') app.quit()
})