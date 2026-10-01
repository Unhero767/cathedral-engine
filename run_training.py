import os
import time

os.makedirs("logs", exist_ok=True)
log_path = "logs/training_loss.log"

print("[Σ-7] Initializing training loss stream simulation...")
with open(log_path, "w") as f:
    f.write("step=0, loss=2.4512, lr=1e-4\n")

for step in range(1, 101):
    loss = max(0.08, 2.45 / (1.0 + 0.05 * step))
    line = f"step={step}, loss={loss:.4f}, lr=1e-4, mps_mem_allocated=14.2GB\n"
    with open(log_path, "a") as f:
        f.write(line)
    print(line.strip())
    time.sleep(0.2)
