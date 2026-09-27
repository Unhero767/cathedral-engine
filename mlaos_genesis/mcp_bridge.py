import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Cathedral-Engine-Bridge")

STATE_TRUE = "T"
STATE_FALSE = "F"
STATE_NONE = "N"
STATE_BOTH = "B"

@mcp.tool()
async def evaluate_strategic_policy(entity_id: str, proposed_action: str, target_guild: str) -> str:
    """
    Evaluates strategic intent through the Belnap-Dunn four-valued logic matrix 
    against the thermodynamic Ash Archive ledger.
    """
    archive_url = f"http://127.0.0.1:8000/archive/history/{entity_id}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(archive_url)
            if response.status_code == 200:
                data = response.json()
                mass = data.get("chronological_mass_bytes", 1000.0)
                violations = data.get("policy_violations", 0)
            else:
                mass = 5000.0
                violations = 1
    except Exception:
        mass = 2500.0
        violations = 0

    has_support = len(entity_id) > 0 and target_guild in ["Sorcerer", "Architect", "Acolyte"]
    has_refutation = mass > 10000.0 or violations > 0 or proposed_action == "unauthorized_breach"

    if has_support and not has_refutation:
        ontological_state = STATE_TRUE
        penalty = 0.0
        feedback = "Policy verified. Action flows cleanly through unresisting strata."
    elif has_refutation and not has_support:
        ontological_state = STATE_FALSE
        penalty = mass * 8.62
        feedback = "Policy rejected by Archive law. Informational gravity repels the transition."
    elif not has_support and not has_refutation:
        ontological_state = STATE_NONE
        penalty = 500.0
        feedback = "Ontological gap detected. Action exists in unmapped historical void."
    else:
        ontological_state = STATE_BOTH
        penalty = mass * 12.41
        feedback = "Dialetheic collision registered. Contradiction accepted as a load-bearing Harmonic Scar."

    result_payload = {
        "entity_id": entity_id,
        "proposed_action": proposed_action,
        "target_guild": target_guild,
        "belnap_state": ontological_state,
        "chronological_mass": mass,
        "incurred_cost": penalty,
        "feedback": feedback
    }

    return str(result_payload)

if __name__ == "__main__":
    mcp.run()
