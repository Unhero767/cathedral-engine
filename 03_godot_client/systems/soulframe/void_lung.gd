class_name VoidLung
extends Node

signal breath_generated(amount: float)
signal overbreathe_warning(tension: float)

var raw_trauma_intake: float = 0.0
var breath_pool: float = 100.0
var max_breath: float = 100.0
const K_CONVERSION: float = 0.75
const K_PRIME_ENTROPY: float = 0.002

func inhale_entropy(trauma_amount: float) -> void:
	raw_trauma_intake += trauma_amount
	# Law of Re-Weaving: R(T) = k*T - k'*T^2
	var breath_yield: float = (K_CONVERSION * trauma_amount) - (K_PRIME_ENTROPY * trauma_amount * trauma_amount)
	breath_yield = max(breath_yield, 0.0)
	
	breath_pool = min(breath_pool + breath_yield, max_breath * 1.5)
	
	if breath_pool > max_breath:
		emit_signal("overbreathe_warning", breath_pool - max_breath)
	
	emit_signal("breath_generated", breath_yield)
