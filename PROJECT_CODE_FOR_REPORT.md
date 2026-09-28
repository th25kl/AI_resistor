# Resistor Value Identifier: Project Code

This appendix contains the application source code, detector and training scripts, tests, and text configuration files.

Images, trained model weights, generated training splits, `node_modules`, and `package-lock.json` are excluded.

## `README.md`

````markdown
# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Train the Resistor Classifier

The images are stored flat in `resistor_dataset/`. Their class labels are kept separately in `resistor_dataset_labels.csv`, with `image` and `class` columns. The training script creates a reproducible 80/10/10 train, validation, and test split, then fine-tunes an Ultralytics image classifier. It writes the model used by the Electron app to `models/resistor_classifier.pt`.

From the project root in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-ml.txt
.\.venv\Scripts\python.exe scripts\train_resistor_classifier.py --epochs 50
npm run electron:dev
```

The first training run downloads the pretrained `yolo11n-cls.pt` starting model. Training automatically uses CUDA when available and otherwise runs on CPU. To recreate the generated split after adding or changing source images, add `--rebuild` to the training command. Test top-1 accuracy is printed after training. The app uses the predicted resistor class and confidence when weights exist, and retains its image-analysis fallback otherwise.

## Expanding the Oxlint configuration

If you are developing a production application, we recommend enabling type-aware lint rules by installing `oxlint-tsgolint` and editing `.oxlintrc.json`:

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["react", "typescript", "oxc"],
  "options": {
    "typeAware": true
  },
  "rules": {
    "react/rules-of-hooks": "error",
    "react/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
```

