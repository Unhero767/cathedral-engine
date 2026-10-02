class ParaconsistentEvaluator:
    """
    Evaluates lattice operations under the Belnap-Dunn four-valued logic system,
    preserving dialetheic collisions as Harmonic Scars rather than collapsing them.
    """

    @staticmethod
    def merge(state_a: ParaconsistentState, state_b: ParaconsistentState) -> ParaconsistentState:
        t_set_a = ParaconsistentEvaluator._to_set(state_a.truth)
        t_set_b = ParaconsistentEvaluator._to_set(state_b.truth)

        # First-degree entailment intersection/union mechanics
        # For parallel merge, we combine evidence vectors
        merged_sources = list(set(state_a.sources + state_b.sources))
        combined_t = t_set_a.union(t_set_b)
        
        resulting_truth = ParaconsistentEvaluator._from_set(combined_t)
        
        scar = None
        if resulting_truth == TruthValue.BOTH:
            scar = f"Harmonic Scar crystallized from collision of sources: {merged_sources}"

        return ParaconsistentState(
            entity_id=state_a.entity_id,
            truth=resulting_truth,
            sources=merged_sources,
            confidence=min(state_a.confidence, state_b.confidence),
            harmonic_scar=scar
        )

    @staticmethod
    def _to_set(val: TruthValue) -> Set[int]:
        if val == TruthValue.TRUE: return {1}
        if val == TruthValue.FALSE: return {0}
        if val == TruthValue.BOTH: return {1, 0}
        return set()

    @staticmethod
    def _from_set(s: Set[int]) -> TruthValue:
        if s == {1}: return TruthValue.TRUE
        if s == {0}: return TruthValue.FALSE
        if s == {1, 0}: return TruthValue.BOTH
        return TruthValue.NEITHER

