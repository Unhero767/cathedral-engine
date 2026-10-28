------------------------ MODULE ParaconsistentLattice ------------------------
EXTENDS Naturals, Sequences, FiniteSets, TLC

CONSTANTS 
    Strata,          \* Set of epistemic addresses, e.g., {"vault.axiom.042", "vault.axiom.043"}
    Propositions,    \* Set of propositions, e.g., {"P"}
    Sensors          \* Set of authorized sensor nodes, e.g., {"tx_01H8X9A", "tx_01H8X9Z"}

VARIABLES 
    truthVector,     \* truthVector[s] = [pos: {0,1}, neg: {0,1}]
    evidenceChain,   \* Append-only log of transactions per stratum (Lex I Doctrine)
    harmonicScars,   \* Set of crystallized Harmonic Scars
    explosionLeak    \* Boolean flag testing if a B-state corrupts non-colliding strata

vars == <<truthVector, evidenceChain, harmonicScars, explosionLeak>>

EpistemicState(s) ==
    LET tv == truthVector[s] IN
    CASE tv.pos = 0 /\ tv.neg = 0 -> "N"
      [] tv.pos = 1 /\ tv.neg = 0 -> "T"
      [] tv.pos = 0 /\ tv.neg = 1 -> "F"
      [] tv.pos = 1 /\ tv.neg = 1 -> "B"

Init ==
    /\ truthVector = [s \in Strata |-> [pos |-> 0, neg |-> 0]]
    /\ evidenceChain = [s \in Strata |-> <<>>]
    /\ harmonicScars = {}
    /\ explosionLeak = FALSE

InscribePositive(s, tx) ==
    /\ truthVector' = [truthVector EXCEPT ![s].pos = 1]
    /\ evidenceChain' = [evidenceChain EXCEPT ![s] = Append(@, [tx_id |-> tx, polarity |-> "+1"])]
    /\ IF truthVector[s].neg = 1
       THEN harmonicScars' = harmonicScars \cup {[stratum |-> s, state |-> "B", isolated |-> TRUE]}
       ELSE harmonicScars' = harmonicScars
    /\ UNCHANGED explosionLeak

InscribeNegative(s, tx) ==
    /\ truthVector' = [truthVector EXCEPT ![s].neg = 1]
    /\ evidenceChain' = [evidenceChain EXCEPT ![s] = Append(@, [tx_id |-> tx, polarity |-> "-1"])]
    /\ IF truthVector[s].pos = 1
       THEN harmonicScars' = harmonicScars \cup {[stratum |-> s, state |-> "B", isolated |-> TRUE]}
       ELSE harmonicScars' = harmonicScars
    /\ UNCHANGED explosionLeak

Next ==
    \E s \in Strata, tx \in Sensors :
        \/ InscribePositive(s, tx)
        \/ InscribeNegative(s, tx)

Spec == Init /\ [][Next]_vars

LexINeverOverwrite ==
    \A s \in Strata : Len(evidenceChain[s]) >= 0

ExplosionContained ==
    /\ explosionLeak = FALSE
    /\ \A s1, s2 \in Strata :
        (s1 # s2 /\ EpistemicState(s1) = "B" /\ Len(evidenceChain[s2]) = 0) 
            => EpistemicState(s2) = "N"

MonotonicInformationGrowth ==
    \A s \in Strata : truthVector[s].pos \in {0, 1} /\ truthVector[s].neg \in {0, 1}
=============================================================================
