class_name CathedralSomaticEngine
extends Node3D

enum ParamIdx {
	ADIPOSE_ABDOMINAL_LOWER = 0,
	ADIPOSE_ABDOMINAL_UPPER = 1,
	ADIPOSE_BRACHIAL = 2,
	ADIPOSE_BUCCAL = 3,
	ADIPOSE_CERVICAL_POSTERIOR = 4,
	ADIPOSE_FEMORAL_ANTERIOR = 5,
	ADIPOSE_FEMORAL_POSTERIOR = 6,
	ADIPOSE_GLUTEAL = 7,
	ADIPOSE_LUMBAR = 8,
	ADIPOSE_PECTORAL = 9,
	ADIPOSE_SCAPULAR = 10,
	ADIPOSE_SUBCUTANEOUS_GENERAL = 11,
	ADIPOSE_SURAL = 12,
	ADIPOSE_TEMPORAL = 13,
	ADIPOSE_VISCERAL = 14,
	ADIPOSE_ZYGOMATIC = 15,
	CLEARANCE_CRANIAL_CALVARIA_OFFSET = 16,
	CRANIAL_VAULT_DEPTH = 45,
	DERMAL_ERYTHEMA_BASAL = 51,
	DERMAL_MELANIN_CONCENTRATION = 52,
	HYPERTROPHY_PECTORALIS_MAJOR = 74,
	HYPERTROPHY_RECTUS_FEMORIS = 77,
	OSTEOLOGY_BICRISTAL_PELVIC_WIDTH = 89,
	RESONANCE_AFIELD_CONDUCTANCE = 104,
	RESONANCE_OCULAR_CYAN_LUMINOSITY = 114,
	VASCULARITY_FOREARM_ANTERIOR = 126
}

var raw_values: PackedFloat32Array = PackedFloat32Array()

func _ready() -> void:
	raw_values.resize(128)
	raw_values.fill(0.0)

func load_dna_buffer(buffer: PackedByteArray) -> bool:
	if buffer.size() != 512:
		return false
	if raw_values.size() != 128:
		raw_values.resize(128)
	for i in range(128):
		raw_values[i] = buffer.decode_float(i * 4)
	return true

func set_param_by_index(idx: int, val: float) -> void:
	if raw_values.size() != 128:
		raw_values.resize(128)
	if idx >= 0 and idx < 128:
		raw_values[idx] = clampf(val, 0.0, 2.0)
