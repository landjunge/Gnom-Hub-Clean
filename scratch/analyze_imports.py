import os
import re
from pathlib import Path

def analyze():
    base_dir = Path("/Users/landjunge/Documents/AG-Flega/src/gnom_hub")
    py_files = [f for f in base_dir.iterdir() if f.is_file() and f.suffix == ".py" and f.name != "__init__.py"]
    
    deps = {}
    import_regex = re.compile(r"^\s*(?:from\s+\.(?!\.)(\w+)\s+import|import\s+\.(?!\.)(\w+)|from\s+gnom_hub\.(\w+)\s+import)")
    
    for pf in py_files:
        content = pf.read_text()
        file_deps = set()
        for line in content.splitlines():
            # simple regex check for local imports
            match = import_regex.search(line)
            if match:
                # print(f"File {pf.name} line: {line} matches {match.groups()}")
                dep = next(g for g in match.groups() if g is not None)
                file_deps.add(dep)
            # check inline imports or from .X import
            matches = re.findall(r"from\s+\.(\w+)\s+import", line)
            for m in matches:
                file_deps.add(m)
            matches = re.findall(r"import\s+\.(\w+)", line)
            for m in matches:
                file_deps.add(m)
            matches = re.findall(r"from\s+gnom_hub\.(\w+)\s+import", line)
            for m in matches:
                file_deps.add(m)
        
        # Filter dependencies to only include other files in the same folder
        clean_deps = []
        for d in file_deps:
            dep_file = base_dir / f"{d}.py"
            if dep_file.exists() and d != pf.stem:
                clean_deps.append(d)
        deps[pf.stem] = sorted(list(set(clean_deps)))
        
    # Sort files by number of dependencies (leaf files first)
    sorted_files = sorted(deps.keys(), key=lambda k: (len(deps[k]), k))
    
    print("DEPENDENCY MAP:")
    for f in sorted_files:
        print(f"{f}: {deps[f]}")
        
if __name__ == "__main__":
    analyze()
