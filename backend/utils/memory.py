import os

MEMORY_FILE = "memory.txt"

def save_memory(text):
    with open(MEMORY_FILE, "w") as f:
        f.write(text)

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return f.read()
    return None