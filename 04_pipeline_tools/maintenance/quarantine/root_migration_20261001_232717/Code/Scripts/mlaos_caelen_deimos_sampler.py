import comfy.sample
import comfy.samplers

class MLAOSDualEngineSampler:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 35, "min": 10, "max": 100}),
                "cfg": ("FLOAT", {"default": 7.0, "min": 1.0, "max": 20.0, "step": 0.5}),
                "caelen_ratio": ("FLOAT", {"default": 0.65, "min": 0.2, "max": 0.9, "step": 0.05, 
                                          "tooltip": "Ratio of steps governed by Caelen (Structural Rigidity)"}),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "latent_image": ("LATENT",),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    FUNCTION = "sample_dual_engine"
    CATEGORY = "MLAOS/Sampling"

    def sample_dual_engine(self, model, seed, steps, cfg, caelen_ratio, positive, negative, latent_image, denoise):
        caelen_steps = int(steps * caelen_ratio)
        
        # Phase 1: Caelen's Lemma (Deterministic structural lock)
        # Sampler: dpmpp_2m / Scheduler: karras
        latent_phase1 = comfy.sample.sample(
            model, seed, steps, cfg, "dpmpp_2m", "karras",
            positive, negative, latent_image,
            denoise=denoise, start_step=0, last_step=caelen_steps,
            force_full_denoise=False
        )

        # Phase 2: Deimos's Variable (Kinetic micro-entropy / stochastic surface weathering)
        # Sampler: dpmpp_sde / Scheduler: exponential
        latent_phase2 = comfy.sample.sample(
            model, seed + 107, steps, max(cfg - 1.0, 3.5), "dpmpp_sde", "exponential",
            positive, negative, latent_phase1,
            denoise=denoise, start_step=caelen_steps, last_step=steps,
            force_full_denoise=True
        )

        return (latent_phase2,)