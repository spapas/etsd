console.log("PRELOAD")

const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld(
  'electron',
  {
    doThing: () => console.log("DO A TING")
  }
)