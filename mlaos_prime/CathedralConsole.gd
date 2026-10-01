extends CanvasLayer
# ====================================================================
# MLAOS-Prime :: Sovereign Quake-Style Console (Optimized)
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================

@onready var panel: PanelContainer = $PanelContainer
@onready var output_log: RichTextLabel = $PanelContainer/VBoxContainer/MarginContainer/OutputLog
@onready var input_line: LineEdit = $PanelContainer/VBoxContainer/InputBar/LineEdit

var base_url: String = "http://127.0.0.1:8000"
var http_client: HTTPRequest

# UX State
var is_open: bool = false
var slide_tween: Tween
var history: Array[String] = []
var history_index: int = -1

# Optimization Limits
const MAX_LOG_LINES: int = 250

# Command Registry Pattern
var command_registry: Dictionary = {}

func _ready() -> void:
	# Hide panel initially by moving it off-screen
	panel.position.y = -panel.size.y
	visible = true # Layer remains visible for tweening
	
	# Setup reusable HTTP Client to prevent GC spikes
	http_client = HTTPRequest.new()
	add_child(http_client)
	http_client.request_completed.connect(_on_http_response)
	
	input_line.text_submitted.connect(_on_command_submitted)
	input_line.gui_input.connect(_on_input_line_gui_input)
	
	_register_commands()
	
	_append_log("[color=gold]MLAOS-Prime Sovereign Console Active.[/color]")
	_append_log("Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)")
	_append_log("Type [color=cyan]help[/color] for directives.\n")

func _register_commands() -> void:
	command_registry["help"] = Callable(self, "_cmd_help")
	command_registry["clear"] = Callable(self, "_cmd_clear")
	command_registry["exit"] = Callable(self, "toggle_console")
	command_registry["quit"] = Callable(self, "toggle_console")
	command_registry["telemetry"] = Callable(self, "_cmd_telemetry")
	command_registry["ledger"] = Callable(self, "_cmd_ledger")
	command_registry["codex"] = Callable(self, "_cmd_codex")
	command_registry["ask"] = Callable(self, "_cmd_ask")
	command_registry["reduce"] = Callable(self, "_cmd_reduce")
	command_registry["reason"] = Callable(self, "_cmd_reason")

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_QUOTELEFT:
		toggle_console()
		get_viewport().set_input_as_handled()

func toggle_console() -> void:
	is_open = !is_open
	
	if slide_tween and slide_tween.is_valid():
		slide_tween.kill()
		
	slide_tween = create_tween().set_trans(Tween.TRANS_EXPO).set_ease(Tween.EASE_OUT)
	
	if is_open:
		get_tree().paused = true
		slide_tween.tween_property(panel, "position:y", 0.0, 0.3)
		input_line.grab_focus()
		input_line.clear()
	else:
		slide_tween.tween_property(panel, "position:y", -panel.size.y, 0.2)
		slide_tween.tween_callback(func(): get_tree().paused = false)

func _on_input_line_gui_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_UP:
			if history.size() > 0:
				history_index = clampi(history_index + 1, 0, history.size() - 1)
				input_line.text = history[history.size() - 1 - history_index]
				input_line.caret_column = input_line.text.length()
				get_viewport().set_input_as_handled()
		elif event.keycode == KEY_DOWN:
			if history_index > 0:
				history_index -= 1
				input_line.text = history[history.size() - 1 - history_index]
			else:
				history_index = -1
				input_line.text = ""
			input_line.caret_column = input_line.text.length()
			get_viewport().set_input_as_handled()

func _on_command_submitted(text: String) -> void:
	var clean_text = text.strip_edges()
	if clean_text.is_empty():
		return
		
	# Update History
	if history.is_empty() or history.back() != clean_text:
		history.append(clean_text)
		if history.size() > 50:
			history.pop_front()
	history_index = -1
		
	_append_log("[color=lightgray]mlaos-prime [T] > %s[/color]" % clean_text)
	input_line.clear()
	
	var tokens = clean_text.split(" ", false)
	var command = tokens[0].to_lower()
	var args = tokens.slice(1)
	
	if command_registry.has(command):
		command_registry[command].call(args)
	else:
		_append_log("[color=red]Unknown command: '%s'. Type 'help' for directives.[/color]\n" % command)

# ====================================================================
# Command Implementations
# ====================================================================

