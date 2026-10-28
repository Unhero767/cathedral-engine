"""
Cathedral-Engine: Margin of Safety & Lithic Capital Reserve Enforcer
Operational compliance: Zero Unbacked Leverage (Lf <= 1.0), Lead Key Permineralization
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple


class LithicAssetClass(str, Enum):
    CYCLOPEAN_GRANITE = "Cyclopean Granite (Delta/Blue: Land, Facilities, Hardware)"
    OBSIDIAN_BALLAST = "Obsidian Ballast (Null/Void: Sovereign Physical Reserves)"


@dataclass(frozen=True)
class ExpansionProposal:
    project_id: str
    estimated_cost: float
    unencumbered_cash_allocated: float
    debt_or_credit_requested: float
    axiomatic_weight: float
    local_entropy: float


class MarginOfSafetyEnforcer:
    MINIMUM_MARGIN_OF_SAFETY = 2.50
    MAXIMUM_LEVERAGE_FACTOR = 1.00  # Strict zero-leverage constraint

    @classmethod
    def evaluate_expansion(cls, proposal: ExpansionProposal) -> Tuple[bool, float, float, str]:
        total_financing = proposal.unencumbered_cash_allocated + proposal.debt_or_credit_requested
        
        if proposal.unencumbered_cash_allocated <= 0:
            return False, 0.0, float('inf'), "REJECTED: Zero unencumbered equity provided."

        leverage_factor = total_financing / proposal.unencumbered_cash_allocated

        if leverage_factor > cls.MAXIMUM_LEVERAGE_FACTOR or proposal.debt_or_credit_requested > 0:
            return False, 0.0, leverage_factor, (
                f"REJECTED: Lex V Violation. Synthetic leverage detected (Lf = {leverage_factor:.2f} > 1.00). "
                "All expansions must be 100% equity funded."
            )

        epsilon = max(proposal.local_entropy, 1e-6)
        solvency_ratio = proposal.unencumbered_cash_allocated / proposal.estimated_cost
        quality_ratio = proposal.axiomatic_weight / epsilon

        margin_of_safety = (quality_ratio * solvency_ratio) / leverage_factor

        if margin_of_safety < cls.MINIMUM_MARGIN_OF_SAFETY:
            return False, margin_of_safety, leverage_factor, (
                f"REJECTED: Margin of Safety ({margin_of_safety:.2f}) below required threshold ({cls.MINIMUM_MARGIN_OF_SAFETY:.2f})."
            )

        return True, margin_of_safety, leverage_factor, "APPROVED: Fully collateralized expansion."


class LithicTreasuryManager:
    """Manages the conversion of operational surplus into multi-century physical assets."""

    def __init__(self):
        self.granite_foundations_reserve: float = 0.0
        self.obsidian_ballast_reserve: float = 0.0

    def allocate_surplus(self, net_surplus: float, granite_pct: float = 0.60) -> Dict[str, float]:
        obsidian_pct = 1.0 - granite_pct
        granite_allocation = net_surplus * granite_pct
        obsidian_allocation = net_surplus * obsidian_pct

        self.granite_foundations_reserve += granite_allocation
        self.obsidian_ballast_reserve += obsidian_allocation

        return {
            "surplus_processed": net_surplus,
            "allocated_to_granite_foundations": round(granite_allocation, 2),
            "allocated_to_obsidian_ballast": round(obsidian_allocation, 2),
            "total_granite_reserve": round(self.granite_foundations_reserve, 2),
            "total_obsidian_reserve": round(self.obsidian_ballast_reserve, 2),
            "governance": "Permineralized via Lead Key (Saturn Duration Consensus)"
        }


def main():
    print("================================================================================")
    print("CATHEDRAL-ENGINE: MARGIN OF SAFETY & ZERO-LEVERAGE CAPITAL ENFORCEMENT")
    print("================================================================================")

    # Case 1: 100% Equity, High Margin of Safety
    prop_sound = ExpansionProposal(
        project_id="EXP-SOLID-001",
        estimated_cost=50000.0,
        unencumbered_cash_allocated=65000.0,
        debt_or_credit_requested=0.0,
        axiomatic_weight=0.98,
        local_entropy=0.10
    )
    ok, mos, lf, reason = MarginOfSafetyEnforcer.evaluate_expansion(prop_sound)
    print(f"Proposal: {prop_sound.project_id} | Status: {'APPROVED' if ok else 'REJECTED'}")
    print(f"  Margin of Safety: {mos:.2f} (Required >= 2.50) | Leverage Factor: {lf:.2f}")
    print(f"  Result: {reason}\n")

    # Case 2: Leveraged Expansion (Debt/Credit financing requested)
    prop_leveraged = ExpansionProposal(
        project_id="EXP-DEBT-002",
        estimated_cost=100000.0,
        unencumbered_cash_allocated=50000.0,
        debt_or_credit_requested=50000.0,
        axiomatic_weight=0.95,
        local_entropy=0.05
    )
    ok, mos, lf, reason = MarginOfSafetyEnforcer.evaluate_expansion(prop_leveraged)
    print(f"Proposal: {prop_leveraged.project_id} | Status: {'APPROVED' if ok else 'REJECTED'}")
    print(f"  Margin of Safety: {mos:.2f} | Leverage Factor: {lf:.2f}")
    print(f"  Result: {reason}\n")

    # Case 3: Sinking Surplus into Permanent Lithic Reserves
    treasury = LithicTreasuryManager()
    print("--------------------------------------------------------------------------------")
    print("CONSOLIDATING SURPLUS INTO CYCLOPEAN GRANITE & OBSIDIAN BALLAST")
    print("--------------------------------------------------------------------------------")
    surplus_q1 = 120000.00
    res = treasury.allocate_surplus(surplus_q1, granite_pct=0.60)
    for k, v in res.items():
        print(f"  {k}: {v}")

    print("================================================================================")


if __name__ == "__main__":
    main()
