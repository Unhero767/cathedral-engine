extends Node

func _ready() -> void:
    # Sensor A reports True
    var ev1 = CathedralEngine.update_state("TARGET_PRESENT", CathedralTypes.FourValue.T, "sensor-A", 0.0, 0.2)
    print("Event 1 Result: ", CathedralTypes.four_val_to_string(ev1.resulting))

    # Sensor B contradicts with False
    var ev2 = CathedralEngine.update_state("TARGET_PRESENT", CathedralTypes.FourValue.F, "sensor-B", 0.35, 0.6)
    print("Event 2 Result: ", CathedralTypes.four_val_to_string(ev2.resulting), " | Contradiction: ", ev2.contradiction)

    # Sensor C asserts True (Should hold B, never overwrite)
    var ev3 = CathedralEngine.update_state("TARGET_PRESENT", CathedralTypes.FourValue.T, "sensor-C", 0.55, 0.8)
    print("Final State for TARGET_PRESENT: ", CathedralTypes.four_val_to_string(CathedralEngine.get_state("TARGET_PRESENT")))
