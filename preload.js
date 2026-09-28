const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('__RESISTOR_DETECTOR__', {
  async detect(image) {
    if (!image || typeof image === 'string') {
      return null
    }

    const canvas = document.createElement('canvas')
    canvas.width = image.naturalWidth || image.width
    canvas.height = image.naturalHeight || image.height
    const context = canvas.getContext('2d')
    if (!context) {
      return null
    }

    context.drawImage(image, 0, 0, canvas.width, canvas.height)
    const dataUrl = canvas.toDataURL('image/png')
    return ipcRenderer.invoke('resistor:detect', dataUrl)
  },
})
