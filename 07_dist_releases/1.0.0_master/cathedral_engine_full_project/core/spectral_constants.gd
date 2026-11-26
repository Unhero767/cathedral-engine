# SpectralConstants.gd
# Metalogical Bedrock: 6 Spectral Constants + Null Space & Transductive Ego Density
class_name SpectralConstants extends Node

# Master Axiom: Emotion = Physics = Magic = Biology = Architecture

# Constants definition
const THETA: String = "THETA"       # Burnished Gold / Joy & Law
const PSI: String = "PSI"           # Matte Teal / Curiosity & Recursion
const DELTA: String = "DELTA"       # Oxford Blue / Sorrow & Archiving
const PHI: String = "PHI"           # Crimson / Anger & Entropy
const OMEGA: String = "OMEGA"       # Dark Violet / Fear & Adaptation
const EPSILON: String = "EPSILON"   # Emerald / Love & Binding
const NULL_CONST: String = "NULL"   # Obsidian / Void & Erasure

# Baseline Telemetry
const RHO_BASELINE: float = 8.3     # Baseline Ego Density (rho_0)
const GOLDEN_RATIO: float = 1.61803398875

# Spectral Constant Property Table
const CONSTANTS_DATA: Dictionary = {
	THETA: {
		"name": "Theta",
		"color": Color(0.855, 0.647, 0.125, 1.0), # #DAA520
		"hex": "#DAA520",
		"frequency_thz": 580.0,
		"semantic": "Joy / Law / Immutable Durability",
		"base_weight": 1.618,
		"rigidity_factor": 1.5,
		"stratum_origin": "Prime Foundations (Book I, Book IV)"
	},
	PSI: {
		"name": "Psi",
		"color": Color(0.0, 0.898, 1.0, 1.0), # #00E5FF / #008080
		"hex": "#00E5FF",
		"frequency_thz": 510.0,
		"semantic": "Curiosity / Recursion / Algorithmic Verification",
		"base_weight": 1.414,
		"rigidity_factor": 1.1,
		"stratum_origin": "Prime Foundations (Book II, Book VI)"
	},
	DELTA: {
		"name": "Delta",
		"color": Color(0.0, 0.129, 0.278, 1.0), # #002147
		"hex": "#002147",
		"frequency_thz": 460.0,
		"semantic": "Sorrow / Archiving / Zero-Decay Permineralization",
		"base_weight": 1.732,
		"rigidity_factor": 1.8,
		"stratum_origin": "Prime Foundations (Book III)"
	},
	PHI: {
		"name": "Phi",
		"color": Color(0.863, 0.078, 0.235, 1.0), # #DC143C
		"hex": "#DC143C",
		"frequency_thz": 430.0,
		"semantic": "Anger / Entropy / Kinetic Remaking",
		"base_weight": 1.0,
		"rigidity_factor": 0.6,
		"stratum_origin": "Prime Foundations (Book V, Book VII)"
	},
	OMEGA: {
		"name": "Omega",
		"color": Color(0.541, 0.169, 0.886, 1.0), # #8A2BE2
		"hex": "#8A2BE2",
		"frequency_thz": 710.0,
		"semantic": "Fear / Adaptation / Edge-Walking Turbulence",
		"base_weight": 1.25,
		"rigidity_factor": 0.8,
		"stratum_origin": "Prime Foundations (Book VIII)"
	},
	EPSILON: {
		"name": "Epsilon",
		"color": Color(0.314, 0.784, 0.471, 1.0), # #50C878
		"hex": "#50C878",
		"frequency_thz": 520.0,
		"semantic": "Love / Binding / Dynamic Tissue Repair",
		"base_weight": 1.618,
		"rigidity_factor": 1.2,
		"stratum_origin": "Inner Mandala (Book XV)"
	},
	NULL_CONST: {
		"name": "Null",
		"color": Color(0.0196, 0.0196, 0.0196, 1.0), # #050505
		"hex": "#050505",
		"frequency_thz": 0.0,
		"semantic": "Obsidian / Void / Absolute Anti-Resonance",
		"base_weight": 0.0,
		"rigidity_factor": 0.0,
		"stratum_origin": "Inner Shadow Canon (Book XXXV)"
	}
}

# Returns the color associated with a constant
func get_spectral_color(constant_key: String) -> Color:
	if CONSTANTS_DATA.has(constant_key):
		return CONSTANTS_DATA[constant_key]["color"]
	return Color(1.0, 1.0, 1.0, 1.0)

# Returns the frequency in THz
func get_frequency_thz(constant_key: String) -> float:
	if CONSTANTS_DATA.has(constant_key):
		return CONSTANTS_DATA[constant_key]["frequency_thz"]
	return 0.0

# Calculates material properties based on:
# M_property = sum(W_s * F_s(rho) * C_s)
func calculate_material_property(spectrum_weights: Dictionary, ego_density: float = RHO_BASELINE) -> Dictionary:
	var total_rigidity: float = 0.0
	var total_durability: float = 0.0
	var total_conductivity: float = 0.0
	var total_mass: float = 0.0
	var dominant_constant: String = THETA
	var max_weight: float = -1.0
	
	var rho_ratio: float = ego_density / RHO_BASELINE
	
	for key in spectrum_weights.keys():
		var weight: float = float(spectrum_weights[key])
		if not CONSTANTS_DATA.has(key):
			continue
		var data: Dictionary = CONSTANTS_DATA[key]
		var f_rho: float = data["rigidity_factor"] * (1.0 + 0.15 * (rho_ratio - 1.0))
		var base_w: float = data["base_weight"]
		
		total_rigidity += weight * f_rho * base_w
		total_durability += weight * (data["frequency_thz"] / 100.0) * rho_ratio
		total_conductivity += weight * (1000.0 / (data["frequency_thz"] + 10.0))
		total_mass += weight * f_rho * 2.5
		
		if weight > max_weight:
			max_weight = weight
			dominant_constant = key
			
	return {
		"rigidity": total_rigidity,
		"durability": total_durability,
		"conductivity": total_conductivity,
		"mass": total_mass,
		"dominant_constant": dominant_constant,
		"dominant_color": get_spectral_color(dominant_constant),
		"ego_density_applied": ego_density
	}

# Calculates A-Field spatial horizon:
# R = R_0 * (1 + beta * ||E|| * (rho / rho_0))
func calculate_spatial_horizon(base_radius: float, emotional_magnitude: float, ego_density: float = RHO_BASELINE, beta: float = 0.35) -> float:
	var rho_ratio: float = ego_density / RHO_BASELINE
	return base_radius * (1.0 + beta * emotional_magnitude * rho_ratio)
