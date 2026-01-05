from pathlib import Path


currentPath = Path('.')
currentFile = Path(__file__).name


print(f"Files in {currentPath}:")

for filepath in currentPath.iterdir():
    if filepath.is_file():
        content = filepath.read_text(encoding='utf-8')
        print(content)