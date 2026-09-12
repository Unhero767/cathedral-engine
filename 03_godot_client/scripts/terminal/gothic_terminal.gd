extends PanelContainer

@export var history_label: RichTextLabel
@export var input_line: LineEdit
@export var prompt_prefix: String = "[color=#d4af37]ZEKE@HEARTH[/color] [color=#5c4033]▶[/color] "

var command_history: Array[String] = []
var history_index: int = -1
var current_prompt_path: String = "/root"

func _ready():
	if input_line != null:
		if not input_line.text_submitted.is_connected(_on_input_line_text_submitted):
			input_line.text_submitted.connect(_on_input_line_text_submitted)
		input_line.grab_focus()

	if history_label == null:
		var _rtls = find_children("*", "RichTextLabel", true, false)
		if not _rtls.is_empty():
			history_label = _rtls[0]
		else:
			var _lbls = find_children("*", "Label", true, false)
			if not _lbls.is_empty():
				history_label = _lbls[0]

	if history_label == null:
		var _rtls = find_children("*", "RichTextLabel", true, false)
		if not _rtls.is_empty():
			history_label = _rtls[0]
		else:
			var _lbls = find_children("*", "Label", true, false)
			if not _lbls.is_empty():
				history_label = _lbls[0]

	if input_line == null:
		var _les = find_children('*', 'LineEdit', true, false)
		if not _les.is_empty():
			input_line = _les[0]
	if input_line != null:
		input_line.placeholder_text = "Enter directive..."
	_print_system_boot()
	input_line.grab_focus()

func _input(event: InputEvent):
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_UP:
			_navigate_history(-1)
			get_viewport().set_input_as_handled()
		elif event.keycode == KEY_DOWN:
			_navigate_history(1)
			get_viewport().set_input_as_handled()

func _on_input_line_text_submitted(text: String):
	if text.is_empty(): return
	var clean_text = text.strip_edges()
	command_history.append(clean_text)
	history_index = command_history.size()
	
	TerminalTick.log_command(clean_text, "Processed", 0)
	_append_to_history(prompt_prefix + current_prompt_path + " > " + text)
	input_line.clear()
	_process_command(clean_text)
	input_line.grab_focus()

func _process_command(cmd: String):
	var parts = cmd.split(" ", false)
	var command = parts[0].to_lower()
	var args = parts.slice(1)
	
	match command:
		"help":
			_append_to_history("[color=#d4af37]DIRECTIVES:[/color]\n  ls, cd [dir], cat [file], clear, status, walk_gently")
		"clear":
			if history_label == null:
				var _rtls = find_children("*", "RichTextLabel", true, false)
				history_label = _rtls[0] if not _rtls.is_empty() else find_children("*", "Label", true, false)[0]
			if history_label != null:
				if history_label == null:
					var _rtls = find_children("*", "RichTextLabel", true, false)
					history_label = _rtls[0] if not _rtls.is_empty() else find_children("*", "Label", true, false)[0]
				if history_label != null:
					history_label.text = ""
		"status":
			_append_to_history("[color=#8b0000]SYSTEM STATUS:[/color]\n  Civic Resonance: Stable\n  Terminal Tick: " + str(TerminalTick._terminal_tick))
		"walk_gently":
			_append_to_history("[i]The cartographer stops walking, but the maps remain.[/i]")
		"ls":
			_append_to_history(VFS.list_directory())
		"cd":
			if args.size() == 0:
				_append_to_history("[color=#8b0000]ERROR:[/color] Specify a directory.")
			else:
				var result = VFS.change_directory(args[0])
				_append_to_history(result)
				current_prompt_path = "/" + "/".join(VFS.current_path.slice(1))
		"cat":
			if args.size() == 0:
				_append_to_history("[color=#8b0000]ERROR:[/color] Specify a file.")
			else:
				_append_to_history(VFS.read_file(args[0]))
		_:
			_append_to_history("[color=#8b0000]HAZARD:[/color] Directive not recognized. The End is Hidden.")

func _append_to_history(text: String):
	if history_label == null:
		var _rtls = find_children("*", "RichTextLabel", true, false)
		history_label = _rtls[0] if not _rtls.is_empty() else find_children("*", "Label", true, false)[0]
	if history_label != null:
		if history_label == null:
			var _rtls = find_children("*", "RichTextLabel", true, false)
			history_label = _rtls[0] if not _rtls.is_empty() else find_children("*", "Label", true, false)[0]
		if history_label != null:
			history_label.text += text + "\n"
	var scroll = history_label.get_parent() as ScrollContainer
	if scroll:
		call_deferred("_scroll_to_bottom", scroll)

func _scroll_to_bottom(scroll: ScrollContainer):
	scroll.scroll_vertical = scroll.get_v_scroll_bar().max_value

func _navigate_history(direction: int):
	if command_history.is_empty(): return
	history_index = clamp(history_index + direction, -1, command_history.size() - 1)
	if history_index == -1:
		input_line.text = ""
	else:
		input_line.text = command_history[history_index]
	input_line.caret_column = input_line.text.length()

func _print_system_boot():
	_append_to_history("[color=#d4af37]Initializing Hearth of Zeke...[/color]")
	_append_to_history("[color=#d4af37]Blue Choir protocol engaged.[/color]\n")
