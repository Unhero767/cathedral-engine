extends Node

@onready var orchestrator = get_node_or_null("../StateOrchestrator")

var event_ledger: Array[String] = []
const MAX_LOG_ENTRIES = 50

func _ready() -> void:
    if orchestrator:
        orchestrator.connect("state_changed", Callable(self, "_on_state_changed"))
        orchestrator.connect("telemetry_broadcast", Callable(self, "_on_telemetry_broadcast"))

func _on_state_changed(new_state: int) -> void:
    var state_name = "UNKNOWN"
    if orchestrator:
        for k in orchestrator.SystemState.keys():
            if orchestrator.SystemState[k] == new_state:
                state_name = k
                break
    log_event("STATE_TRANSITION: " + state_name)

func _on_telemetry_broadcast(metric: String, value: float) -> void:
    log_event("TELEMETRY [" + metric + "] -> " + str(value))

func log_event(message: String) -> void:
    var timestamp = Time.get_time_string_from_system()
    var entry = "[" + timestamp + "] " + message
    event_ledger.push_front(entry)
    
    if event_ledger.size() > MAX_LOG_ENTRIES:
        event_ledger.pop_back()
        
    print(entry)
