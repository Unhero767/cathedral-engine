import os

dirs = [
    "dataset",
    "models",
    "output",
    "logs",
    "sd-scripts/networks"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"Directory verified/created: {d}")

print("Local workspace structure initialized.")
