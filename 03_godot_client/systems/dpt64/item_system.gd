class_name ItemSystem
extends RefCounted

static var shuffled_potions = {}

static func initialize_run_items():
    var colors = ["Cerulean", "Amber", "Crimson-Opaque", "Vantablack", "Iridescent"]
    colors.shuffle()
    shuffled_potions = {
        "heal": colors[0],
        "caloric": colors[1],
        "poison": colors[2]
    }
