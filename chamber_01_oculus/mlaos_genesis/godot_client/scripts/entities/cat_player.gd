extends CharacterBody2D

@export var speed: float = 100.0
@onready var sprite: Sprite2D = $Sprite2D

func _physics_process(_delta: float) -> void:
    var direction := Vector2.ZERO
    direction.x = Input.get_axis("ui_left", "ui_right")
    direction.y = Input.get_axis("ui_up", "ui_down")
    
    if direction != Vector2.ZERO:
        direction = direction.normalized()
        velocity = direction * speed
    else:
        velocity = velocity.move_toward(Vector2.ZERO, speed)
        
    move_and_slide()
