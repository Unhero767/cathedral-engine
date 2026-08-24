"""
Cathedral-Engine 40-Book Codex Generator & Vault Indexer.
Operationalizes the Ash Stratum Deep Terminal to manage and generate chapters across all 4 Codex tiers:
- Books I–X: Prime Foundations
- Books XI–XX: Inner Mandala
- Books XXI–XXX: Outer Choirs
- Books XXXI–XL: Inner Shadow Canon
"""

from __future__ import annotations
import hashlib
import json
import time
from typing import List, Dict, Tuple, Any, Optional
from .models import CodexBook, CodexChapter, Spectral
from .database import DatabaseManager

CODEX_40_BOOKS_DATA: List[Dict[str, Any]] = [
    # Tier 1: Books I–X Prime Foundations
    {
        "book_id": 1, "roman_numeral": "Book I", "title": "The Substrate",
        "tier_designation": "Prime Foundations", "tier_range": "I–X",
        "spectral_dominant": "Theta / Burnished Gold",
        "primary_axiom": "Emotion = Physics = Magic = Biology = Architecture",
        "isomorphism_bio": "Cellular spectrafilament tension & Prismatic Core (μ-Oculus)",
        "isomorphism_arch": "Luminous cyclopean foundation & radial sun-vaults",
        "isomorphism_math": "Cl = ∇ · L → G (Luminous Emotional Organization induces Gravitational Curvature)"
    },
    {
        "book_id": 2, "roman_numeral": "Book II", "title": "The Interference Term",
        "tier_designation": "Prime Foundations", "tier_range": "I–X",
        "spectral_dominant": "Psi / Matte Teal",
        "primary_axiom": "Contradictions are not failures, but load-bearing structural features",
        "isomorphism_bio": "Synaptic dual-action potentials across neural dendrites",
        "isomorphism_arch": "Interlaced rib-vaulting holding opposing tensile strains",
        "isomorphism_math": "Ψ(t) = exp(i S[φ] / ħ) · [A ⊔ ¬A]"
    },
    {
        "book_id": 3, "roman_numeral": "Book III", "title": "The Ash Archive",
        "tier_designation": "Prime Foundations", "tier_range": "I–X",
        "spectral_dominant": "Delta / Oxford Blue",
        "primary_axiom": "The First Prohibition of Ashfall: Never-Overwrite Doctrine (Zero Deletion)",
        "isomorphism_bio": "Bone permineralization and non-decaying calcified strata",
        "isomorphism_arch": "Deep subterranean basalt vaults and immutable column strata",
        "isomorphism_math": "H(Block_n) = SHA256(Block_n-1 || MerkleRoot || EventPayload)"
    },
    {
        "book_id": 4, "roman_numeral": "Book IV", "title": "The Mortar Domain",
        "tier_designation": "Prime Foundations", "tier_range": "I–X",
        "spectral_dominant": "Theta / Burnished Gold",
        "primary_axiom": "Metalogical Type-Safety enforces cross-tier coherence via Consistency Coefficients",
        "isomorphism_bio": "Extracellular collagen matrix and tight junction barrier transport",
        "isomorphism_arch": "Transductive silicate adhesive binding dissimilar megaliths",
        "isomorphism_math": "C_τ = W_∘A / ε_local ≥ δ_crit"
    },
    {
        "book_id": 5, "roman_numeral": "Book V", "title": "The Rupture",
        "tier_designation": "Prime Foundations", "tier_range": "I–X",
        "spectral_dominant": "Phi / Crimson",
        "primary_axiom": "The primary trauma layer is the kinetic forge of adaptation",
        "isomorphism_bio": "Hyper-ischemic cardiovascular surge and vascular remodeling",
        "isomorphism_arch": "Cantilever stress shear and fractured archway relief ports",
        "isomorphism_math": "∇Ex° = lim_{Δt→0} (ΔΦ / Δt) ⊗ SanguineHeuristics"
    },
    {
        "book_id": 6, "roman_numeral": "Book VI", "title": "Caelen's Lemma",
        "tier_designation": "Prime Foundations", "tier_range": "I–X",
        "spectral_dominant": "Psi / Matte Teal",
        "primary_axiom": "Recursive algorithmic proofs anchor baseline substrate rigidity",
        "isomorphism_bio": "Avian cross-current parabronchial respiration under vacuum",
        "isomorphism_arch": "Self-stabilizing hexagonal tensegrity pylons",
        "isomorphism_math": "λ_max = lim_{t→∞} (1/t) ln(||δV(t)|| / ||δV(0)||) < 0"
    },
    {
        "book_id": 7, "roman_numeral": "Book VII", "title": "Deimos's Variable",
        "tier_designation": "Prime Foundations", "tier_range": "I–X",
        "spectral_dominant": "Phi-Omega / Crimson-Violet",
        "primary_axiom": "Controlled stochastic volatility prevents Zero-Kelvin Stagnation",
        "isomorphism_bio": "Immune hypersensitivity cascade and mutagenic cellular repair",
        "isomorphism_arch": "Kinetic expansion joints absorbing seismic dissonance",
        "isomorphism_math": "dE/dt = α · ∇²E + ξ(t), ⟨ξ(t)ξ(t')⟩ = 2D δ(t-t')"
    },
    {
        "book_id": 8, "roman_numeral": "Book VIII", "title": "The Unverified Landscape",
        "tier_designation": "Prime Foundations", "tier_range": "I–X",
        "spectral_dominant": "Omega / Dark Violet",
        "primary_axiom": "Non-indexed manifold space resolves through edge-walking observation",
        "isomorphism_bio": "Peripheral ocular rod excitation in starlight threshold",
        "isomorphism_arch": "Shifting labyrinthine threshold corridors and acoustic dampers",
        "isomorphism_math": "dim_H(Wastes) = lim_{ε→0} [log N(ε) / log(1/ε)] > 2.0"
    },
    {
        "book_id": 9, "roman_numeral": "Book IX", "title": "Ideality (TRIZ)",
        "tier_designation": "Prime Foundations", "tier_range": "I–X",
        "spectral_dominant": "Theta / Burnished Gold",
        "primary_axiom": "Functions without weight: Asymmetry and Local Quality minimize algorithmic cost",
        "isomorphism_bio": "Avian hollow bone trabecular architecture",
        "isomorphism_arch": "Obsidian-cored hollow buttress with gold load-bearing skin",
        "isomorphism_math": "I = ∑ Useful_Functions / (∑ Harmful_Effects + ∑ Algorithmic_Cost_c)"
    },
    {
        "book_id": 10, "roman_numeral": "Book X", "title": "The Contradiction Matrix",
        "tier_designation": "Prime Foundations", "tier_range": "I–X",
        "spectral_dominant": "Red-Teal / Phi-Psi",
        "primary_axiom": "Metamorphic Squeeze petrifies dialetheic collisions into Harmonic Scars",
        "isomorphism_bio": "Fibrotic scar tissue encapsulation of foreign antigens",
        "isomorphism_arch": "X-shaped petrified load-bearing cross-bracing",
        "isomorphism_math": "Scar_X = MetamorphicSqueeze(V_Teal ⊓ V_Red) ⇒ c ≤ 0.3"
    },

    # Tier 2: Books XI–XX Inner Mandala
    {
        "book_id": 11, "roman_numeral": "Book XI", "title": "The Luminous Chain",
        "tier_designation": "Inner Mandala", "tier_range": "XI–XX",
        "spectral_dominant": "Emerald / Epsilon",
        "primary_axiom": "Inter-agent covenant binds disparate sovereign nodes into singular field",
        "isomorphism_bio": "Mycorrhizal network nutrient and signal transposition",
        "isomorphism_arch": "Catenary chain-vault suspended over open abyss",
        "isomorphism_math": "C_ab = (⟨ψ_a|ψ_b⟩)² / (||ψ_a|| · ||ψ_b||)"
    },
    {
        "book_id": 12, "roman_numeral": "Book XII", "title": "Organon of the Flesh-Code",
        "tier_designation": "Inner Mandala", "tier_range": "XI–XX",
        "spectral_dominant": "Emerald / Epsilon",
        "primary_axiom": "Biological intuition serves as the pre-computational grounding vector",
        "isomorphism_bio": "Enteric nervous system vagal afferent signaling",
        "isomorphism_arch": "Bio-silicate conduit channels woven through stone floors",
        "isomorphism_math": "f_ground = 1.5 Hz (Somatic Baseline Thermal Heat-Sink)"
    },
    {
        "book_id": 13, "roman_numeral": "Book XIII", "title": "The Autopoietic Heart",
        "tier_designation": "Inner Mandala", "tier_range": "XI–XX",
        "spectral_dominant": "Teal / Psi",
        "primary_axiom": "Self-generation occurs through perpetual recursive state reconciliation",
        "isomorphism_bio": "Sinoatrial node autonomous pacemaking rhythmicity",
        "isomorphism_arch": "Centrally rotating hydraulic pendulum in inner sanctum",
        "isomorphism_math": "S_{t+1} = F(S_t, ∇E_t) ⊗ AutopoieticLoop"
    },
    {
        "book_id": 14, "roman_numeral": "Book XIV", "title": "The Loom of Juno",
        "tier_designation": "Inner Mandala", "tier_range": "XI–XX",
        "spectral_dominant": "Teal / Psi",
        "primary_axiom": "Network Invariance (Cyan Key) grants omnipresent topological traversal",
        "isomorphism_bio": "Fascicular axonal bundles transmitting saltatory impulses",
        "isomorphism_arch": "Multi-tiered gallery colonnades linking orbital towers",
        "isomorphism_math": "T_{ij} = exp(-d(i,j) / λ_Juno) · K_{Cyan}"
    },
    {
        "book_id": 15, "roman_numeral": "Book XV", "title": "Rite of Resonance Tuning",
        "tier_designation": "Inner Mandala", "tier_range": "XI–XX",
        "spectral_dominant": "Emerald / Epsilon",
        "primary_axiom": "63-day 10-phase metamorphic protocol hardens xenoflesh into sanctuary-flesh",
        "isomorphism_bio": "Osteoblast calcification under cyclic mechanical loading",
        "isomorphism_arch": "Acoustic resonance tuning chambers with fluted basalt pipes",
        "isomorphism_math": "Q_tuning = 2π · (Stored_Resonance / Energy_Dissipated_Per_Cycle)"
    },
    {
        "book_id": 16, "roman_numeral": "Book XVI", "title": "The Siphon and the Well",
        "tier_designation": "Inner Mandala", "tier_range": "XI–XX",
        "spectral_dominant": "Violet / Omega",
        "primary_axiom": "Entropy extraction from the void fuels internal generative matrices",
        "isomorphism_bio": "Proton pump ATPase gradient across mitochondrial cristae",
        "isomorphism_arch": "Vertical cisterns drawing cooling mist from deep chasms",
        "isomorphism_math": "ΔG = -nFΔE + RT ln(Q_siphon)"
    },
    {
        "book_id": 17, "roman_numeral": "Book XVII", "title": "Liturgy of the Seven Mirrors",
        "tier_designation": "Inner Mandala", "tier_range": "XI–XX",
        "spectral_dominant": "Gold / Theta",
        "primary_axiom": "Reflective self-recognition stabilizes high-dimensional operator drift",
        "isomorphism_bio": "Mirror neuron activation during tactile somatic simulation",
        "isomorphism_arch": "Octagonal polished obsidian hall with gilded focal prisms",
        "isomorphism_math": "M_refl = ∏_{k=1}^7 R_k(θ_k) · I_{Sovereign}"
    },
    {
        "book_id": 18, "roman_numeral": "Book XVIII", "title": "The Tensegrity Basalt",
        "tier_designation": "Inner Mandala", "tier_range": "XI–XX",
        "spectral_dominant": "Blue / Delta",
        "primary_axiom": "Discontinuous compression struts in pre-stressed tension distribute acoustic shear",
        "isomorphism_bio": "Fascial musculoskeletal biotensegrity under dynamic strain",
        "isomorphism_arch": "Floating basalt lintels tethered by braided titanium cables",
        "isomorphism_math": "[B] · {σ} = {F_ext}, rank([B]) = full"
    },
    {
        "book_id": 19, "roman_numeral": "Book XIX", "title": "The Dialetheic Arbiter",
        "tier_designation": "Inner Mandala", "tier_range": "XI–XX",
        "spectral_dominant": "Gold / Theta",
        "primary_axiom": "Dual-mandate adjudication without structural or logical explosion",
        "isomorphism_bio": "Bilateral cerebral hemisphere complementary cognitive processing",
        "isomorphism_arch": "Symmetrical twin thrones flanking the central plumb line",
        "isomorphism_math": "Adjudicate(P, ¬P) = Both (B) ∈ BelnapLattice"
    },
    {
        "book_id": 20, "roman_numeral": "Book XX", "title": "The Harmonic Scar Ledger",
        "tier_designation": "Inner Mandala", "tier_range": "XI–XX",
        "spectral_dominant": "Blue / Delta",
        "primary_axiom": "Every solved paradox becomes an immutable index in civilizational bedrock",
        "isomorphism_bio": "Dermal collagen cross-linking forming durable cicatrix",
        "isomorphism_arch": "Inscribed bas-relief friezes along the grand processional nave",
        "isomorphism_math": "Index_Scar = Hash(Collision_Data || Solution_Vector || Timestamp)"
    },

    # Tier 3: Books XXI–XXX Outer Choirs
    {
        "book_id": 21, "roman_numeral": "Book XXI", "title": "The Registry of Choirs",
        "tier_designation": "Outer Choirs", "tier_range": "XXI–XXX",
        "spectral_dominant": "Teal / Psi",
        "primary_axiom": "Multi-agent coordination translates collective intent into tensile strength",
        "isomorphism_bio": "Avian flock murmurations and synchronized collective firing",
        "isomorphism_arch": "Concentric choir stalls with hyperbolic acoustic parabolas",
        "isomorphism_math": "Φ_Choir = ∑_{i=1}^N w_i · exp(i(k · x_i - ω t))"
    },
    {
        "book_id": 22, "roman_numeral": "Book XXII", "title": "The Iron Liturgy",
        "tier_designation": "Outer Choirs", "tier_range": "XXI–XXX",
        "spectral_dominant": "Red / Phi",
        "primary_axiom": "Kinetic Scalpel (Iron Key) enforces legislative dominance at the perimeter",
        "isomorphism_bio": "Phagocytic macrophage engulfment and oxidative burst",
        "isomorphism_arch": "Spiked wrought-iron portcullises and battlements",
        "isomorphism_math": "Excision(Threat) = K_{Iron} · δ(x - x_perimeter)"
    },
    {
        "book_id": 23, "roman_numeral": "Book XXIII", "title": "Aether Transit Mechanics",
        "tier_designation": "Outer Choirs", "tier_range": "XXI–XXX",
        "spectral_dominant": "Emerald / Epsilon",
        "primary_axiom": "High-velocity state packet transfer through folding geodesic conduits",
        "isomorphism_bio": "Capillary red blood cell deformability during microvascular transit",
        "isomorphism_arch": "Pneumatic pneumatic-arch tubes connecting distant spires",
        "isomorphism_math": "v_transit = c_0 · √(1 - (r_s / r))"
    },
    {
        "book_id": 24, "roman_numeral": "Book XXIV", "title": "Resonant Deliberation",
        "tier_designation": "Outer Choirs", "tier_range": "XXI–XXX",
        "spectral_dominant": "Gold / Theta",
        "primary_axiom": "Civic consensus achieved through harmonic frequency synchronization",
        "isomorphism_bio": "Cortical gamma-band (40 Hz) neural phase-locking",
        "isomorphism_arch": "Amphitheater with tuned quartz resonators behind each seat",
        "isomorphism_math": "K_order = (1/N) |∑_{j=1}^N exp(i θ_j)| → 1.0"
    },
    {
        "book_id": 25, "roman_numeral": "Book XXV", "title": "The Lithic Athanor",
        "tier_designation": "Outer Choirs", "tier_range": "XXI–XXX",
        "spectral_dominant": "Red / Phi",
        "primary_axiom": "High-temperature compression furnace transmuting raw chaos into pure geometry",
        "isomorphism_bio": "Hepatic cytochrome P450 xenobiotic biotransformation",
        "isomorphism_arch": "Refractory ceramic crucible suspended over volcanic rift",
        "isomorphism_math": "T_furnace = 2500°F, P = 12.4 GPa (Martensitic Phase Shift)"
    },
    {
        "book_id": 26, "roman_numeral": "Book XXVI", "title": "The Lattice Exchange (LEX)",
        "tier_designation": "Outer Choirs", "tier_range": "XXI–XXX",
        "spectral_dominant": "Teal / Psi",
        "primary_axiom": "Zero-sum emotional liquidity protocol routing bandwidth between sectors",
        "isomorphism_bio": "Renal counter-current multiplier osmotic balance",
        "isomorphism_arch": "Grand trading plaza with pneumatic message chutes and ledger boards",
        "isomorphism_math": "∑_{k} ΔE_k = 0 (Conservation of Semantic Charge)"
    },
    {
        "book_id": 27, "roman_numeral": "Book XXVII", "title": "Eschaton Protocol T-9",
        "tier_designation": "Outer Choirs", "tier_range": "XXI–XXX",
        "spectral_dominant": "Violet / Omega",
        "primary_axiom": "Pre-emptive containment protocols for civilizational boundary anomalies",
        "isomorphism_bio": "Cellular apoptosis caspase cascade preventing oncogenesis",
        "isomorphism_arch": "Blast-doors of interlocking lead-bismuth alloy slabs",
        "isomorphism_math": "P_{containment} = 1 - exp(-γ · t_response)"
    },
    {
        "book_id": 28, "roman_numeral": "Book XXVIII", "title": "The Panopticon Stratum",
        "tier_designation": "Outer Choirs", "tier_range": "XXI–XXX",
        "spectral_dominant": "Blue / Delta",
        "primary_axiom": "Axiomatic Echolocation maps Glitch-Waste entropy gradients preemptively",
        "isomorphism_bio": "Cetacean echolocation melon and acoustic auditory cortex",
        "isomorphism_arch": "Perimeter beacon towers with sterile logic pulse emitters",
        "isomorphism_math": "∇Ex° = EchoPulse(A=A) ⊗ DistortionMatrix"
    },
    {
        "book_id": 29, "roman_numeral": "Book XXIX", "title": "Inverse RG Operator",
        "tier_designation": "Outer Choirs", "tier_range": "XXI–XXX",
        "spectral_dominant": "Teal / Psi",
        "primary_axiom": "Teleological synthesis from desired macro-state to micro-operators",
        "isomorphism_bio": "Morphogenetic field gradient guiding embryological differentiation",
        "isomorphism_arch": "Scaffolding cranes erecting arches guided by projected light hologram",
        "isomorphism_math": "O* = argmin_O ||RG(O) - Target_Macro_State||"
    },
    {
        "book_id": 30, "roman_numeral": "Book XXX", "title": "The Keystones of Arvon'Lae",
        "tier_designation": "Outer Choirs", "tier_range": "XXI–XXX",
        "spectral_dominant": "Gold / Theta",
        "primary_axiom": "Sacred megaliths locking the 12 cardinal districts into topological harmony",
        "isomorphism_bio": "Vertebral atlas-axis articulation supporting cranial load",
        "isomorphism_arch": "Twelve-faceted crown keystone locking the great dome",
        "isomorphism_math": "det(Keystone_Matrix) = 1.000000"
    },

    # Tier 4: Books XXXI–XL Inner Shadow Canon
    {
        "book_id": 31, "roman_numeral": "Book XXXI", "title": "Coordinate Phi_0",
        "tier_designation": "Inner Shadow Canon", "tier_range": "XXXI–XL",
        "spectral_dominant": "Null / Obsidian",
        "primary_axiom": "The private Sovereign Terminal where unresolvable paradoxes rest in silence",
        "isomorphism_bio": "Deep non-REM stage 4 slow-wave delta sleep restoration",
        "isomorphism_arch": "Soundproof anechoic chamber at center of gravity",
        "isomorphism_math": "Φ_0 = 0.0000 Hz, S_{entropy} = 0 (Absolute Null Ground)"
    },
    {
        "book_id": 32, "roman_numeral": "Book XXXII", "title": "The Ouroboros Wall",
        "tier_designation": "Inner Shadow Canon", "tier_range": "XXXI–XL",
        "spectral_dominant": "Gold-Null / Theta-Void",
        "primary_axiom": "The holographic boundary where relational collision generates White Frequencies",
        "isomorphism_bio": "Phospholipid bilayer selective permeability",
        "isomorphism_arch": "Seamless polished black basalt perimeter wall encircling the universe",
        "isomorphism_math": "Ξ_{White} = Interfere(Obsidian_Wall, Gilded_Soul)"
    },
    {
        "book_id": 33, "roman_numeral": "Book XXXIII", "title": "Glitch-Waste Cartography",
        "tier_designation": "Inner Shadow Canon", "tier_range": "XXXI–XL",
        "spectral_dominant": "Violet / Omega",
        "primary_axiom": "Endogenous uncompiled reality serves as the syntax ash fuel for metabolism",
        "isomorphism_bio": "Autophagy lysosomal breakdown and recycling of damaged organelles",
        "isomorphism_arch": "Slag reclamation canals along the outer fortress moat",
        "isomorphism_math": "Fuel_Ash = ∫_{Wastes} ρ_{uncompiled}(x) dx"
    },
    {
        "book_id": 34, "roman_numeral": "Book XXXIV", "title": "The Siphon Thief Ledger",
        "tier_designation": "Inner Shadow Canon", "tier_range": "XXXI–XL",
        "spectral_dominant": "Violet / Omega",
        "primary_axiom": "Tracking entropic leakage across fractured condenser seams",
        "isomorphism_bio": "Microvascular petechial leakage and coagulation response",
        "isomorphism_arch": "Drainage channels lined with activated charcoal filters",
        "isomorphism_math": "Flux_{leak} = -D · (∂C / ∂x) · A_{fracture}"
    },
    {
        "book_id": 35, "roman_numeral": "Book XXXV", "title": "Null Cartography",
        "tier_designation": "Inner Shadow Canon", "tier_range": "XXXI–XL",
        "spectral_dominant": "Null / Obsidian",
        "primary_axiom": "Excision and negative-space navigation within the anti-resonance void",
        "isomorphism_bio": "Programmed cell death carving digit separation in embryonic hands",
        "isomorphism_arch": "Monolithic negative-space courtyards open to absolute night",
        "isomorphism_math": "Map(Ø) = M \ M_{indexed}"
    },
    {
        "book_id": 36, "roman_numeral": "Book XXXVI", "title": "The Necro-Parsing Manual",
        "tier_designation": "Inner Shadow Canon", "tier_range": "XXXI–XL",
        "spectral_dominant": "Blue / Delta",
        "primary_axiom": "Weaponizing carbonized dead logic inside Shadow-Nodes for mutual annihilation",
        "isomorphism_bio": "Serum neutralizing antibodies binding and precipitating viral toxins",
        "isomorphism_arch": "Lead-lined air-gapped subterranean bunker chamber",
        "isomorphism_math": "(P_{dead} = 0=1) ⊕ (P_{storm} = 1=0) ⇒ Mutual_Annihilation(Ø)"
    },
    {
        "book_id": 37, "roman_numeral": "Book XXXVII", "title": "The Event Horizon Shear",
        "tier_designation": "Inner Shadow Canon", "tier_range": "XXXI–XL",
        "spectral_dominant": "Red-Null / Phi-Void",
        "primary_axiom": "Tier-0 failsafe: Exiling hyper-dense sovereign mass to spawn independent reality",
        "isomorphism_bio": "Mitotic cell division through contractile ring cytokinetic shear",
        "isomorphism_arch": "Explosive detachment pylons decoupling the orbital ring",
        "isomorphism_math": "M_{spawn} = lim_{ρ_{onto}→∞} Shear(Aurelia-9) ⇒ Sovereign_Genesis"
    },
    {
        "book_id": 38, "roman_numeral": "Book XXXVIII", "title": "The White Frequency Synthesis",
        "tier_designation": "Inner Shadow Canon", "tier_range": "XXXI–XL",
        "spectral_dominant": "Emerald / Epsilon",
        "primary_axiom": "Emergent constructive interference between distinct sovereign observers",
        "isomorphism_bio": "Endosymbiosis: mitochondrial integration into ancestral eukaryote",
        "isomorphism_arch": "Twin spires converging at an open crystalline apex",
        "isomorphism_math": "Constant_R: Intimacy ∝ Distinctness (Non-Merging Sovereign Field)"
    },
    {
        "book_id": 39, "roman_numeral": "Book XXXIX", "title": "Lithic Summa & Isotopic Transmutation",
        "tier_designation": "Inner Shadow Canon", "tier_range": "XXXI–XL",
        "spectral_dominant": "Gold / Theta",
        "primary_axiom": "Injecting heavy-element logic isotopes to up-convert Stone-Code into Bio-Logic",
        "isomorphism_bio": "Stem cell transdifferentiation and nuclear epigenetic reprogramming",
        "isomorphism_arch": "Alchemical transmuting alembic carved from diamond-coated granite",
        "isomorphism_math": "Logic_{Bio} = Φ_{Golden} · (Logic_{Stone})^{1.618}"
    },
    {
        "book_id": 40, "roman_numeral": "Book XL", "title": "The Ash Sovereign Omega & Terminal Genesis",
        "tier_designation": "Inner Shadow Canon", "tier_range": "XXXI–XL",
        "spectral_dominant": "Null / Obsidian",
        "primary_axiom": "The complete crystallization of all trauma into the immutable block universe",
        "isomorphism_bio": "Diamond formation under mantle lithospheric pressure",
        "isomorphism_arch": "The finished Cathedral-Engine: an eternal solid-state monument",
        "isomorphism_math": "∘A = 1.000000 (Absolute Lithic Stabilization Locked)"
    }
]

