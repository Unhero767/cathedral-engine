"""
EAS-03 Atlas Compiler & SpriteFrames Resource Exporter
"""
import os

ANIMATION_DEFINITIONS = {
    "liturgical_idle": {"start": 0, "count": 4, "fps": 6.0, "loop": "true"},
    "lumen_pulse": {"start": 4, "count": 6, "fps": 8.0, "loop": "true"},
    "ocular_surge": {"start": 10, "count": 6, "fps": 10.0, "loop": "true"},
    "harmonic_resonance": {"start": 16, "count": 8, "fps": 8.0, "loop": "true"},
    "dialetheic_shift": {"start": 24, "count": 4, "fps": 6.0, "loop": "true"},
    "penitent_recitation": {"start": 28, "count": 4, "fps": 8.0, "loop": "true"}
}

class AtlasCompiler:
    def generate_godot4_spriteframes_tres(self, atlas_texture_path: str, output_tres_path: str) -> str:
        tres_content = [
            "[gd_resource type=\"SpriteFrames\" load_steps=34 format=3 uid=\"uid://mlaoseas03atlas001\"]",
            "",
            f"[ext_resource type=\"Texture2D\" path=\"{atlas_texture_path}\" id=\"1_master_atlas\"]",
            ""
        ]

        for i in range(32):
            sub_id = f"sub_resource_frame_{i:02d}"
            x_pos = i * 128
            tres_content.extend([
                f"[sub_resource type=\"AtlasTexture\" id=\"{sub_id}\"]",
                "atlas = ExtResource(\"1_master_atlas\")",
                f"region = Rect2({x_pos}, 0, 128, 128)",
                "filter_clip = true",
                ""
            ])

        tres_content.append("[resource]")
        tres_content.append("animations = [{")

        anim_entries = []
        for anim_name, config in ANIMATION_DEFINITIONS.items():
            frames_list = [f"{{\"duration\": 1.0, \"texture\": SubResource(\"sub_resource_frame_{f:02d}\")}}" for f in range(config["start"], config["start"] + config["count"])]
            frames_str = ", ".join(frames_list)
            entry = (
                f"\"frames\": [{frames_str}],\n"
                f"\"loop\": {config['loop']},\n"
                f"\"name\": &\"{anim_name}\",\n"
                f"\"speed\": {config['fps']}"
            )
            anim_entries.append("{\n" + entry + "\n}")

        tres_content.append(", ".join(anim_entries))
        tres_content.append("}]")

        full_tres_text = "\n".join(tres_content)
        if output_tres_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_tres_path)), exist_ok=True)
            with open(output_tres_path, "w", encoding="utf-8") as f:
                f.write(full_tres_text)

        return full_tres_text