func _cmd_help(_args: PackedStringArray) -> void:
	_append_log("[color=yellow]Available Commands:[/color]")
	_append_log("  [cyan]ask <query>[/cyan]     - Direct backend prompt evaluation")
	_append_log("  [cyan]codex <term>[/cyan]    - Search 40-Book Codex registry")
	_append_log("  [cyan]telemetry[/cyan]       - Fetch Nonary State Vector & Olney Datum")
	_append_log("  [cyan]ledger [--verify][/cyan] - Inspect Ash Archive tip block / integrity")
	_append_log("  [cyan]reduce <goal>[/cyan]    - Execute Lex V Load-Bearing Reduction")
	_append_log("  [cyan]reason <p1> <p2>[/cyan] - Evaluate contradictory claims via Squeeze")
	_append_log("  [cyan]clear[/cyan]           - Clear console log")
	_append_log("  [cyan]exit / quit[/cyan]     - Close console terminal\n")

func _cmd_clear(_args: PackedStringArray) -> void:
	output_log.clear()

func _cmd_telemetry(_args: PackedStringArray) -> void:
	_dispatch_http("/telemetry", HTTPClient.METHOD_GET)

func _cmd_ledger(args: PackedStringArray) -> void:
	if not args.is_empty() and args[0] == "--verify":
		_dispatch_http("/ledger/verify", HTTPClient.METHOD_GET)
	else:
		_dispatch_http("/ledger", HTTPClient.METHOD_GET)

func _cmd_codex(args: PackedStringArray) -> void:
	if args.is_empty():
		_append_log("[color=red]Error: Missing search term.[/color]\n")
	else:
		_dispatch_http("/codex/" + " ".join(args).uri_encode(), HTTPClient.METHOD_GET)

func _cmd_ask(args: PackedStringArray) -> void:
	if args.is_empty():
		_append_log("[color=red]Error: Missing query string.[/color]\n")
	else:
		_dispatch_http("/ask", HTTPClient.METHOD_POST, {"prompt": " ".join(args)})

func _cmd_reduce(args: PackedStringArray) -> void:
	if args.is_empty():
		_append_log("[color=red]Error: Missing goal string.[/color]\n")
	else:
		_dispatch_http("/reduce", HTTPClient.METHOD_POST, {"goal": " ".join(args)})

func _cmd_reason(args: PackedStringArray) -> void:
	if args.size() < 2:
		_append_log("[color=red]Error: Requires two claims.[/color]\n")
	else:
		_dispatch_http("/reason", HTTPClient.METHOD_POST, {"claim_a": args[0], "claim_b": args[1]})

# ====================================================================
# HTTP Networking & Logging
# ====================================================================

func _dispatch_http(endpoint: String, method: int, payload: Dictionary = {}) -> void:
	if http_client.get_http_client_status() != HTTPClient.STATUS_DISCONNECTED:
		http_client.cancel_request()
		
	var headers = ["Content-Type: application/json"]
	var body = JSON.stringify(payload) if not payload.is_empty() else ""
	
	var err = http_client.request(base_url + endpoint, headers, method, body)
	if err != OK:
		_append_log("[color=red]Failed to connect to MLAOS-Prime backend at %s[/color]\n" % base_url)

func _on_http_response(result: int, code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if code == 200:
		var json_str = body.get_string_from_utf8()
		# Pretty print JSON for readability in console
		var parsed = JSON.parse_string(json_str)
		if parsed != null:
			_append_log("[color=green][BACKEND RESPONSE][/color]\n" + JSON.stringify(parsed, "  ") + "\n")
		else:
			_append_log("[color=green][BACKEND RESPONSE][/color]\n" + json_str + "\n")
	else:
		_append_log("[color=red]Backend error (HTTP %d). Is FastAPI running?[/color]\n" % code)

func _append_log(text: String) -> void:
	output_log.append_text(text + "\n")
	
	# Optimization: Cap log lines to prevent memory bloat and lag
	if output_log.get_line_count() > MAX_LOG_LINES:
		# Godot 4 RichTextLabel doesn't have a direct "remove oldest line"
		# So we clear and keep the last 50% to prevent continuous re-allocations
		var full_text = output_log.text
		var cutoff = full_text.length() / 2
		output_log.text = full_text.substr(cutoff)
		
	# Auto-scroll
	var scroll = output_log.get_v_scroll_bar()
	scroll.value = scroll.max_value
