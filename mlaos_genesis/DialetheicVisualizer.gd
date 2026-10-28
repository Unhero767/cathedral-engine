extends CanvasLayer
class_name DialetheicVisualizer

var panel: Panel
var asset_label: Label
var status_label: Label
var hash_label: Label

func _ready() -> void:
    panel = Panel.new()
    panel.set_anchors_preset(Control.PRESET_FULL_RECT)
    panel.modulate = Color(0.05, 0.05, 0.1)
    add_child(panel)

    var center = CenterContainer.new()
    center.set_anchors_preset(Control.PRESET_FULL_RECT)
    panel.add_child(center)

    var vbox = VBoxContainer.new()
    center.add_child(vbox)

    asset_label = Label.new()
    asset_label.add_theme_font_size_override("font_size", 24)
    vbox.add_child(asset_label)

    status_label = Label.new()
    status_label.add_theme_font_size_override("font_size", 32)
    vbox.add_child(status_label)

    hash_label = Label.new()
    hash_label.add_theme_font_size_override("font_size", 18)
    vbox.add_child(hash_label)
    
    update_display("AWAITING ASSET MANIFESTATION", 0)

func update_display(asset_id: String, state: int, archive_hash: String = "") -> void:
    asset_label.text = "ASSET DESIGNATION: " + asset_id
    
    match state:
        0:
            status_label.text = "ONTOLOGICAL STATE: UNMANIFESTED"
            status_label.modulate = Color(0.5, 0.5, 0.5)
        1:
            status_label.text = "ONTOLOGICAL STATE: ALIVE (Grid Active)"
            status_label.modulate = Color(0.2, 0.8, 0.5)
        2:
            status_label.text = "ONTOLOGICAL STATE: TERMINATED (Inert)"
            status_label.modulate = Color(0.8, 0.2, 0.2)
        3:
            status_label.text = "ONTOLOGICAL STATE: DIALETHEIC (Harmonic Scar)"
            status_label.modulate = Color(0.9, 0.7, 0.1)
            
    if archive_hash != "":
        hash_label.text = "\nASH ARCHIVE MERKLE ROOT:\n" + archive_hash
