class_name CathedralTypes
extends RefCounted

enum FourValue { T, F, B, N }
enum MitigationLevel { NOMINAL, OBSERVE, REDISTRIBUTE, THROTTLE, CONTAIN, SURVIVE }

static func join_state(previous: int, observed: int) -> int:
    if previous == observed:
        return previous
    if previous == FourValue.N:
        return observed
    if observed == FourValue.N:
        return previous
    if previous == FourValue.B or observed == FourValue.B:
        return FourValue.B
    # T + F or F + T conflict
    return FourValue.B

static func four_val_to_string(val: int) -> String:
    match val:
        FourValue.T: return "T"
        FourValue.F: return "F"
        FourValue.B: return "B"
        _: return "N"
