extends Node

@export var shader_material: ShaderMaterial
@export var entropy_file_path: String = "res://assets/entropy_map.bin"

func _ready() -> void:
    apply_entropy_texture_uniform()

func apply_entropy_texture_uniform() -> void:
    if not FileAccess.file_exists(entropy_file_path):
        return
    var file = FileAccess.open(entropy_file_path, FileAccess.READ)
    var buffer = file.get_buffer(file.get_length())
    
    var image = Image.create_from_data(256, 256, false, Image.FORMAT_RF, buffer)
    var texture = ImageTexture.create_from_image(image)
    
    if shader_material:
        shader_material.set_shader_parameter("u_entropy_attenuation", texture)
