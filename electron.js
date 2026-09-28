import { app, BrowserWindow, ipcMain } from 'electron'
import path from 'node:path'
import { access, mkdtemp, rm, writeFile } from 'node:fs/promises'
import os from 'node:os'
import { spawn } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const MODEL_CANDIDATES = [
  path.join(__dirname, 'models', 'resistor_classifier.pt'),
  path.join(__dirname, 'models', 'resistor_detector.pt'),
  path.join(__dirname, 'models', 'best.pt'),
]

function getPythonExecutable() {
  const candidates = [
    process.env.PYTHON_PATH,
    path.join(__dirname, '.venv', 'Scripts', 'python.exe'),
    path.join(__dirname, '.venv', 'Scripts', 'python'),
    'python',
  ]

  return candidates.find(Boolean) || 'python'
}

async function resolveModelPath() {
  for (const candidate of MODEL_CANDIDATES) {
    try {
      await access(candidate)
      return candidate
    } catch {
      // Ignore missing weight files; the app falls back gracefully.
    }
  }

  return null
}

function runDetectorScript(imageDataUrl, modelPath) {
  return new Promise(async (resolve) => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), 'resistor-detector-'))
    const tempImagePath = path.join(tempDir, `resistor-${Date.now()}.png`)
    const scriptPath = path.join(__dirname, 'scripts', 'detect_resistor.py')
    const pythonExecutable = getPythonExecutable()

    const base64 = imageDataUrl.replace(/^data:image\/[a-zA-Z0-9.+-]+;base64,/, '')

    const cleanup = async () => {
      try {
        await rm(tempDir, { recursive: true, force: true })
      } catch {
        // Best effort cleanup only.
      }
    }

    try {
      await writeFile(tempImagePath, Buffer.from(base64, 'base64'))

      const child = spawn(pythonExecutable, [scriptPath, tempImagePath, modelPath || ''], {
        stdio: ['ignore', 'pipe', 'pipe'],
      })

      let stdout = ''

      child.stdout.on('data', (chunk) => {
        stdout += chunk.toString()
      })

      child.stderr.on('data', () => {
        // Ignore stderr noise while the detection script falls back to empty results.
      })

      child.on('error', async () => {
        await cleanup()
        resolve({ detections: [] })
      })

      child.on('close', async () => {
        await cleanup()

        try {
          const payload = JSON.parse(stdout || '{"detections": []}')
          resolve({
            detections: Array.isArray(payload.detections) ? payload.detections : [],
            classification: payload.classification && typeof payload.classification.label === 'string'
              ? payload.classification
              : null,
          })
        } catch {
          resolve({ detections: [] })
        }
      })
    } catch {
      await cleanup()
      resolve({ detections: [] })
    }
  })
}

ipcMain.handle('resistor:detect', async (_event, imageDataUrl) => {
  if (!imageDataUrl || typeof imageDataUrl !== 'string') {
    return { detections: [] }
  }

  const modelPath = await resolveModelPath()
  return runDetectorScript(imageDataUrl, modelPath)
})

const devServerUrl = process.env.VITE_DEV_SERVER_URL

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1500,
    height: 960,
    minWidth: 1200,
    minHeight: 820,
    backgroundColor: '#0f172a',
    autoHideMenuBar: true,
    title: 'Resistor Value Identifier',
    icon: path.join(__dirname, 'icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  })

  mainWindow.maximize()

  if (devServerUrl) {
    mainWindow.loadURL(devServerUrl)
    mainWindow.webContents.openDevTools({ mode: 'detach' })
  } else {
    mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'))
  }
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