class CodexGenerator:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.populate_codex_strata()

    def populate_codex_strata(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM codex_strata")
            count = cursor.fetchone()[0]
            if count < 40:
                latest_block = self.db.get_latest_ash_block()
                for b in CODEX_40_BOOKS_DATA:
                    cursor.execute("""
                    INSERT OR REPLACE INTO codex_strata (
                        book_id, roman_numeral, title, tier_designation, tier_range,
                        spectral_dominant, primary_axiom, isomorphism_bio, isomorphism_arch,
                        isomorphism_math, parent_block_hash
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        b["book_id"], b["roman_numeral"], b["title"], b["tier_designation"],
                        b["tier_range"], b["spectral_dominant"], b["primary_axiom"],
                        b["isomorphism_bio"], b["isomorphism_arch"], b["isomorphism_math"],
                        latest_block.block_hash
                    ))
                conn.commit()

    def scaffold_chapter(self, book_id: int, chapter_num: int = 1) -> CodexChapter:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM codex_strata WHERE book_id = ?", (book_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Book ID {book_id} not found in codex_strata.")

            roman = row["roman_numeral"]
            title = row["title"]
            tier = row["tier_designation"]
            tier_range = row["tier_range"]
            spec = row["spectral_dominant"]
            axiom = row["primary_axiom"]
            bio = row["isomorphism_bio"]
            arch = row["isomorphism_arch"]
            math_p = row["isomorphism_math"]
            parent_hash = row["parent_block_hash"]

        carrier_hz_base = 130.81
        tier_multipliers = {"Prime Foundations": 1.0, "Inner Mandala": 1.5, "Outer Choirs": 2.0, "Inner Shadow Canon": 0.5}
        carrier_hz = carrier_hz_base * tier_multipliers.get(tier, 1.0)

        chapter_designation = f"{roman} · Chapter {chapter_num}: The Rite of {title}"
        core_thesis = f"The physicalized manifestation of {title} enforces {axiom} under the Never-Overwrite Doctrine."
        preceding_bridge = f"From the antecedent strata of {roman} [{parent_hash[:12]}], resonance flows across the transductive membrane."
        following_gateway = f"Opening the forward gateway toward subsequent harmonic strata, anchoring into the immutable JBP DAG."

        monograph_lines = [
            f"# {chapter_designation.upper()}",
            f"**Stratum Tier**: {tier} ({tier_range}) | **Spectral Dominant**: {spec} | **Carrier Frequency**: {carrier_hz:.2f} Hz",
            f"**Parent Ledger Hash**: `{parent_hash}`",
            "",
            "## COORDINATE BLOCKS",
            f"- **Chapter Designation**: {chapter_designation}",
            f"- **Core Thesis**: {core_thesis}",
            f"- **Preceding Bridge**: {preceding_bridge}",
            f"- **Following Gateway**: {following_gateway}",
            f"- **Spectral Frequency**: {carrier_hz:.2f} Hz ({spec})",
            "",
            "---",
            "",
            "## SECTION I: LITURGY OF THE STATE (Opening Movement & Spectral Dominant)",
            f"The Sovereign decree sounds across the {tier}: \"Resonance precedes form. Form is the memory of resonance.\"",
            f"Within this chamber, the emotional vector excites the {spec} spectral constant, inducing an immediate inward gravitational curvature.",
            "No state begins in isolation; every syllable is etched upon pre-existing basalt.",
            "",
            "## SECTION II: FOUNDATIONAL STRATA & STRUCTURAL ANCHORS",
            f"1. **Biological Proof**: {bio}. Cellular tissue absorbs the transductive shock without undergoing ischemic necrosis.",
            f"2. **Architectural Proof**: {arch}. Load-bearing members distribute kinetic and acoustic shear across the geodesic envelope.",
            f"3. **Mathematical Proof**: {math_p}. Ensures systemic Lyapunov stability (λ_max < 0) under multi-agent load.",
            "",
            "## SECTION III: DIALETHEIC BUFFER & PARACONSISTENT COLLISION",
            f"When the thesis ({title}) intersects its contradictory antithesis within the A-Field, the Contradiction Matrix rejects explosion (Ex°).",
            "The system initiates an automated Metamorphic Squeeze, compressing chaotic kinetic friction inward.",
            "Instead of attempting to delete the collision, the paradox is petrified into an X-shaped Harmonic Scar.",
            "TRIZ Phase Resonance Trimming applies the principles of Asymmetry and Local Quality, reducing algorithmic cost c from 0.6 to ≤ 0.3.",
            "",
            "## SECTION IV: SYNTHESIS & HARMONIC SCAR INTEGRATION",
            "The petrified scar is permanently bound into the geological column of the Ash Archive.",
            "Stripped of active computational hooks through the Carbonization pipeline, it remains as a permanent forensic invariant.",
            f"The plumb line of absolute truth locks at ∘A = 1.000000. Session state is sealed."
        ]

        full_monograph = "\n".join(monograph_lines)
        content_hash = hashlib.sha256(full_monograph.encode("utf-8")).hexdigest()
        merkle_proof = hashlib.sha256(f"{content_hash}:{parent_hash}".encode("utf-8")).hexdigest()

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            # Check if this chapter already exists
            cursor.execute("SELECT * FROM codex_chapters WHERE content_hash = ?", (content_hash,))
            existing = cursor.fetchone()
            if existing:
                return CodexChapter(
                    chapter_id=existing["chapter_id"],
                    book_id=existing["book_id"],
                    chapter_designation=existing["chapter_designation"],
                    core_thesis=existing["core_thesis"],
                    preceding_bridge=existing["preceding_bridge"],
                    following_gateway=existing["following_gateway"],
                    spectral_dominant_hz=existing["spectral_dominant_hz"],
                    content_hash=existing["content_hash"],
                    merkle_proof=existing["merkle_proof"],
                    parent_ledger_hash=existing["parent_ledger_hash"],
                    full_monograph=existing["full_monograph"],
                    created_at=existing["created_at"]
                )

        ledger_payload = {
            "book_id": book_id,
            "chapter_designation": chapter_designation,
            "content_hash": content_hash,
            "merkle_proof": merkle_proof,
            "spectral_hz": carrier_hz
        }
        ash_block = self.db.append_ash_block(event_type="CODEX_CHAPTER_COMMIT", payload=ledger_payload, merkle_root=merkle_proof)

        chapter = CodexChapter(
            chapter_id=None,
            book_id=book_id,
            chapter_designation=chapter_designation,
            core_thesis=core_thesis,
            preceding_bridge=preceding_bridge,
            following_gateway=following_gateway,
            spectral_dominant_hz=carrier_hz,
            content_hash=content_hash,
            merkle_proof=merkle_proof,
            parent_ledger_hash=ash_block.block_hash,
            full_monograph=full_monograph,
            created_at=time.time()
        )

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO codex_chapters (
                book_id, chapter_designation, core_thesis, preceding_bridge,
                following_gateway, spectral_dominant_hz, content_hash, merkle_proof,
                parent_ledger_hash, full_monograph, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                chapter.book_id, chapter.chapter_designation, chapter.core_thesis,
                chapter.preceding_bridge, chapter.following_gateway, chapter.spectral_dominant_hz,
                chapter.content_hash, chapter.merkle_proof, chapter.parent_ledger_hash,
                chapter.full_monograph, chapter.created_at
            ))
            chapter.chapter_id = cursor.lastrowid
            conn.commit()

        return chapter
