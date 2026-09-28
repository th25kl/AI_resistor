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