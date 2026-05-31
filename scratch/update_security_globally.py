import os

def replace_in_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    orig = content
    content = content.replace("gnom_hub.security", "gnom_hub.core.security")
    
    if content != orig:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {file_path}")

for root, dirs, files in os.walk("src/gnom_hub/"):
    for file in files:
        if file.endswith(".py"):
            replace_in_file(os.path.join(root, file))
