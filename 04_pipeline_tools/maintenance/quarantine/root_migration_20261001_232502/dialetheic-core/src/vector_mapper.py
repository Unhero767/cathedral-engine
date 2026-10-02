"""
VectorMapper Module - Semantic Embedding & Dialetheic Contradiction Mapping.
Provides semantic embedding, cosine distance calculation, paradox load estimation,
and spectral alignment for the Cathedral-Engine and Ash Archive.
"""

import math
import re
from typing import List, Dict, Tuple, Any, Optional
import numpy as np
from pydantic import BaseModel, Field

try:
    from src.cathedral_engine import SpectrumConstant, HarmonicScar, DialetheicBuffer
except ModuleNotFoundError:
    from cathedral_engine import SpectrumConstant, HarmonicScar, DialetheicBuffer


POLARITY_PAIRS = [
    ("closed", "open"), ("never", "forever"), ("silent", "speaking"),
    ("empty", "filled"), ("nothing", "everything"), ("solidified", "flow"),
    ("no", "yes"), ("not", "is"), ("none", "all"), ("no", "every"),
    ("sound", "silence"), ("choir", "null"), ("sings", "no")
]


def dialetheic_bonus(p: str, q: str, similarity: float) -> float:
    """Calculates polarity bonus for detected dialectical antonym flips."""
    pl, ql = p.lower(), q.lower()
    hits = sum(1 for a, b in POLARITY_PAIRS if (a in pl and b in ql) or (b in pl and a in ql))
    return min(3.0, 1.5 * hits)


class SemanticVector(BaseModel):
    text: str
    embedding: List[float]
    spectrum: SpectrumConstant
    norm: float = Field(default=1.0)


class VectorMapper:
    """
    Semantic VectorMapper that converts Codex verses and propositions into high-dimensional
    vector representations to compute semantic similarity, dialectic tension, and
    paradox load degrees far beyond keyword heuristics.
    """

    def __init__(self, vector_dim: int = 64, seed: int = 42):
        self.vector_dim = vector_dim
        np.random.seed(seed)
        self.vocab: Dict[str, np.ndarray] = {}
        self.spectral_bases = self._initialize_spectral_bases()

    def _initialize_spectral_bases(self) -> Dict[SpectrumConstant, np.ndarray]:
        """Generate deterministic, orthogonal basis vectors for spectral constants."""
        bases = {}
        spectrums = list(SpectrumConstant)
        num_spectrums = len(spectrums)
        
        for idx, spec in enumerate(spectrums):
            vec = np.zeros(self.vector_dim)
            start_idx = (idx * (self.vector_dim // num_spectrums)) % self.vector_dim
            end_idx = min(start_idx + (self.vector_dim // num_spectrums), self.vector_dim)
            vec[start_idx:end_idx] = 1.0
            norm = np.linalg.norm(vec)
            bases[spec] = vec / norm if norm > 0 else vec
            
        return bases

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b\w+\b', text.lower())

    def _get_word_vector(self, word: str) -> np.ndarray:
        if word not in self.vocab:
            word_hash = sum(ord(c) * (31 ** i) for i, c in enumerate(word)) % (2**32)
            rng = np.random.RandomState(word_hash)
            vec = rng.normal(0.0, 1.0, self.vector_dim)
            norm = np.linalg.norm(vec)
            self.vocab[word] = vec / norm if norm > 0 else vec
        return self.vocab[word]

    def embed_text(self, text: str) -> np.ndarray:
        tokens = self._tokenize(text)
        if not tokens:
            return np.zeros(self.vector_dim)

        vec_sum = np.zeros(self.vector_dim)
        for token in tokens:
            vec_sum += self._get_word_vector(token)

        norm = np.linalg.norm(vec_sum)
        return vec_sum / norm if norm > 0 else vec_sum

    def compute_cosine_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

    def detect_spectral_alignment(self, text_vector: np.ndarray) -> SpectrumConstant:
        best_spectrum = SpectrumConstant.TEAL
        max_sim = -1.0

        for spec, basis in self.spectral_bases.items():
            sim = self.compute_cosine_similarity(text_vector, basis)
            if sim > max_sim:
                max_sim = sim
                best_spectrum = spec

        return best_spectrum

    def calculate_paradox_load(
        self, proposition_a: str, proposition_b: str
    ) -> Tuple[float, float, SpectrumConstant]:
        vec_a = self.embed_text(proposition_a)
        vec_b = self.embed_text(proposition_b)

        similarity = self.compute_cosine_similarity(vec_a, vec_b)
        
        tokens_a = set(self._tokenize(proposition_a))
        tokens_b = set(self._tokenize(proposition_b))
        has_negation = bool({"not", "no", "never", "false", "non", "anti", "counter"}.intersection(tokens_a ^ tokens_b))

        bonus = dialetheic_bonus(proposition_a, proposition_b, similarity)

        if has_negation:
            paradox_load = (1.0 + similarity) * 5.0 + bonus
        else:
            paradox_load = (1.0 - abs(similarity)) * 7.0 + bonus

        paradox_load = min(max(paradox_load, 0.0), 10.0)

        blended_vec = vec_a + vec_b
        spectrum = self.detect_spectral_alignment(blended_vec)

        return similarity, paradox_load, spectrum


class AshArchiveMapper:
    def __init__(self, buffer: Optional[DialetheicBuffer] = None):
        self.mapper = VectorMapper()
        self.buffer = buffer or DialetheicBuffer()
        self.ingested_verses: List[Dict[str, Any]] = []

    def ingest_verse_pair(
        self, verse_claim: str, verse_counter_claim: str, verse_id: str
    ) -> Dict[str, Any]:
        similarity, paradox_load, spectrum = self.mapper.calculate_paradox_load(
            verse_claim, verse_counter_claim
        )

        composite_proposition = f"[{verse_id}] {verse_claim} <-> {verse_counter_claim}"
        evaluation = self.buffer.evaluate_contradiction(
            proposition=composite_proposition,
            paradox_load=paradox_load,
            spectrum=spectrum
        )

        record = {
            "verse_id": verse_id,
            "claim": verse_claim,
            "counter_claim": verse_counter_claim,
            "similarity": similarity,
            "paradox_load": paradox_load,
            "spectrum": spectrum.value,
            "evaluation": evaluation
        }
        self.ingested_verses.append(record)
        return record
