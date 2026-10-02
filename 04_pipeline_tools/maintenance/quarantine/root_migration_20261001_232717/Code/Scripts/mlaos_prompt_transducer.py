import torch

class MLAOSPromptTransducer:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP",),
                "archetype": (["Aurelia-9 (Vanguard)", "Caelen (Architect)", "Deimos (Catalyst)", "Reliquary Scribe", "Void Runner Pilot", "Monumental Cathedral"],),
                "spectral_constant": (["Theta (Gold / Law)", "Psi (Matte Teal / Logic)", "Delta (Oxford Blue / Archive)", "Phi (Crimson / Remaking)", "Omega (Dark Violet / Shadow)", "Null (Obsidian / Void)"],),
                "scale_hierarchy": (["Human Anchor", "Architectural Scale", "Cathedral-Engine Systemic", "Cosmological Horizon"],),
                "custom_subject": ("STRING", {"multiline": True, "default": "armored knight in fluted plate kneeling before a monolithic conduit"}),
                "weathering_level": ("FLOAT", {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.05}),
            }
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "STRING", "STRING")
    RETURN_NAMES = ("positive", "negative", "pos_prompt_text", "neg_prompt_text")
    FUNCTION = "transduce_prompt"
    CATEGORY = "MLAOS/Prompting"

    def transduce_prompt(self, clip, archetype, spectral_constant, scale_hierarchy, custom_subject, weathering_level):
        # 1. Cosmological & Material Foundation
        spectral_tag = {
            "Theta (Gold / Law)": "aged gold leaf, burnished brass accents, sovereign radiance, 585nm gold aura",
            "Psi (Matte Teal / Logic)": "matte teal conduits, recursive lattice geometry, cold cyan data pulses",
            "Delta (Oxford Blue / Archive)": "oxford blue oxidized surfaces, deep indigo stone, fossilized parchment",
            "Phi (Crimson / Remaking)": "crimson heat fissures, kinetic remaking scars, dark red combustion residue",
            "Omega (Dark Violet / Shadow)": "dark violet refraction, shadow-walking boundary, deep purple obsidian",
            "Null (Obsidian / Void)": "matte black ceramic, anti-resonance negative space, lightless obsidian"
        }[spectral_constant]

        # 2. V_MLAOS Master Formula Assembly
        c_layer = "mythotechnical ritualized infrastructure, sacred architecture as active machine"
        a_layer = f"monumental scale, {scale_hierarchy.lower()}, towering arched vaults, brutalist monastic geometry"
        s_layer = f"radial glyph conduits, tri-key insignia, {spectral_tag}"
        m_layer = "weathered charcoal stone, fluted blackened steel, brushed brass joints, matte ceramic armor"
        l_layer = "dramatic volumetric god rays, heavy dust and suspended ash, deep directional occluded shadows, recessed lumen cores"
        h_layer = "harmonic contrast, sacred precision meeting physical brutality, ancient masonry fused with functioning circuits"
        t_layer = f"historical battle scars, surface oxidation, patina, soot deposits, weathering index {weathering_level:.2f}, never-overwritten data"

        positive_text = (
            f"masterpiece, authentic MLAOS art direction, {custom_subject}, {archetype}, "
            f"{c_layer}, {a_layer}, {s_layer}, {m_layer}, {l_layer}, {h_layer}, {t_layer}, "
            f"cinematic lighting, hyper-detailed textures, 8k resolution"
        )

        negative_text = (
            "neon cyberpunk, high-gloss clean surfaces, pristine plastic armor, chrome plating, "
            "generic medieval fantasy, glowing anime eyes, messy lineart, oversaturated rainbow colors, "
            "sterile sci-fi corridors, decorative gothic clutter without function, modern logos, text watermark"
        )

        tokens_pos = clip.tokenize(positive_text)
        cond_pos, pooled_pos = clip.encode_from_tokens(tokens_pos, return_pooled=True)

        tokens_neg = clip.tokenize(negative_text)
        cond_neg, pooled_neg = clip.encode_from_tokens(tokens_neg, return_pooled=True)

        return ([[cond_pos, {"pooled_output": pooled_pos}]], 
                [[cond_neg, {"pooled_output": pooled_neg}]], 
                positive_text, 
                negative_text)