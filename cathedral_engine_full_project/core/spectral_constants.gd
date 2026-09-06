# class_name SpectralConstants
extends Node

enum Constant {
	THETA_GOLD,    # Joy / Law / Coherence
	PSI_TEAL,      # Curiosity / Recursion / Branching
	DELTA_BLUE,    # Sorrow / Memory / Archiving
	PHI_RED,       # Anger / Entropy / Rupture
	OMEGA_VIOLET,  # Fear / Adaptation / Noise
	EPSILON_GREEN, # Love / Binding / Ligature
	NULL_OBSIDIAN  # Void / Anti-Resonance / Erasure
}

const PALETTE: Dictionary = {
	Constant.THETA_GOLD: Color("#D4AF37"),
	Constant.PSI_TEAL: Color("#008080"),
	Constant.DELTA_BLUE: Color("#002147"),
	Constant.PHI_RED: Color("#8B0000"),
	Constant.OMEGA_VIOLET: Color("#4B0082"),
	Constant.EPSILON_GREEN: Color("#50C878"),
	Constant.NULL_OBSIDIAN: Color("#0B0B0B")
}

const BASELINE_EGO_DENSITY: float = 8.3
const CRITICAL_CONSISTENCY: float = 1.0
