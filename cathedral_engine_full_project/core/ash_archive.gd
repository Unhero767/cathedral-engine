extends Node

# AshArchive.gd
# SHA-256 Merkle DAG Append-Only Ledger & Never-Overwrite Carbonization Pipeline

signal entry_committed(merkle_hash: String, j_hash: String, sequence_id: int)
signal logic_carbonized(ast_hash: String, reason: String)
signal chain_tamper_detected(node_id: int)

# Merkle DAG Node Structure
class AshNode:
	var id: int
	var timestamp_usec: int
	var parent_hashes: Array[String] = []
	var payload: Dictionary = {}
	var merkle_hash: String = ""
	var j_hash: String = "" # Obsidian Cipher Hash
	var tags: Array = []
	var is_carbonized: bool = false
	
	func _init(p_id: int, p_parents: Array[String], p_payload: Dictionary, p_tags: Array = [], p_carbon: bool = false):
		id = p_id
		timestamp_usec = Time.get_unix_time_from_system() * 1000000 + Time.get_ticks_usec()
		parent_hashes = p_parents
		payload = p_payload
		tags = p_tags
		is_carbonized = p_carbon
		merkle_hash = compute_merkle_hash()
		j_hash = compute_j_hash()
		
	func compute_merkle_hash() -> String:
		var raw_str = str(id) + ":" + str(timestamp_usec) + ":" + str(parent_hashes) + ":" + JSON.stringify(payload)
		return raw_str.sha256_text()
		
	func compute_j_hash() -> String:
		# Obsidian cipher combines merkle hash with reverse entropy salt
		var salt = "MLAOS_OBSIDIAN_CORE_" + str(id * 377)
		return (merkle_hash + salt).sha256_text()

var ledger: Array[AshNode] = []
var hash_lookup: Dictionary = {} # String -> AshNode
var genesis_hash: String = ""

func _ready() -> void:
	_init_genesis()

func _init_genesis() -> void:
	if ledger.is_empty():
		var genesis_payload = {
			"protocol": "MLAOS_JUSTIFIED_BELIEF_PROTOCOL_V1",
			"doctrine": "NEVER_OVERWRITE",
			"prime_axiom": "Emotion = Physics = Magic = Biology = Architecture",
			"root_sovereign": "Kenneth Dallmier"
		}
		var genesis_node = AshNode.new(0, [], genesis_payload, ["GENESIS", "BEDROCK"], true)
		ledger.append(genesis_node)
		hash_lookup[genesis_node.merkle_hash] = genesis_node
		genesis_hash = genesis_node.merkle_hash
		print("[AshArchive] Genesis block initialized: ", genesis_hash)

# Appends a new immutable state entry to the DAG
func commit_entry(state_payload: Dictionary, tags: Array = []) -> String:
	var parents: Array[String] = []
	if not ledger.is_empty():
		parents.append(ledger.back().merkle_hash)
		
	var node = AshNode.new(ledger.size(), parents, state_payload, tags, false)
	ledger.append(node)
	hash_lookup[node.merkle_hash] = node
	
	emit_signal("entry_committed", node.merkle_hash, node.j_hash, node.id)
	return node.merkle_hash

# Carbonization Pipeline: Strips active computational hooks and fossilizes failed logic
func carbonize_failed_logic(ast_dict: Dictionary, reason: String) -> String:
	var fossilized_payload = {
		"type": "CARBONIZED_AST",
		"reason": reason,
		"fossilized_structure": ast_dict,
		"read_only": true,
		"active_hooks_stripped": true
	}
	var parents: Array[String] = []
	if not ledger.is_empty():
		parents.append(ledger.back().merkle_hash)
		
	var node = AshNode.new(ledger.size(), parents, fossilized_payload, ["CARBONIZED", "AST_FOSSIL"], true)
	ledger.append(node)
	hash_lookup[node.merkle_hash] = node
	
	emit_signal("logic_carbonized", node.merkle_hash, reason)
	return node.merkle_hash

# Necro-Parsing: Air-gapped retrieval for annihilation ritual against active logic storms
func necro_parse(target_hash: String) -> Dictionary:
	if hash_lookup.has(target_hash):
		var node: AshNode = hash_lookup[target_hash]
		return {
			"id": node.id,
			"merkle_hash": node.merkle_hash,
			"j_hash": node.j_hash,
			"payload": node.payload,
			"is_carbonized": node.is_carbonized,
			"necro_parsed": true
		}
	return {}

# Verify cryptographic DAG integrity
func verify_chain_integrity() -> bool:
	for i in range(1, ledger.size()):
		var node = ledger[i]
		var recomputed = node.compute_merkle_hash()
		if node.merkle_hash != recomputed:
			emit_signal("chain_tamper_detected", node.id)
			return false
	return true

func get_ledger_count() -> int:
	return ledger.size()
