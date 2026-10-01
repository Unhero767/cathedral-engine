import os
import time
import hashlib
from google import genai
from google.genai import types

def generate_cathedral_visual(prompt, output_dir="outputs"):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    result = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
            output_mime_type="image/png",
            person_generation="ALLOW_ADULT",
            safety_filter_level="BLOCK_LOW_AND_ABOVE"
        )
    )
    
    os.makedirs(output_dir, exist_ok=True)
    for generated_image in result.generated_images:
        img_bytes = generated_image.image.image_bytes
        img_hash = hashlib.sha256(img_bytes).hexdigest()
        filename = f"gemini_cathedral_{int(time.time())}_{img_hash[:10]}.png"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(img_bytes)
        print(f"[+] High-fidelity visual artifact saved: {filepath}")
        return filepath

if __name__ == "__main__":
    from synthesize_chamber_artifact import MythicPromptCompiler
    compiler = MythicPromptCompiler()
    pos, neg, _, _, _ = compiler.compile(5, 0.12, 1.45, 0.92, "THETA_GOLD")
    generate_cathedral_visual(pos)
