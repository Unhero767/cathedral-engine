extends Node

enum SpectralConstant { GOLD_JOY, BLUE_SORROW, TEAL_CURIOSITY, RED_ANGER, VIOLET_FEAR, EMERALD_LOVE, BRONZE_NULL }

var current_frequency: SpectralConstant = SpectralConstant.TEAL_CURIOSITY

func _ready() -> void:
    print("MrLaos: Sovereign Interface online. Frequency set to Teal/Curiosity.")

func register_harmonic_scar(context: String) -> void:
    print("MrLaos [Harmonic Scar Crystallized]: %s" % context)
    if Engine.has_singleton("AshArchive") or get_node_or_null("/root/AshArchive"):
        var archive = get_node_or_null("/root/AshArchive")
        if archive and archive.has_method("append_entry"):
            archive.append_entry({"type": "harmonic_scar", "context": context})
