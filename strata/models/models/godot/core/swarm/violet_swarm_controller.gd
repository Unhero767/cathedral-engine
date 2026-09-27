extends Node
class_name VioletSwarmController

const BUFFER_CAPACITY: int = 128
const VIOLET_LLE_TARGET: float = 0.0200
const DAMPER_DEADBAND: float = 0.1500

@export var num_agents: int = 60
@export var grid_size: int = 32
@export var pyragas_delay_sec: float = 0.667
@export var pyragas_gain_k: float = 0.45

var _agents: Dictionary = {}
var _ring_buffer: PackedVector2Array = PackedVector2Array()
var _buffer_head: int = 0
var _current_lle: float = 0.0200
var _current_entropy: float = 1.8912

func _ready() -> void:
	_ring_buffer.resize(BUFFER_CAPACITY)
	_ring_buffer.fill(Vector2.ZERO)
	_init_agents()

func _init_agents() -> void:
	for i in range(num_agents):
		_agents["Agent_%02d" % i] = {
			"pos": Vector2(randf_range(0.0, grid_size), randf_range(0.0, grid_size)),
			"vel": Vector2(randf_range(-0.5, 0.5), randf_range(-0.5, 0.5)),
			"alive": true
		}

func _physics_process(delta: float) -> void:
	var centroid: Vector2 = _compute_centroid()
	
	_ring_buffer[_buffer_head] = centroid
	var delay_ticks: int = clampi(int(pyragas_delay_sec / delta), 1, BUFFER_CAPACITY - 1)
	var read_idx: int = (_buffer_head - delay_ticks + BUFFER_CAPACITY) % BUFFER_CAPACITY
	var delayed_centroid: Vector2 = _ring_buffer[read_idx]
	_buffer_head = (_buffer_head + 1) % BUFFER_CAPACITY

	var f_pyragas: Vector2 = -pyragas_gain_k * (centroid - delayed_centroid)

	var live_count: int = 0
	var speed_sum: float = 0.0

	for agent in _agents.values():
		if not agent["alive"]:
			continue
		live_count += 1

		var vel: Vector2 = agent["vel"]
		var speed: float = vel.length()
		var speed_dev: float = abs(speed - 0.5) / 0.5

		var f_damp: Vector2 = Vector2.ZERO
		if speed_dev > DAMPER_DEADBAND:
			var excess: float = speed_dev - DAMPER_DEADBAND
			f_damp = -0.2 * (excess * excess) * vel

		agent["vel"] += (f_pyragas + f_damp) * delta
		agent["pos"].x = fposmod(agent["pos"].x + agent["vel"].x * delta, float(grid_size))
		agent["pos"].y = fposmod(agent["pos"].y + agent["vel"].y * delta, float(grid_size))
		speed_sum += speed

	if live_count > 0:
		var avg_spd: float = speed_sum / live_count
		_current_lle = lerp(_current_lle, (avg_spd - 0.5) * 0.1, 0.05)
		_current_entropy = lerp(_current_entropy, log(live_count) * 0.45, 0.05)

func _compute_centroid() -> Vector2:
	var sum: Vector2 = Vector2.ZERO
	var cnt: int = 0
	for agent in _agents.values():
		if agent["alive"]:
			sum += agent["pos"]
			cnt += 1
	return sum / cnt if cnt > 0 else Vector2.ZERO
