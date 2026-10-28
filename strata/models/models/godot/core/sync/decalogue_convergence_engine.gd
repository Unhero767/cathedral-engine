class_name DecalogueConvergenceEngine
extends Node

enum BelnapDunnState { 
	NEITHER = 0, 
	FALSE = 1, 
	TRUE = 2, 
	BOTH = 3 
}

func evaluate_belnap_dunn_fast(pos_confidence: float, neg_confidence: float, threshold: float = 0.5) -> BelnapDunnState:
	var pos_bit: int = int(pos_confidence >= threshold)
	var neg_bit: int = int(neg_confidence >= threshold)
	var state_mask: int = (pos_bit << 1) | neg_bit
	return state_mask as BelnapDunnState
