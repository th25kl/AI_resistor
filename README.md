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

## Publish on GitHub Pages

1. Create a GitHub repository and push this project to its `main` branch.
2. Open the repository's **Settings > Pages**.
3. Under **Build and deployment**, choose **GitHub Actions** as the source.
4. Push to `main` or run the **Deploy Vite site to GitHub Pages** workflow manually.
5. GitHub will publish the site at `https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/`.

The hosted site uses the browser-based color-band reader. Electron, Python, and the trained model are for local desktop development and are not required by GitHub Pages.

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
