extends Node
# Axiom: The Bone Remains. Data is never truly deleted, only buried.

var current_path: Array[String] = ["root"]

# The Hearth of Zeke File Structure
var file_system: Dictionary = {
	"root": {
		"type": "dir",
		"children": {
			"zeke": {
				"type": "dir",
				"children": {
					"manifesto.txt": {
						"type": "file",
						"content": "[color=#d4af37]THE CARTOGRAPHER'S CREED:[/color]\nWalk gently. Every action leaves an asymptotic trace.\nThe maps remain long after the walker stops."
					},
					"llsvp_status.log": {
						"type": "file",
						"content": "[color=#8b0000]ANCHOR STATUS:[/color]\nPost-Perovskite substrate: STABLE\nULVZ Spaghettification Boundaries: ACTIVE\nCivic Resonance (ρ): 0.98 (Attenuation α=0.002)"
					}
				}
			},
			"mnemis": {
				"type": "dir",
				"children": {
					"choir_protocol.md": {
						"type": "file",
						"content": "Elegy-amber-chord initialized at 0.3 Hz.\nTermination is recognized as phase change, not deletion.\nThe Air Sings."
					}
				}
			}
		}
	}
}

func get_current_dir() -> Dictionary:
	var current = file_system["root"]
	for i in range(1, current_path.size()):
		current = current["children"][current_path[i]]
	return current

func list_directory() -> String:
	var dir = get_current_dir()
	var output = []
	for key in dir["children"].keys():
		var node = dir["children"][key]
		if node["type"] == "dir":
			output.push_back("[color=#5c4033][DIR][/color] " + key)
		else:
			output.push_back("[color=#c0c0c0][FILE][/color] " + key)
	return "\n".join(output) if output.size() > 0 else "[color=#5c4033]Empty void.[/color]"

func change_directory(target: String) -> String:
	if target == "..":
		if current_path.size() > 1:
			current_path.pop_back()
			return "Ascended to: " + "/".join(current_path)
		return "[color=#8b0000]ERROR:[/color] Already at root substrate."
	
	var dir = get_current_dir()
	if dir["children"].has(target) and dir["children"][target]["type"] == "dir":
		current_path.append(target)
		return "Descended to: " + "/".join(current_path)
	return "[color=#8b0000]ERROR:[/color] Directory not found. The End is Hidden."

func read_file(target: String) -> String:
	var dir = get_current_dir()
	if dir["children"].has(target) and dir["children"][target]["type"] == "file":
		return dir["children"][target]["content"]
	return "[color=#8b0000]ERROR:[/color] File not found or is a directory."