See the [Oxlint rules documentation](https://oxc.rs/docs/guide/usage/linter/rules) for the full list of rules and categories.
````

## `.gitignore`

```text
# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
.venv/
training-data/
runs/
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
```

## `.oxlintrc.json`

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["react", "typescript", "oxc"],
  "rules": {
    "react/rules-of-hooks": "error",
    "react/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
```

## `package.json`

```json
{
  "name": "resistor-ai-project",
  "private": true,
  "version": "0.0.0",
  "main": "electron.js",
  "type": "module",
  "build": {
    "appId": "com.resistor.value.identifier",
    "productName": "Resistor Value Identifier",
    "win": {
      "icon": "icon.ico"
    },
    "directories": {
      "output": "release-builds"
    },
    "files": [
      "dist/**/*",
      "electron.js",
      "icon.png",
      "icon.ico"
    ]
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "oxlint",
    "preview": "vite preview",
    "test": "vitest run",
    "electron": "electron .",
    "electron:dev": "set VITE_DEV_SERVER_URL=http://localhost:5175&& concurrently \"npm run dev -- --host 0.0.0.0 --port 5175 --strictPort\" \"wait-on http://localhost:5175/ && electron .\"",
    "electron:build": "npm run build && electron-builder"
  },
  "dependencies": {
    "react": "^19.2.8",
    "react-dom": "^19.2.8"
  },
  "devDependencies": {
    "@types/node": "^24.13.3",
    "@types/react": "^19.2.18",
    "@types/react-dom": "^19.2.7",
    "@vitejs/plugin-react": "^6.1.1",
    "concurrently": "^10.0.5",
    "electron": "^44.4.5",
    "electron-builder": "^26.15.3",
    "oxlint": "^1.81.0",
    "typescript": "~6.0.2",
    "vite": "^8.3.0",
    "vitest": "^5.0.1",
    "wait-on": "^9.1.0"
  }
}
```

## `requirements-ml.txt`

```text
ultralytics>=8.3.0,<9
```

## `data.yaml`

```yaml
train: ../train/images
val: ../valid/images
test: ../test/images

nc: 56
names: ['1.2k ohms', '1.5k ohms', '1.8k ohms', '10 ohms', '100 ohms', '100k ohms', '100k ohms 5 bands', '10k ohms', '120 ohms', '12k ohms', '15 ohms', '150 ohms', '15k ohms', '180 ohms', '18k ohms', '1k ohms', '2.2k ohms', '2.2k ohms 5 bands', '2.7k ohms', '200 ohms 5 bands', '22 ohms 5 bands', '220 ohms', '22k ohms', '270 ohms', '27k ohms', '3.3k ohms', '3.9k ohms', '300k ohms 5 bands', '33 ohms', '330 ohms', '33k ohms', '390 ohms', '39k ohms', '4.7 ohms', '4.7k ohms', '4.7k ohms 5 bands', '47 ohms', '470 ohms', '470k ohms 5 bands', '47k ohms', '47k ohms 5 bands', '5.1k ohms 5 bands', '5.6 ohms', '5.6k ohms', '51k ohms 5 bands', '56 ohms', '560 ohms', '56k ohms', '58 ohms', '6.8k ohms', '680 ohms', '68k ohms', '8.2k ohms', '82 ohms', '820 ohms', 'busted']

roboflow:
  workspace: resistor-color-code
  project: resistors-color
  version: 1
  license: CC BY 4.0
  url: https://universe.roboflow.com/resistor-color-code/resistors-color/dataset/1
```

## `index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>resistor-ai-project</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

## `vite.config.ts`

```typescript
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [react()],
})
```

## `tsconfig.json`

```json
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ]
}
```

## `tsconfig.app.json`

```json
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "target": "es2023",
    "lib": ["ES2023", "DOM"],
    "module": "esnext",
    "types": ["vite/client"],
    "allowArbitraryExtensions": true,
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "erasableSyntaxOnly": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
```

## `tsconfig.node.json`

```json
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.node.tsbuildinfo",
    "target": "es2023",
    "lib": ["ES2023"],
    "types": ["node"],
    "skipLibCheck": true,

    /* Bundler mode */
    "module": "nodenext",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,

    /* Linting */
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "erasableSyntaxOnly": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["vite.config.ts"]
}
```

## `electron.js`

```javascript
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
```

## `preload.js`

```javascript
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
```

## `launch-app.vbs`

```text
Option Explicit

Dim shell, projectPath, electronPath, command
Set shell = CreateObject("WScript.Shell")
projectPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
electronPath = projectPath & "\node_modules\electron\dist\electron.exe"
command = """" & electronPath & """ """ & projectPath & """"
shell.Run command, 0, False
```

## `launch-electron.ps1`

```text
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$electronExe = Join-Path $projectPath "node_modules\electron\dist\electron.exe"

if (-not (Test-Path $electronExe)) {
    throw "Electron executable not found: $electronExe"
}

Start-Process -FilePath $electronExe -ArgumentList "`"$projectPath`"" -WorkingDirectory $projectPath
```

## `run-app.bat`

```bat
@echo off
setlocal
set "NODE_PATH=C:\Program Files\nodejs"
set "PATH=%NODE_PATH%;%PATH%"
cd /d "%~dp0"
npm run electron:dev
```

## `run-app.cmd`

```text
@echo off
setlocal
cd /d "%~dp0"
start "" /B "%~dp0\node_modules\.bin\electron.cmd" "%~dp0"
```

## `scripts/detect_resistor.py`

```python
import json
import os
import sys
from pathlib import Path

image_path = sys.argv[1] if len(sys.argv) > 1 else ''
model_path = sys.argv[2] if len(sys.argv) > 2 else ''

if not image_path or not os.path.exists(image_path):
    print(json.dumps({"detections": []}))
    sys.exit(0)

candidate_paths = []
if model_path:
    candidate_paths.append(model_path)

project_root = Path(__file__).resolve().parent.parent
candidate_paths.extend([
    str(project_root / 'models' / 'resistor_classifier.pt'),
    str(project_root / 'models' / 'resistor_detector.pt'),
    str(project_root / 'models' / 'best.pt'),
])

resolved_model = next((value for value in candidate_paths if value and os.path.exists(value)), '')
if not resolved_model:
    print(json.dumps({"detections": []}))
    sys.exit(0)

try:
    from ultralytics import YOLO

    model = YOLO(resolved_model)
    image_size = 224 if model.task == 'classify' else 640
    results = model(str(image_path), conf=0.25, imgsz=image_size, verbose=False)

    detections = []
    classification = None
    for result in results:
        if result.probs is not None:
            class_id = int(result.probs.top1)
            classification = {
                'label': str(result.names[class_id]),
                'confidence': float(result.probs.top1conf),
            }
            continue

        if result.boxes is None:
            continue

        boxes = result.boxes
        for index in range(len(boxes)):
            box = boxes[index]
            xyxy = box.xyxy[0].tolist()
            detections.append({
                'classId': int(box.cls[0]),
                'confidence': float(box.conf[0]),
                'box': {
                    'x1': float(xyxy[0]),
                    'y1': float(xyxy[1]),
                    'x2': float(xyxy[2]),
                    'y2': float(xyxy[3]),
                },
            })

    print(json.dumps({"detections": detections, "classification": classification}))
except Exception:
    print(json.dumps({"detections": []}))
    sys.exit(0)
```

## `scripts/export_project_report.py`

````python
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / 'PROJECT_CODE_FOR_REPORT.md'
REPORT_FILES = [
    'README.md',
    '.gitignore',
    '.oxlintrc.json',
    'package.json',
    'requirements-ml.txt',
    'data.yaml',
    'index.html',
    'vite.config.ts',
    'tsconfig.json',
    'tsconfig.app.json',
    'tsconfig.node.json',
    'electron.js',
    'preload.js',
    'launch-app.vbs',
    'launch-electron.ps1',
    'run-app.bat',
    'run-app.cmd',
    'scripts/detect_resistor.py',
    'scripts/export_project_report.py',
    'scripts/train_resistor_classifier.py',
    'src/App.tsx',
    'src/App.css',
    'src/bandVision.ts',
    'src/bandVision.test.ts',
    'src/detector.ts',
    'src/detector.test.ts',
    'src/index.css',
    'src/main.tsx',
    'src/resistorCalculator.ts',
    'src/resistorCalculator.test.ts',
]

LANGUAGES = {
    '.bat': 'bat',
    '.css': 'css',
    '.html': 'html',
    '.js': 'javascript',
    '.json': 'json',
    '.md': 'markdown',
    '.py': 'python',
    '.ts': 'typescript',
    '.tsx': 'tsx',
    '.txt': 'text',
    '.yaml': 'yaml',
}


def main() -> None:
    sections = [
        '# Resistor Value Identifier: Project Code',
        '',
        'This appendix contains the application source code, detector and training scripts, tests, and text configuration files.',
        '',
        'Images, trained model weights, generated training splits, `node_modules`, and `package-lock.json` are excluded.',
        '',
    ]

    for relative_path in REPORT_FILES:
        file_path = PROJECT_ROOT / relative_path
        if not file_path.is_file():
            raise FileNotFoundError(f'Required report source file is missing: {relative_path}')

        content = file_path.read_text(encoding='utf-8').rstrip()
        language = LANGUAGES.get(file_path.suffix.lower(), 'text')
        fence = '````' if '```' in content else '```'
        sections.extend([
            f'## `{relative_path}`',
            '',
            f'{fence}{language}',
            content,
            fence,
            '',
        ])

    OUTPUT_FILE.write_text('\n'.join(sections), encoding='utf-8')
    print(f'Wrote {OUTPUT_FILE.relative_to(PROJECT_ROOT)} ({len(REPORT_FILES)} files).')


if __name__ == '__main__':
    main()
````

## `scripts/train_resistor_classifier.py`

```python
import argparse
import csv
import random
import shutil
from pathlib import Path

from ultralytics import YOLO


IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def discover_classes(source: Path, labels_file: Path) -> dict[str, list[Path]]:
    if not source.is_dir():
        raise FileNotFoundError(f'Image folder not found: {source}')
    if not labels_file.is_file():
        raise FileNotFoundError(f'Class labels CSV not found: {labels_file}')

    classes: dict[str, list[Path]] = {}
    with labels_file.open(newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        if not {'image', 'class'}.issubset(reader.fieldnames or []):
            raise ValueError('The labels CSV must have image and class columns.')

        for row in reader:
            image_name = (row.get('image') or '').strip()
            class_name = (row.get('class') or '').strip()
            if not image_name or not class_name or Path(image_name).name != image_name:
                raise ValueError(f'Invalid image/class row in {labels_file}: {row}')

            image_path = source / image_name
            if image_path.suffix.lower() not in IMAGE_EXTENSIONS or not image_path.is_file():
                raise FileNotFoundError(f'Labeled image is missing: {image_path}')
            classes.setdefault(class_name, []).append(image_path)

    classes = {name: sorted(images) for name, images in classes.items()}
    if not classes:
        raise RuntimeError(f'No labeled images found in {labels_file}')

    too_small = [name for name, images in classes.items() if len(images) < 3]
    if too_small:
        raise RuntimeError(f'Each class needs at least 3 images; too few: {", ".join(too_small)}')

    return classes


def prepare_dataset(classes: dict[str, list[Path]], output: Path, seed: int, rebuild: bool) -> None:
    if output.exists():
        if not rebuild:
            raise FileExistsError(f'{output} already exists. Pass --rebuild to regenerate this dataset.')
        shutil.rmtree(output)

    rng = random.Random(seed)
    for class_name, images in classes.items():
        shuffled = list(images)
        rng.shuffle(shuffled)
        test_count = max(1, round(len(shuffled) * 0.1))
        val_count = max(1, round(len(shuffled) * 0.1))
        splits = {
            'test': shuffled[:test_count],
            'val': shuffled[test_count:test_count + val_count],
            'train': shuffled[test_count + val_count:],
        }

        for split_name, split_images in splits.items():
            destination = output / split_name / class_name
            destination.mkdir(parents=True, exist_ok=True)
            for source_image in split_images:
                target = destination / source_image.name
                try:
                    target.hardlink_to(source_image)
                except OSError:
                    shutil.copy2(source_image, target)

        print(f'{class_name}: {len(splits["train"])} train, {len(splits["val"])} val, {len(splits["test"])} test')


def main() -> None:
    parser = argparse.ArgumentParser(description='Train a resistor-value classifier from a flat image folder and labels CSV.')
    parser.add_argument('--source', type=Path, default=PROJECT_ROOT / 'resistor_dataset', help='Folder containing the resistor images.')
    parser.add_argument('--labels', type=Path, default=PROJECT_ROOT / 'resistor_dataset_labels.csv', help='CSV file with image and class columns.')
    parser.add_argument('--data', type=Path, default=PROJECT_ROOT / 'training-data' / 'resistor-values', help='Generated train/val/test dataset directory.')
    parser.add_argument('--weights', type=Path, default=PROJECT_ROOT / 'models' / 'resistor_classifier.pt', help='Output model weights path.')
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--imgsz', type=int, default=224)
    parser.add_argument('--batch', type=int, default=16)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--rebuild', action='store_true', help='Recreate the generated dataset directory if it already exists.')
    args = parser.parse_args()

    source = args.source.resolve()
    labels_file = args.labels.resolve()
    data_dir = args.data.resolve()
    weights_path = args.weights.resolve()
    classes = discover_classes(source, labels_file)
    print(f'Found {len(classes)} resistor classes and {sum(map(len, classes.values()))} images.')
    prepare_dataset(classes, data_dir, args.seed, args.rebuild)

    model = YOLO('yolo11n-cls.pt')
    model.train(
        data=str(data_dir),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        patience=10,
        seed=args.seed,
        project=str(PROJECT_ROOT / 'runs' / 'classify'),
        name='resistor-values',
        exist_ok=True,
    )

    best_weights = PROJECT_ROOT / 'runs' / 'classify' / 'resistor-values' / 'weights' / 'best.pt'
    if not best_weights.is_file():
        raise FileNotFoundError(f'Training finished without producing {best_weights}')

    weights_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(best_weights, weights_path)
    print(f'Trained classifier saved to: {weights_path}')

    trained_model = YOLO(str(weights_path))
    metrics = trained_model.val(data=str(data_dir), split='test', imgsz=args.imgsz)
    print(f'Test top-1 accuracy: {metrics.top1:.4f}')


if __name__ == '__main__':
    main()
```

## `src/App.tsx`

```tsx
import { useMemo, useState } from 'react'
import './App.css'
import { normalizeDetectorResult, type DetectorDetection } from './detector'
import { detectColorBandSequence } from './bandVision'
import { decodeResistor, type BandType, type ResistorColor } from './resistorCalculator'

declare global {
  interface Window {
    __RESISTOR_DETECTOR__?: {
      detect: (image: HTMLImageElement) => Promise<{
        detections?: DetectorDetection[]
        classification?: { label: string; confidence: number } | null
      } | DetectorDetection[] | null>
    }
  }
}

type DetectionState = {
  status: 'idle' | 'processing' | 'success' | 'warning' | 'error'
  message: string
  bands: string[]
  resistance: string
  tolerance: string
  bandEstimate: string
  confidence: number
  imageUrl: string | null
}

const colors: ResistorColor[] = [
  'black',
  'brown',
  'red',
  'orange',
  'yellow',
  'green',
  'blue',
  'violet',
  'grey',
  'white',
  'gold',
  'silver',
]

const colorHex: Record<ResistorColor, string> = {
  black: '#000000',
  brown: '#7c3f0f',
  red: '#d32525',
  orange: '#f59e0b',
  yellow: '#facc15',
  green: '#16a34a',
  blue: '#2563eb',
  violet: '#7c3aed',
  grey: '#6b7280',
  white: '#f8fafc',
  gold: '#d4af37',
  silver: '#cbd5e1',
}

const bandNames = ['1st band', '2nd band', '3rd band', '4th band', '5th band']

const defaultDetectionState: DetectionState = {
  status: 'idle',
  message: 'Upload a resistor image to start analysis.',
  bands: [],
  resistance: '',
  tolerance: '',
  bandEstimate: '',
  confidence: 0,
  imageUrl: null,
}

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max)
}

function rgbToHex(r: number, g: number, b: number) {
  const toHex = (value: number) => value.toString(16).padStart(2, '0')
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`
}

function getNearestColor(hexColor: string): ResistorColor {
  const rgb = hexColor.replace('#', '')
  const r = Number.parseInt(rgb.slice(0, 2), 16)
  const g = Number.parseInt(rgb.slice(2, 4), 16)
  const b = Number.parseInt(rgb.slice(4, 6), 16)
  const brightness = (r + g + b) / 3
  const maximum = Math.max(r, g, b)
  const minimum = Math.min(r, g, b)
  const saturation = maximum === 0 ? 0 : (maximum - minimum) / maximum

  if (brightness < 52) {
    return 'black'
  }
  if (saturation < 0.14 && brightness < 155) {
    return 'grey'
  }
  if (saturation < 0.12 && brightness >= 155) {
    return 'white'
  }

  let nearestColor: ResistorColor = 'black'
  let minimumDistance = Number.POSITIVE_INFINITY

  for (const color of colors) {
    const target = colorHex[color].replace('#', '')
    const tr = Number.parseInt(target.slice(0, 2), 16)
    const tg = Number.parseInt(target.slice(2, 4), 16)
    const tb = Number.parseInt(target.slice(4, 6), 16)

    const distance = (r - tr) ** 2 + (g - tg) ** 2 + (b - tb) ** 2
    if (distance < minimumDistance) {
      minimumDistance = distance
      nearestColor = color
    }
  }

  return nearestColor
}

function readFileAsDataUrl(file: File) {
  return new Promise<string>((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(String(reader.result))
    reader.onerror = () => reject(new Error('Unable to read image file.'))
    reader.readAsDataURL(file)
  })
}

function parseResistanceLabel(label: string) {
  const code = label.split('_')[0].replace(/\s*ohms?$/i, '').trim().toUpperCase()
  const multiplier = (unit?: string) => unit === 'K' ? 1e3 : unit === 'M' ? 1e6 : unit === 'G' ? 1e9 : 1

  let match = code.match(/^(\d+)R(\d+)([KMG]?)$/)
  if (match) {
    return Number(`${match[1]}.${match[2]}`) * multiplier(match[3])
  }

  match = code.match(/^(\d+)([KMG])(\d+)$/)
  if (match) {
    return Number(`${match[1]}.${match[3]}`) * multiplier(match[2])
  }

  match = code.match(/^(\d+(?:\.\d+)?)([RKM]?)$/)
  if (match) {
    return Number(match[1]) * multiplier(match[2])
  }

  return null
}

function createImageFromUrl(url: string) {
  return new Promise<HTMLImageElement>((resolve, reject) => {
    const img = new Image()
    img.onload = () => resolve(img)
    img.onerror = () => reject(new Error('The uploaded file is not a valid image.'))
    img.src = url
  })
}

async function detectWithModel(image: HTMLImageElement) {
  const detector = window.__RESISTOR_DETECTOR__
  if (!detector || typeof detector.detect !== 'function') {
    return null
  }

  const payload = await detector.detect(image)
  if (!Array.isArray(payload) && payload?.classification?.label) {
    return {
      type: 'classification' as const,
      label: payload.classification.label,
      confidence: payload.classification.confidence,
    }
  }

  const detections = Array.isArray(payload) ? payload : payload?.detections

  if (!detections || detections.length === 0) {
    return null
  }

  const normalized = normalizeDetectorResult({
    detections,
    sourceWidth: image.width,
    sourceHeight: image.height,
  })

  return normalized.available ? { type: 'detection' as const, ...normalized } : null
}

function detectResistorBandsFromImage(
  image: HTMLImageElement,
  initialCrop?: { x: number; y: number; width: number; height: number },
) {
  const canvas = document.createElement('canvas')
  const maxWidth = 1000
  const scale = Math.min(1, maxWidth / image.width)
  const width = Math.max(260, Math.round(image.width * scale))
  const height = Math.max(180, Math.round(image.height * scale))
  canvas.width = width
  canvas.height = height

  const context = canvas.getContext('2d')
  if (!context) {
    throw new Error('Canvas is not available in this browser.')
  }

  context.drawImage(image, 0, 0, width, height)
  const imageData = context.getImageData(0, 0, width, height)
  const pixels = imageData.data

  const cropPadding = initialCrop ? 18 : 0

  let cropX = 0
  let cropY = 0
  let cropWidth = width
  let cropHeight = height

  if (initialCrop) {
    const x = clamp(Math.round(initialCrop.x * (width / image.width)) - cropPadding, 0, width - 1)
    const y = clamp(Math.round(initialCrop.y * (height / image.height)) - cropPadding, 0, height - 1)
    const boxWidth = clamp(Math.round(initialCrop.width * (width / image.width)) + cropPadding * 2, 32, width - x)
    const boxHeight = clamp(Math.round(initialCrop.height * (height / image.height)) + cropPadding * 2, 32, height - y)

    cropX = x
    cropY = y
    cropWidth = boxWidth
    cropHeight = boxHeight
  } else {
    const cornerSamples = [
      [0, 0],
      [width - 1, 0],
      [0, height - 1],
      [width - 1, height - 1],
      [Math.floor(width / 2), 0],
      [Math.floor(width / 2), height - 1],
    ]

    let backgroundR = 0
    let backgroundG = 0
    let backgroundB = 0
    for (const [x, y] of cornerSamples) {
      const index = (y * width + x) * 4
      backgroundR += pixels[index]
      backgroundG += pixels[index + 1]
      backgroundB += pixels[index + 2]
    }

    const bgR = Math.round(backgroundR / cornerSamples.length)
    const bgG = Math.round(backgroundG / cornerSamples.length)
    const bgB = Math.round(backgroundB / cornerSamples.length)

    let minX = width
    let minY = height
    let maxX = 0
    let maxY = 0

    for (let row = 0; row < height; row += 1) {
      for (let column = 0; column < width; column += 1) {
        const index = (row * width + column) * 4
        const r = pixels[index]
        const g = pixels[index + 1]
        const b = pixels[index + 2]
        const diff = Math.abs(r - bgR) + Math.abs(g - bgG) + Math.abs(b - bgB)

        if (diff > 90) {
          minX = Math.min(minX, column)
          minY = Math.min(minY, row)
          maxX = Math.max(maxX, column)
          maxY = Math.max(maxY, row)
        }
      }
    }

    if (maxX <= minX || maxY <= minY) {
      throw new Error('The uploaded image does not clearly show a resistor. Try a higher-contrast photo.')
    }

    const pad = Math.max(10, Math.round((maxX - minX) * 0.08))
    cropX = Math.max(0, minX - pad)
    cropY = Math.max(0, minY - pad)
    cropWidth = Math.min(width - cropX, maxX - minX + pad * 2)
    cropHeight = Math.min(height - cropY, maxY - minY + pad * 2)
  }

  const cropCanvas = document.createElement('canvas')
  cropCanvas.width = cropWidth
  cropCanvas.height = cropHeight
  const cropContext = cropCanvas.getContext('2d')
  if (!cropContext) {
    throw new Error('Canvas processing is unavailable in this browser.')
  }

  cropContext.drawImage(canvas, cropX, cropY, cropWidth, cropHeight, 0, 0, cropWidth, cropHeight)
  const cropData = cropContext.getImageData(0, 0, cropWidth, cropHeight)
  const cropPixels = cropData.data
  const visualBands = detectColorBandSequence(cropData)

  if (visualBands.length === 4 || visualBands.length === 5) {
    const detectedType: BandType = visualBands.length === 5 ? '5-band' : '4-band'
    for (const bands of [visualBands, [...visualBands].reverse()]) {
      try {
        return {
          result: decodeResistor(bands, detectedType),
          bandType: detectedType,
          confidence: 90,
          bands,
        }
      } catch {
        continue
      }
    }
  }

  const scoreMap: number[] = new Array(cropWidth).fill(0)
  let bestRow = Math.floor(cropHeight / 2)
  let bestRowScore = 0

  for (let row = 0; row < cropHeight; row += 1) {
    let rowScore = 0
    for (let column = 0; column < cropWidth; column += 2) {
      const index = (row * cropWidth + column) * 4
      const r = cropPixels[index]
      const g = cropPixels[index + 1]
      const b = cropPixels[index + 2]
      const maximum = Math.max(r, g, b)
      const minimum = Math.min(r, g, b)
      const brightness = (r + g + b) / 3
      const saturation = maximum === 0 ? 0 : (maximum - minimum) / maximum

      if (brightness > 105 && saturation < 0.55) {
        rowScore += 1
      }
    }

    if (rowScore > bestRowScore) {
      bestRow = row
      bestRowScore = rowScore
    }
  }

  const rowPadding = Math.max(8, Math.floor(cropHeight * 0.08))
  const midRowStart = Math.max(0, bestRow - rowPadding)
  const midRowEnd = Math.min(cropHeight - 1, bestRow + rowPadding)
  let bodyStart = 0
  let bodyEnd = cropWidth - 1
  let firstBodyColumn = cropWidth
  let lastBodyColumn = -1

  for (let column = 0; column < cropWidth; column += 1) {
    let brightPixels = 0
    for (let row = midRowStart; row <= midRowEnd; row += 1) {
      const index = (row * cropWidth + column) * 4
      const r = cropPixels[index]
      const g = cropPixels[index + 1]
      const b = cropPixels[index + 2]
      const maximum = Math.max(r, g, b)
      const minimum = Math.min(r, g, b)
      const brightness = (r + g + b) / 3
      const saturation = maximum === 0 ? 0 : (maximum - minimum) / maximum

      if (brightness > 115 && saturation < 0.72) {
        brightPixels += 1
      }
    }

    if (brightPixels >= Math.max(2, Math.floor((midRowEnd - midRowStart) * 0.25))) {
      firstBodyColumn = Math.min(firstBodyColumn, column)
      lastBodyColumn = Math.max(lastBodyColumn, column)
    }
  }

  if (lastBodyColumn - firstBodyColumn > cropWidth * 0.12) {
    bodyStart = firstBodyColumn
    bodyEnd = lastBodyColumn
  }

  for (let column = 0; column < cropWidth; column += 1) {
    if (column < bodyStart || column > bodyEnd) {
      continue
    }
    let sum = 0
    let count = 0

    for (let row = midRowStart; row <= midRowEnd; row += 1) {
      const index = (row * cropWidth + column) * 4
      const r = cropPixels[index]
      const g = cropPixels[index + 1]
      const b = cropPixels[index + 2]
      const max = Math.max(r, g, b)
      const minValue = Math.min(r, g, b)
      const saturation = max === 0 ? 0 : (max - minValue) / max
      const brightness = (r + g + b) / 3

      if (brightness > 8 && brightness < 248 && (saturation > 0.12 || brightness < 72)) {
        const darkBandBoost = brightness < 72 ? 0.3 : 0
        sum += saturation + darkBandBoost
        count += 1
      }
    }

    scoreMap[column] = count > 0 ? sum / count : 0
  }

  for (let column = 1; column < cropWidth - 1; column += 1) {
    scoreMap[column] = (scoreMap[column - 1] + scoreMap[column] + scoreMap[column + 1]) / 3
  }

  const threshold = Math.max(0.08, Math.max(...scoreMap) * 0.2)
  const groupings: Array<{ start: number; end: number; strength: number }> = []
  let start = -1
  let strength = 0

  for (let x = 0; x < cropWidth; x += 1) {
    const active = scoreMap[x] > threshold
    if (active && start === -1) {
      start = x
      strength = scoreMap[x]
    } else if (active && start !== -1) {
      strength = Math.max(strength, scoreMap[x])
    }

    if (!active && start !== -1) {
      const widthOfSegment = x - start
      if (widthOfSegment >= 3) {
        groupings.push({ start, end: x - 1, strength })
      }
      start = -1
      strength = 0
    }
  }

  if (start !== -1) {
    const widthOfSegment = cropWidth - start
    if (widthOfSegment >= 3) {
      groupings.push({ start, end: cropWidth - 1, strength })
    }
  }

  let sortedBands = groupings
    .filter((segment) => segment.end - segment.start >= 3 && segment.end - segment.start <= cropWidth * 0.35)
    .sort((a, b) => a.start - b.start)

  if (sortedBands.length < 4) {
    const minimumDistance = Math.max(8, Math.floor(cropWidth * 0.035))
    const peakCandidates: Array<{ start: number; end: number; strength: number }> = []

    for (let column = 1; column < cropWidth - 1; column += 1) {
      if (scoreMap[column] < threshold * 0.7) {
        continue
      }
      if (scoreMap[column] < scoreMap[column - 1] || scoreMap[column] < scoreMap[column + 1]) {
        continue
      }

      const nearbyPeak = peakCandidates.find((candidate) => Math.abs(candidate.start - column) < minimumDistance)
      if (nearbyPeak) {
        if (scoreMap[column] > nearbyPeak.strength) {
          nearbyPeak.start = column
          nearbyPeak.end = column
          nearbyPeak.strength = scoreMap[column]
        }
      } else {
        peakCandidates.push({ start: column, end: column, strength: scoreMap[column] })
      }
    }

    sortedBands = peakCandidates
      .sort((a, b) => b.strength - a.strength)
      .slice(0, 5)
      .map((peak) => ({
        start: Math.max(0, peak.start - Math.floor(minimumDistance / 2)),
        end: Math.min(cropWidth - 1, peak.end + Math.floor(minimumDistance / 2)),
        strength: peak.strength,
      }))
      .sort((a, b) => a.start - b.start)
  }

  if (sortedBands.length < 4 && cropWidth / cropHeight > 1.5) {
    const sampleWidth = Math.max(4, Math.floor(cropWidth * 0.045))
    const sampleCenters = [0.2, 0.4, 0.6, 0.8]
    const bodyWidth = bodyEnd - bodyStart
    sortedBands = sampleCenters.map((position) => {
      const center = Math.floor(bodyStart + bodyWidth * position)
      return {
        start: Math.max(0, center - Math.floor(sampleWidth / 2)),
        end: Math.min(cropWidth - 1, center + Math.floor(sampleWidth / 2)),
        strength: scoreMap[center] ?? 0,
      }
    })
  }

  const strongest = [...sortedBands].sort((a, b) => b.strength - a.strength)
  const horizontalSampleBands = cropWidth / cropHeight > 1.5
    ? [0.2, 0.4, 0.6, 0.8].map((position) => {
        const bodyWidth = bodyEnd - bodyStart
        const center = Math.floor(bodyStart + bodyWidth * position)
        const sampleWidth = Math.max(4, Math.floor(bodyWidth * 0.055))
        return {
          start: Math.max(0, center - Math.floor(sampleWidth / 2)),
          end: Math.min(cropWidth - 1, center + Math.floor(sampleWidth / 2)),
          strength: scoreMap[center] ?? 0,
        }
      })
    : null
  const selected = (horizontalSampleBands ?? strongest.slice(0, 4)).sort((a, b) => a.start - b.start)

  if (selected.length < 4) {
    throw new Error('Unable to detect four resistor bands. Please upload a clear, horizontal resistor photo.')
  }

  const detectedColors: ResistorColor[] = []

  for (const segment of selected) {
    const xStart = Math.max(0, segment.start)
    const xEnd = Math.min(cropWidth - 1, segment.end)
    let r = 0
    let g = 0
    let b = 0
    let count = 0

    for (let column = xStart; column <= xEnd; column += 1) {
      for (let row = midRowStart; row <= midRowEnd; row += 1) {
        const index = (row * cropWidth + column) * 4
        r += cropPixels[index]
        g += cropPixels[index + 1]
        b += cropPixels[index + 2]
        count += 1
      }
    }

    if (count === 0) {
      detectedColors.push('black')
      continue
    }

    const averageHex = rgbToHex(Math.round(r / count), Math.round(g / count), Math.round(b / count))
    detectedColors.push(getNearestColor(averageHex))
  }

  const bandType: BandType = detectedColors.length >= 5 ? '5-band' : '4-band'
  const bandCount = bandType === '5-band' ? 5 : 4
  const forwardBands = detectedColors.slice(0, bandCount)
  let finalBands = forwardBands
  let result: ReturnType<typeof decodeResistor>

  try {
    result = decodeResistor(forwardBands, bandType)
  } catch {
    finalBands = [...forwardBands].reverse()
    result = decodeResistor(finalBands, bandType)
  }

  const confidence = clamp(70 + finalBands.length * 5, 65, 97)

  return {
    result,
    bandType,
    confidence,
    bands: finalBands,
  }
}

function App() {
  const [bandType, setBandType] = useState<BandType>('4-band')
  const [selectedColors, setSelectedColors] = useState<string[]>(['brown', 'black', 'red', 'gold'])
  const [imageState, setImageState] = useState<DetectionState>(defaultDetectionState)

  const decoded = useMemo(() => {
    const activeBands = bandType === '4-band' ? selectedColors.slice(0, 4) : selectedColors.slice(0, 5)
    if (activeBands.length < (bandType === '4-band' ? 4 : 5)) {
      return { ohms: 0, tolerance: 0, formatted: 'Pick complete bands' }
    }
    try {
      return decodeResistor(activeBands, bandType)
    } catch {
      return { ohms: 0, tolerance: 0, formatted: 'Invalid band combination' }
    }
  }, [selectedColors, bandType])

  const updateBand = (index: number, value: string) => {
    const updated = [...selectedColors]
    updated[index] = value
    setSelectedColors(updated)
  }

  const visibleBandCount = bandType === '4-band' ? 4 : 5

  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) {
      return
    }

    setImageState({
      status: 'processing',
      message: 'Analyzing the resistor image…',
      bands: [],
      resistance: '',
      tolerance: '',
      bandEstimate: '',
      confidence: 0,
      imageUrl: null,
    })

    let dataUrl = ''

    try {
      dataUrl = await readFileAsDataUrl(file)
      const image = await createImageFromUrl(dataUrl)
      const modelResult = await detectWithModel(image)

      if (modelResult?.type === 'classification') {
        let bandCheck: ReturnType<typeof detectResistorBandsFromImage> | null = null
        try {
          bandCheck = detectResistorBandsFromImage(image)
        } catch {
          bandCheck = null
        }

        if (bandCheck) {
          setBandType(bandCheck.bandType)
          setSelectedColors(bandCheck.bands)
        }

        const confidence = Math.round(modelResult.confidence * 100)
        const predictedOhms = parseResistanceLabel(modelResult.label)
        const disagrees = bandCheck && predictedOhms !== null &&
          Math.abs(predictedOhms - bandCheck.result.ohms) > Math.max(0.01, predictedOhms * 0.01)
        const bandEstimate = bandCheck?.result.formatted ?? ''

        setImageState({
          status: disagrees || !bandCheck ? 'warning' : 'success',
          message: disagrees
              ? `Model predicts ${modelResult.label} (${confidence}%), but the color bands decode to ${bandEstimate}. Using the color-band value; check the image.`
            : !bandCheck
              ? `Model predicts ${modelResult.label} (${confidence}%), but the color bands could not be verified. Check the image before using this value.`
            : bandEstimate
              ? `Model predicts ${modelResult.label} (${confidence}%). Color-band check: ${bandEstimate}.`
              : `Model predicts ${modelResult.label} (${confidence}%).`,
          bands: bandCheck?.bands ?? [],
            resistance: bandEstimate || modelResult.label,
            tolerance: bandCheck ? `±${bandCheck.result.tolerance}%` : '',
          bandEstimate,
          confidence,
          imageUrl: dataUrl,
        })
        return
      }

      const { result, bandType: detectedType, confidence, bands } = detectResistorBandsFromImage(
        image,
        modelResult?.type === 'detection' ? modelResult.crop : undefined,
      )

      setBandType(detectedType)
      setSelectedColors(bands)

      const modelMessage = modelResult?.type === 'detection' && modelResult.label
        ? `Model detected ${modelResult.label} with ${modelResult.confidence.toFixed(2)} confidence.`
        : ''

      setImageState({
        status: 'success',
        message: modelMessage || `Detected a ${detectedType} resistor with strong matching.`,
        bands,
        resistance: result.formatted,
        tolerance: `±${result.tolerance}%`,
        bandEstimate: '',
        confidence,
        imageUrl: dataUrl,
      })
    } catch (error) {
      setImageState({
        status: 'error',
        message: error instanceof Error ? error.message : 'The resistor could not be detected. Try a clearer image.',
        bands: [],
        resistance: '',
        tolerance: '',
        bandEstimate: '',
        confidence: 0,
        imageUrl: dataUrl,
      })
    }
  }

  return (
    <main className="app-shell">
      <section className="panel">
        <header className="header-row">
          <div>
            <p className="eyebrow">ECE Project</p>
            <h1>Resistor Value Identifier</h1>
          </div>
          <div className="toggle-group" aria-label="Resistor band type">
            <button
              type="button"
              className={bandType === '4-band' ? 'active' : ''}
              onClick={() => setBandType('4-band')}
            >
              4-band
            </button>
            <button
              type="button"
              className={bandType === '5-band' ? 'active' : ''}
              onClick={() => setBandType('5-band')}
            >
              5-band
            </button>
          </div>
        </header>

        <div className="two-column-layout">
          <section className="calculator-panel">
            <div className="section-heading">
              <h2>Manual Calculator</h2>
              <span>Fallback mode</span>
            </div>

            <div className="resistor-card">
              <div className="resistor-body">
                <span className="wire left" />
                <span className="wire right" />
                {Array.from({ length: visibleBandCount }).map((_, index) => (
                  <div key={index} className="band-slot">
                    <select
                      value={selectedColors[index] ?? colors[0]}
                      onChange={(event) => updateBand(index, event.target.value)}
                    >
                      {colors.map((color) => (
                        <option key={color} value={color}>
                          {color}
                        </option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>
            </div>

            <div className="info-grid">
              <div className="card">
                <h3>Band Selection</h3>
                <div className="band-list">
                  {Array.from({ length: visibleBandCount }).map((_, index) => (
                    <label key={index} className="band-field">
                      <span>{bandNames[index]}</span>
                      <select
                        value={selectedColors[index] ?? colors[0]}
                        onChange={(event) => updateBand(index, event.target.value)}
                      >
                        {colors.map((color) => (
                          <option key={color} value={color}>
                            {color}
                          </option>
                        ))}
                      </select>
                    </label>
                  ))}
                </div>
              </div>

              <div className="card result-card">
                <h3>Decoded Value</h3>
                <div className="result-box">
                  <p className="result-label">Resistance</p>
                  <p className="result-value">{decoded.formatted}</p>
                </div>
                <ul className="result-details">
                  <li>
                    <span>Ohms</span>
                    <strong>{decoded.ohms} Ω</strong>
                  </li>
                  <li>
                    <span>Tolerance</span>
                    <strong>±{decoded.tolerance}%</strong>
                  </li>
                </ul>
              </div>
            </div>
          </section>

          <section className="ai-panel">
            <div className="section-heading">
              <h2>AI Image Detection</h2>
              <span>Automatic mode</span>
            </div>

            <label className="upload-box" htmlFor="resistor-upload">
              <input id="resistor-upload" type="file" accept="image/*" onChange={handleImageUpload} />
              <span>Upload resistor photo</span>
            </label>

            {imageState.imageUrl ? (
              <div className="image-preview-wrap">
                <img src={imageState.imageUrl} alt="Uploaded resistor" className="uploaded-image" />
              </div>
            ) : (
              <div className="placeholder-image">No image uploaded yet</div>
            )}

            <div className={`status-panel ${imageState.status}`}>
              <div className="status-header">
                <span className="status-dot" />
                <strong>{imageState.status === 'success' ? 'Detection successful' : imageState.status === 'warning' ? 'Check detection' : imageState.status === 'error' ? 'Detection failed' : imageState.status === 'processing' ? 'Analyzing' : 'Waiting for input'}</strong>
              </div>
              <p>{imageState.message}</p>
              {imageState.confidence > 0 && (
                <div className="confidence-row">
                  <span>Confidence</span>
                  <strong>{imageState.confidence}%</strong>
                </div>
              )}
            </div>

            <div className="detected-output">
              <h3>Detected color bands</h3>
              {imageState.bands.length > 0 ? (
                <div className="band-pills">
                  {imageState.bands.map((band, index) => (
                    <span key={`${band}-${index}`} className="band-pill" style={{ background: colorHex[band as ResistorColor] }}>
                      {band}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="empty-text">No bands detected yet.</p>
              )}
            </div>

            <div className="result-summary-card">
              <div>
                <span>Resistance</span>
                <strong>{imageState.resistance || '—'}</strong>
              </div>
              <div>
                <span>Tolerance</span>
                <strong>{imageState.tolerance || '—'}</strong>
              </div>
              {imageState.bandEstimate && (
                <div>
                  <span>Color-band check</span>
                  <strong>{imageState.bandEstimate}</strong>
                </div>
              )}
            </div>
          </section>
        </div>
      </section>
    </main>
  )
}

export default App
```

## `src/App.css`

```css
.app-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
  padding: 28px 18px;
}

.panel {
  width: min(1450px, 100%);
  background: rgba(15, 23, 42, 0.72);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 28px;
  padding: 32px;
  box-shadow: 0 20px 60px rgba(15, 23, 42, 0.55);
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: #a5b4fc;
  font-size: 0.7rem;
  font-weight: 700;
}

h1 {
  margin: 6px 0 0;
  font-size: clamp(2.2rem, 5vw, 3.5rem);
  color: #f8fafc;
}

.toggle-group {
  display: inline-flex;
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 999px;
  padding: 6px;
}

.toggle-group button {
  border: none;
  background: transparent;
  color: #cbd5e1;
  padding: 10px 18px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
}

.toggle-group button.active {
  background: linear-gradient(135deg, #4f46e5, #8b5cf6);
  color: white;
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.45);
}

.two-column-layout {
  display: grid;
  grid-template-columns: 1.18fr 0.82fr;
  gap: 24px;
}

.calculator-panel,
.ai-panel {
  background: rgba(15, 23, 42, 0.78);
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 22px;
  padding: 20px;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.section-heading h2 {
  margin: 0;
  color: #f8fafc;
  font-size: 1.2rem;
}

.section-heading span {
  color: #cbd5e1;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.resistor-card {
  background: linear-gradient(180deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.9));
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 22px;
  padding: 28px 18px;
  margin-bottom: 24px;
}

.resistor-body {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 130px;
  background: linear-gradient(180deg, #cbd5e1, #94a3b8 52%, #e2e8f0);
  border-radius: 18px;
  border: 2px solid rgba(15, 23, 42, 0.45);
  overflow: hidden;
}

.wire {
  position: absolute;
  top: 50%;
  width: 36px;
  height: 6px;
  background: #1f2937;
  transform: translateY(-50%);
}

.wire.left { left: 16px; }
.wire.right { right: 16px; }

.band-slot {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 100%;
  background: rgba(15, 23, 42, 0.08);
  border-left: 1px solid rgba(15, 23, 42, 0.18);
  border-right: 1px solid rgba(15, 23, 42, 0.18);
}

.band-slot select,
.band-field select {
  width: 100%;
  min-width: 90px;
  border: none;
  background: linear-gradient(180deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
  color: #0f172a;
  font-weight: 700;
  text-transform: capitalize;
  padding: 8px 10px;
  appearance: none;
}

.info-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 20px;
}

.card {
  background: rgba(15, 23, 42, 0.75);
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 20px;
  padding: 20px;
}

.card h3 {
  margin: 0 0 16px;
  color: #f8fafc;
  font-size: 1rem;
}

.band-list {
  display: grid;
  gap: 12px;
}

.band-field {
  display: grid;
  gap: 8px;
  color: #cbd5e1;
}

.band-field select {
  border-radius: 10px;
  min-width: unset;
  padding: 10px 12px;
}

.result-card {
  display: flex;
  flex-direction: column;
}

.result-box {
  background: linear-gradient(135deg, #1d4ed8, #7c3aed);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 18px;
  min-height: 112px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.result-label {
  margin: 0;
  font-size: 0.74rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.75);
}

.result-value {
  margin: 10px 0 0;
  font-size: clamp(1.15rem, 2.8vw, 2.2rem);
  line-height: 1.08;
  font-weight: 800;
  color: white;
  overflow-wrap: anywhere;
}

.result-details {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 12px;
}

.result-details li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  color: #cbd5e1;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
  padding-top: 12px;
}

.upload-box {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1d4ed8, #7c3aed);
  border: 1px solid rgba(191, 219, 254, 0.35);
  border-radius: 16px;
  padding: 14px 18px;
  color: white;
  font-weight: 700;
  cursor: pointer;
  margin-bottom: 18px;
  overflow: hidden;
  position: relative;
}

.upload-box input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.image-preview-wrap {
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 18px;
  overflow: hidden;
  background: rgba(15, 23, 42, 0.8);
  margin-bottom: 18px;
}

.uploaded-image {
  display: block;
  width: 100%;
  max-height: 260px;
  object-fit: contain;
  background: #e2e8f0;
}

.placeholder-image {
  display: grid;
  place-items: center;
  min-height: 180px;
  border: 1px dashed rgba(148, 163, 184, 0.4);
  color: #cbd5e1;
  border-radius: 18px;
  margin-bottom: 18px;
}

.status-panel {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 18px;
  padding: 16px;
  margin-bottom: 18px;
}

.status-panel.processing {
  border-color: rgba(250, 204, 21, 0.6);
}

.status-panel.success {
  border-color: rgba(34, 197, 94, 0.6);
}

.status-panel.warning {
  border-color: rgba(250, 204, 21, 0.8);
}

.status-panel.error {
  border-color: rgba(239, 68, 68, 0.6);
}

.status-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  color: #f8fafc;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: currentColor;
  display: inline-block;
}

.status-panel p {
  margin: 0;
  color: #dbeafe;
}

.confidence-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  color: #e2e8f0;
}

.detected-output {
  margin-bottom: 18px;
}

.detected-output h3 {
  margin: 0 0 10px;
  color: #f8fafc;
  font-size: 1rem;
}

.band-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.band-pill {
  padding: 10px 14px;
  border-radius: 999px;
  color: #ffffff;
  font-weight: 700;
  text-transform: capitalize;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.35);
}

.empty-text {
  color: #cbd5e1;
  margin: 0;
}

.result-summary-card {
  display: grid;
  gap: 12px;
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 18px;
  padding: 16px;
}

.result-summary-card div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  color: #cbd5e1;
}

.result-summary-card strong {
  color: #f8fafc;
}

@media (max-width: 960px) {
  .two-column-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  .header-row {
    display: grid;
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .toggle-group {
    width: 100%;
    justify-content: center;
  }

  .panel {
    padding: 20px 16px;
  }

  .resistor-body {
    height: 110px;
  }
}
```

## `src/bandVision.ts`

```typescript
import type { ResistorColor } from './resistorCalculator'

type PixelImage = {
  data: Uint8ClampedArray
  width: number
  height: number
}

type Range = { start: number; end: number }

function getPixelColor(data: Uint8ClampedArray, index: number): ResistorColor | null {
  const red = data[index]
  const green = data[index + 1]
  const blue = data[index + 2]
  const maximum = Math.max(red, green, blue)
  const minimum = Math.min(red, green, blue)
  const value = maximum / 255
  const saturation = maximum === 0 ? 0 : (maximum - minimum) / maximum

  if (saturation < 0.42) {
    if (value < 0.18) return 'black'
    if (saturation < 0.1 && value > 0.88) return 'white'
    if (saturation < 0.16 && value > 0.55) return 'silver'
    return null
  }

  const redNorm = red / 255
  const greenNorm = green / 255
  const blueNorm = blue / 255
  const delta = (maximum - minimum) / 255
  let hue = 0

  if (maximum === red) {
    hue = 60 * (((greenNorm - blueNorm) / delta) % 6)
  } else if (maximum === green) {
    hue = 60 * ((blueNorm - redNorm) / delta + 2)
  } else {
    hue = 60 * ((redNorm - greenNorm) / delta + 4)
  }
  hue = (hue + 360) % 360

  if (hue < 10 || hue >= 350) return 'red'
  if (hue < 35) return value < 0.62 ? 'brown' : 'orange'
  if (hue < 49) return 'gold'
  if (hue < 75) return 'yellow'
  if (hue < 165) return 'green'
  if (hue < 235) return 'blue'
  return 'violet'
}

function longestRange(mask: boolean[], allowedGap: number): Range | null {
  let best: Range | null = null
  let start = -1
  let lastActive = -1

  for (let index = 0; index < mask.length; index += 1) {
    if (mask[index]) {
      if (start === -1) start = index
      lastActive = index
      continue
    }

    if (start !== -1 && index - lastActive > allowedGap) {
      const candidate = { start, end: lastActive }
      if (!best || candidate.end - candidate.start > best.end - best.start) best = candidate
      start = -1
      lastActive = -1
    }
  }

  if (start !== -1) {
    const candidate = { start, end: lastActive }
    if (!best || candidate.end - candidate.start > best.end - best.start) best = candidate
  }

  return best
}

export function detectColorBandSequence(image: PixelImage): ResistorColor[] {
  const { data, width, height } = image
  if (width < 80 || height < 30) return []

  const brightRowThreshold = Math.max(8, Math.floor(height * 0.09))
  const bodyColumns = Array.from({ length: width }, (_, x) => {
    let brightRows = 0
    for (let y = 0; y < height; y += 1) {
      const index = (y * width + x) * 4
      if ((data[index] + data[index + 1] + data[index + 2]) / 3 > 50) brightRows += 1
    }
    return brightRows >= brightRowThreshold
  })

  const body = longestRange(bodyColumns, 4)
  if (!body || body.end - body.start < width * 0.16) return []

  const bodyWidth = body.end - body.start + 1
  const rowThreshold = Math.max(4, Math.floor(bodyWidth * 0.24))
  const bodyRows = Array.from({ length: height }, (_, y) => {
    let brightColumns = 0
    for (let x = body.start; x <= body.end; x += 1) {
      const index = (y * width + x) * 4
      if ((data[index] + data[index + 1] + data[index + 2]) / 3 > 100) brightColumns += 1
    }
    return brightColumns >= rowThreshold
  })

  const verticalBody = longestRange(bodyRows, 3)
  if (!verticalBody || verticalBody.end - verticalBody.start < height * 0.08) return []

  const top = verticalBody.start + Math.floor((verticalBody.end - verticalBody.start) * 0.12)
  const bottom = verticalBody.end - Math.floor((verticalBody.end - verticalBody.start) * 0.12)
  const left = body.start + Math.floor(bodyWidth * 0.06)
  const right = body.end - Math.floor(bodyWidth * 0.06)
  const sampleHeight = bottom - top + 1
  const columnColors: Array<ResistorColor | null> = []

  for (let x = left; x <= right; x += 1) {
    const votes = new Map<ResistorColor, number>()
    for (let y = top; y <= bottom; y += 1) {
      const color = getPixelColor(data, (y * width + x) * 4)
      if (color) votes.set(color, (votes.get(color) ?? 0) + 1)
    }

    const [color, count] = [...votes.entries()].sort((a, b) => b[1] - a[1])[0] ?? []
    columnColors.push(color && count >= sampleHeight * 0.34 ? color : null)
  }

  for (let index = 1; index < columnColors.length - 1; index += 1) {
    if (columnColors[index] === null && columnColors[index - 1] && columnColors[index - 1] === columnColors[index + 1]) {
      columnColors[index] = columnColors[index - 1]
    }
  }

  const minimumBandWidth = Math.max(2, Math.floor(bodyWidth * 0.012))
  const bands: ResistorColor[] = []
  let currentColor: ResistorColor | null = null
  let runLength = 0

  const saveBand = () => {
    if (currentColor && runLength >= minimumBandWidth && runLength <= bodyWidth * 0.22) {
      bands.push(currentColor)
    }
  }

  for (const color of columnColors) {
    if (color === currentColor && color !== null) {
      runLength += 1
      continue
    }
    saveBand()
    currentColor = color
    runLength = color ? 1 : 0
  }
  saveBand()

  return bands.length === 4 || bands.length === 5 ? bands : []
}
```

## `src/bandVision.test.ts`

```typescript
import { describe, expect, it } from 'vitest'
import { detectColorBandSequence } from './bandVision'

function makeResistorImage(bandColors = [
  [238, 205, 0],
  [75, 43, 176],
  [210, 25, 24],
  [204, 160, 35],
]) {
  const width = 200
  const height = 80
  const data = new Uint8ClampedArray(width * height * 4)
  const background = [18, 18, 18]
  const body = [232, 216, 182]
  const bands = [
    { start: 55, end: 67, color: bandColors[0] },
    { start: 82, end: 94, color: bandColors[1] },
    { start: 109, end: 121, color: bandColors[2] },
    { start: 136, end: 148, color: bandColors[3] },
  ]

  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const color = x >= 35 && x <= 165 && y >= 25 && y <= 54
        ? bands.find((band) => x >= band.start && x <= band.end)?.color ?? body
        : background
      const index = (y * width + x) * 4
      data[index] = color[0]
      data[index + 1] = color[1]
      data[index + 2] = color[2]
      data[index + 3] = 255
    }
  }

  return { data, width, height }
}

describe('detectColorBandSequence', () => {
  it('detects yellow-violet-red-gold bands on a dark background', () => {
    expect(detectColorBandSequence(makeResistorImage())).toEqual(['yellow', 'violet', 'red', 'gold'])
  })

  it('detects red-red-brown-gold bands on a dark background', () => {
    expect(detectColorBandSequence(makeResistorImage([
      [210, 25, 24],
      [210, 25, 24],
      [124, 63, 15],
      [204, 160, 35],
    ]))).toEqual(['red', 'red', 'brown', 'gold'])
  })
})
```

## `src/detector.ts`

```typescript
export type DetectorBox = {
  x1: number
  y1: number
  x2: number
  y2: number
}

export type DetectorDetection = {
  classId: number
  confidence: number
  box: DetectorBox
}

export type DetectorResultInput = {
  detections: DetectorDetection[]
  sourceWidth: number
  sourceHeight: number
}

export type NormalizedDetectorResult = {
  available: boolean
  confidence: number
  classId: number | null
  crop: {
    x: number
    y: number
    width: number
    height: number
  }
  label: string | null
}

const DETECTOR_CLASS_LABELS = [
  '1.2k ohms',
  '1.5k ohms',
  '1.8k ohms',
  '10 ohms',
  '100 ohms',
  '100k ohms',
  '100k ohms 5 bands',
  '10k ohms',
  '120 ohms',
  '12k ohms',
  '15 ohms',
  '150 ohms',
  '15k ohms',
  '180 ohms',
  '18k ohms',
  '1k ohms',
  '2.2k ohms',
  '2.2k ohms 5 bands',
  '2.7k ohms',
  '200 ohms 5 bands',
  '22 ohms 5 bands',
  '220 ohms',
  '22k ohms',
  '270 ohms',
  '27k ohms',
  '3.3k ohms',
  '3.9k ohms',
  '300k ohms 5 bands',
  '33 ohms',
  '330 ohms',
  '33k ohms',
  '390 ohms',
  '39k ohms',
  '4.7 ohms',
  '4.7k ohms',
  '4.7k ohms 5 bands',
  '47 ohms',
  '470 ohms',
  '470k ohms 5 bands',
  '47k ohms',
  '47k ohms 5 bands',
  '5.1k ohms 5 bands',
  '5.6 ohms',
  '5.6k ohms',
  '51k ohms 5 bands',
  '56 ohms',
  '560 ohms',
  '56k ohms',
  '58 ohms',
  '6.8k ohms',
  '680 ohms',
  '68k ohms',
  '8.2k ohms',
  '82 ohms',
  '820 ohms',
  'busted',
]

const MIN_CONFIDENCE = 0.35

export function normalizeDetectorResult(input: DetectorResultInput): NormalizedDetectorResult {
  const validDetections = input.detections.filter((detection) => {
    if (detection.confidence < MIN_CONFIDENCE) {
      return false
    }

    const width = detection.box.x2 - detection.box.x1
    const height = detection.box.y2 - detection.box.y1
    return width > 10 && height > 10 && width < input.sourceWidth && height < input.sourceHeight
  })

  if (validDetections.length === 0) {
    return {
      available: false,
      confidence: 0,
      classId: null,
      crop: { x: 0, y: 0, width: 0, height: 0 },
      label: null,
    }
  }

  const best = validDetections.reduce((current, candidate) =>
    candidate.confidence > current.confidence ? candidate : current
  )

  const x = Math.max(0, Math.round(best.box.x1))
  const y = Math.max(0, Math.round(best.box.y1))
  const width = Math.max(1, Math.round(best.box.x2 - best.box.x1))
  const height = Math.max(1, Math.round(best.box.y2 - best.box.y1))

  return {
    available: true,
    confidence: Number(best.confidence.toFixed(3)),
    classId: best.classId,
    crop: { x, y, width, height },
    label: DETECTOR_CLASS_LABELS[best.classId] ?? null,
  }
}
```

## `src/detector.test.ts`

```typescript
import { describe, expect, it } from 'vitest'
import { normalizeDetectorResult } from './detector'

describe('normalizeDetectorResult', () => {
  it('keeps the highest-confidence resistor box and exposes the crop bounds', () => {
    const result = normalizeDetectorResult({
      detections: [
        { classId: 12, confidence: 0.44, box: { x1: 60, y1: 130, x2: 260, y2: 280 } },
        { classId: 27, confidence: 0.91, box: { x1: 150, y1: 111, x2: 520, y2: 250 } },
      ],
      sourceWidth: 800,
      sourceHeight: 400,
    })

    expect(result.available).toBe(true)
    expect(result.crop.x).toBe(150)
    expect(result.crop.y).toBe(111)
    expect(result.crop.width).toBe(370)
    expect(result.crop.height).toBe(139)
    expect(result.confidence).toBeGreaterThan(0.9)
  })

  it('returns unavailable when no valid detection is present', () => {
    const result = normalizeDetectorResult({
      detections: [{ classId: 0, confidence: 0.1, box: { x1: 10, y1: 10, x2: 20, y2: 20 } }],
      sourceWidth: 800,
      sourceHeight: 400,
    })

    expect(result.available).toBe(false)
  })
})
```

## `src/index.css`

```css
:root {
  --text: #6b6375;
  --text-h: #08060d;
  --bg: #fff;
  --border: #e5e4e7;
  --code-bg: #f4f3ec;
  --accent: #aa3bff;
  --accent-bg: rgba(170, 59, 255, 0.1);
  --accent-border: rgba(170, 59, 255, 0.5);
  --social-bg: rgba(244, 243, 236, 0.5);
  --shadow:
    rgba(0, 0, 0, 0.1) 0 10px 15px -3px, rgba(0, 0, 0, 0.05) 0 4px 6px -2px;

  --sans: system-ui, 'Segoe UI', Roboto, sans-serif;
  --heading: system-ui, 'Segoe UI', Roboto, sans-serif;
  --mono: ui-monospace, Consolas, monospace;

  font: 18px/145% var(--sans);
  letter-spacing: 0.18px;
  color-scheme: light dark;
  color: var(--text);
  background: var(--bg);
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  @media (max-width: 1024px) {
    font-size: 16px;
  }
}

@media (prefers-color-scheme: dark) {
  :root {
    --text: #9ca3af;
    --text-h: #f3f4f6;
    --bg: #16171d;
    --border: #2e303a;
    --code-bg: #1f2028;
    --accent: #c084fc;
    --accent-bg: rgba(192, 132, 252, 0.15);
    --accent-border: rgba(192, 132, 252, 0.5);
    --social-bg: rgba(47, 48, 58, 0.5);
    --shadow:
      rgba(0, 0, 0, 0.4) 0 10px 15px -3px, rgba(0, 0, 0, 0.25) 0 4px 6px -2px;
  }

  #social .button-icon {
    filter: invert(1) brightness(2);
  }
}

#root {
  width: 1126px;
  max-width: 100%;
  margin: 0 auto;
  text-align: center;
  border-inline: 1px solid var(--border);
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

body {
  margin: 0;
}

h1,
h2 {
  font-family: var(--heading);
  font-weight: 500;
  color: var(--text-h);
}

h1 {
  font-size: 56px;
  letter-spacing: -1.68px;
  margin: 32px 0;
  @media (max-width: 1024px) {
    font-size: 36px;
    margin: 20px 0;
  }
}
h2 {
  font-size: 24px;
  line-height: 118%;
  letter-spacing: -0.24px;
  margin: 0 0 8px;
  @media (max-width: 1024px) {
    font-size: 20px;
  }
}
p {
  margin: 0;
}

code,
.counter {
  font-family: var(--mono);
  display: inline-flex;
  border-radius: 4px;
  color: var(--text-h);
}

code {
  font-size: 15px;
  line-height: 135%;
  padding: 4px 8px;
  background: var(--code-bg);
}
```

## `src/main.tsx`

```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

## `src/resistorCalculator.ts`

```typescript
export type BandType = '4-band' | '5-band'

export type ResistorColor =
  | 'black'
  | 'brown'
  | 'red'
  | 'orange'
  | 'yellow'
  | 'green'
  | 'blue'
  | 'violet'
  | 'grey'
  | 'white'
  | 'gold'
  | 'silver'

const colorValues: Record<ResistorColor, number> = {
  black: 0,
  brown: 1,
  red: 2,
  orange: 3,
  yellow: 4,
  green: 5,
  blue: 6,
  violet: 7,
  grey: 8,
  white: 9,
  gold: -1,
  silver: -2,
}

const colorMultiplier: Record<ResistorColor, number> = {
  black: 1,
  brown: 10,
  red: 100,
  orange: 1000,
  yellow: 10000,
  green: 100000,
  blue: 1000000,
  violet: 10000000,
  grey: 100000000,
  white: 1000000000,
  gold: 0.1,
  silver: 0.01,
}

const digitColors = new Set<ResistorColor>([
  'black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet', 'grey', 'white',
])

export function decodeResistor(bands: string[], type: BandType) {
  const normalized = bands.map((band) => band.toLowerCase() as ResistorColor)
  const expectedCount = type === '4-band' ? 4 : 5
  if (normalized.length !== expectedCount || normalized.some((color) => !(color in colorValues))) {
    throw new Error(`A ${type} resistor requires ${expectedCount} valid color bands.`)
  }

  if (type === '4-band') {
    const [a, b, c, t] = normalized
    if (!digitColors.has(a) || !digitColors.has(b)) {
      throw new Error('Gold and silver cannot be significant-digit bands.')
    }
    const value = (colorValues[a] * 10 + colorValues[b]) * colorMultiplier[c]
    const tolerance = t === 'gold' ? 5 : t === 'silver' ? 10 : 20
    return {
      ohms: value,
      tolerance,
      formatted: formatResistance(value, tolerance),
    }
  }

  const [a, b, c, d, t] = normalized
  if (!digitColors.has(a) || !digitColors.has(b) || !digitColors.has(c)) {
    throw new Error('Gold and silver cannot be significant-digit bands.')
  }
  const value =
    (colorValues[a] * 100 + colorValues[b] * 10 + colorValues[c]) * colorMultiplier[d]
  const tolerance = t === 'gold' ? 5 : t === 'silver' ? 10 : 20

  return {
    ohms: value,
    tolerance,
    formatted: formatResistance(value, tolerance),
  }
}

function formatResistance(value: number, tolerance: number) {
  const absValue = Math.abs(value)
  if (absValue >= 1000000) {
    return `${(value / 1000000).toFixed(2).replace(/\.00$/, '')} MΩ ±${tolerance}%`
  }
  if (absValue >= 1000) {
    return `${(value / 1000).toFixed(2).replace(/\.00$/, '')} kΩ ±${tolerance}%`
  }
  if (absValue >= 1) {
    return `${value.toFixed(0)} Ω ±${tolerance}%`
  }
  if (absValue >= 0.001) {
    return `${(value * 1000).toFixed(2).replace(/\.00$/, '')} mΩ ±${tolerance}%`
  }
  return `${value} Ω ±${tolerance}%`
}
```

## `src/resistorCalculator.test.ts`

```typescript
import { describe, expect, it } from 'vitest'
import { decodeResistor } from './resistorCalculator'

describe('decodeResistor', () => {
  it('decodes a 4-band resistor correctly', () => {
    expect(decodeResistor(['brown', 'black', 'red', 'gold'], '4-band')).toEqual({
      ohms: 1000,
      tolerance: 5,
      formatted: '1 kΩ ±5%',
    })
  })

  it('decodes the red-red-brown-gold photo as 220 ohms', () => {
    expect(decodeResistor(['red', 'red', 'brown', 'gold'], '4-band').ohms).toBe(220)
  })

  it('decodes the yellow-violet-red-gold photo as 4.7 kilo-ohms', () => {
    expect(decodeResistor(['yellow', 'violet', 'red', 'gold'], '4-band').ohms).toBe(4700)
  })

  it('decodes a 5-band resistor correctly', () => {
    expect(decodeResistor(['red', 'violet', 'green', 'brown', 'gold'], '5-band')).toEqual({
      ohms: 2750,
      tolerance: 5,
      formatted: '2.75 kΩ ±5%',
    })
  })

  it('rejects gold or silver in significant digit positions', () => {
    expect(() => decodeResistor(['gold', 'brown', 'red', 'gold'], '4-band')).toThrow()
    expect(() => decodeResistor(['silver', 'brown', 'red', 'black', 'gold'], '5-band')).toThrow()
  })
})
```
