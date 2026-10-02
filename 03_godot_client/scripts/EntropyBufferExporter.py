import jax.numpy as jnp
import numpy as np
import os

def export_entropy_buffer_for_godot(entropy_buffer: jnp.ndarray, output_path: str = "03_godot_client/assets/entropy_map.bin"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    host_array = np.array(entropy_buffer, dtype=np.float32)
    with open(output_path, "wb") as f:
        f.write(host_array.tobytes())
    print(f"Exported entropy buffer ({host_array.shape}) to {output_path}")

if __name__ == "__main__":
    dummy_buffer = jnp.zeros((256, 256, 256), dtype=jnp.float32)
    export_entropy_buffer_for_godot(dummy_buffer)
