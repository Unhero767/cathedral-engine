extends Node

# Global Event Bus for MLAOS runtime communication
signal terminal_command_executed(command: String)
signal system_state_changed(state_name: String, active: bool)
