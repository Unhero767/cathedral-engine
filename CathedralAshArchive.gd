class_name CathedralAshArchive
extends RefCounted

enum TraumaType { PRAYER_BRAND = 0, COMBAT_LACERATION = 1, ASH_DEPOSIT = 2 }

var _img: Image
var _tex: ImageTexture

func _init() -> void:
	_img = Image.create(128, 128, false, Image.FORMAT_RGBA8)
	_img.fill(Color(0, 0, 0, 0))
	_tex = ImageTexture.create_from_image(_img)

func inscribe_trauma(type: TraumaType, uv: Vector2, sev: float) -> void:
	var cx: int = int(uv.x * 128.0)
	var cy: int = int(uv.y * 128.0)
	var col: Color = Color(1.0, 0.82, 0.28, 0.9)
	if type == TraumaType.COMBAT_LACERATION:
		col = Color(0.8, 0.15, 0.1, 0.9)
	elif type == TraumaType.ASH_DEPOSIT:
		col = Color(0.25, 0.23, 0.22, 0.7)
		
	for y in range(-3, 4):
		for x in range(-3, 4):
			if (x * x + y * y) <= 9:
				var px: int = cx + x
				var py: int = cy + y
				if px >= 0 and px < 128 and py >= 0 and py < 128:
					_img.set_pixel(px, py, col)
	_tex.update(_img)

func get_texture() -> ImageTexture:
	return _tex
