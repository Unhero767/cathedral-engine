extends Node

enum SystemState { IDLE, ARMED, ACTIVE, FOCUS, WARNING, OVERLOAD, DISABLED }

signal state_changed(new_state: SystemState)
signal telemetry_broadcast(metric_name: String, value: float)

var current_state: SystemState = SystemState.IDLE

const STATE_PROFILES = {
    SystemState.IDLE: { "speed": 0.5, "aberration": 0.002, "depth_steps": 16.0 },
    SystemState.ARMED: { "speed": 1.0, "aberration": 0.005, "depth_steps": 16.0 },
    SystemState.ACTIVE: { "speed": 1.5, "aberration": 0.012, "depth_steps": 12.0 },
    SystemState.FOCUS: { "speed": 1.0, "aberration": 0.003, "depth_steps": 24.0 },
    SystemState.WARNING: { "speed": 2.0, "aberration": 0.025, "depth_steps": 8.0 },
    SystemState.OVERLOAD: { "speed": 3.0, "aberration": 0.050, "depth_steps": 4.0 },
    SystemState.DISABLED: { "speed": 0.0, "aberration": 0.0, "depth_steps": 32.0 }
}

func transition_to(new_state: SystemState) -> void:
    if current_state == new_state:
        return
    current_state = new_state
    state_changed.emit(current_state)
    apply_state_profile(current_state)

func apply_state_profile(state: SystemState) -> void:
    var profile = STATE_PROFILES.get(state, STATE_PROFILES[SystemState.IDLE])
    telemetry_broadcast.emit("speed", profile["speed"])
    telemetry_broadcast.emit("aberration", profile["aberration"])
    telemetry_broadcast.emit("depth_steps", profile["depth_steps"])
